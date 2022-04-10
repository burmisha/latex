import library.download
from library.logging import cm, color

import pytube

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
        (' .', '.'),
        ('..', ' '),
        ('  ', ' '),
        ('  ', ' '),
        ('  ', ' '),
        ('..', ''),
    ]:
        title = title.replace(src, dst)

    return title


def run(args):
    save_files = args.save
    add_pavel_victor = args.pavel_viktor
    download_cfg = library.files.load_yaml_data('download.yaml')

    if save_files and add_pavel_victor:
        log.error('Could not download Павел Виктор videos from save as there too many large videos')
        raise RuntimeError('Could not save all videos')

    if args.channels:
        log.warning(cm('Listing channels is almost infinite', color=color.Red))
        for path_part, channel_url in download_cfg['Channels'].items():
            path = library.location.udr('Видео', path_part)
            log.info(f'Got channel {cm(channel_url, color=color.Blue)}, path part: {path_part}')
            channel = pytube.Channel(channel_url)
            for video in channel.videos:
                title = clean_title(video.title.strip())
                extension = 'mp4'
                filename = f'{video.publish_date.strftime("%F")} - {title}.{extension}'
                log.info(f'got video {cm(filename, color=color.Green)}')
                if save_files:
                    streams = video.streams.filter(progressive=True, file_extension=extension)
                    best_stream = streams.order_by('resolution').desc().first()
                    log.info(f'Downloading {cm(filename, color=color.Green)}')
                    best_stream.download(output_path=path, filename=filename, skip_existing=True)

    for items, dirname in [
        # (library.download.mathus.get_items(), library.location.udr('Материалы - mathus')),
        # (library.download.znakka4estva.get_items(), library.location.udr('Материалы - znakka4estva')),
        # (library.download.phys_nsu_ru.get_items(), library.location.udr('Материалы - phys.nsu.ru')),
    ]:
        library.download.multiple.download_items(items, dirname, force=False)

    all_videos = []

    for dirname, playlist_url in download_cfg['Playlists'].items():
        playlist = library.download.youtube.YoutubePlaylist(playlist_url)
        playlist_title, videos = playlist.ListVideos()
        dstdir = library.location.udr('Видео', dirname)
        if not os.path.exists(dstdir):
            os.mkdir(dstdir)
        for video in videos:
            video.set_dstdir(dstdir)
            all_videos.append(video)

    for dirname, videos in download_cfg['Explicit'].items():
        dirname = library.location.udr('Видео', dirname)
        for url, title in videos.items():
            video = library.download.youtube.YoutubeVideo(url, title, dstdir=dirname, use_requests=True)
            all_videos.append(video)

    if add_pavel_victor:
        pavel_victor_config = download_cfg['PavelVictor']
    else:
        pavel_victor_config = {}

    for key, playlists in pavel_victor_config.items():
        prefix, large_topic = key.split(' ', 1)
        for index, playlist_url in enumerate(playlists, 1):
            youtube_playlist = library.download.youtube.YoutubePlaylist(playlist_url)
            small_topic, videos = youtube_playlist.ListVideos()
            dirname = f'Павел Виктор - {prefix}-{index} - {large_topic} - {small_topic}'
            for video in videos:
                video.set_dstdir(library.location.udr('Видео', dirname))
                all_videos.append(video)

    log.info(f'Got total of {len(all_videos)} videos')

    topic_detector = library.topic.TopicDetector()
    topic_filter =  library.topic.TopicFilter(args.filter)

    video_with_topics = []
    for video in all_videos:
        topic_index = topic_detector.get_topic_index(video._title)
        video_with_topics.append((video, topic_index))

    if args.sort:
        video_with_topics = [(v, t) for v, t in video_with_topics if t]
        video_with_topics.sort(key=lambda t: t[1])

    failed_videos = []
    for video, topic_index in video_with_topics:
        if save_files:
            try:
                video.download()
            except KeyboardInterrupt:
                log.error(f'Download cancelled: {video}')
                raise
            except:
                log.error(f'Failed to download {video}')
                failed_videos.append(video)
        else:
            if topic_filter.matches(topic_index):
                if not topic_index:
                    log.info(video)
                else:
                    log.info(f'{video}, {topic_index}')

    if failed_videos:
        for video in failed_videos:
            log.info(f'Failed to download {video}')
        raise RuntimeError(f'Got {len(failed_videos)} failed videos:')


def populate_parser(parser):
    parser.add_argument('-s', '--save', help='Save videos to hard drive', action='store_true')
    parser.add_argument('-p', '--pavel-viktor', help='Add Pavel Viktor', action='store_true')
    parser.add_argument('-f', '--filter', help='Choose only videos matching filters')
    parser.add_argument('--sort', help='Sort by topic', action='store_true')
    parser.add_argument('--channels', help='Add channels (infinite)', action='store_true')
    parser.set_defaults(func=run)
