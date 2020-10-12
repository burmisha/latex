import library

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


class MathusPhys(object):
    def Download(self, path):
        for partIndex, (partName, files) in enumerate(MATHUS_PHYS_CONFIG, 1):
            partDir = os.path.join(path, '%02d-%s' % (partIndex, partName))
            if not os.path.isdir(partDir):
                os.mkdir(partDir)
            log.info('Chapter %s -> %s', partName, partDir)
            for index, (location, name) in enumerate(files, 1):
                assert location.endswith('.pdf')
                url = 'http://mathus.ru' + location
                filename = ('%02d-%s' % (index, name)).replace(' ', '-').replace('.', '') + '.pdf'
                log.info('    Download %s into %s', url, filename)
                assert '/' not in filename
                dstFile = os.path.join(partDir, filename)
                data = requests.get(url).content
                with open(dstFile, 'w') as f:
                    f.write(data)

    def GetDirname(self):
        return 'Материалы - mathus'


class ZnakKachestava(object):
    def Download(self, path):
        host = 'http://znakka4estva.ru'
        urls = []
        for i in range(1, 14):
            url = '%s/prezentacii/fizika-i-energetika/' % host
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
                    link = '%s/uploads/category_items/%s.ppt' % (host, presName)
                    filename = re.sub(r'\. (\d)\. ', r'. 0\1. ', ll)
                    filename = '%s.ppt' % filename
                    filename = os.path.join(path, filename)
                    print('Saving %s to %s' % (presName, filename))
                    # with open(filename, 'w') as f:
                    #     f.write(requests.get(link).content)

    def GetDirname(self):
        return 'znakka4estva'


class YoutubeDownloader(object):
    def __init__(self, sleepTime=1200):
        self.SleepTime = sleepTime

    def GetBestStream(self, url, preftype=None):
        log.debug('Searching best stream for %s', url)
        ok = False
        while not ok:
            try:
                video = pafy.new(url)
                ok = True
            except IndexError:
                log.exception('Failed, traceback:')
                log.info('Sleeping for %d', self.SleepTime)
                time.sleep(self.SleepTime)
        log.info('Streams: %r', video.streams)
        bestStream = video.getbest(preftype=preftype)
        log.debug('Best stream: %r', bestStream)
        return bestStream


class GetAClass(YoutubeDownloader):
    def Download(self, path):
        for url, name in [
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
            ('https://www.youtube.com/watch?v=p15KNqWUZ-c', 'Сергей Гуриев - Экономика красоты и счастья - 2012'),
            ('https://www.youtube.com/watch?v=OHCobJjMHuM', 'Творческая дистанционка от Димы Зицера - 2020-03-20'),
            ('https://www.youtube.com/watch?v=dSVdjmabpgg', 'HBO - Welcome to Chechnya - 2020'),
            # ('https://www.youtube.com/watch?v=lYTdewh-dhY', 'Открытая Россия - Семья - Фильм о Рамзане Кадырове - 2015'),
            ('https://www.youtube.com/watch?v=2nTmeuXQT5w', '2020 - Математический марафон'),
            ('https://www.youtube.com/watch?v=vF1UGmi5m8s', '2019 - Дудь - Беслан'),
            ('https://www.youtube.com/watch?v=-TSD1cX2htQ', '2019 - Новая Газета - Беслан'),
        ]:
            dstFile = os.path.join(path, 'GetAClass', '%s.mp4' % name)
            if os.path.exists(dstFile):
                log.info('Skipping %s as "%s" exists', url, name)
            else:
                log.info('Downloading %s to "%s"', url, dstFile)
                bestStream = self.GetBestStream(url, preftype='mp4')
                bestStream.download(filepath=dstFile)


