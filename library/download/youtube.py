import library.files
from library.normalize import TitleCanonizer
from library.logging import cm, colorize_json, color

import json
import logging
import os
import requests
import time

log = logging.getLogger(__name__)


try:
    import pafy  # http://np1.github.io/pafy/
except ImportError:
    log.error('Failed to load pafy')


class YoutubeVideo:
    def __init__(self, url, title, dstdir=None, use_requests=False):
        assert url.startswith('https://www.youtube.com/watch?v=')
        self._url = url
        self._title = title
        self._dstdir = dstdir
        self._use_requests = use_requests

    def __str__(self):
        return f'{cm(self._title, color=color.Yellow)} ({self._url}) from {os.path.basename(self._dstdir)}'

    def set_dstdir(self, dstdir):
        self._dstdir = dstdir

    def get_filename(self):
        assert library.files.is_dir(self._dstdir)
        return os.path.join(self._dstdir, f'{self._title}.mp4')

    def set_use_requests(self, use_requests):
        self._use_requests = use_requests

    def get_best_stream(self, preftype=None, sleepTime=1200):
        log.debug(f'Searching best stream for {self}')
        ok = False
        while not ok:
            try:
                video = pafy.new(self._url)
                ok = True
            except IndexError:
                log.exception('Failed to get best stream')
                log.info(f'Sleeping for {sleepTime} seconds')
                time.sleep(sleepTime)
        best_stream = video.getbest(preftype=preftype)
        log.info(f'Streams: {video.streams}, best stream: {best_stream}')
        return best_stream

    def download(self):
        filename = self.get_filename()
        if os.path.exists(filename):
            log.info(f'Skipping {self} as \'{filename}\' exists')
        else:
            log.info(f'Downloading {self} to \'{filename}\'')
            best_stream = self.get_best_stream(preftype='mp4')
            if self._use_requests:
                data = requests.get(best_stream.url).content
                with open(filename, 'wb') as f:
                    f.write(data)
            else:
                best_stream.download(filepath=filename)


class YoutubePlaylist:
    def __init__(self, url):
        assert url.startswith('https://www.youtube.com/playlist?list=PL')
        self._Url = url
        self._TitleCanonizer = TitleCanonizer()

    def __str__(self):
        return f'{cm(self._Url, color=color.Cyan)}'

    def get_unique_suffix(self, videos, title, url):
        suffixes = [''] + [f' - {i}' for i in range(2, 4)]
        for suffix in suffixes:
            new_title = title + suffix
            has_duplicate = False
            for video in videos:
                if video._title == new_title:
                    has_duplicate = True
                    if video._url == url:
                        log.info(f'Found full duplicate for {title!r}, skipping')
                        return False, None
                    else:
                        log.warn((
                            f'Found duplicate for {title!r} with another url: '
                            f'check {video._url} and {url}'
                        ))
            if not has_duplicate:
                if suffix:
                    log.warn(f'Got suffix {suffix} for {title} at {url}')
                return True, suffix

        raise RuntimeError(f'Could not resolve duplicate {title!r}, check {url}')

    def ListVideos(self):
        log.debug(f'Looking for videos in {cm(self._Url, color=color.Cyan)}')
        text = requests.get(self._Url).text

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
                title_text = self._TitleCanonizer.Canonize(title_text)
                url = f'https://www.youtube.com/watch?v={video_id}'

                is_unique, suffix = self.get_unique_suffix(videos, title_text, url)
                if is_unique:
                    videos.append(YoutubeVideo(url, title_text + suffix))
            except:
                log.error(f'Error on {colorize_json(contentItem)} in {self}')
                raise

        log.info(f'Found {len(videos)} unique videos for \'{playlistTitle}\' in {self}')
        return playlistTitle, videos
