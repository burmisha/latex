from library.logging import cm, colorize_json, color

import json
import logging
import os
import re
import requests
import time

log = logging.getLogger(__name__)


try:
    import pafy  # http://np1.github.io/pafy/
except ImportError:
    log.error('Failed to load pafy')


MATHUS_PHYS_CONFIG = [
    ('Механика', [
        ('/phys/ravnomer.pdf', 'Равномерное движение'),
        ('/phys/ravnouskor.pdf', 'Равноускоренное движение'),
        ('/phys/vertical.pdf', 'Вертикальное движение'),
        ('/phys/neravnomer.pdf', 'Неравномерное движение'),
        ('/phys/otnodvi.pdf', 'Относительность движения'),
        ('/phys/uprugotr.pdf', 'Упругое отражение'),
        ('/phys/ballistika.pdf', 'Баллистика. Координаты'),
        ('/phys/ballisvec.pdf', 'Баллистика. Векторы'),
        ('/phys/ballisotr.pdf', 'Баллистика. Отражения'),
        ('/phys/pizan.pdf', 'Баллистика. Относительность'),
        ('/phys/dviok.pdf', 'Движение по окружности'),
        ('/phys/zakopal.pdf', 'Движение со связями. Кинематика'),
        ('/phys/mro.pdf', 'Масса и плотность'),
        ('/phys/zanew.pdf', 'Законы Ньютона'),
        ('/phys/grav.pdf', 'Гравитация'),
        ('/phys/silaupr.pdf', 'Сила упругости'),
        ('/phys/silatren.pdf', 'Сила трения'),
        ('/phys/svtela.pdf', 'Связанные тела'),
        ('/phys/naplos.pdf', 'Наклонная плоскость'),
        ('/phys/kinsv.pdf', 'Движение со связями. Динамика'),
        ('/phys/imp.pdf', 'Импульс'),
        ('/phys/sysmat.pdf', 'Системы материальных точек'),
        ('/phys/cmass.pdf', 'Центр масс'),
        ('/phys/peremass.pdf', 'Движение с переменной массой'),
        ('/phys/ae.pdf', 'Работа и энергия'),
        ('/phys/conserva.pdf', 'Консервативные системы'),
        ('/phys/dynpend.pdf', 'Динамика маятника'),
        ('/phys/mpet.pdf', 'Мёртвая петля'),
        ('/phys/sosf.pdf', 'Соскальзывание со сферы'),
        ('/phys/upru.pdf', 'Упругие взаимодействия'),
        ('/phys/krivitra.pdf', 'Кривизна траектории'),
        ('/phys/neconserva.pdf', 'Неконсервативные системы'),
        ('/phys/neupru.pdf', 'Неупругие взаимодействия'),
        ('/phys/raspad.pdf', 'Распад частиц'),
        ('/phys/rasse.pdf', 'Рассеяние частиц'),
        ('/phys/nucreac.pdf', 'Ядерные реакции'),
        ('/phys/conpend.pdf', 'Конический маятник'),
        ('/phys/udarsil.pdf', 'Ударные силы'),
        ('/phys/statika.pdf', 'Статика'),
        ('/phys/mevip.pdf', 'Метод виртуальных перемещений'),
        ('/phys/gs.pdf', 'Гидростатика'),
        ('/phys/truzhi.pdf', 'Трубка с жидкостью'),
        ('/phys/gorsilar.pdf', 'Горизонтальная сила Архимеда'),
        ('/phys/tolkanat.pdf', 'Массивный канат'),
        ('/phys/masspru.pdf', 'Массивная пружина'),
        ('/phys/momentsil.pdf', 'Момент силы'),
        ('/phys/vratela.pdf', 'Вращение твёрдого тела'),
        ('/phys/motiliq.pdf', 'Движение жидкости'),
        ('/phys/podobraz.pdf', 'Подобие и размерность'),
        ('/phys/soprosred.pdf', 'Сопротивление среды'),
        ('/phys/avtomobil.pdf', 'Движение автомобиля'),
        ('/phys/velipro.pdf', 'Процессы и измерения'),
        ('/phys/difur.pdf', 'Дифференциальные уравнения'),
        ('/phys/urkol1.pdf', 'Уравнение колебаний. 1'),
        ('/phys/urkol2.pdf', 'Уравнение колебаний. 2'),
        ('/phys/garmod.pdf', 'Гармоническое движение'),
        ('/phys/neiso.pdf', 'Неинерциальные системы отсчёта'),
        ('/phys/mehavol.pdf', 'Механические волны'),
        ('/phys/vecmech.pdf', 'Векторы и механика'),
        ('/phys/kepler.pdf', 'Законы Кеплера'),
        ('/phys/ustoravno.pdf', 'Устойчивость равновесия'),
        ('/phys/integral-mech.pdf', 'Интеграл. Механика'),
        ('/phys/Zmech.pdf', 'Задавальник МФТИ. Механика'),
    ]),
    ('Термодинамика', [
        ('/phys/atomol.pdf', 'Атомы и молекулы'),
        ('/phys/osnurav_mkt.pdf', 'Основное уравнение МКТ'),
        ('/phys/ursos.pdf', 'Уравнение состояния'),
        ('/phys/vosh.pdf', 'Воздушный шар'),
        ('/phys/sfersloy.pdf', 'Сферический слой'),
        ('/phys/gaspru.pdf', 'Газ и пружина'),
        ('/phys/podvodrab.pdf', 'Подводные работы'),
        ('/phys/smesigas.pdf', 'Газовые смеси'),
        ('/phys/isopr.pdf', 'Изопроцессы'),
        ('/phys/trurtu.pdf', 'Трубка со ртутью'),
        ('/phys/poluper.pdf', 'Полупрозрачные перегородки'),
        ('/phys/effusion.pdf', 'Эффузия'),
        ('/phys/vnutren.pdf', 'Внутренняя энергия'),
        ('/phys/teplo.pdf', 'Теплообмен'),
        ('/phys/newrilaw.pdf', 'Теплопроводность'),
        ('/phys/cycwork.pdf', 'Работа в цикле'),
        ('/phys/perzater.pdf', 'Первый закон термодинамики'),
        ('/phys/cgaza.pdf', 'Теплоёмкость газа'),
        ('/phys/teploma.pdf', 'Тепловые двигатели'),
        ('/phys/holonasos.pdf', 'Холодильник и тепловой насос'),
        ('/phys/dvigaza.pdf', 'Движение газа'),
        ('/phys/npar.pdf', 'Насыщенный пар'),
        ('/phys/vvpp.pdf', 'Влажный воздух'),
        ('/phys/uravadia.pdf', 'Уравнение адиабаты'),
        ('/phys/politrop.pdf', 'Политропический процесс'),
        ('/phys/baroformula.pdf', 'Модели атмосферы'),
        ('/phys/neidegas.pdf', 'Неидеальный газ'),
        ('/phys/povernat.pdf', 'Поверхностное натяжение'),
        ('/phys/integral-therm.pdf', 'Интеграл. Термодинамика'),
    ]),
    ('Оптика', [
        ('/phys/luchi.pdf', 'Световые лучи'),
        ('/phys/plozer.pdf', 'Плоское зеркало'),
        ('/phys/sferizer.pdf', 'Сферическое зеркало'),
        ('/phys/prelozak.pdf', 'Закон преломления'),
        ('/phys/polnotrazh.pdf', 'Полное отражение'),
        ('/phys/prelomal.pdf', 'Преломление. Малые углы'),
        ('/phys/tolstolin.pdf', 'Толстые линзы'),
        ('/phys/prinfer.pdf', 'Принцип Ферма'),
        ('/phys/linfocus.pdf', 'Фокусное расстояние линзы'),
        ('/phys/linrays.pdf', 'Ход лучей в линзах'),
        ('/phys/formulin.pdf', 'Формула линзы'),
        ('/phys/genformulin.pdf', 'Обобщённая формула линзы'),
        ('/phys/produv.pdf', 'Продольное увеличение'),
        ('/phys/skoriz.pdf', 'Скорость изображения'),
        ('/phys/linpen.pdf', 'Линза и маятник'),
        ('/phys/dvelin.pdf', 'Система двух линз'),
        ('/phys/linzer.pdf', 'Линза и зеркало'),
        ('/phys/linliq.pdf', 'Линза и жидкость'),
        ('/phys/linplast.pdf', 'Линза и пластина'),
        ('/phys/ropsis.pdf', 'Разные оптические системы'),
        ('/phys/priboropt.pdf', 'Оптические приборы'),
        ('/phys/glaz.pdf', 'Глаз человека'),
        ('/phys/neosreda.pdf', 'Неоднородная среда'),
        ('/phys/interf.pdf', 'Интерференция света'),
    ]),
    ('Общефизическое', [
        ('/phys/grafmet.pdf', 'Графические методы'),
        ('/phys/szf.pdf', 'Среднее значение функции'),
        ('/phys/fxyz.pdf', 'Функции нескольких переменных'),
        ('/phys/sto.pdf', 'Теория относительности'),
    ]),
    ('Электродинамика', [
        ('/phys/zakon_kulona.pdf', 'Закон Кулона'),
        ('/phys/superposition.pdf', 'Напряжённость электрического поля'),
        ('/phys/teorema-gaussa.pdf', 'Теорема Гаусса'),
        ('/phys/zgir.pdf', 'Потенциал электрического поля'),
        ('/phys/prosf.pdf', 'Проводящие сферы'),
        ('/phys/zarplast.pdf', 'Заряженная пластина'),
        ('/phys/metiz.pdf', 'Метод изображений'),
        ('/phys/plokon.pdf', 'Плоский конденсатор'),
        ('/phys/dielkon.pdf', 'Конденсатор с диэлектриком'),
        ('/phys/electrodav.pdf', 'Электрическое давление'),
        ('/phys/teorema-edinstvennosti.pdf', 'Теорема единственности'),
        ('/phys/zener.pdf', 'Энергия зарядов'),
        ('/phys/enerpol.pdf', 'Энергия электрического поля'),
        ('/phys/dviel.pdf', 'Движение в электрическом поле'),
        ('/phys/localom.pdf', 'Локальный закон Ома'),
        ('/phys/elcirc.pdf', 'Электрические цепи'),
        ('/phys/r.pdf', 'Вычисление сопротивлений'),
        ('/phys/mtoka.pdf', 'Мощность тока'),
        ('/phys/elenag.pdf', 'Электронагреватель'),
        ('/phys/pravila_kirhgofa.pdf', 'Правила Кирхгофа'),
        ('/phys/e0r0.pdf', 'Эквивалентный источник'),
        ('/phys/vah.pdf', 'Вольт-амперная характеристика'),
        ('/phys/nelinel.pdf', 'Нелинейные элементы'),
        ('/phys/diodrez.pdf', 'Диод и резисторы'),
        ('/phys/ucap.pdf', 'Цепь с конденсатором'),
        ('/phys/icap.pdf', 'Ток через конденсатор'),
        ('/phys/cc.pdf', 'Соединения конденсаторов'),
        ('/phys/c.pdf', 'Вычисление ёмкостей'),
        ('/phys/qc.pdf', 'Количество теплоты. Конденсатор'),
        ('/phys/slokon.pdf', 'Сложный конденсатор'),
        ('/phys/podviplast.pdf', 'Подвижная пластина'),
        ('/phys/diodcap.pdf', 'Диод и конденсаторы'),
        ('/phys/flor.pdf', 'Сила Лоренца'),
        ('/phys/famp.pdf', 'Сила Ампера'),
        ('/phys/magnipol.pdf', 'Магнитное поле токов'),
        ('/phys/magnipotok.pdf', 'Магнитный поток'),
        ('/phys/halleffect.pdf', 'Эффект Холла'),
        ('/phys/eledvig.pdf', 'Двигатель постоянного тока'),
        ('/phys/mgd.pdf', 'Магнитная гидродинамика'),
        ('/phys/emind.pdf', 'Вихревое электрическое поле'),
        ('/phys/selfind.pdf', 'Самоиндукция'),
        ('/phys/emkol.pdf', 'Электромагнитные колебания'),
        ('/phys/slokonkol.pdf', 'Сложный конденсатор. Колебания'),
        ('/phys/paramkol.pdf', 'Параметрические колебания'),
        ('/phys/ql.pdf', 'Количество теплоты. Катушка'),
        ('/phys/diod.pdf', 'Диод и катушка'),
        ('/phys/properehod.pdf', 'Переходные процессы'),
        ('/phys/peremetok.pdf', 'Переменный ток'),
        ('/phys/transformator.pdf', 'Трансформатор'),
        ('/phys/emw.pdf', 'Электромагнитные волны'),
        ('/phys/integral-el.pdf', 'Интеграл. Электродинамика'),
        ('/phys/edipole.pdf', 'Электрический диполь'),
        ('/phys/mdipole.pdf', 'Магнитный диполь'),
    ]),
    ('Квантовая физика', [
        ('/phys/dasveta.pdf', 'Давление света'),
        ('/phys/ff.pdf', 'Фотоэффект'),
        ('/phys/atnuc.pdf', 'Атомы и ядра'),
        ('/phys/radecay.pdf', 'Радиоактивный распад'),
        ('/phys/defectmass.pdf', 'Дефект масс'),
    ]),
]