class Foxford(YoutubeDownloader):
    def Download(self, path):
        log.info('Downloading playlist https://www.youtube.com/playlist?list=PL66kIi3dt8A6Hd7soGMFXe6E5366Y66So')
        for url, name in [
            ('https://www.youtube.com/watch?v=iWr6U3-rynQ', 'Кинематика - Плоское движение точек твердого тела'),
            ('https://www.youtube.com/watch?v=W6zOwbHkA8g', 'Термодинамика - Адиабатный процесс'),
            ('https://www.youtube.com/watch?v=RXvNehmSfl8', 'Статика - Условия равновесия тела'),
            ('https://www.youtube.com/watch?v=YPTGHZZ6H0I', 'Термодинамика - Теплоёмкость'),
            ('https://www.youtube.com/watch?v=7ZpPP_LZYNM', 'Термодинамика - Молярная теплоёмкость'),
            ('https://www.youtube.com/watch?v=b_LlqXeABQU', 'Термодинамика - Удельная теплоёмкость'),
            ('https://www.youtube.com/watch?v=KAcCPNDmRe8', 'Статика - Момент силы'),
            ('https://www.youtube.com/watch?v=0hFWeR8ybxs', 'Последовательное и параллельное соединение проводников'),
            ('https://www.youtube.com/watch?v=vUkOstwz1kA', 'Постоянный ток - Закон Ома для участка цепи'),
            ('https://www.youtube.com/watch?v=487Z6jJVngQ', 'Постоянный ток - Электрическое сопротивление проводника'),
            ('https://www.youtube.com/watch?v=frJYMkK6lFk', 'Постоянный ток - Напряжение'),
            ('https://www.youtube.com/watch?v=At9OP9pQqCE', 'Постоянный ток - Сила тока'),
            ('https://www.youtube.com/watch?v=Hp3dJNEXW00', 'Постоянный ток - Электрический ток'),
            ('https://www.youtube.com/watch?v=hxfowwBlDWg', 'Термодинамика - Количество теплоты'),
            ('https://www.youtube.com/watch?v=2QrBqGvGCKA', 'Термодинамика - Циклические процессы'),
            ('https://www.youtube.com/watch?v=iDDGCf9eyes', 'Термодинамика - Тепловые машины'),
            ('https://www.youtube.com/watch?v=piKLPtzJ1sk', 'МКТ - Графики газовых процессов'),
            ('https://www.youtube.com/watch?v=emwG8AVHciM', 'МКТ - Основные термодинамические процессы'),
            ('https://www.youtube.com/watch?v=ewDWrUCY8sk', 'Геометрическая оптика - Скорость света'),
            ('https://www.youtube.com/watch?v=tEfEaBmYPrI', 'Геометрическая оптика - Плоское зеркало'),
            ('https://www.youtube.com/watch?v=lrBE5EHwbqg', 'Кинематика - Относительность механического движения'),
            ('https://www.youtube.com/watch?v=cMBrpdpOAfU', 'Геометрическая оптика - Законы преломления'),
            ('https://www.youtube.com/watch?v=AuqJHgDFJmY', 'Геометрическая оптика - Законы отражения'),
            ('https://www.youtube.com/watch?v=GpuqosemhBk', 'Кинематика - Поступательное и вращательное движение твёрдого тела'),
            ('https://www.youtube.com/watch?v=uVL3SoDDMNg', 'Геометрическая оптика - Фокусное расстояние и оптическая сила линзы'),
            ('https://www.youtube.com/watch?v=vjmyDrCSFm8', 'Геометрическая оптика - Построение изображений в тонких линзах'),
            ('https://www.youtube.com/watch?v=8Vm_svrry9A', 'Геометрическая оптика - Формула тонкой линзы'),
            ('https://www.youtube.com/watch?v=gy29hTFu54E', 'Геометрическая оптика - Действительный и мнимый источники'),
            ('https://www.youtube.com/watch?v=c1cqOmLOQ9M', 'Геометрическая оптика - Тонкие линзы'),
            ('https://www.youtube.com/watch?v=fQCZkmd9MUk', 'Геометрическая оптика - Действительное и мнимое изображения'),
            ('https://www.youtube.com/watch?v=fvRCNxAjgQ4', 'Геометрическая оптика - Показатель преломления'),
            ('https://www.youtube.com/watch?v=pxc2NUAroLI', 'Геометрическая оптика - Образование тени и полутени'),
            ('https://www.youtube.com/watch?v=sxCkJ_4sT9U', 'Геометрическая оптика - Распространение света'),
            ('https://www.youtube.com/watch?v=utJyyEPMXBU', 'Законы сохранения в механике - Внутренние и внешние силы'),
            ('https://www.youtube.com/watch?v=wsVmAedcD2A', 'Законы сохранения в механике - Неупругий удар'),
            ('https://www.youtube.com/watch?v=RfO-7rPHRTg', 'Общее - Плотность'),
            ('https://www.youtube.com/watch?v=PXyIVNgxfvM', 'МКТ - Основное уравнение МКТ'),
            ('https://www.youtube.com/watch?v=kr8kkIszQbM', 'Термодинамика - Внутренняя энергия и способы её изменения'),
            ('https://www.youtube.com/watch?v=LlPHqQ3UaS4', 'Термодинамика - Внутренняя энергия идеального газа'),
            ('https://www.youtube.com/watch?v=-IFzslacWrI', 'Законы сохранения в механике - Абсолютно упругий удар'),
            ('https://www.youtube.com/watch?v=dqijLBR1qZc', 'Законы сохранения в механике - Закон сохранения импульса'),
            ('https://www.youtube.com/watch?v=CBz4S4gKMfY', 'Законы сохранения в механике - Импульс'),
            ('https://www.youtube.com/watch?v=T72IA5QmUZU', 'Термодинамика - Работа газа'),
            ('https://www.youtube.com/watch?v=lao0b2VD-Bk', 'Термодинамика - Первое начало термодинамики'),
            ('https://www.youtube.com/watch?v=XJS1llpnZK8', 'МКТ - Уравнение Менделеева-Клапейрона для идеального газа'),
            ('https://www.youtube.com/watch?v=ivwYzV9Ar2k', 'МКТ - Смеси газов. Закон Дальтона'),
            ('https://www.youtube.com/watch?v=2nMyiIQtgvM', 'МКТ - Идеальный газ'),
            ('https://www.youtube.com/watch?v=Jo_EXQzgHT0', 'МКТ - Основные положения МКТ и их опытное обоснование'),
            ('https://www.youtube.com/watch?v=OBArlSVHl70', 'МКТ - Изобарный процесс'),
            ('https://www.youtube.com/watch?v=n12aZKl-fWE', 'МКТ - Изохорный процесс'),
            ('https://www.youtube.com/watch?v=RETZXUDfDhc', 'МКТ - Изотермический процесс'),
            ('https://www.youtube.com/watch?v=oFrkSRFOvcE', 'Механика жидкостей и газов - Сила Архимеда'),
            ('https://www.youtube.com/watch?v=DFuQya7Oe9U', 'Динамика - Закон Всемирного тяготения'),
            ('https://www.youtube.com/watch?v=MxfuBo6ih_M', 'Динамика - Третий закон Ньютона'),
            ('https://www.youtube.com/watch?v=kgfpqLNrjuk', 'Динамика - Второй закон Ньютона'),
            ('https://www.youtube.com/watch?v=niJFMDiuMj8', 'Динамика - Первый закон Ньютона'),
            ('https://www.youtube.com/watch?v=d5QhXjgW8tw', 'Общее - Масса'),
            ('https://www.youtube.com/watch?v=M0pnXB_cEMY', 'Динамика - Силы'),
        ]:
            dstFile = os.path.join(path, 'Foxford', '%s.mp4' % name)
            if os.path.exists(dstFile):
                log.info('Skipping %s as "%s" exists', url, name)
            else:
                log.info('Downloading %s to "%s"', url, dstFile)
                bestStream = self.GetBestStream(url, preftype='mp4')
                bestStream.download(filepath=dstFile)


