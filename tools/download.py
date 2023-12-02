import library.download
import library.normalize
from library.logging import cm, color
from typing import List, Optional
import multiprocessing

import pytube
import attr
import os

import logging
log = logging.getLogger(__name__)


THREADS_COUNT = 4
RETRIES_COUNT = 3


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
    channel = pytube.Channel(channel_config.url)
    for video in channel.videos:
        title = canonizer.Canonize(video.title.strip())
        filename = f'{video.publish_date.strftime("%F")} - {title}'
        if not channel_config.matches(title):
            log.info(f'  skip {cm(filename, color=color.Green)}')
            continue
        log.info(f'  got  {cm(filename, color=color.Green)}')

        yield library.download.youtube.YoutubeVideo(
            f'https://www.youtube.com/watch?v={video.video_id}',
            filename,
            dstdir=channel_config.dirname,
            mode=library.download.youtube.Mode.PYTYBE,
        )


def get_explicit_videos(explicit_config: dict):
    log.info('Getting explicit videos')
    for dirname, videos in explicit_config.items():
        for url, title in videos.items():
            yield library.download.youtube.YoutubeVideo(
                url,
                title,
                dst_dir=dirname,
                # mode=library.download.youtube.Mode.PYTYBE,
                # mode=library.download.youtube.Mode.PAFY,
                mode=library.download.youtube.Mode.REQUESTS,
            )


def get_pavel_viktor_videos(pavel_victor_config: dict):
    log.info('Getting Pavel Viktor videos')
    for key, playlists in pavel_victor_config.items():
        prefix, large_topic = key.split(' ', 1)
        for index, playlist_url in enumerate(playlists, 1):
            youtube_playlist = library.download.youtube.YoutubePlaylist(playlist_url)
            small_topic, videos = youtube_playlist.ListVideos()
            dirname = f'Павел Виктор - {prefix}-{index} - {large_topic} - {small_topic}'
            for video in videos:
                video.dstdir = library.location.external_toshiba(dirname)
                yield video


def download_videos(
    *,
    videos: List[library.download.youtube.YoutubeVideo],
    base_dir: str,
    threads: int,
    retries: int,
):
    for try_index in range(retries):
        videos = [video for video in videos if not os.path.exists(video.filename)]
        if videos:
            log.info(f'[{try_index + 1}/{retries}] Downloading {len(videos)} videos in {threads} threads:')
            for video in videos:
                log.info(f'  {video}')
            pool = multiprocessing.Pool(processes=threads)
            pool.map(library.download.youtube.download_video, videos)
        else:
            log.info(f'No more videos to download')
            return

    if videos:
        raise RuntimeError(f'После {retries} попыток не скачано {len(videos)} видео')


def get_all_videos(*, add_channels: bool=False, add_playlists: bool=False, add_pavel_viktor: bool=False):
    download_cfg = library.files.load_yaml_data('download.yaml')

    if add_channels:
        log.warning(cm('Listing channels is almost infinite', color=color.Red))
        for row in download_cfg['Channels']:
            channel_config = ChannelConfig(**row)
            for video in get_videos_from_channel(channel_config):
                yield video

    if add_playlists:
        log.info('Listing playlists')
        for dirname, playlist_url in download_cfg['Playlists'].items():
            playlist = library.download.youtube.YoutubePlaylist(playlist_url)
            _, videos = playlist.ListVideos()
            for video in videos:
                video.dstdir = dirname
                yield video

    for video in get_explicit_videos(download_cfg['Explicit']):
        yield video

    if add_pavel_viktor:
        log.info('Listing Pavel Viktor')
        for video in get_pavel_viktor_videos(download_cfg['PavelVictor']):
            yield video


def run(args):
    save_files = args.save

    if save_files and args.pavel_viktor:
        log.warning(cm('Saving all Павел Виктор videos will take up to 20 hours', color=color.Red))

    for items, dirname in [
        # (library.download.mathus.get_items(), library.location.udr('Материалы - mathus')),
        # (library.download.znakka4estva.get_items(), library.location.udr('Материалы - znakka4estva')),
        # (library.download.phys_nsu_ru.get_items(), library.location.udr('Материалы - phys.nsu.ru')),
    ]:
        library.download.multiple.download_items(items, dirname, force=False)

    videos = [
        video
        for video in get_all_videos(
            add_channels=args.channels,
            add_playlists=args.playlists,
            add_pavel_viktor=args.pavel_viktor
        )
    ]

    for video in videos:
        video.base_dir = args.base_dir

    if args.title_filter:
        videos = [video for video in videos if args.title_filter in video.title]

    missing_dirs = set(video.dir_name for video in videos if not os.path.exists(video.dir_name))
    for missing_dir in sorted(missing_dirs):
        log.info(f'Create missing dir: {missing_dir}')
        os.mkdir(missing_dir)

    log.info(f'Got total of {len(videos)} videos')

    canonizer = library.normalize.TitleCanonizer()
    for video in videos:
        video.title = canonizer.Canonize(video.title)

    topic_detector = library.topic.TopicDetector()
    topic_filter = library.topic.TopicFilter(args.filter)

    video_with_topics = []
    for video in videos:
        topic_index = topic_detector.get_topic_index(video.title)
        video_with_topics.append((video, topic_index))

    if args.sort:
        video_with_topics = [(v, t) for v, t in video_with_topics if t]
        video_with_topics.sort(key=lambda video_with_topic: video_with_topic[1])

    if save_files:
        download_videos(
            videos=videos,
            base_dir=args.base_dir,
            threads=args.threads,
            retries=args.retries,
        )
    else:
        for video, topic_index in video_with_topics:
            if topic_filter.matches(topic_index):
                log.info(f'{video}, topic index: {topic_index}')


def populate_parser(parser):
    parser.add_argument('-s', '--save', help='Save videos to hard drive', action='store_true')
    parser.add_argument('-p', '--pavel-viktor', help='Add Pavel Viktor', action='store_true')
    parser.add_argument('-f', '--filter', help='Choose only videos matching filters')
    parser.add_argument('--title-filter', help='Choose video by title')
    parser.add_argument('--sort', help='Sort by topic', action='store_true')
    parser.add_argument('--channels', help='Add channels (infinite)', action='store_true')
    parser.add_argument('--playlists', help='Add playlists (finite)', action='store_true')
    parser.add_argument('--threads', help='Threads count to download', type=int, default=THREADS_COUNT)
    parser.add_argument('--retries', help='Retries count', type=int, default=RETRIES_COUNT)
    parser.add_argument('--base-dir', help='Base dir', default=library.location.udr('Видео'))
    parser.set_defaults(func=run)
