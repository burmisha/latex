import library.download
from library.logging import cm, color

import pytube

import os

import logging
log = logging.getLogger(__name__)


def run(args):
    save_files = args.save
    add_pavel_victor = args.pavel_viktor

    if save_files and add_pavel_victor:
        log.error('Could not download Павел Виктор videos from save as there too many large videos')
        raise RuntimeError('Could not save all videos')

    channels = [
        # (
        #     'https://www.youtube.com/c/%D0%9F%D1%80%D0%BE%D0%B4%D0%BE%D0%BB%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5%D1%81%D0%BB%D0%B5%D0%B4%D1%83%D0%B5%D1%82',
        #     library.location.udr('Видео', 'Продолжение следует'),
        # ),
        # (
        #     'https://www.youtube.com/c/NovayagazetaRu',
        #     library.location.udr('Видео', 'Новая газета'),
        # ),
    ]
    for url, path in channels:
        channel = pytube.Channel(url)
        for video in channel.videos:
            title = video.title.strip()
            extension = 'mp4'
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
            ]:
                title = title.replace(src, dst)

            filename = f'{video.publish_date.strftime("%F")} - {title}.{extension}'
            if save_files:
                streams = video.streams.filter(progressive=True, file_extension=extension)
                best_stream = streams.order_by('resolution').desc().first()
                log.info(f'Downloading {cm(filename, color=color.Green)}')
                best_stream.download(output_path=path, filename=filename, skip_existing=True)

    for downloader in [
        # library.download.MathusPhys(library.location.udr('Материалы - mathus')),
        # library.download.ZnakKachestva(library.location.udr('Материалы - znakka4estva')),
        # library.download.PhysNsuRu(library.location.udr('Материалы - phys.nsu.ru')),
    ]:
        downloader.Download(force=False)

    all_videos = []

    download_playlists_cfg = {
        # 'Foxford': 'https://www.youtube.com/playlist?list=PL66kIi3dt8A6Hd7soGMFXe6E5366Y66So',
        # 'OnliSkill - 7 класс': 'https://www.youtube.com/playlist?list=PLRqVDT_WVZRkqpQBB1rIGzVKCaPf5qtYi',
        # 'OnliSkill - 8 класс': 'https://www.youtube.com/playlist?list=PLRqVDT_WVZRmWRPyyVVOTe0Jc46eVxqEz',
        # 'OnliSkill - 9 класс': 'https://www.youtube.com/playlist?list=PLRqVDT_WVZRlWUbTOSqswejgrO1RvQQs1',
        # 'OnliSkill - 10 класс': 'https://www.youtube.com/playlist?list=PLRqVDT_WVZRkKOQFruLNC1v74_jTp6LzW',
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
        'CrashCoursePhysics': {
            # https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV
            'https://www.youtube.com/watch?v=ZM8ECpBuQYE': '1 - Motion - 01 - Motion in a Straight Line',
            'https://www.youtube.com/watch?v=ObHJJYvu3RE': '1 - Motion - 02 - Derivatives',
            'https://www.youtube.com/watch?v=jLJLXka2wEM': '1 - Motion - 03 - Integrals',
            'https://www.youtube.com/watch?v=w3BhzYI6zXU': '1 - Motion - 04 - Vectors and 2D Motion',
            'https://www.youtube.com/watch?v=kKKM8Y-u7ds': '1 - Motion - 05 - Newtons Laws',
            'https://www.youtube.com/watch?v=fo_pmp5rtzo': '1 - Motion - 06 - Friction',
            'https://www.youtube.com/watch?v=bpFK2VCRHUs': '1 - Motion - 07 - Uniform Circular Motion',
            'https://www.youtube.com/watch?v=7gf6YpdvtE0': '1 - Motion - 08 - Newtonian Gravity',
            'https://www.youtube.com/watch?v=w4QFJb9a8vo': '1 - Motion - 09 - Work Energy and Power',
            'https://www.youtube.com/watch?v=Y-QOfc2XqOk': '1 - Motion - 10 - Collisions',
            'https://www.youtube.com/watch?v=fmXFWi-WfyU': '1 - Motion - 11 - Rotational Motion',
            'https://www.youtube.com/watch?v=b-HZ1SZPaQw': '1 - Motion - 12 - Torque',
            'https://www.youtube.com/watch?v=9cbF9A6eQNA': '1 - Motion - 13 - Statics',
            'https://www.youtube.com/watch?v=b5SqYuWT4-4': '1 - Motion - 14 - Fluids at Rest',
            'https://www.youtube.com/watch?v=fJefjG3xhW0': '1 - Motion - 15 - Fluids in Motion',
            'https://www.youtube.com/watch?v=jxstE6A_CYQ': '1 - Motion - 16 - Simple Harmonic Motion',
            'https://www.youtube.com/watch?v=TfYCnOvNnFU': '2 - Waves and Sound - 17 - Traveling Waves',
            'https://www.youtube.com/watch?v=qV4lR9EWGlY': '2 - Waves and Sound - 18 - Sound',
            'https://www.youtube.com/watch?v=XDsk6tZX55g': '2 - Waves and Sound - 19 - The Physics of Music',
            'https://www.youtube.com/watch?v=6BHbJ_gBOk0': '3 - Temperature - 20 - Temperature',
            'https://www.youtube.com/watch?v=WOEvvHbc240': '3 - Temperature - 21 - Kinetic Theory and Phase Changes',
            'https://www.youtube.com/watch?v=tuSC0ObB-qY': '3 - Temperature - 22 - The Physics of Heat',
            'https://www.youtube.com/watch?v=4i1MUWJoI0U': '3 - Temperature - 23 - Thermodynamics',
            'https://www.youtube.com/watch?v=p1woKh2mdVQ': '3 - Temperature - 24 - Engines',
            'https://www.youtube.com/watch?v=TFlVWf8JX4A': '4 - Electricity and Magnetism - 25 - Electric Charge',
            'https://www.youtube.com/watch?v=mdulzEfQXDE': '4 - Electricity and Magnetism - 26 - Electric Fields',
            'https://www.youtube.com/watch?v=ZrMltpK6iAw': '4 - Electricity and Magnetism - 27 - Voltage Electric Energy and Capacitors',
            'https://www.youtube.com/watch?v=HXOok3mfMLM': '4 - Electricity and Magnetism - 28 - Electric Current',
            'https://www.youtube.com/watch?v=g-wjP1otQWI': '4 - Electricity and Magnetism - 29 - DC Resistors &amp; Batteries',
            'https://www.youtube.com/watch?v=-w-VTw0tQlE': '4 - Electricity and Magnetism - 30 - Circuit Analysis',
            'https://www.youtube.com/watch?v=vuCJP_5KOlI': '4 - Electricity and Magnetism - 31 - Capacitors and Kirchhoff',
            'https://www.youtube.com/watch?v=s94suB5uLWw': '4 - Electricity and Magnetism - 32 - Magnetism',
            'https://www.youtube.com/watch?v=5fqwJyt4Lus': '4 - Electricity and Magnetism - 33 - Amperes Law',
            'https://www.youtube.com/watch?v=pQp6bmJPU_0': '4 - Electricity and Magnetism - 34 - Induction - An Introduction',
            'https://www.youtube.com/watch?v=9kgzA0Vd8S8': '4 - Electricity and Magnetism - 35 - How Power Gets to Your Home',
            'https://www.youtube.com/watch?v=Jveer7vhjGo': '4 - Electricity and Magnetism - 36 - AC Circuits',
            'https://www.youtube.com/watch?v=K40lNL3KsJ4': '4 - Electricity and Magnetism - 37 - Maxwells Equations',
            'https://www.youtube.com/watch?v=Oh4m8Ees-3Q': '5 - Light - 38 - Geometric Optics',
            'https://www.youtube.com/watch?v=IRBfpBPELmE': '5 - Light - 39 - Light Is Waves',
            'https://www.youtube.com/watch?v=-ob7foUzXaY': '5 - Light - 40 - Spectra Interference',
            'https://www.youtube.com/watch?v=SddBPTcmqOk': '5 - Light - 41 - Optical Instruments',
            'https://www.youtube.com/watch?v=AInCqm5nCzw': '5 - Light - 42 - Special Relativity',
            'https://www.youtube.com/watch?v=7kb1VT0J3DE': '6 - Quantum - 43 - Quantum Mechanics - Part 1',
            'https://www.youtube.com/watch?v=qO_W70VegbQ': '6 - Quantum - 44 - Quantum Mechanics - Part 2',
            'https://www.youtube.com/watch?v=lUhJL7o6_cA': '6 - Quantum - 45 - Nuclear Physics',
            'https://www.youtube.com/watch?v=VYxYuaDvdM0': '6 - Quantum - 46 - Astrophysics and Cosmology',
        },
        'Горбушин': {
            # https://www.youtube.com/playlist?list=PLNG6BIg2XJxCfZtigKso6rBpJ2yk_JFVp'
            'https://www.youtube.com/watch?v=yvZoJ9oA2T0': 'Подготовка к ЕГЭ по физике. Занятие 01',
            'https://www.youtube.com/watch?v=znsFzrsHXcw': 'Подготовка к ЕГЭ по физике. Занятие 02',
            'https://www.youtube.com/watch?v=woiO_HENO20': 'Подготовка к ЕГЭ по физике. Занятие 03',
            'https://www.youtube.com/watch?v=cPP9sPWmNds': 'Подготовка к ЕГЭ по физике. Занятие 04',
            'https://www.youtube.com/watch?v=9zUxpWaRnN0': 'Подготовка к ЕГЭ по физике. Занятие 05',
            'https://www.youtube.com/watch?v=2vZfPKmfeCs': 'Подготовка к ЕГЭ по физике. Занятие 06',
            'https://www.youtube.com/watch?v=lkRIteVb0lU': 'Подготовка к ЕГЭ по физике. Занятие 07',
            'https://www.youtube.com/watch?v=E3tFXjh5WFY': 'Подготовка к ЕГЭ по физике. Занятие 08',
            'https://www.youtube.com/watch?v=9XIZffuvibY': 'Подготовка к ЕГЭ по физике. Занятие 09',
            'https://www.youtube.com/watch?v=ScpikkktFeM': 'Подготовка к ЕГЭ по физике. Занятие 10',
            'https://www.youtube.com/watch?v=E214eHekXGA': 'Подготовка к ЕГЭ по физике. Занятие 11',
            'https://www.youtube.com/watch?v=E77nKXA3XGM': 'Подготовка к ЕГЭ по физике. Занятие 12',
            'https://www.youtube.com/watch?v=Yso604wZlls': 'Подготовка к ЕГЭ по физике. Занятие 13',
            'https://www.youtube.com/watch?v=f4i99JCpDaE': 'Подготовка к ЕГЭ по физике. Занятие 14',
            'https://www.youtube.com/watch?v=JPQe2wTsq34': 'Подготовка к ЕГЭ по физике. Занятие 15',
            'https://www.youtube.com/watch?v=o2rI59dasHc': 'Подготовка к ЕГЭ по физике. Занятие 16',
            'https://www.youtube.com/watch?v=XrAvEu7dU4o': 'Подготовка к ЕГЭ по физике. Занятие 17',
            'https://www.youtube.com/watch?v=un39S9MGUtQ': 'Подготовка к ЕГЭ по физике. Занятие 18',
            'https://www.youtube.com/watch?v=DEVHbDMiTA8': 'Подготовка к ЕГЭ по физике. Занятие 19',
            'https://www.youtube.com/watch?v=-mHpFMPXgfs': 'Подготовка к ЕГЭ по физике. Занятие 20',
            'https://www.youtube.com/watch?v=ieZkxvs-134': 'Подготовка к ЕГЭ по физике. Занятие 21',
            'https://www.youtube.com/watch?v=Dc_yG7EAuls': 'Подготовка к ЕГЭ по физике. Занятие 22',
            'https://www.youtube.com/watch?v=TdKHj4ZKM9o': 'Подготовка к ЕГЭ по физике. Занятие 23',
            'https://www.youtube.com/watch?v=2kOmU6WItv8': 'Подготовка к ЕГЭ по физике. Занятие 24',
            'https://www.youtube.com/watch?v=pc0wzU-wTMg': 'Подготовка к ЕГЭ по физике. Занятие 25',
        },
        'GetAClass': {
            'https://www.youtube.com/watch?v=8yXf4Gawl4w': '8 - 01 - Действия электрического тока',
            'https://www.youtube.com/watch?v=SwNJwbU_lYU': '8 - 02 - Электролиз',
            'https://www.youtube.com/watch?v=RU_-6Ahalqk': '8 - 03 - Направление электрического тока',
            'https://www.youtube.com/watch?v=iyR4Nt7Twg4': '8 - 04 - Закон Ома',
            'https://www.youtube.com/watch?v=RnQGENiF-QM': '8 - 05 - Внутреннее сопротивление',
            'https://www.youtube.com/watch?v=X7_lDtGzXTY': '8 - 06 - Последовательное и параллельное соединение сопротивлений',
            'https://www.youtube.com/watch?v=no9KjloMdxU': '8 - 07 - Сопротивление куба',
            'https://www.youtube.com/watch?v=DowFnoMYqgI': '8 - 08 - Лампа накаливания',
            'https://www.youtube.com/watch?v=8GvuGCE9JQI': '8 - 09 - Электродвижущая сила (ЭДС)',
            'https://www.youtube.com/watch?v=GGnFhHSCuAs': '8 - 10 - Закон Джоуля-Ленца. Часть 1',
            'https://www.youtube.com/watch?v=xlDaZVQWbNA': '8 - 11 - Закон Джоуля-Ленца. Часть 2',
            'https://www.youtube.com/watch?v=4j4T9wyRAGQ': '10 - 12 - Коэффициент мощности косинус фи',
            'https://www.youtube.com/watch?v=1T8FRhLCUJM': '8 - Коронный разряд и огни святого Эльма',
            'https://www.youtube.com/watch?v=627QB4DGE8k': '10 - 05 - Диэлектрик в электрическом поле',
            'https://www.youtube.com/watch?v=NV2V5VcXlEI': '8 - Переменный ток',
            'https://www.youtube.com/watch?v=BQOK_b9TsjE': '8 - Когда переменный ток становится постоянным',
            'https://www.youtube.com/watch?v=denwtwcfvZw': '8 - Стабилитрон',
            'https://www.youtube.com/watch?v=4E1AxUMUz-g': '9 - Дисперсия света',
            'https://www.youtube.com/watch?v=BhYKN21olBw': '9 - Brain Damage',
            'https://www.youtube.com/watch?v=eFUBPqwLxjY': '8 - 40 - Магнитное взаимодействие токов',
            'https://www.youtube.com/watch?v=mh-LTSGjFsE': '9 - 10 - Закон Гука и энергия упругой деформации',
            'https://www.youtube.com/watch?v=F4JL2vvYd8c': '9-5-1 - НИЯУ МИФИ - Опыт Эрстеда со стрелкой',
        },
        'misc': {
            'https://www.youtube.com/watch?v=p15KNqWUZ-c': '2012 - Сергей Гуриев - Экономика красоты и счастья',
            'https://www.youtube.com/watch?v=OHCobJjMHuM': '2020 - 2020-03-20 - Творческая дистанционка от Димы Зицера',
            'https://www.youtube.com/watch?v=dSVdjmabpgg': '2020 - HBO - Welcome to Chechnya',
            'https://www.youtube.com/watch?v=lYTdewh-dhY': '2015 - Открытая Россия - Семья - Фильм о Рамзане Кадырове',
            'https://www.youtube.com/watch?v=2nTmeuXQT5w': '2020 - Математический марафон',
            'https://www.youtube.com/watch?v=vF1UGmi5m8s': '2019 - Дудь - Беслан',
            'https://www.youtube.com/watch?v=-TSD1cX2htQ': '2019 - Новая Газета - Беслан',
            'https://www.youtube.com/watch?v=jKw3n1Gsrtw': '2021 - Александр Гудков - АКВАДИСКОТЕКА',
            'https://www.youtube.com/watch?v=-vt3FHuqDM0': '2021 - Следственный комитет - поздравление с днём рождения',
            'https://www.youtube.com/watch?v=2k9CIfJsONw': '2021 - The Trial of the Chicago 7 - FULL FEATURE - Netflix',
            'https://www.youtube.com/watch?v=dOR41kRQ2tg': '2017 - American Anarchist - Американский анархист',
            'https://www.youtube.com/watch?v=i8fD_jG_TM8': 'FREE BEATS',
            'https://www.youtube.com/watch?v=LXpfBwApM3E': '2021 - 554 - 1 класс',
            'https://www.youtube.com/watch?v=pySJ3cNrZKA': '2022 - Вынос ели',
            'https://www.youtube.com/watch?v=rckEw0z7aK4': '1964 - Что такое теория относительности',
            'https://www.youtube.com/watch?v=N9eW-QRiamA': '2022 - 2022-03-01 Статус',
            'https://www.youtube.com/watch?v=9QV2q8JLVY8': '2022 - 2022-03-03 Гозман',
            'https://www.youtube.com/watch?v=70RmF0rPj9o': '2022 - 2022-03-04 Дудь-Акунин',
            'https://www.youtube.com/watch?v=ARaX2djZYFw': '2022 - 2022-03-17 Дудь-Эйдельман',
            'https://www.youtube.com/watch?v=KDQ-WaKHJnY': '2022 - 2022-03-03 Fack This Job',
            'https://www.youtube.com/watch?v=3-S29KGlQro': '2022 - 2022-03-01 Редакция - Спецреп',
            'https://www.youtube.com/watch?v=Q0vkjM-p_Dk': '2022 - 2022-03-08 Статус S05E27',
            'https://www.youtube.com/watch?v=ADbWCBF6N6s': '2022 - 2022-03-15 Статус',
            'https://www.youtube.com/watch?v=k_EQwMozrJc': '2019 - 2019-11-11 Мой друг Борис Немцов',
            'https://www.youtube.com/watch?v=wFiRz0f9LdE': '2022 - 2022-03-17 НГ - Стрим с Кириллом Мартыновым',
            'https://www.youtube.com/watch?v=XlKFjEblvTc': '2012 - Бремзен Андрей - Как торговать человеческими почками',
            'https://www.youtube.com/watch?v=Zd2n8stiPj4': '2016 - Слишком свободный человек',
            'https://www.youtube.com/watch?v=mQRTKvoLAEM': '2022 - 2022-03-27 Интервью Зеленского',
        },
        'Масяня': {
            'https://www.youtube.com/watch?v=kzx_N8AJiKw':  'Масяня. Эпизод 160. Вакидзаси',
            'https://www.youtube.com/watch?v=HNBvY6J9Pqs':  'Масяня. Эпизод 159. Лафбокс',
            'https://www.youtube.com/watch?v=U9Pwn6F9rgo':  'Не мульт. Просто поздравление с новым годом!',
            'https://www.youtube.com/watch?v=vDoD1rMmfGc':  'Масяня. Эпизод 158. Аешаллензолбрухштелленвеурзахер',
            'https://www.youtube.com/watch?v=QLpQSc54GPw':  'Масяня. Эпизод 157. Только Две Сцены',
            'https://www.youtube.com/watch?v=Kvqz5T_PlTc':  'Масяня. Эпизод 156. Вечный бан',
            'https://www.youtube.com/watch?v=z-KyTHhWeJc':  'Масяня. Эпизод 155. Катапульта',
            'https://www.youtube.com/watch?v=tBUFz_clVOU':  'Масяня. Эпизод 154. Щещя',
            'https://www.youtube.com/watch?v=5Hp0l0AAxtU':  'Масяня. Эпизод 153. Обормотень',
            'https://www.youtube.com/watch?v=qVkQif8opaA':  'Масяня. Эпизод 152. Доппельгангер',
            'https://www.youtube.com/watch?v=1qOXkslawuo':  'Масяня. Эпизод 151. Неудобняк',
            'https://www.youtube.com/watch?v=ANKJM-99G1k':  'Масяня. Эпизод 150. Мазурик',
            'https://www.youtube.com/watch?v=lBeMDqcWTG8':  'Масяня. Эпизод 149. Ёршик',
            'https://www.youtube.com/watch?v=fzETanMXFJA':  'Масяня. Эпизод 148. Листья Ясеня',
            'https://www.youtube.com/watch?v=F4HvmHdtpiw':  'Масяня. Эпизод 147. Тесла с Маском',
            'https://www.youtube.com/watch?v=9I4gu3weD48':  'Масяня. Эпизод 146. Джентельмены предпочитают ботинок',
            'https://www.youtube.com/watch?v=1TCeJhVXXx0':  'Масяня. Эпизод 145. Шницель',
            'https://www.youtube.com/watch?v=NMwd4SRzP0c':  'Масяня. Эпизод 144. Гуляш',
            'https://www.youtube.com/watch?v=2wcEoKJCuhY':  'Масяня. Эпизод 143. Билефельд',
            'https://www.youtube.com/watch?v=ZWzVBUlCxow':  'Масяня. Эпизод 142. Изоляция.',
            'https://www.youtube.com/watch?v=IOhISmvAXv8':  'Бонус нарезка. Инстаграмасяня',
            'https://www.youtube.com/watch?v=Y4lOd3L-Uks':  'Это не пипец',
            'https://www.youtube.com/watch?v=MMi5Fu56OAI':  'Масяня. Эпизод 141. Блоб',
            'https://www.youtube.com/watch?v=8mC4f3LYDGM':  'Масяня. Эпизод 140. The Weird Face',
            'https://www.youtube.com/watch?v=Ihb85teP0XA':  'Масяня. Эпизод 139. Дед Сабзиро',
            'https://www.youtube.com/watch?v=M01LeCQM-j4':  'Масяня. Эпизод 138. Проделки Эйнштейна',
            'https://www.youtube.com/watch?v=mzNrTkK8VNA':  'Масяня. Эпизод 137. Шухер',
            'https://www.youtube.com/watch?v=_jNw1CZlfxQ':  'Масяня. Эпизод 136. Легалайз',
            'https://www.youtube.com/watch?v=pkV4ae6lTCM':  'Масяня. Эпизод 135. Высокие отношения',
            'https://www.youtube.com/watch?v=iMSn4db-cCE':  'Масяня. Эпизод 134. Хухры-Мухры',
            'https://www.youtube.com/watch?v=XEM7oThdLyM':  'Масяня. Эпизод 133. Снусы и Манюшки',
            'https://www.youtube.com/watch?v=C4vZkb_juyQ':  'Масяня. Эпизод 132. Шайсе',
            'https://www.youtube.com/watch?v=Rl2xw-LxU-w':  'Масяня. Эпизод 131. Бегулеле',
            'https://www.youtube.com/watch?v=r9loc1UQ9ZI':  'Масяня. Эпизод 130. Зерцало',
            'https://www.youtube.com/watch?v=XuO9NIQVXDE':  'Масяня. Эпизод 129. Агрегат',
            'https://www.youtube.com/watch?v=Ggv6o7ptvdg':  'Масяня в Швеции. Мини-сериал. Эпизод 5',
            'https://www.youtube.com/watch?v=Ez3AgHySXL8':  'Масяня в Швеции. Мини-сериал. Эпизод 4',
            'https://www.youtube.com/watch?v=20PXoz8l6mc':  'Масяня в Швеции. Мини-сериал. Эпизод 3',
            'https://www.youtube.com/watch?v=C_a0DWzXwtc':  'Масяня в Швеции. Мини-сериал. Эпизод 2',
            'https://www.youtube.com/watch?v=mEELfbDUgvE':  'Масяня в Швеции. Мини-сериал. Эпизод 1',
            'https://www.youtube.com/watch?v=G-Uz4PmBiDE':  'Масяня. Эпизод 128. Факультет',
            'https://www.youtube.com/watch?v=uNHw0SxBK3g':  'Олег Куваев. Чисто Питерские Заморочки',
            'https://www.youtube.com/watch?v=jvqBRQYisxA':  'Слендермэн Масяня-стайл',
            'https://www.youtube.com/watch?v=8a8R9oRjGrU':  'Масянерон vs Кувайный',
            'https://www.youtube.com/watch?v=tXiwpFVMEXs':  'Масяня. Эпизод 127. Традесканция',
            'https://www.youtube.com/watch?v=I5HEy2IDx2A':  'Масяня. Эпизод 126. Кейзи Джонс',
            'https://www.youtube.com/watch?v=Nru8dbN9_SQ':  'Масяня. Эпизод 125. Baghdad banana',
            'https://www.youtube.com/watch?v=ClZg5g0ekk8':  'Масяня. Эпизод 124. Срытая угроза',
            'https://www.youtube.com/watch?v=Rtxu2kGajOQ':  'Масяня. Эпизод 123. Ватрушка',
            'https://www.youtube.com/watch?v=bI7DTKWvAl4':  'Масяня. Водяное Ведро',
            'https://www.youtube.com/watch?v=mvS6dh0AC5A':  'Масяня. Эпизод 122. Сублимация',
            'https://www.youtube.com/watch?v=_dydTviK8gY':  'Масяня. Эпизод 121. Будапешт',
            'https://www.youtube.com/watch?v=W12J6FuzIww':  'Масяня. Эпизод 120. Nice and sweet cartoon with not really clear message',
            'https://www.youtube.com/watch?v=a5W3vKwL6_Y':  'Масяня. Эпизод 53. День сурком',
            'https://www.youtube.com/watch?v=L6elgC3fZDU':  'Масяня. Эпизод 119. Пескун в непонятках',
            'https://www.youtube.com/watch?v=mSM-x5g2IVE':  'Масяня. Эпизод 118. Кури, дедушка, нарзан!',
            'https://www.youtube.com/watch?v=GFgjLQX9rps':  'Масяня. Эпизод 117. Абстиненция',
            'https://www.youtube.com/watch?v=11Vyj7LGi3U':  'Масяня. Эпизод 116. Питерское лето',
            'https://www.youtube.com/watch?v=38mxlvmXKzA':  'Масяня. Эпизод 115. Царь-ру',
            'https://www.youtube.com/watch?v=TnUZtvHKBiE':  'Самый первый мульт про Масяню',
            'https://www.youtube.com/watch?v=KxRmUm4OTzI':  'Кайф по выходным',
            'https://www.youtube.com/watch?v=6PzliGsq9nw':  'Масяня. Эпизод 114. Зеленая кикимора',
            'https://www.youtube.com/watch?v=rHgTSVyTWWw':  'Масяня. Трейлер.',
            'https://www.youtube.com/watch?v=yhvFdE7AQtM':  'Масяня. Эпизод 113. Человечики',
            'https://www.youtube.com/watch?v=C773PuOs9Q0':  'Масяня. Эпизод 112. Ктулху и пингвин с пропеллером',
            'https://www.youtube.com/watch?v=3jbLMFSwrm0':  'Магазинчик БО. Эпизод 2. Набережная',
            'https://www.youtube.com/watch?v=WU88HVn-XGc':  'Магазинчик БО. Эпизод 9. Зоосад',
            'https://www.youtube.com/watch?v=1FUMlvZLoWs':  'Магазинчик БО. Эпизод 8. НеЩАС',
            'https://www.youtube.com/watch?v=HFyiZpI-ToQ':  'Магазинчик БО. Эпизод 1. Интро плюс фонарь',
            'https://www.youtube.com/watch?v=dMs9W0fe4hs':  'Магазинчик Бо. Эпизод 14. Люляки БО',
            'https://www.youtube.com/watch?v=hMD1nD5RLLI':  'Магазинчик Бо. Эпизод 12. Ты знаешь где меня найти',
            'https://www.youtube.com/watch?v=_WJrukzMKsw':  'Магазинчик Бо. Эпизод 10. Раб Дафны',
            'https://www.youtube.com/watch?v=ZWpnHZuNQlw':  'Магазинчик БО. Эпизод 5. Дубликатор и фотоген',
            'https://www.youtube.com/watch?v=sha97rJQ3aA':  'Магазинчик БО. Эпизод 6. Зайберпанк',
            'https://www.youtube.com/watch?v=VDpIuQZPVz0':  'Магазинчик Бо. Эпизод 13. Бо-гемия',
            'https://www.youtube.com/watch?v=0BfDquOqazE':  'Магазинчик Бо. Эпизод 11. Иммерз',
            'https://www.youtube.com/watch?v=6Sda0W6A7as':  'Магазинчик БО. Эпизод 4. Свобоdа слова',
            'https://www.youtube.com/watch?v=C6Esw36YuBo':  'Магазинчик БО. Эпизод 3. Sупердраг',
            'https://www.youtube.com/watch?v=2GXEdkwp3AA':  'Магазинчик Бо. Эпизод 24. Крем материализации',
            'https://www.youtube.com/watch?v=otj2T_-RUrw':  'Магазинчик Бо. Эпизод 19. Жыл',
            'https://www.youtube.com/watch?v=8ShX7y-rgWc':  'Магазинчик Бо. Эпизод 21. Грузилово',
            'https://www.youtube.com/watch?v=qkIQl-3H0Kg':  'Магазинчик Бо. Эпизод 17. БО-жья воля',
            'https://www.youtube.com/watch?v=xGcskAWJqYY':  'Магазинчик Бо. Эпизод 20. Пропасть',
            'https://www.youtube.com/watch?v=NqOAAqZ1SPY':  'Магазинчик Бо. Эпизод 22. Психологическое топливо',
            'https://www.youtube.com/watch?v=WKjYRP25ncc':  'Магазинчик Бо. Эпизод 26. Армия медведей',
            'https://www.youtube.com/watch?v=jwYDk5Unm40':  'Магазинчик Бо. Эпизод 15. Кечак',
            'https://www.youtube.com/watch?v=xMs-IxeIfxM':  'Магазинчик БО. Эпизод 16. Мятый элемент',
            'https://www.youtube.com/watch?v=OCndqQqHlQo':  'Магазинчик Бо. Эпизод 23. Сень Бо-Гэ',
            'https://www.youtube.com/watch?v=pj3yMKYD45Y':  'Магазинчик Бо. Эпизод 25. Деление на всех',
            'https://www.youtube.com/watch?v=O0ni7xLdUXY':  'Магазинчик Бо. Эпизод 18. Мартын',
            'https://www.youtube.com/watch?v=1LuyZ7ZdOow':  'Масяня. Эпизод 111. Троллейбус',
            'https://www.youtube.com/watch?v=--JYQvbzw00':  'Масяня. Эпизод 110. Шевелёнка',
            'https://www.youtube.com/watch?v=QbbeieVjT0E':  'Масяня. Эпизод 109. Нехилый супец',
            'https://www.youtube.com/watch?v=GBo7kKcg3bU':  'Масяня. Эпизод 108. Ядрёный взрыв',
            'https://www.youtube.com/watch?v=phuNrhPFSjM':  'Масяня. Эпизод 107. Свой Чужой',
            'https://www.youtube.com/watch?v=z_Tswjx7Lpk':  'Масяня. Эпизод 106. Как сделать мульт',
            'https://www.youtube.com/watch?v=YOkvT_z3CmU':  'Масяня. Эпизод 105. Будтенате',
            'https://www.youtube.com/watch?v=Bl1ptKWH5Mc':  'Масяня. Эпизод 104. Опаньки',
            'https://www.youtube.com/watch?v=KUGXSD0YObI':  'Масяня. Эпизод 103. Жаба',
            'https://www.youtube.com/watch?v=f_YftiwXeKo':  'Масяня. Эпизод 102. Пицца-Пицца',
            'https://www.youtube.com/watch?v=9FzmEV6SDvI':  'Масяня. Эпизод 101. Трудный способ бросить курить',
            'https://www.youtube.com/watch?v=zy4NJWoUabw':  'Масяня. Эпизод 100. Сюрпризец',
            'https://www.youtube.com/watch?v=cVvhYpEucIc':  'Масяня. Эпизод 99. Аэро треугольники',
            'https://www.youtube.com/watch?v=c39yE_lv8T8':  'Масяня. Эпизод 98. Женские треугольники',
            'https://www.youtube.com/watch?v=Clq3n4ufdRw':  'Масяня. Эпизод 97. Отдача',
            'https://www.youtube.com/watch?v=at8UEb6BKHE':  'Масяня. Эпизод 96. Угадай всё',
            'https://www.youtube.com/watch?v=w4ksppoBDjw':  'Масяня. Эпизод 95. Груша и Кондрашка',
            'https://www.youtube.com/watch?v=fo3Hr1TRfg8':  'Масяня. Эпизод 94. Морква',
            'https://www.youtube.com/watch?v=Lw4WFBzT1Kc':  'Масяня. Эпизод 93. Курыцца',
            'https://www.youtube.com/watch?v=cgJ6q9pg4gg':  'Масяня. Эпизод 92. Мотыль.',
            'https://www.youtube.com/watch?v=vzMm_pwFlJg':  'Масяня. Эпизод 91. Серенгетти',
            'https://www.youtube.com/watch?v=kljmbJIVjPQ':  'Масяня. Эпизод 90. Бурасяно',
            'https://www.youtube.com/watch?v=RUr3E3Yq91k':  'Масяня. Эпизод 89. Джонатан Хрюндельсон',
            'https://www.youtube.com/watch?v=-O0g7WL2WEA':  'Масяня. Эпизод 88. Муравьиная оратория',
            'https://www.youtube.com/watch?v=8ni7jyGKITA':  'Масяня. Эпизод 87. О без яна',
            'https://www.youtube.com/watch?v=daP4ocakdiw':  'Масяня. Эпизод 86. Чернооухий попугай',
            'https://www.youtube.com/watch?v=0Rua4sZBGHk':  'Масяня. Эпизод 85. Масяптиц и Хрюндептицепап',
            'https://www.youtube.com/watch?v=_cfv0LoQhsg':  'Масяня. Эпизод 84. Жизнь с котом',
            'https://www.youtube.com/watch?v=HDpLv2-o0rE':  'Масяня. Эпизод 83. Нерпа',
            'https://www.youtube.com/watch?v=Up9tWPii4No':  'Масяня. Эпизод 82. Пингвин',
            'https://www.youtube.com/watch?v=5wOkOjHs97o':  'Масяня. Эпизод 81. Зеркало',
            'https://www.youtube.com/watch?v=GwQA0_wHigs':  'Масяня. Эпизод 80. Дерево друидов',
            'https://www.youtube.com/watch?v=lJqHDl6c6q4':  'Масяня. Эпизод 79. Лузер',
            'https://www.youtube.com/watch?v=DJrc6dAo40U':  'Масяня. Эпизод 78. Рашн трафико',
            'https://www.youtube.com/watch?v=EGo2K9v17_Q':  'Масяня. Эпизод 77. Кофе по-масяньски',
            'https://www.youtube.com/watch?v=BN6dE-bKJv4':  'Масяня. Эпизод 76. Всем лицам',
            'https://www.youtube.com/watch?v=FwEeOLgShgA':  'Масяня. Эпизод 75. Новогодний обход',
            'https://www.youtube.com/watch?v=wOSJJjyz_mw':  'Масяня. Эпизод 74. Кузина',
            'https://www.youtube.com/watch?v=GWpF9LIhXhk':  'Масяня. Эпизод 73. Десять дохлых енотов',
            'https://www.youtube.com/watch?v=FgCLoF8AM8o':  'Масяня. Эпизод 72. Ночной эльф',
            'https://www.youtube.com/watch?v=JeOci7mQGz4':  'Масяня. Эпизод 71. Боян',
            'https://www.youtube.com/watch?v=daHn0laSgkw':  'Масяня. Эпизод 70. Обескураж',
            'https://www.youtube.com/watch?v=PcLOTb8SrTg':  'Масяня. Эпизод 69. В раю денег не берут',
            'https://www.youtube.com/watch?v=THCUGiQ93P4':  'Масяня. Эпизод 68. Мораторий - Диета',
            'https://www.youtube.com/watch?v=LcgIw_OLguU':  'Масяня. Эпизод 67. Судьба Нигилиста или Че',
            'https://www.youtube.com/watch?v=0KC6c4acrZg':  'Масяня. Эпизод 66. Воробей',
            'https://www.youtube.com/watch?v=yoTJSmKZ0DA':  'Масяня. Эпизод 65. Мануке - полиция Рунета',
            'https://www.youtube.com/watch?v=TVpWYbvMLAY':  'Масяня. Эпизод 64. Ганди или Ищи Дурака',
            'https://www.youtube.com/watch?v=YsUHmexMWQU':  'Масяня. Эпизод 63. Анатомический театр',
            'https://www.youtube.com/watch?v=wjubRM-2ljw':  'Масяня. Эпизод 62. Искушение Лохматого',
            'https://www.youtube.com/watch?v=3GULUaILnQg':  'Масяня. Эпизод 61. Мани-мани',
            'https://www.youtube.com/watch?v=4Jix85fykBw':  'Масяня. Эпизод 60. Гавеный день или Масяня в тумане',
            'https://www.youtube.com/watch?v=FHb4w76VhEw':  'Масяня. Эпизод 59. Ляпы на сьемках',
            'https://www.youtube.com/watch?v=cgKXnoGerug':  'Масяня. Эпизод 58. Флудеры',
            'https://www.youtube.com/watch?v=k8LVUJx5nlI':  'Масяня. Эпизод 57. Треугольники',
            'https://www.youtube.com/watch?v=CxyeWAOesYw':  'Масяня. Эпизод 56. Околобаха',
            'https://www.youtube.com/watch?v=GDL8cIuXIQA':  'Масяня. Эпизод 55. Такой секс',
            'https://www.youtube.com/watch?v=l33x3td5gfg':  'Масяня. Эпизод 54. Общество борьбы с козлами',
            'https://www.youtube.com/watch?v=ghLDvqXLl1M':  'Масяня. Эпизод 52. Карусель',
            'https://www.youtube.com/watch?v=N_oR3sAkCwI':  'Масяня. Эпизод 51. Хабиби',
            'https://www.youtube.com/watch?v=pixiF83bEcg':  'Масяня. Эпизод 50. Посленовогодний бред',
            'https://www.youtube.com/watch?v=YQT-jJGpf8c':  'Масяня. Эпизод 49. Сказка 2003',
            'https://www.youtube.com/watch?v=rfzTgB1JSPE':  'Масяня. Эпизод 48. Здоровье',
            'https://www.youtube.com/watch?v=NfakZ426zYE':  'Масяня. Эпизод 47. Эффект Дятла',
            'https://www.youtube.com/watch?v=atAp8l9uVNM':  'Масяня. Эпизод 46. Попсня',
            'https://www.youtube.com/watch?v=A1m0gXPuqnI':  'Масяня. Эпизод 45. Принц Альберт',
            'https://www.youtube.com/watch?v=LrYsGgV0S0I':  'Масяня. Эпизод 44. Киноавангард',
            'https://www.youtube.com/watch?v=TQeoN01n2JQ':  'Масяня. Эпизод 43. Хомяк',
            'https://www.youtube.com/watch?v=rUT3boOZUJc':  'Масяня. Эпизод 42. Пого',
            'https://www.youtube.com/watch?v=a3ogrOqtErM':  'Масяня. Эпизод 41. Во вне',
            'https://www.youtube.com/watch?v=7Ov6y3hgRD8':  'Масяня. Эпизод 40. Таблетки на Блюхера',
            'https://www.youtube.com/watch?v=gojj9N2ZtXo':  'Масяня. Эпизод 39. Катаклизм',
            'https://www.youtube.com/watch?v=VxkuTiXF1C4':  'Масяня. Эпизод 38. Крыса',
            'https://www.youtube.com/watch?v=0CYR-IY_jDQ':  'Масяня. Эпизод 37. Два моста',
            'https://www.youtube.com/watch?v=Ct8qDUDsMy8':  'Масяня. Эпизод 36. Пуговица Пушкина',
            'https://www.youtube.com/watch?v=MCpBMpdOukE':  'Масяня. Эпизод 35. Розовая кофточка',
            'https://www.youtube.com/watch?v=ivfF5B3IsSU':  'Масяня. Эпизод 34. Языковой барьер',
            'https://www.youtube.com/watch?v=ufRJzhBtGSI':  'Масяня. Эпизод 33. ТВ-Интро',
            'https://www.youtube.com/watch?v=tJofh3icVi8':  'Масяня. Эпизод 30. Русский панкрок',
            'https://www.youtube.com/watch?v=NmUn-QX3bS0':  'Масяня. Эпизод 29. На измене',
            'https://www.youtube.com/watch?v=cmPpG1Nb-ss':  'Масяня. Эпизод 26. Колёса',
            'https://www.youtube.com/watch?v=nZeBWUPaEaU':  'Масяня. Эпизод 32. Деньги, Небо и Машины',
            'https://www.youtube.com/watch?v=LhCKRIZl9X4':  'Масяня. Эпизод 31. Кукла',
            'https://www.youtube.com/watch?v=VYgTvWPft04':  'Масяня. Эпизод 28. Депресняк',
            'https://www.youtube.com/watch?v=aGxQ71et5Eo':  'Масяня. Эпизод 27. Поттер',
            'https://www.youtube.com/watch?v=k9uO9zZsQmc':  'Масяня. Эпизод 25. Взаимопонимание полов',
            'https://www.youtube.com/watch?v=OvZqKc-36kw':  'Масяня. Эпизод 24. Городские ужасы',
            'https://www.youtube.com/watch?v=ISZsQiSpzy8':  'Масяня. Эпизод 23. 8 марта',
            'https://www.youtube.com/watch?v=wsLXO-Nmn-U':  'Масяня. Эпизод 22. Экскурсия по Санкт-Петербургу',
            'https://www.youtube.com/watch?v=mXdJ8OT-4UI':  'Масяня. Эпизод 21. Валентинки',
            'https://www.youtube.com/watch?v=m05xKxkIGU4':  'Масяня. Эпизод 20. Даунлоад',
            'https://www.youtube.com/watch?v=7_wYv6Y21rg':  'Масяня. Эпизод 19. Шоу-бизнес',
            'https://www.youtube.com/watch?v=k2oCEOxeEnk':  'Масяня. Эпизод 18. Подарочки',
            'https://www.youtube.com/watch?v=hLCwl0asqSI':  'Масяня. Эпизод 17. Новогодняя сказочка',
            'https://www.youtube.com/watch?v=KPrqEN27Ohg':  'Масяня. Эпизод 16. Сладкие грёзы',
            'https://www.youtube.com/watch?v=g9gKkej9gGg':  'Масяня. Эпизод 15. Москва',
            'https://www.youtube.com/watch?v=ElUhVkyxZi4':  'Масяня. Эпизод 14. Как-нибудь',
            'https://www.youtube.com/watch?v=Klxm8y3WLHE':  'Масяня. Эпизод 13. День радио',
            'https://www.youtube.com/watch?v=YboUUyuEgIM':  'Масяня. Эпизод 12. В отрыв',
            'https://www.youtube.com/watch?v=PjBSoBhZWu0':  'Масяня. Эпизод 11. Мороженое',
            'https://www.youtube.com/watch?v=n5Ly_V7aZ8s':  'Масяня. Эпизод 10. Пятница',
            'https://www.youtube.com/watch?v=yb0hEebmZeA':  'Масяня. Эпизод 9. Обломчики',
            'https://www.youtube.com/watch?v=NLuof0H9u6M':  'Масяня. Эпизод 8. Масяня и Сплин',
            'https://www.youtube.com/watch?v=KvPHuukuj3U':  'Масяня. Эпизод 7. День Рождения',
            'https://www.youtube.com/watch?v=S7xNSEtIGQQ':  'Масяня. Эпизод 6. Амстердам',
            'https://www.youtube.com/watch?v=EnpunGElAk8':  'Масяня. Эпизод 5. Анекдот',
            'https://www.youtube.com/watch?v=FiQymYIhTW8':  'Масяня. Эпизод 4. Телевизор',
            'https://www.youtube.com/watch?v=ER1g5D2Thnc':  'Масяня. Эпизод 3. Электричка',
            'https://www.youtube.com/watch?v=AjXdcEiEEeY':  'Масяня. Эпизод 2. Модем',
            'https://www.youtube.com/watch?v=_Ynb7PSfK4w':  'Масяня. Эпизод 1. Автолюбитель',
        },
        'Veritasium': {
            'https://www.youtube.com/watch?v=AaZ_RSt0KP8': '2021.08.31 - The Universe is Hostile to Computers',
            'https://www.youtube.com/watch?v=jOTM9T59IX4': '2021.08.31 - The Universe is Hostile to Computers - Rus',
        },
        '3Blue1Brown': {
            'https://www.youtube.com/watch?v=jOTM9T59IX4': 'How to send a self-correcting message',
        },
    }
    for dirname, videos in videos_download_cfg.items():
        dirname = library.location.udr('Видео', dirname)
        for url, title in videos.items():
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
    parser.set_defaults(func=run)
