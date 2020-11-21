import library.download


def run(args):
    for downloader in [
        # library.download.MathusPhys(),
        # library.download.ZnakKachestava(),
    ]:
        downloader.Download(library.location.udr(downloader.GetDirname()))

    for videoDownloader in [
        # library.download.GetAClass(),
        # library.download.Gorbushin(),
        # library.download.CrashCoursePhysics(),
        # library.download.Foxford(),
    ]:
        videoDownloader.Download(library.location.udr('Видео'))

    video_count = 0

    for url in [
        # 'https://www.youtube.com/playlist?list=PLNG6BIg2XJxCfZtigKso6rBpJ2yk_JFVp',  # Горбушин
        'https://www.youtube.com/playlist?list=PL66kIi3dt8A6Hd7soGMFXe6E5366Y66So',  # Фоксфорд
        # 'Курс физики основной школы'
        'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9TcTQiq-EZeVuVPc6P8PSX',  # 7 класс
        'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_dGE-7OdXgBXu52_GbnvF7',  # 8 класс
        'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9fX9rgG5Z20V_M2AaUKErL',  # 9 класс — это 8-й
        # 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8Y5BWL3nyecfr2nK6xqwIO',  # Підготовка до ДПА 9 клас
    ]:
        youtubePlaylist = library.download.YoutubePlaylist(url)
        title, videos = youtubePlaylist.ListVideos()
        log.info(f'{title}')
        for index, url, video_title in videos:
            video_count += 1
            log.info(f'{video_title} {url}')

    pavel_victor_config = {
        ('10-0', 'Курс физики старшей школы. Физические величины и их измерение. Теория погрешностей'): {
            0: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw-LHb3pbAt99Uvx6RRehPPk',  # Измерения. Теория погрешностей.
            1: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw-O0knvaGt6jCCLA7gpD_UN',  # Физический практикум
        },
        ('10-1', 'Механика. Кинематика'): {
            1: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_h-12xDu-GKRHqtVFYgDHt',  # Основные понятия кинематики
            2: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_DkIADOZqsWYn2hTFohPBU',  # Равномерное прямолинейное движение
            3: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw-Z3QO7VYVcyWO1QHHi6pbf',  # Равноускоренное движение
            4: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8Pe-su21PGMr9hhYPxhcGK',  # Криволинейное и вращательдвижение</a>
        },
        ('10-2', 'Механика. Законы динамики'): {
            1: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8mS6wFGCLPvweu8yRGcU4j',  # Законы Ньютона
            2: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9QCJdAsJFv2rQ4NrgNGBsV',  # Силы в природе
            3: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw__kE2T8jk0xFAgjKmQ2dF2',  # Статика
            4: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_2yM8RxiH6Ff18cGWY9WOD',  # Применение законов динамики
            5: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw-kdIQk9HA2MZGuUCqdGTKY',  # Динамика вращательного движения
        },
        ('10-3', 'Механика. Законы сохранения. Движение жидкостей и газов'): {
            1: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8zTgiJU5BM0hf-9seXf-Eq',  # Импульс и момент импульса
            2: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_7NJesD6o9yfzDk0vtnnIm',  # Работа и энергия
            3: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw-2R0i_j9tf1Z6QEw1WhJzt',  # Движение жидкостей и газов
        },
        ('10-5', 'Молекулярная физика. МКТ и термодинамика'): {
            1: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_6jGjxZmTxnAKY-LdrzM1a',  # Основы молекулярно-кинетичестеории</a>
            2: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw80Lo4RK0VPCvCiDdS3ISgq',  # Уравнение состояния идеального газа
            3: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_ksmc1o1ZNUBG5zqvqq0Ue',  # Основы термодинамики
        },
        ('10-6', 'Молекулярная физика. Свойства паров, жидкостей и твердых тел'): {
            1: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_rrO-8LVG4vA2MLHw1VJ4Y',  # Свойства паров
            2: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw98LcoigAEMKWmC0o0zilBO',  # Свойства жидкостей
            3: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8sdkmL_wvHS8zTr7BRY6py',  # Свойства твердых тел
        },
        ('10-7', 'Основы электродинамики'): {
            1: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8Jtndre2W-4cZCnZTfuqc4',  # Электростатика
            2: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_HRBg3k8VFTp2mDMgKFyIZ',  # Законы постоянного тока
            3: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_clhMs2ShkQayZK3xIGiSf',  # Магнитное поле
            4: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw-4S63vaIZs4XJmsGx9WylD',  # Электромагнитная индукция
            5: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8twHGrxC2EsgswUgrlH2eF',  # Электрический ток в различных средах
        },
        ('11-1', 'Колебания и волны'): {
            1: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8eAdCNXDpyu85Pn95ZXFiE',  # Повторение механики (обзор)
            2: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9GedypbA-En9aam5M356v8',  # Элементы дифференциальнисчисления</a>
            3: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_uIvisbeffNrk6G44ma735',  # Механические колебания
            4: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9hcmjWIr-E_eJwWoJpboQ5',  # Электромагнитные колебания
            5: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8IDqme-3NQWQEBlTHxlEfm',  # Механические волны
            6: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9R8PfiMnh2wkLwcpyV9ahA',  # Электромагнитные волны
        },
        ('11-2', 'Оптика, физика атома и ядра'): {
            1: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw-t-V-oTSJBemkt9gysB8xE',  # Геометрическая оптика
            2: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9M6EaKwezrpPY361i4FqZ1',  # Фотометрия
            3: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9nEvX4BxcRMTRffGvIzMis',  # Физическая оптика
            4: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw-1grjrzQxwUBhI7Qy-zS0D',  # Атомная физика
            5: 'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_sm3UrSTHX4EPZZJjBsoTs',  # Физика ядра
        },
    }
    for (index_1, title_1), parts_1 in sorted(pavel_victor_config.items()):
        for parts_1, url in sorted(parts_1.items()):
            youtubePlaylist = library.download.YoutubePlaylist(url)
            title_2, videos = youtubePlaylist.ListVideos()
            # assert title_1 == title_2, f'{title_1} != {title_2}'
            full_chapter = f'{index_1}-{parts_1} - {title_2}'
            for index, url, video_title in videos:
                video_count += 1
                log.info(f'{full_chapter}: {video_title} {url}')
    log.info(f'Got total of {video_count} videos')


def populate_parser(parser):
    parser.set_defaults(func=run)