class CrashCoursePhysics(YoutubeDownloader):
    def Download(self, path):
        log.info('Downloading playlist https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV')
        for url, name in [
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
        ]:
            dstFile = os.path.join(path, 'CrashCoursePhysics', '%s.mp4' % name)
            if os.path.exists(dstFile):
                log.info('Skipping %s as "%s" exists', name, dstFile)
            else:
                log.info('Downloading %s to %s', url, dstFile)
                bestStream = self.GetBestStream(url, preftype='mp4')
                data = requests.get(bestStream.url).content
                with open(dstFile, 'w') as f:
                    f.write(data)


class Gorbushin(YoutubeDownloader):
    def Download(self, path):
        log.info('Downloading playlist https://www.youtube.com/playlist?list=PLNG6BIg2XJxCfZtigKso6rBpJ2yk_JFVp')
        for url, name in [
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
        ]:
            dstFile = os.path.join(path, 'Горбушин', '%s.mp4' % name)
            if os.path.exists(dstFile):
                log.info('Skipping %s as "%s" exists', name, dstFile)
            else:
                log.info('Downloading %s to %s', url, dstFile)
                bestStream = self.GetBestStream(url)
                data = requests.get(bestStream.url).content
                with open(dstFile, 'w') as f:
                    f.write(data)