class MathusPhys:
    def Download(self, path):
        for partIndex, (partName, files) in enumerate(MATHUS_PHYS_CONFIG, 1):
            partDir = os.path.join(path, f'{partIndex:02d}-{partName}')
            if not os.path.isdir(partDir):
                os.mkdir(partDir)
            log.info(f'Chapter {partName} -> {partDir}')
            for index, (location, name) in enumerate(files, 1):
                assert location.endswith('.pdf')
                url = 'http://mathus.ru' + location
                filename = f'{index:02d}-{name}'.replace(' ', '-').replace('.', '') + '.pdf'
                log.info('    Download {url} into {filename}')
                assert '/' not in filename
                dstFile = os.path.join(partDir, filename)
                data = requests.get(url).content
                with open(dstFile, 'wb') as f:
                    f.write(data)

    def GetDirname(self):
        return 'Материалы - mathus'


class ZnakKachestava:
    def Download(self, path):
        host = 'http://znakka4estva.ru'
        urls = []
        for i in range(1, 14):
            url = f'{host}/prezentacii/fizika-i-energetika/'
            d = requests.get(url, params={'page': i}).text
            for line in d.split('\n'):
                if 'blog-img-wrapper' in line and 'href="' + url in line:
                    l = re.sub(r'.*href="', '', line)
                    ll = re.sub(r'" class=".*', '', l)
                    urls.append(ll)

        for url in urls:
            lines = requests.get(url).text.split('\n')
            for line in lines:
                if '<h1 class="pull-sm-left">' in line:
                    l = re.sub(r'.*"pull-sm-left">', '', line)
                    ll = re.sub(r'<.*', '', l)
                    klassStart = ll.find('. ')
                    presName = ll[klassStart + 2:]
                    link = f'{host}/uploads/category_items/{presName}.ppt'
                    filename = re.sub(r'\. (\d)\. ', r'. 0\1. ', ll)
                    filename = '{filename}.ppt'
                    filename = os.path.join(path, filename)
                    log.info(f'Saving {presName} to {filename}')
                    response = requests.get(link)
                    if response.ok and response.content:
                        with open(filename, 'wb') as f:
                            f.write(response.content)

    def GetDirname(self):
        return 'znakka4estva'


