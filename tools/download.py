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
            log.info(f'Downloading channel {cm(channel_url, color=color.Blue)} to {path}')
            channel = pytube.Channel(channel_url)
            for video in channel.videos:
                title = clean_title(video.title.strip())
                extension = 'mp4'
                filename = f'{video.publish_date.strftime("%F")} - {title}.{extension}'
                if save_files:
                    streams = video.streams.filter(progressive=True, file_extension=extension)
                    best_stream = streams.order_by('resolution').desc().first()
                    log.info(f'Downloading {cm(filename, color=color.Green)}')
                    best_stream.download(output_path=path, filename=filename, skip_existing=True)
                else:
                    log.info(f'got video {cm(filename, color=color.Green)}')

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

    pavel_victor_config = [
        # 'Курс физики основной школы'
        ('07', '7 класс', [
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9TcTQiq-EZeVuVPc6P8PSX',
        ]),
        ('08', '8 класс', [
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_dGE-7OdXgBXu52_GbnvF7',
        ]),
        ('09', '9 класс', [
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9fX9rgG5Z20V_M2AaUKErL',
        ]),
        ('09', 'Подготовка к ДПА', [
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8Y5BWL3nyecfr2nK6xqwIO',
        ]),
        ('10-0', 'Курс физики старшей школы. Физические величины и их измерение. Теория погрешностей', [
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw-LHb3pbAt99Uvx6RRehPPk',  # Измерения. Теория погрешностей.
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw-O0knvaGt6jCCLA7gpD_UN',  # Физический практикум
        ]),
        ('10-1', 'Механика. Кинематика', [
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_h-12xDu-GKRHqtVFYgDHt',  # Основные понятия кинематики
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_DkIADOZqsWYn2hTFohPBU',  # Равномерное прямолинейное движение
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw-Z3QO7VYVcyWO1QHHi6pbf',  # Равноускоренное движение
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8Pe-su21PGMr9hhYPxhcGK',  # Криволинейное и вращательдвижение
        ]),
        ('10-2', 'Механика. Законы динамики', [
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8mS6wFGCLPvweu8yRGcU4j',  # Законы Ньютона
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9QCJdAsJFv2rQ4NrgNGBsV',  # Силы в природе
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw__kE2T8jk0xFAgjKmQ2dF2',  # Статика
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_2yM8RxiH6Ff18cGWY9WOD',  # Применение законов динамики
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw-kdIQk9HA2MZGuUCqdGTKY',  # Динамика вращательного движения
        ]),
        ('10-3', 'Механика. Законы сохранения. Движение жидкостей и газов', [
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8zTgiJU5BM0hf-9seXf-Eq',  # Импульс и момент импульса
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_7NJesD6o9yfzDk0vtnnIm',  # Работа и энергия
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw-2R0i_j9tf1Z6QEw1WhJzt',  # Движение жидкостей и газов
        ]),
        ('10-6', 'Молекулярная физика. МКТ и термодинамика', [
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_6jGjxZmTxnAKY-LdrzM1a',  # Основы молекулярно-кинетичестеории
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw80Lo4RK0VPCvCiDdS3ISgq',  # Уравнение состояния идеального газа
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_ksmc1o1ZNUBG5zqvqq0Ue',  # Основы термодинамики
        ]),
        ('10-7', 'Молекулярная физика. Свойства паров, жидкостей и твердых тел', [
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_rrO-8LVG4vA2MLHw1VJ4Y',  # Свойства паров
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw98LcoigAEMKWmC0o0zilBO',  # Свойства жидкостей
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8sdkmL_wvHS8zTr7BRY6py',  # Свойства твердых тел
        ]),
        ('10-8', 'Основы электродинамики', [
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8Jtndre2W-4cZCnZTfuqc4',  # Электростатика
        ]),
        ('10-9', 'Основы электродинамики', [
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_HRBg3k8VFTp2mDMgKFyIZ',  # Законы постоянного тока
        ]),
        ('11-1', 'Основы электродинамики', [
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_clhMs2ShkQayZK3xIGiSf',  # Магнитное поле
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw-4S63vaIZs4XJmsGx9WylD',  # Электромагнитная индукция
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8twHGrxC2EsgswUgrlH2eF',  # Электрический ток в различных средах
        ]),
        ('11-2', 'Колебания и волны', [
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8eAdCNXDpyu85Pn95ZXFiE',  # Повторение механики (обзор)
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9GedypbA-En9aam5M356v8',  # Элементы дифференциальнисчисления
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_uIvisbeffNrk6G44ma735',  # Механические колебания
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9hcmjWIr-E_eJwWoJpboQ5',  # Электромагнитные колебания
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8IDqme-3NQWQEBlTHxlEfm',  # Механические волны
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9R8PfiMnh2wkLwcpyV9ahA',  # Электромагнитные волны
        ]),
        ('11-3', 'Оптика, физика атома и ядра', [
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw-t-V-oTSJBemkt9gysB8xE',  # Геометрическая оптика
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9M6EaKwezrpPY361i4FqZ1',  # Фотометрия
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9nEvX4BxcRMTRffGvIzMis',  # Физическая оптика
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw-1grjrzQxwUBhI7Qy-zS0D',  # Атомная физика
            'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_sm3UrSTHX4EPZZJjBsoTs',  # Физика ядра
        ]),
    ]

    if not add_pavel_victor:
        pavel_victor_config = []

    for prefix, large_topic, playlists in pavel_victor_config:
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
