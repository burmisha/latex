import library.download
from library.logging import cm, color
from typing import List, Optional
import multiprocessing

import pytube
import attr
import os

import logging
log = logging.getLogger(__name__)


def clean_title(title: str) -> str:
    for src, dst in [
        (' @Продолжение следует', ''),
        ('?', '.'),
        ('@', ''),
        ('*', ''),
        ('№', ''),
        ('«', ''),
        ('»', ''),
        (' 18+', ''),
        ('18+', ''),
        (': ', ' - '),
        ('–', '-'),
        ('—', '-'),
        ('/', ' ',),
        ('(', '',),
        (')', '',),
        ('#', '',),
        ('$', '',),
        ('%', '',),
        ('^', '',),
        ('&', '',),
        (' .', '.'),
        ('..', ' '),
        ('  ', ' '),
        ('  ', ' '),
        ('  ', ' '),
        ('..', ''),
        ('"', ''),
        ('…', ''),
    ]:
        title = title.replace(src, dst)

    return title


@attr.s
class ChannelConfig:
    dirname: str = attr.ib()
    url: str = attr.ib()
    filters: Optional[List[str]] = attr.ib(default=None)

    def matches(self, name):
        if not self.filters:
            return True
        return any(flt in name for flt in self.filters)

    def __str__(self):
        return f'channel {cm(self.url, color=color.Blue)}, path part: {self.dirname}'


def get_videos_from_channel(channel_config: ChannelConfig):
    log.info(f'Getting videos from {channel_config}')
    path = library.location.udr('Видео', channel_config.dirname)
    channel = pytube.Channel(channel_config.url)
    index = 0
    for index, video in enumerate(channel.videos, 1):
        title = clean_title(video.title.strip())
        filename = f'{video.publish_date.strftime("%F")} - {title}'
        if not channel_config.matches(title):
            log.info(f'  skip {cm(filename, color=color.Green)}')
            continue
        log.info(f'  got  {cm(filename, color=color.Green)}')

        yield library.download.youtube.YoutubeVideo(
            f'https://www.youtube.com/watch?v={video.video_id}',
            filename,
            dstdir=path,
            mode=library.download.youtube.Mode.PYTYBE,
        )

    log.info(f'Found {index} videos in {channel_config}')


def get_pavel_victor_videos(pavel_victor_config: dict):
    for key, playlists in pavel_victor_config.items():
        prefix, large_topic = key.split(' ', 1)
        for index, playlist_url in enumerate(playlists, 1):
            youtube_playlist = library.download.youtube.YoutubePlaylist(playlist_url)
            small_topic, videos = youtube_playlist.ListVideos()
            dirname = f'Павел Виктор - {prefix}-{index} - {large_topic} - {small_topic}'
            for video in videos:
                video.dstdir = library.location.udr('Видео', dirname)
                yield video


def run(args):
    save_files = args.save
    add_pavel_victor = args.pavel_viktor
    download_cfg = library.files.load_yaml_data('download.yaml')

    if save_files and add_pavel_victor:
        log.error('Could not download Павел Виктор videos from save as there\'re too many large videos')
        raise RuntimeError('Could not save all videos')

    all_videos = []

    if args.channels:
        log.warning(cm('Listing channels is almost infinite', color=color.Red))
        for row in download_cfg['Channels']:
            channel_config = ChannelConfig(**row)
            for video in get_videos_from_channel(channel_config):
                all_videos.append(video)

    for items, dirname in [
        # (library.download.mathus.get_items(), library.location.udr('Материалы - mathus')),
        # (library.download.znakka4estva.get_items(), library.location.udr('Материалы - znakka4estva')),
        # (library.download.phys_nsu_ru.get_items(), library.location.udr('Материалы - phys.nsu.ru')),
    ]:
        library.download.multiple.download_items(items, dirname, force=False)

    for dirname, playlist_url in download_cfg['Playlists'].items():
        playlist = library.download.youtube.YoutubePlaylist(playlist_url)
        dstdir = library.location.udr('Видео', dirname)
        if not os.path.exists(dstdir):
            os.mkdir(dstdir)
        _, videos = playlist.ListVideos()
        for video in videos:
            video.dstdir = dstdir
            all_videos.append(video)

    for dirname, videos in download_cfg['Explicit'].items():
        dirname = library.location.udr('Видео', dirname)
        for url, title in videos.items():
            video = library.download.youtube.YoutubeVideo(
                url,
                title,
                dstdir=dirname,
                mode=library.download.youtube.Mode.REQUESTS,
            )
            all_videos.append(video)

    if add_pavel_victor:
        for video in get_pavel_victor_videos(download_cfg['PavelVictor']):
            all_videos.append(video)

    log.info(f'Got total of {len(all_videos)} videos')

    topic_detector = library.topic.TopicDetector()
    topic_filter =  library.topic.TopicFilter(args.filter)

    video_with_topics = []
    for video in all_videos:
        topic_index = topic_detector.get_topic_index(video.title)
        video_with_topics.append((video, topic_index))

    if args.sort:
        video_with_topics = [(v, t) for v, t in video_with_topics if t]
        video_with_topics.sort(key=lambda video_with_topic: video_with_topic[1])

    if save_files:
        missing_videos = [video for video in all_videos if not os.path.exists(video.filename)]
        if missing_videos:
            threads_count = args.threads
            log.info(f'Downloading {len(missing_videos)} videos in {threads_count} threads:')
            for video in missing_videos:
                log.info(f'  {video}')
            pool = multiprocessing.Pool(processes=threads_count)
            results = pool.map(library.download.youtube.download_video, missing_videos)

            failed_videos_count = sum(1 for r in results if r)
            if failed_videos_count:
                raise RuntimeError(f'Got {failed_videos_count} failed videos:')
    else:
        for video, topic_index in video_with_topics:
            if topic_filter.matches(topic_index):
                if not topic_index:
                    log.info(video)
                else:
                    log.info(f'{video}, {topic_index}')


def populate_parser(parser):
    parser.add_argument('-s', '--save', help='Save videos to hard drive', action='store_true')
    parser.add_argument('-p', '--pavel-viktor', help='Add Pavel Viktor', action='store_true')
    parser.add_argument('-f', '--filter', help='Choose only videos matching filters')
    parser.add_argument('--sort', help='Sort by topic', action='store_true')
    parser.add_argument('--channels', help='Add channels (infinite)', action='store_true')
    parser.add_argument('--threads', help='Threads count to download', type=int, default=4)
    parser.set_defaults(func=run)
