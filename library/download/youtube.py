import library.files
from library.normalize import TitleCanonizer
from library.logging import cm, colorize_json, color

import json
import logging
import os
import requests
import time
import attr

from typing import Optional

log = logging.getLogger(__name__)

import pytube

try:
    import pafy  # http://np1.github.io/pafy/
except ImportError:
    log.error('Failed to load pafy')


class Mode:
    # local pytube was fixed, see: https://github.com/pytube/pytube/issues/1281
    PYTYBE = 'pytube'
    PAFY = 'pafy'
    REQUESTS = 'requests'


@attr.s
class YoutubeVideo:
    url: str = attr.ib()
    title: str = attr.ib()
    mode: str = attr.ib()
    dstdir: Optional[str] = attr.ib(default=None)
    extension: str = attr.ib(default='mp4')

    @url.validator
    def is_valid(self, attribute, value):
        if not value.startswith('https://www.youtube.com/watch?v='):
            raise ValueError(f'Got url {value}')

    def __str__(self):
        return f'{cm(self.title, color=color.Yellow)} ({self.url}) from {os.path.basename(self.dstdir)}'

    def get_best_stream(self, preftype=None, sleepTime=1200):
        log.debug(f'Searching best stream for {self}')
        ok = False
        while not ok:
            try:
                video = pafy.new(self.url)
                ok = True
            except IndexError:
                log.exception('Failed to get best stream')
                log.info(f'Sleeping for {sleepTime} seconds')
                time.sleep(sleepTime)
        best_stream = video.getbest(preftype=preftype)
        log.info(f'Streams: {video.streams}, best stream: {best_stream}')
        return best_stream

    @property
    def basename(self):
        return f'{self.title}.{self.extension}'

    @property
    def filename(self):
        if not library.files.is_dir(self.dstdir):
            raise ValueError(f'Not dir: {value}')

        return os.path.join(self.dstdir, self.basename)


def download_video(video: YoutubeVideo) -> Optional[Exception]:
    try:
        log.info(f'Downloading {video}...')
        if video.mode == Mode.REQUESTS:
            best_stream = video.get_best_stream(preftype=video.extension)
            data = requests.get(best_stream.url).content
            with open(video.filename, 'wb') as f:
                f.write(data)
        elif video.mode == Mode.PAFY:
            best_stream = video.get_best_stream(preftype=video.extension)
            best_stream.download(filepath=video.filename)
        elif video.mode == Mode.PYTYBE:
            streams = pytube.YouTube(video.url).streams
            streams = streams.filter(progressive=True, file_extension=video.extension)
            # streams = streams.get_highest_resolution()
            best_stream = streams.order_by('resolution').desc().first()
            best_stream.download(output_path=video.dstdir, filename=video.basename)
        else:
            raise RuntimeError(f'Invalid mode: {video.mode}')
        log.info(f'Downloaded {video}')
    except KeyboardInterrupt:
        log.error(f'Download cancelled: {video}')
    except Exception as e:
        log.exception(f'Failed to download {video}')
        return e
    return None


@attr.s
class YoutubePlaylist:
    url: str = attr.ib()
    title_canonizer: Optional[TitleCanonizer] = attr.ib(default=TitleCanonizer())

    @url.validator
    def is_valid(self, attribute, value):
        if not value.startswith('https://www.youtube.com/playlist?list=PL'):
            raise ValueError(f'Got url {value}')

    def __str__(self):
        return f'{cm(self.url, color=color.Cyan)}'

    def get_unique_suffix(self, videos, title, url):
        suffixes = [''] + [f' - {i}' for i in range(2, 4)]
        for suffix in suffixes:
            new_title = title + suffix
            has_duplicate = False
            for video in videos:
                if video.title == new_title:
                    has_duplicate = True
                    if video.url == url:
                        log.info(f'Found full duplicate for {title!r}, skipping')
                        return False, None
                    else:
                        log.warn((
                            f'Found duplicate for {title!r} with another url: '
                            f'check {video.url} and {url}'
                        ))
            if not has_duplicate:
                if suffix:
                    log.warn(f'Got suffix {suffix} for {title} at {url}')
                return True, suffix

        raise RuntimeError(f'Could not resolve duplicate {title!r}, check {url}')

    def ListVideos(self):
        log.debug(f'Looking for videos in {self}')
        text = requests.get(self.url).text

        start_expression = 'var ytInitialData ='
        end_expression = '</script>'
        start_pos = text.find(start_expression) + len(start_expression)
        end_pos = text.find(end_expression, start_pos)
        js_data = text[start_pos:end_pos].strip().strip(';')
        loaded = json.loads(js_data)
        playlistTitle = loaded['metadata']['playlistMetadataRenderer']['title']
        contentItems = loaded['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']

        content_items = [item for item in contentItems if 'playlistVideoRenderer' in item]
        videos = []
        for index, contentItem in enumerate(content_items, 1):
            try:
                index_text = int(contentItem['playlistVideoRenderer']['index']['simpleText'])
                assert index_text == index, f'Got index {index_text} instead of {index}'
                video_id = contentItem['playlistVideoRenderer']['videoId']
                title_text = contentItem['playlistVideoRenderer']['title']['runs'][0]['text']
                title_text = self.title_canonizer.Canonize(title_text)
                url = f'https://www.youtube.com/watch?v={video_id}'

                is_unique, suffix = self.get_unique_suffix(videos, title_text, url)
                if is_unique:
                    video = YoutubeVideo(
                        url,
                        title_text + suffix,
                        mode=Mode.PAFY,
                    )
                    videos.append(video)
            except:
                log.error(f'Error on {colorize_json(contentItem)} in {self}')
                raise

        log.info(f'Found {len(videos)} unique videos for \'{playlistTitle}\' in {self}')
        return playlistTitle, videos