class TitleCanonizer(object):
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
            ]

        self._Replacements = replacements

    def Canonize(self, title):
        canonized = str(title)
        for pattern, replacement in self._Replacements:
            canonized = re.sub(pattern, replacement, canonized)
        canonized = canonized.strip()
        return canonized


class YoutubePlaylist(object):
    def __init__(self, url):
        assert url.startswith('https://www.youtube.com/playlist?list=PL')
        self._Url = url
        self._TitleCanonizer = TitleCanonizer()

    def ListVideos(self):
        log.info('Looking for videos in %s', self._Url)

        searchPrefix = 'window["ytInitialData"] = '
        count = 0
        index = None
        playlistTitle = None
        videos = []
        for line in requests.get(self._Url).text.split('\n'):
            if line.strip().startswith(searchPrefix):
                l = line.strip()[len(searchPrefix):].strip(';')
                loaded = json.loads(l)
                playlistTitle = loaded['metadata']['playlistMetadataRenderer']['title']
                for contentItem in loaded['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']:
                    try:
                        index = int(contentItem['playlistVideoRenderer']['index']['simpleText'])
                        url = 'https://www.youtube.com/watch?v=%s' % contentItem['playlistVideoRenderer']['videoId']
                        title = contentItem['playlistVideoRenderer']['title']['runs'][0]['text']
                        log.debug('  #%02d %s, %s', index, self._TitleCanonizer.Canonize(title), url)
                        count += 1
                        videos.append((index, url, title))
                    except Exception as e:
                        log.error('Error %s on %s', e, json.dumps(json.loads(l), separators=(",", ":"), sort_keys=True, indent=4, ensure_ascii=False))
                        raise

        assert index == count, f'{index} (index) != {count} (count)'
        log.info('Found %d videos for \'%s\' %s', count, playlistTitle, self._Url)
        return playlistTitle, videos



def runDownload(args):
    for downloader in [
        # library.download.MathusPhys(),
        # library.download.ZnakKachestava(),
    ]:
        downloader.Download(library.files.udrPath(downloader.GetDirname()))

    for videoDownloader in [
        library.download.GetAClass(),
        library.download.Gorbushin(),
        library.download.CrashCoursePhysics(),
        library.download.Foxford(),
    ]:
        videoDownloader.Download(library.files.udrPath('Видео'))

    video_count = 0

    for url in [
        'https://www.youtube.com/playlist?list=PLNG6BIg2XJxCfZtigKso6rBpJ2yk_JFVp',  # Горбушин
        'https://www.youtube.com/playlist?list=PL66kIi3dt8A6Hd7soGMFXe6E5366Y66So',  # Фоксфорд
        # 'Курс физики основной школы'
        'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9TcTQiq-EZeVuVPc6P8PSX',  # 7 класс
        'https://www.youtube.com/playlist?list=PLYLAAGsAQhw_dGE-7OdXgBXu52_GbnvF7',  # 8 класс
        'https://www.youtube.com/playlist?list=PLYLAAGsAQhw9fX9rgG5Z20V_M2AaUKErL',  # 9 класс — это 8-й
        'https://www.youtube.com/playlist?list=PLYLAAGsAQhw8Y5BWL3nyecfr2nK6xqwIO',  # Підготовка до ДПА 9 клас
    ]:
        youtubePlaylist = library.download.YoutubePlaylist(url)
        title, videos = youtubePlaylist.ListVideos()
        for index, url, video_title in videos:
            video_count += 1
            log.info(f'{title}: {video_title}')

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
                log.info(f'{full_chapter}: {video_title}')
    log.info(f'Got total of {video_count} videos')


def populate_parser(parser):
    parser.set_defaults(func=runDownload)
