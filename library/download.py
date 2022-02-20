import library
from library.normalize import TitleCanonizer
from library.logging import cm, colorize_json, color

import collections
import json
import os
import re
import requests
import time

import logging
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


class MultipleFilesDownloader:
    def __init__(self, dirname):
        self._dirname = dirname

    def _get_filename_and_urls(self):
        raise NotImplementedError()

    def _create_missing_local_dir(self, filename):
        local_dirname = os.path.dirname(filename)
        base_dir = os.path.join(self._dirname, local_dirname)
        if not os.path.isdir(base_dir):
            log.info(f'Create missing {base_dir}')
            os.mkdir(base_dir)

    def Download(self, force=False):
        log.info(f'Download into {self._dirname}:')
        for filename, url in self._get_filename_and_urls():
            self._create_missing_local_dir(filename)

            fullname = os.path.join(self._dirname, filename)
            assert library.files.path_is_ok(fullname)
            if not os.path.exists(fullname) or force:
                log.info(f'    Download {url} into {filename} ...')
                response = requests.get(url)
                if response.ok and response.content:
                    with open(fullname, 'wb') as f:
                        f.write(response.content)
                else:
                    log.error(f'{cm("Could not download", color=color.Red)} {url}: {response}')
                    # raise RuntimeError(f'Could not download')
            else:
                log.info(f'    Already exists: {filename} ...')


class MathusPhys(MultipleFilesDownloader):
    HOST = 'http://mathus.ru'

    def _get_filename_and_urls(self):
        for part_index, (part_name, files) in enumerate(MATHUS_PHYS_CONFIG, 1):
            for index, (url_suffix, name) in enumerate(files, 1):
                assert url_suffix.endswith('.pdf')
                assert '/' not in name
                filename = f'{index:02d}-{name}'.replace(' ', '-').replace('.', '') + '.pdf'
                yield os.path.join(f'{part_index:02d}-{part_name}', filename), f'{self.HOST}{url_suffix}'