class YoutubeVideo:
    def __init__(self, url, title):
        assert url.startswith('https://www.youtube.com/watch?v=')
        self._url = url
        self._title = title

    def __str__(self):
        return f'{cm(self._title, color=color.Yellow)} ({self._url})'

    def get_filename(self, dstdir):
        return os.path.join(dstdir, f'{self._title}.mp4')

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

    def download(self, dstdir, use_requests=False):
        filename = self.get_filename(dstdir)
        if os.path.exists(filename):
            log.info(f'Skipping {self} as \'{filename}\' exists')
        else:
            log.info(f'Downloading {self} to \'{filename}\'')
            best_stream = self.get_best_stream(preftype='mp4')
            if use_requests:
                data = requests.get(best_stream.url).content
                with open(filename, 'wb') as f:
                    f.write(data)
            else:
                best_stream.download(filepath=filename)


class TitleCanonizer:
    def __init__(self, replacements=None):
        if replacements is None:
            log.debug('Using default replacements')
            replacements = [
                (r'^Физика[\.:] ', ''),
                (r'  +', ' '),
                (r' Центр онлайн-обучения «Фоксфорд»$', ''),
                (r'\.$', ''),
                (r' \(осн\)\.?', '.'),
                (r'^8 кл - ([0-9]{3})', r'Урок \1'),
                (r' \(осн, запись 2014 года\)\.', r'.'),
                (r' \| Видеоурок', r''),
                (r' \| ', r' и '),
                (r'(.): ', r'\1 - '),
                (r' : ', r' - '),
                (r'\?', r''),
                (r'Подготовка к ЕГЭ по физике. Занятие', r' - '),
                (r'Ф..... 10 класс ?[:.] ?', r'Физика 10 класс. '),
            ]

        self._Replacements = replacements

    def Canonize(self, title):
        canonized = str(title)
        for pattern, replacement in self._Replacements:
            canonized = re.sub(pattern, replacement, canonized)
        canonized = canonized.strip()
        return canonized


