import library.files
from library.logging import cm, colorize_json, color

import json
import logging
import os
import requests
import time
import attr

from typing import Optional, List, Tuple

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

    @property
    def basename(self):
        return f'{self.title}.{self.extension}'

    @property
    def filename(self):
        if not library.files.is_dir(self.dstdir):
            raise ValueError(f'Not dir: {value}')

        return os.path.join(self.dstdir, self.basename)


def get_best_stream(video: YoutubeVideo, sleepTime=1200):
    log.debug(f'Searching best stream for {video}')
    ok = False
    while not ok:
        try:
            pafy_video = pafy.new(video.url)
            ok = True
        except IndexError:
            log.exception('Failed to create pafy video')
            log.info(f'Sleeping for {sleepTime} seconds')
            time.sleep(sleepTime)
    best_stream = pafy_video.getbest(preftype=video.preftype)
    log.info(f'Streams: {pafy_video.streams}, best stream: {best_stream}')
    return best_stream


def download_video() -> Optional[Exception]:
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

    def _fast_url_title(self):
        text = requests.get(self.url).text

        start_expression = 'var ytInitialData ='
        end_expression = '</script>'
        start_pos = text.find(start_expression) + len(start_expression)
        end_pos = text.find(end_expression, start_pos)
        js_data = text[start_pos:end_pos].strip().strip(';')
        loaded = json.loads(js_data)
        self.playlistTitle = loaded['metadata']['playlistMetadataRenderer']['title']
        contentItems = loaded['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']

        content_items = [item for item in contentItems if 'playlistVideoRenderer' in item]
        for index, contentItem in enumerate(content_items, 1):
            try:
                index_text = int(contentItem['playlistVideoRenderer']['index']['simpleText'])
                assert index_text == index, f'Got index {index_text} instead of {index}'
                video_id = contentItem['playlistVideoRenderer']['videoId']
                title_text = contentItem['playlistVideoRenderer']['title']['runs'][0]['text']
                url = f'https://www.youtube.com/watch?v={video_id}'
                yield url, title_text
            except:
                log.error(f'Error on {colorize_json(contentItem)} in {self}')
                raise

    def _slow_url_title(self):
        pl = pytube.Playlist(self.url)
        self.playlistTitle = pl.title
        for pl_video in pl.videos:
            url = pl_video.watch_url.replace('https://youtube.com', 'https://www.youtube.com')
            yield url, pl_video.title

    def ListVideos(self) -> Tuple[str, List[YoutubeVideo]]:
        log.info(f'Looking for videos in {self}')
        videos = []
        for url, title in self._fast_url_title():
            is_unique, suffix = self.get_unique_suffix(videos, title, url)
            if is_unique:
                video = YoutubeVideo(url, title + suffix, mode=Mode.PAFY)
                videos.append(video)

        log.info(f'Found {len(videos)} unique videos for {self.playlistTitle!r} in {self}')
        return self.playlistTitle, videos
