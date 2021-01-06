import library.download
from library.logging import cm, color

import os

import logging
log = logging.getLogger(__name__)


def run(args):
    save_files = args.save
    add_pavel_victor = args.pavel_viktor

    if save_files and add_pavel_victor:
        log.error('Could not download Павел Виктор videos from save as there too many large videos')
        raise RuntimeError('Could not save all videos')

    for downloader in [
        # library.download.MathusPhys(),
        # library.download.ZnakKachestava(),
    ]:
        downloader.Download(library.location.udr(downloader.GetDirname()))

    all_videos = []

    download_playlists_cfg = {
        # 'Foxford': 'https://www.youtube.com/playlist?list=PL66kIi3dt8A6Hd7soGMFXe6E5366Y66So',
        # 'OnliSkill - 7 класс': 'https://www.youtube.com/playlist?list=PLRqVDT_WVZRkqpQBB1rIGzVKCaPf5qtYi',
        # 'OnliSkill - 8 класс': 'https://www.youtube.com/playlist?list=PLRqVDT_WVZRmWRPyyVVOTe0Jc46eVxqEz',
        # 'OnliSkill - 9 класс': 'https://www.youtube.com/playlist?list=PLRqVDT_WVZRlWUbTOSqswejgrO1RvQQs1',
        'OnliSkill - 10 класс': 'https://www.youtube.com/playlist?list=PLRqVDT_WVZRkKOQFruLNC1v74_jTp6LzW',
        # 'OnliSkill - 11 класс': 'https://www.youtube.com/playlist?list=PLRqVDT_WVZRkCHtZmveDa9z3G1IiPpisi',
    }
    for dirname, playlist_url in download_playlists_cfg.items():
        playlist = library.download.YoutubePlaylist(playlist_url)
        playlist_title, videos = playlist.ListVideos()
        dstdir = library.location.udr('Видео', dirname)
        if not os.path.exists(dstdir):
            os.mkdir(dstdir)
        for video in videos:
            video.set_dstdir(dstdir)
            all_videos.append(video)

    videos_download_cfg = {
        'CrashCoursePhysics': [
            # https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV
            ('https://www.youtube.com/watch?v=ZM8ECpBuQYE', '1 - Motion - 01 - Motion in a Straight Line'),
            ('https://www.youtube.com/watch?v=ObHJJYvu3RE', '1 - Motion - 02 - Derivatives'),
            ('https://www.youtube.com/watch?v=jLJLXka2wEM', '1 - Motion - 03 - Integrals'),
            ('https://www.youtube.com/watch?v=w3BhzYI6zXU', '1 - Motion - 04 - Vectors and 2D Motion'),
            ('https://www.youtube.com/watch?v=kKKM8Y-u7ds', '1 - Motion - 05 - Newtons Laws'),
            ('https://www.youtube.com/watch?v=fo_pmp5rtzo', '1 - Motion - 06 - Friction'),
            ('https://www.youtube.com/watch?v=bpFK2VCRHUs', '1 - Motion - 07 - Uniform Circular Motion'),
            ('https://www.youtube.com/watch?v=7gf6YpdvtE0', '1 - Motion - 08 - Newtonian Gravity'),
            ('https://www.youtube.com/watch?v=w4QFJb9a8vo', '1 - Motion - 09 - Work Energy and Power'),
            ('https://www.youtube.com/watch?v=Y-QOfc2XqOk', '1 - Motion - 10 - Collisions'),
            ('https://www.youtube.com/watch?v=fmXFWi-WfyU', '1 - Motion - 11 - Rotational Motion'),
            ('https://www.youtube.com/watch?v=b-HZ1SZPaQw', '1 - Motion - 12 - Torque'),
            ('https://www.youtube.com/watch?v=9cbF9A6eQNA', '1 - Motion - 13 - Statics'),
            ('https://www.youtube.com/watch?v=b5SqYuWT4-4', '1 - Motion - 14 - Fluids at Rest'),
            ('https://www.youtube.com/watch?v=fJefjG3xhW0', '1 - Motion - 15 - Fluids in Motion'),
            ('https://www.youtube.com/watch?v=jxstE6A_CYQ', '1 - Motion - 16 - Simple Harmonic Motion'),
            ('https://www.youtube.com/watch?v=TfYCnOvNnFU', '2 - Waves and Sound - 17 - Traveling Waves'),
            ('https://www.youtube.com/watch?v=qV4lR9EWGlY', '2 - Waves and Sound - 18 - Sound'),
            ('https://www.youtube.com/watch?v=XDsk6tZX55g', '2 - Waves and Sound - 19 - The Physics of Music'),
            ('https://www.youtube.com/watch?v=6BHbJ_gBOk0', '3 - Temperature - 20 - Temperature'),
            ('https://www.youtube.com/watch?v=WOEvvHbc240', '3 - Temperature - 21 - Kinetic Theory and Phase Changes'),
            ('https://www.youtube.com/watch?v=tuSC0ObB-qY', '3 - Temperature - 22 - The Physics of Heat'),
            ('https://www.youtube.com/watch?v=4i1MUWJoI0U', '3 - Temperature - 23 - Thermodynamics'),
            ('https://www.youtube.com/watch?v=p1woKh2mdVQ', '3 - Temperature - 24 - Engines'),
            ('https://www.youtube.com/watch?v=TFlVWf8JX4A', '4 - Electricity and Magnetism - 25 - Electric Charge'),
            ('https://www.youtube.com/watch?v=mdulzEfQXDE', '4 - Electricity and Magnetism - 26 - Electric Fields'),
            ('https://www.youtube.com/watch?v=ZrMltpK6iAw', '4 - Electricity and Magnetism - 27 - Voltage Electric Energy and Capacitors'),
            ('https://www.youtube.com/watch?v=HXOok3mfMLM', '4 - Electricity and Magnetism - 28 - Electric Current'),
            ('https://www.youtube.com/watch?v=g-wjP1otQWI', '4 - Electricity and Magnetism - 29 - DC Resistors &amp; Batteries'),
            ('https://www.youtube.com/watch?v=-w-VTw0tQlE', '4 - Electricity and Magnetism - 30 - Circuit Analysis'),
            ('https://www.youtube.com/watch?v=vuCJP_5KOlI', '4 - Electricity and Magnetism - 31 - Capacitors and Kirchhoff'),
            ('https://www.youtube.com/watch?v=s94suB5uLWw', '4 - Electricity and Magnetism - 32 - Magnetism'),
            ('https://www.youtube.com/watch?v=5fqwJyt4Lus', '4 - Electricity and Magnetism - 33 - Amperes Law'),
            ('https://www.youtube.com/watch?v=pQp6bmJPU_0', '4 - Electricity and Magnetism - 34 - Induction - An Introduction'),
            ('https://www.youtube.com/watch?v=9kgzA0Vd8S8', '4 - Electricity and Magnetism - 35 - How Power Gets to Your Home'),
            ('https://www.youtube.com/watch?v=Jveer7vhjGo', '4 - Electricity and Magnetism - 36 - AC Circuits'),
            ('https://www.youtube.com/watch?v=K40lNL3KsJ4', '4 - Electricity and Magnetism - 37 - Maxwells Equations'),
            ('https://www.youtube.com/watch?v=Oh4m8Ees-3Q', '5 - Light - 38 - Geometric Optics'),
            ('https://www.youtube.com/watch?v=IRBfpBPELmE', '5 - Light - 39 - Light Is Waves'),
            ('https://www.youtube.com/watch?v=-ob7foUzXaY', '5 - Light - 40 - Spectra Interference'),
            ('https://www.youtube.com/watch?v=SddBPTcmqOk', '5 - Light - 41 - Optical Instruments'),
            ('https://www.youtube.com/watch?v=AInCqm5nCzw', '5 - Light - 42 - Special Relativity'),
            ('https://www.youtube.com/watch?v=7kb1VT0J3DE', '6 - Quantum - 43 - Quantum Mechanics - Part 1'),
            ('https://www.youtube.com/watch?v=qO_W70VegbQ', '6 - Quantum - 44 - Quantum Mechanics - Part 2'),
            ('https://www.youtube.com/watch?v=lUhJL7o6_cA', '6 - Quantum - 45 - Nuclear Physics'),
            ('https://www.youtube.com/watch?v=VYxYuaDvdM0', '6 - Quantum - 46 - Astrophysics and Cosmology'),
        ],
        'Горбушин': [
            # https://www.youtube.com/playlist?list=PLNG6BIg2XJxCfZtigKso6rBpJ2yk_JFVp'
            ('https://www.youtube.com/watch?v=yvZoJ9oA2T0', 'Подготовка к ЕГЭ по физике. Занятие 01'),
            ('https://www.youtube.com/watch?v=znsFzrsHXcw', 'Подготовка к ЕГЭ по физике. Занятие 02'),
            ('https://www.youtube.com/watch?v=woiO_HENO20', 'Подготовка к ЕГЭ по физике. Занятие 03'),
            ('https://www.youtube.com/watch?v=cPP9sPWmNds', 'Подготовка к ЕГЭ по физике. Занятие 04'),
            ('https://www.youtube.com/watch?v=9zUxpWaRnN0', 'Подготовка к ЕГЭ по физике. Занятие 05'),
            ('https://www.youtube.com/watch?v=2vZfPKmfeCs', 'Подготовка к ЕГЭ по физике. Занятие 06'),
            ('https://www.youtube.com/watch?v=lkRIteVb0lU', 'Подготовка к ЕГЭ по физике. Занятие 07'),
            ('https://www.youtube.com/watch?v=E3tFXjh5WFY', 'Подготовка к ЕГЭ по физике. Занятие 08'),
            ('https://www.youtube.com/watch?v=9XIZffuvibY', 'Подготовка к ЕГЭ по физике. Занятие 09'),
            ('https://www.youtube.com/watch?v=ScpikkktFeM', 'Подготовка к ЕГЭ по физике. Занятие 10'),
            ('https://www.youtube.com/watch?v=E214eHekXGA', 'Подготовка к ЕГЭ по физике. Занятие 11'),
            ('https://www.youtube.com/watch?v=E77nKXA3XGM', 'Подготовка к ЕГЭ по физике. Занятие 12'),
            ('https://www.youtube.com/watch?v=Yso604wZlls', 'Подготовка к ЕГЭ по физике. Занятие 13'),
            ('https://www.youtube.com/watch?v=f4i99JCpDaE', 'Подготовка к ЕГЭ по физике. Занятие 14'),
            ('https://www.youtube.com/watch?v=JPQe2wTsq34', 'Подготовка к ЕГЭ по физике. Занятие 15'),
            ('https://www.youtube.com/watch?v=o2rI59dasHc', 'Подготовка к ЕГЭ по физике. Занятие 16'),
            ('https://www.youtube.com/watch?v=XrAvEu7dU4o', 'Подготовка к ЕГЭ по физике. Занятие 17'),
            ('https://www.youtube.com/watch?v=un39S9MGUtQ', 'Подготовка к ЕГЭ по физике. Занятие 18'),
            ('https://www.youtube.com/watch?v=DEVHbDMiTA8', 'Подготовка к ЕГЭ по физике. Занятие 19'),
            ('https://www.youtube.com/watch?v=-mHpFMPXgfs', 'Подготовка к ЕГЭ по физике. Занятие 20'),
            ('https://www.youtube.com/watch?v=ieZkxvs-134', 'Подготовка к ЕГЭ по физике. Занятие 21'),
            ('https://www.youtube.com/watch?v=Dc_yG7EAuls', 'Подготовка к ЕГЭ по физике. Занятие 22'),
            ('https://www.youtube.com/watch?v=TdKHj4ZKM9o', 'Подготовка к ЕГЭ по физике. Занятие 23'),
            ('https://www.youtube.com/watch?v=2kOmU6WItv8', 'Подготовка к ЕГЭ по физике. Занятие 24'),
            ('https://www.youtube.com/watch?v=pc0wzU-wTMg', 'Подготовка к ЕГЭ по физике. Занятие 25'),
        ],
        'GetAClass': [
            ('https://www.youtube.com/watch?v=8yXf4Gawl4w', '8 - 01 - Действия электрического тока'),
            ('https://www.youtube.com/watch?v=SwNJwbU_lYU', '8 - 02 - Электролиз'),
            ('https://www.youtube.com/watch?v=RU_-6Ahalqk', '8 - 03 - Направление электрического тока'),
            ('https://www.youtube.com/watch?v=iyR4Nt7Twg4', '8 - 04 - Закон Ома'),
            ('https://www.youtube.com/watch?v=RnQGENiF-QM', '8 - 05 - Внутреннее сопротивление'),
            ('https://www.youtube.com/watch?v=X7_lDtGzXTY', '8 - 06 - Последовательное и параллельное соединение сопротивлений'),
            ('https://www.youtube.com/watch?v=no9KjloMdxU', '8 - 07 - Сопротивление куба'),
            ('https://www.youtube.com/watch?v=DowFnoMYqgI', '8 - 08 - Лампа накаливания'),
            ('https://www.youtube.com/watch?v=8GvuGCE9JQI', '8 - 09 - Электродвижущая сила (ЭДС)'),
            ('https://www.youtube.com/watch?v=GGnFhHSCuAs', '8 - 10 - Закон Джоуля-Ленца. Часть 1'),
            ('https://www.youtube.com/watch?v=xlDaZVQWbNA', '8 - 11 - Закон Джоуля-Ленца. Часть 2'),
            ('https://www.youtube.com/watch?v=4j4T9wyRAGQ', '10 - 12 - Коэффициент мощности косинус фи'),
            ('https://www.youtube.com/watch?v=1T8FRhLCUJM', '8 - Коронный разряд и огни святого Эльма'),
            ('https://www.youtube.com/watch?v=627QB4DGE8k', '10 - 05 - Диэлектрик в электрическом поле'),
            ('https://www.youtube.com/watch?v=NV2V5VcXlEI', '8 - Переменный ток'),
            ('https://www.youtube.com/watch?v=BQOK_b9TsjE', '8 - Когда переменный ток становится постоянным'),
            ('https://www.youtube.com/watch?v=denwtwcfvZw', '8 - Стабилитрон'),
            ('https://www.youtube.com/watch?v=4E1AxUMUz-g', '9 - Дисперсия света'),
            ('https://www.youtube.com/watch?v=BhYKN21olBw', '9 - Brain Damage'),
            ('https://www.youtube.com/watch?v=mh-LTSGjFsE', '9 - 10 - Закон Гука и энергия упругой деформации'),
        ],
        'misc': [
            ('https://www.youtube.com/watch?v=p15KNqWUZ-c', 'Сергей Гуриев - Экономика красоты и счастья - 2012'),
            ('https://www.youtube.com/watch?v=OHCobJjMHuM', 'Творческая дистанционка от Димы Зицера - 2020-03-20'),
            ('https://www.youtube.com/watch?v=dSVdjmabpgg', 'HBO - Welcome to Chechnya - 2020'),
            ('https://www.youtube.com/watch?v=lYTdewh-dhY', 'Открытая Россия - Семья - Фильм о Рамзане Кадырове - 2015'),
            ('https://www.youtube.com/watch?v=2nTmeuXQT5w', '2020 - Математический марафон'),
            ('https://www.youtube.com/watch?v=vF1UGmi5m8s', '2019 - Дудь - Беслан'),
            ('https://www.youtube.com/watch?v=-TSD1cX2htQ', '2019 - Новая Газета - Беслан'),
        ],
    }
    for dirname, videos in videos_download_cfg.items():
        dirname = library.location.udr('Видео', dirname)
        for url, title in videos:
            video = library.download.YoutubeVideo(url, title, dstdir=dirname, use_requests=True)
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
        ('10-9', 'Основы электродинамики', [
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
            youtube_playlist = library.download.YoutubePlaylist(playlist_url)
            small_topic, videos = youtube_playlist.ListVideos()
            dirname = f'Павел Виктор - {prefix}-{index} - {large_topic} - {small_topic}'
            for video in videos:
                video.set_dstdir(library.location.udr('Видео', dirname))
                all_videos.append(video)

    log.info(f'Got total of {len(all_videos)} videos')

    for video in all_videos:
        if save_files:
            video.download()
        else:
            log.info(video)


def populate_parser(parser):
    parser.add_argument('-s', '--save', help='Save videos to hard drive', action='store_true')
    parser.add_argument('-p', '--pavel-viktor', help='Add Pavel Viktor', action='store_true')
    parser.set_defaults(func=run)