class YoutubePlaylist:
    def __init__(self, url):
        assert url.startswith('https://www.youtube.com/playlist?list=PL')
        self._Url = url
        self._TitleCanonizer = TitleCanonizer()

    def ListVideos(self):
        log.info(f'Looking for videos in {cm(self._Url, color=color.Cyan)}')
        text = requests.get(self._Url).text

        start_expression = 'var ytInitialData ='
        end_expression = '</script>'
        start_pos = text.find(start_expression) + len(start_expression)
        end_pos = text.find(end_expression, start_pos)
        js_data = text[start_pos:end_pos].strip().strip(';')
        loaded = json.loads(js_data)
        playlistTitle = loaded['metadata']['playlistMetadataRenderer']['title']
        contentItems = loaded['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']

        videos = []
        for index, contentItem in enumerate(contentItems, 1):
            try:
                index_text = int(contentItem['playlistVideoRenderer']['index']['simpleText'])
                assert index_text == index, f'Got index {index_text} instead of {index}'
                video_id = contentItem['playlistVideoRenderer']['videoId']
                title_text = contentItem['playlistVideoRenderer']['title']['runs'][0]['text']
                youtube_video = YoutubeVideo(
                    f'https://www.youtube.com/watch?v={video_id}',
                    self._TitleCanonizer.Canonize(title_text),
                )
                videos.append(youtube_video)
            except:
                log.error(f'Error on {colorize_json(contentItem)}')
                raise

        log.info(f'Found {len(videos)} videos for \'{playlistTitle}\' at {self._Url}')
        return playlistTitle, videos