PhysNsuRu_Config = [
    ('First%20Semester/Urok1.pdf', '1 - Урок 1 - Закон Кулона'),
    ('First%20Semester/Urok2.pdf', '1 - Урок 2 - Теорема Гаусса'),
    ('First%20Semester/urok3.pdf', '1 - Урок 3 - Диполь'),
    ('First%20Semester/Urok4.pdf', '1 - Урок 4 - Мультиполи'),
    ('First%20Semester/Urok5.pdf', '1 - Урок 5 - Уравнения Пуассона и Лапласа'),
    ('First%20Semester/Urok6.pdf', '1 - Урок 6 - Разделение переменных в декартовых координатах'),
    ('First%20Semester/Urok7.pdf', '1 - Урок 7 - Разделение переменных в сферических и цилиндрических координатах'),
    ('First%20Semester/Urok8.pdf', '1 - Урок 8 - Метод изображений. Плоскость'),
    ('First%20Semester/urok9.pdf', '1 - Урок 9 - Метод изображений. Сфера'),
    ('First%20Semester/Urok10.pdf', '1 - Урок 10 - Электростатика в среде'),
    ('First%20Semester/Urok11.pdf', '1 - Урок 11 - Метод изображений на границе диэлектрик-диэлектрик'),
    ('First%20Semester/urok12.pdf', '1 - Урок 12 - Емкость 1'),
    ('First%20Semester/urok13.pdf', '1 - Урок 13 - Емкость 2'),
    ('First%20Semester/Urok14.pdf', '1 - Урок 14 - Энергия поля. давление. Сила'),
    ('First%20Semester/Urok15.pdf', '1 - Урок 15 - Закон сохранения заряда. Закон Ома'),
    ('First%20Semester/Urok16.pdf', '1 - Урок 16 - Закон сохранения заряда. Закон Ома'),
    ('First%20Semester/Urok17.pdf', '1 - Урок 17 - Закон 3-2'),
    ('First%20Semester/Urok18.pdf', '1 - Урок 18 - Закон Био-Савара-Лапласа. Суперпозиция. теорема Стокса'),
    ('First%20Semester/Urok19.pdf', '1 - Урок 19 - Векторный потенциал. Магнитный диполь'),
    ('First%20Semester/Urok20.pdf', '1 - Урок 20 - Магнитное поле в среде'),
    ('First%20Semester/Urok21.pdf', '1 - Урок 21 - Граничные условия. Метод изображений'),
    ('First%20Semester/Urok22.pdf', '1 - Урок 22 - Магнитные цепи. Постоянные магниты'),
    ('First%20Semester/Urok23.pdf', '1 - Урок 23 - Индуктивность. Взаимная индукция'),
    ('First%20Semester/Urok24.pdf', '1 - Урок 24 - Взаимная индукция'),
    ('First%20Semester/urok25.pdf', '1 - Урок 25 - Сохранение магнитного потока'),
    ('First%20Semester/Urok26.pdf', '1 - Урок 26 - Электромагнитная индукция'),
    ('First%20Semester/Urok27.pdf', '1 - Урок 27 - Скин-эффект. Базовые решения - плоскость, шар, цилиндр'),
    ('First%20Semester/Skin2.pdf', '1 - Учебник по скин-эффекту'),
    ('Urok1.pdf', '2 - Урок 1 - Кинематика'),
    ('Urok2.pdf', '2 - Урок 2 - Формулы Френеля'),
    ('Urok3.pdf', '2 - Урок 3 - Фурье-анализ'),
    ('Urok4.pdf', '2 - Урок 4 - Волновой пакет'),
    ('Urok5.pdf', '2 - Урок 5 - Фазовая и групповая скорость'),
    ('Urok6.pdf', '2 - Урок 6 - Соотношение неопределнностей'),
    ('Urok7.pdf', '2 - Урок 7 - Волноводы и резонаторы'),
    ('Urok8.pdf', '2 - Урок 8 - Резонаторы'),
    ('Urok9.pdf', '2 - Урок 9 - Контрольная работа'),
    ('Urok10.pdf', '2 - Урок 10 - Интерференция. Схема Юнга и Ллойда'),
    ('Urok11.pdf', '2 - Урок 11 - Видность'),
    ('Urok12.pdf', '2 - Урок 12 - Линии равного наклона и линии равной толщины'),
    ('Urok13.pdf', '2 - Урок 13 - Зоны Френеля. Дифракция Френеля'),
    ('Urok14.pdf', '2 - Урок 14 - Геометрическое представление зон Френеля'),
    ('Urok15.pdf', '2 - Урок 15 - Дифракция Фраунгофера. Дифракционные решетки'),
    ('Urok16.pdf', '2 - Урок 16 - Фазовые решетки'),
    ('Urok17.pdf', '2 - Урок 17 - Фурье-оптика и голография'),
    ('Urok18.pdf', '2 - Урок 18 - Дипольное излучение'),
    ('UrokXXI.pdf', '2 - Урок 21 - Мультипольное излучение. Антены'),
    ('UrokXXII.pdf', '2 - Урок 22 - Рассеяние волны. Давление света'),
    ('UrokXXIII.pdf', '2 - Урок 23 - Преобразование векторов и полей'),
    ('UrokXXIV.pdf', '2 - Урок 24 - Излучение релятивистской частицы'),
]


class PhysNsuRu(MultipleFilesDownloader):
    HOST = 'http://phys.nsu.ru'

    def _get_filename_and_urls(self):
        # see 'http://phys.nsu.ru/cherk/Zadanie/zadaniya.htm'
        for suffix, filename in PhysNsuRu_Config:
            yield f'{filename}.pdf', f'{self.HOST}/cherk/Eldin/{suffix}'


class ZnakKachestva(MultipleFilesDownloader):
    HOST = 'http://znakka4estva.ru'

    def _get_presentation_urls(self):
        for page_index in range(1, 14):
            page_url = f'{self.HOST}/prezentacii/fizika-i-energetika/'
            log.info(f'Processing page {page_index}: {page_url}')
            response = requests.get(page_url, params={'page': page_index})
            for line in response.text.split('\n'):
                if 'blog-img-wrapper' in line and 'href="' + page_url in line:
                    l = re.sub(r'.*href="', '', line)
                    presentation_url = re.sub(r'" class=".*', '', l)
                    log.info(f'    New presentation: {presentation_url}')
                    yield presentation_url

    def _get_filename_and_urls(self):
        for presentation_url in self._get_presentation_urls():
            response = requests.get(presentation_url)
            for line in response.text.split('\n'):
                if '<h1 class="pull-sm-left">' in line:
                    l = re.sub(r'.*"pull-sm-left">', '', line)
                    ll = re.sub(r'<.*', '', l)
                    split_position = ll.find('. ')
                    name = ll[split_position + 2:]
                    grade = int(presentation_url.split('/')[-2].split('-')[0])
                    assert 7 <= grade <= 11, f'Invalid grade: {grade}'
                    link = f'{self.HOST}/uploads/category_items/{name}.ppt'
                    filename = re.sub(r'\. (\d)\. ', r'. 0\1. ', ll)
                    yield os.path.join(f'{grade} класс', f'{filename}.ppt'), link


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
