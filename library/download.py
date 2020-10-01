# -*- coding: utf-8 -*-

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
    (u'Механика', [
        ('/phys/ravnomer.pdf', u'Равномерное движение'),
        ('/phys/ravnouskor.pdf', u'Равноускоренное движение'),
        ('/phys/vertical.pdf', u'Вертикальное движение'),
        ('/phys/neravnomer.pdf', u'Неравномерное движение'),
        ('/phys/otnodvi.pdf', u'Относительность движения'),
        ('/phys/uprugotr.pdf', u'Упругое отражение'),
        ('/phys/ballistika.pdf', u'Баллистика. Координаты'),
        ('/phys/ballisvec.pdf', u'Баллистика. Векторы'),
        ('/phys/ballisotr.pdf', u'Баллистика. Отражения'),
        ('/phys/pizan.pdf', u'Баллистика. Относительность'),
        ('/phys/dviok.pdf', u'Движение по окружности'),
        ('/phys/zakopal.pdf', u'Движение со связями. Кинематика'),
        ('/phys/mro.pdf', u'Масса и плотность'),
        ('/phys/zanew.pdf', u'Законы Ньютона'),
        ('/phys/grav.pdf', u'Гравитация'),
        ('/phys/silaupr.pdf', u'Сила упругости'),
        ('/phys/silatren.pdf', u'Сила трения'),
        ('/phys/svtela.pdf', u'Связанные тела'),
        ('/phys/naplos.pdf', u'Наклонная плоскость'),
        ('/phys/kinsv.pdf', u'Движение со связями. Динамика'),
        ('/phys/imp.pdf', u'Импульс'),
        ('/phys/sysmat.pdf', u'Системы материальных точек'),
        ('/phys/cmass.pdf', u'Центр масс'),
        ('/phys/peremass.pdf', u'Движение с переменной массой'),
        ('/phys/ae.pdf', u'Работа и энергия'),
        ('/phys/conserva.pdf', u'Консервативные системы'),
        ('/phys/dynpend.pdf', u'Динамика маятника'),
        ('/phys/mpet.pdf', u'Мёртвая петля'),
        ('/phys/sosf.pdf', u'Соскальзывание со сферы'),
        ('/phys/upru.pdf', u'Упругие взаимодействия'),
        ('/phys/krivitra.pdf', u'Кривизна траектории'),
        ('/phys/neconserva.pdf', u'Неконсервативные системы'),
        ('/phys/neupru.pdf', u'Неупругие взаимодействия'),
        ('/phys/raspad.pdf', u'Распад частиц'),
        ('/phys/rasse.pdf', u'Рассеяние частиц'),
        ('/phys/nucreac.pdf', u'Ядерные реакции'),
        ('/phys/conpend.pdf', u'Конический маятник'),
        ('/phys/udarsil.pdf', u'Ударные силы'),
        ('/phys/statika.pdf', u'Статика'),
        ('/phys/mevip.pdf', u'Метод виртуальных перемещений'),
        ('/phys/gs.pdf', u'Гидростатика'),
        ('/phys/truzhi.pdf', u'Трубка с жидкостью'),
        ('/phys/gorsilar.pdf', u'Горизонтальная сила Архимеда'),
        ('/phys/tolkanat.pdf', u'Массивный канат'),
        ('/phys/masspru.pdf', u'Массивная пружина'),
        ('/phys/momentsil.pdf', u'Момент силы'),
        ('/phys/vratela.pdf', u'Вращение твёрдого тела'),
        ('/phys/motiliq.pdf', u'Движение жидкости'),
        ('/phys/podobraz.pdf', u'Подобие и размерность'),
        ('/phys/soprosred.pdf', u'Сопротивление среды'),
        ('/phys/avtomobil.pdf', u'Движение автомобиля'),
        ('/phys/velipro.pdf', u'Процессы и измерения'),
        ('/phys/difur.pdf', u'Дифференциальные уравнения'),
        ('/phys/urkol1.pdf', u'Уравнение колебаний. 1'),
        ('/phys/urkol2.pdf', u'Уравнение колебаний. 2'),
        ('/phys/garmod.pdf', u'Гармоническое движение'),
        ('/phys/neiso.pdf', u'Неинерциальные системы отсчёта'),
        ('/phys/mehavol.pdf', u'Механические волны'),
        ('/phys/vecmech.pdf', u'Векторы и механика'),
        ('/phys/kepler.pdf', u'Законы Кеплера'),
        ('/phys/ustoravno.pdf', u'Устойчивость равновесия'),
        ('/phys/integral-mech.pdf', u'Интеграл. Механика'),
        ('/phys/Zmech.pdf', u'Задавальник МФТИ. Механика'),
    ]),
    (u'Термодинамика', [
        ('/phys/atomol.pdf', u'Атомы и молекулы'),
        ('/phys/osnurav_mkt.pdf', u'Основное уравнение МКТ'),
        ('/phys/ursos.pdf', u'Уравнение состояния'),
        ('/phys/vosh.pdf', u'Воздушный шар'),
        ('/phys/sfersloy.pdf', u'Сферический слой'),
        ('/phys/gaspru.pdf', u'Газ и пружина'),
        ('/phys/podvodrab.pdf', u'Подводные работы'),
        ('/phys/smesigas.pdf', u'Газовые смеси'),
        ('/phys/isopr.pdf', u'Изопроцессы'),
        ('/phys/trurtu.pdf', u'Трубка со ртутью'),
        ('/phys/poluper.pdf', u'Полупрозрачные перегородки'),
        ('/phys/effusion.pdf', u'Эффузия'),
        ('/phys/vnutren.pdf', u'Внутренняя энергия'),
        ('/phys/teplo.pdf', u'Теплообмен'),
        ('/phys/newrilaw.pdf', u'Теплопроводность'),
        ('/phys/cycwork.pdf', u'Работа в цикле'),
        ('/phys/perzater.pdf', u'Первый закон термодинамики'),
        ('/phys/cgaza.pdf', u'Теплоёмкость газа'),
        ('/phys/teploma.pdf', u'Тепловые двигатели'),
        ('/phys/holonasos.pdf', u'Холодильник и тепловой насос'),
        ('/phys/dvigaza.pdf', u'Движение газа'),
        ('/phys/npar.pdf', u'Насыщенный пар'),
        ('/phys/vvpp.pdf', u'Влажный воздух'),
        ('/phys/uravadia.pdf', u'Уравнение адиабаты'),
        ('/phys/politrop.pdf', u'Политропический процесс'),
        ('/phys/baroformula.pdf', u'Модели атмосферы'),
        ('/phys/neidegas.pdf', u'Неидеальный газ'),
        ('/phys/povernat.pdf', u'Поверхностное натяжение'),
        ('/phys/integral-therm.pdf', u'Интеграл. Термодинамика'),
    ]),
    (u'Оптика', [
        ('/phys/luchi.pdf', u'Световые лучи'),
        ('/phys/plozer.pdf', u'Плоское зеркало'),
        ('/phys/sferizer.pdf', u'Сферическое зеркало'),
        ('/phys/prelozak.pdf', u'Закон преломления'),
        ('/phys/polnotrazh.pdf', u'Полное отражение'),
        ('/phys/prelomal.pdf', u'Преломление. Малые углы'),
        ('/phys/tolstolin.pdf', u'Толстые линзы'),
        ('/phys/prinfer.pdf', u'Принцип Ферма'),
        ('/phys/linfocus.pdf', u'Фокусное расстояние линзы'),
        ('/phys/linrays.pdf', u'Ход лучей в линзах'),
        ('/phys/formulin.pdf', u'Формула линзы'),
        ('/phys/genformulin.pdf', u'Обобщённая формула линзы'),
        ('/phys/produv.pdf', u'Продольное увеличение'),
        ('/phys/skoriz.pdf', u'Скорость изображения'),
        ('/phys/linpen.pdf', u'Линза и маятник'),
        ('/phys/dvelin.pdf', u'Система двух линз'),
        ('/phys/linzer.pdf', u'Линза и зеркало'),
        ('/phys/linliq.pdf', u'Линза и жидкость'),
        ('/phys/linplast.pdf', u'Линза и пластина'),
        ('/phys/ropsis.pdf', u'Разные оптические системы'),
        ('/phys/priboropt.pdf', u'Оптические приборы'),
        ('/phys/glaz.pdf', u'Глаз человека'),
        ('/phys/neosreda.pdf', u'Неоднородная среда'),
        ('/phys/interf.pdf', u'Интерференция света'),
    ]),
    (u'Общефизическое', [
        ('/phys/grafmet.pdf', u'Графические методы'),
        ('/phys/szf.pdf', u'Среднее значение функции'),
        ('/phys/fxyz.pdf', u'Функции нескольких переменных'),
        ('/phys/sto.pdf', u'Теория относительности'),
    ]),
    (u'Электродинамика', [
        ('/phys/zakon_kulona.pdf', u'Закон Кулона'),
        ('/phys/superposition.pdf', u'Напряжённость электрического поля'),
        ('/phys/teorema-gaussa.pdf', u'Теорема Гаусса'),
        ('/phys/zgir.pdf', u'Потенциал электрического поля'),
        ('/phys/prosf.pdf', u'Проводящие сферы'),
        ('/phys/zarplast.pdf', u'Заряженная пластина'),
        ('/phys/metiz.pdf', u'Метод изображений'),
        ('/phys/plokon.pdf', u'Плоский конденсатор'),
        ('/phys/dielkon.pdf', u'Конденсатор с диэлектриком'),
        ('/phys/electrodav.pdf', u'Электрическое давление'),
        ('/phys/teorema-edinstvennosti.pdf', u'Теорема единственности'),
        ('/phys/zener.pdf', u'Энергия зарядов'),
        ('/phys/enerpol.pdf', u'Энергия электрического поля'),
        ('/phys/dviel.pdf', u'Движение в электрическом поле'),
        ('/phys/localom.pdf', u'Локальный закон Ома'),
        ('/phys/elcirc.pdf', u'Электрические цепи'),
        ('/phys/r.pdf', u'Вычисление сопротивлений'),
        ('/phys/mtoka.pdf', u'Мощность тока'),
        ('/phys/elenag.pdf', u'Электронагреватель'),
        ('/phys/pravila_kirhgofa.pdf', u'Правила Кирхгофа'),
        ('/phys/e0r0.pdf', u'Эквивалентный источник'),
        ('/phys/vah.pdf', u'Вольт-амперная характеристика'),
        ('/phys/nelinel.pdf', u'Нелинейные элементы'),
        ('/phys/diodrez.pdf', u'Диод и резисторы'),
        ('/phys/ucap.pdf', u'Цепь с конденсатором'),
        ('/phys/icap.pdf', u'Ток через конденсатор'),
        ('/phys/cc.pdf', u'Соединения конденсаторов'),
        ('/phys/c.pdf', u'Вычисление ёмкостей'),
        ('/phys/qc.pdf', u'Количество теплоты. Конденсатор'),
        ('/phys/slokon.pdf', u'Сложный конденсатор'),
        ('/phys/podviplast.pdf', u'Подвижная пластина'),
        ('/phys/diodcap.pdf', u'Диод и конденсаторы'),
        ('/phys/flor.pdf', u'Сила Лоренца'),
        ('/phys/famp.pdf', u'Сила Ампера'),
        ('/phys/magnipol.pdf', u'Магнитное поле токов'),
        ('/phys/magnipotok.pdf', u'Магнитный поток'),
        ('/phys/halleffect.pdf', u'Эффект Холла'),
        ('/phys/eledvig.pdf', u'Двигатель постоянного тока'),
        ('/phys/mgd.pdf', u'Магнитная гидродинамика'),
        ('/phys/emind.pdf', u'Вихревое электрическое поле'),
        ('/phys/selfind.pdf', u'Самоиндукция'),
        ('/phys/emkol.pdf', u'Электромагнитные колебания'),
        ('/phys/slokonkol.pdf', u'Сложный конденсатор. Колебания'),
        ('/phys/paramkol.pdf', u'Параметрические колебания'),
        ('/phys/ql.pdf', u'Количество теплоты. Катушка'),
        ('/phys/diod.pdf', u'Диод и катушка'),
        ('/phys/properehod.pdf', u'Переходные процессы'),
        ('/phys/peremetok.pdf', u'Переменный ток'),
        ('/phys/transformator.pdf', u'Трансформатор'),
        ('/phys/emw.pdf', u'Электромагнитные волны'),
        ('/phys/integral-el.pdf', u'Интеграл. Электродинамика'),
        ('/phys/edipole.pdf', u'Электрический диполь'),
        ('/phys/mdipole.pdf', u'Магнитный диполь'),
    ]),
    (u'Квантовая физика', [
        ('/phys/dasveta.pdf', u'Давление света'),
        ('/phys/ff.pdf', u'Фотоэффект'),
        ('/phys/atnuc.pdf', u'Атомы и ядра'),
        ('/phys/radecay.pdf', u'Радиоактивный распад'),
        ('/phys/defectmass.pdf', u'Дефект масс'),
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
                filename = (u'%02d-%s' % (index, name)).replace(' ', '-').replace('.', '') + '.pdf'
                log.info(u'    Download %s into %s', url, filename)
                assert '/' not in filename
                dstFile = os.path.join(partDir, filename)
                data = requests.get(url).content
                with open(dstFile, 'w') as f:
                    f.write(data)

    def GetDirname(self):
        return u'Материалы - mathus'


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
                    print 'Saving %s to %s' % (presName, filename)
                    # with open(filename, 'w') as f:
                    #     f.write(requests.get(link).content)

    def GetDirname(self):
        return u'znakka4estva'


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
            ('https://www.youtube.com/watch?v=8yXf4Gawl4w', u'8 - 01 - Действия электрического тока'),
            ('https://www.youtube.com/watch?v=SwNJwbU_lYU', u'8 - 02 - Электролиз'),
            ('https://www.youtube.com/watch?v=RU_-6Ahalqk', u'8 - 03 - Направление электрического тока'),
            ('https://www.youtube.com/watch?v=iyR4Nt7Twg4', u'8 - 04 - Закон Ома'),
            ('https://www.youtube.com/watch?v=RnQGENiF-QM', u'8 - 05 - Внутреннее сопротивление'),
            ('https://www.youtube.com/watch?v=X7_lDtGzXTY', u'8 - 06 - Последовательное и параллельное соединение сопротивлений'),
            ('https://www.youtube.com/watch?v=no9KjloMdxU', u'8 - 07 - Сопротивление куба'),
            ('https://www.youtube.com/watch?v=DowFnoMYqgI', u'8 - 08 - Лампа накаливания'),
            ('https://www.youtube.com/watch?v=8GvuGCE9JQI', u'8 - 09 - Электродвижущая сила (ЭДС)'),
            ('https://www.youtube.com/watch?v=GGnFhHSCuAs', u'8 - 10 - Закон Джоуля-Ленца. Часть 1'),
            ('https://www.youtube.com/watch?v=xlDaZVQWbNA', u'8 - 11 - Закон Джоуля-Ленца. Часть 2'),
            ('https://www.youtube.com/watch?v=4j4T9wyRAGQ', u'10 - 12 - Коэффициент мощности косинус фи'),
            ('https://www.youtube.com/watch?v=1T8FRhLCUJM', u'8 - Коронный разряд и огни святого Эльма'),
            ('https://www.youtube.com/watch?v=627QB4DGE8k', u'10 - 05 - Диэлектрик в электрическом поле'),
            ('https://www.youtube.com/watch?v=NV2V5VcXlEI', u'8 - Переменный ток'),
            ('https://www.youtube.com/watch?v=BQOK_b9TsjE', u'8 - Когда переменный ток становится постоянным'),
            ('https://www.youtube.com/watch?v=denwtwcfvZw', u'8 - Стабилитрон'),
            ('https://www.youtube.com/watch?v=4E1AxUMUz-g', u'9 - Дисперсия света'),
            ('https://www.youtube.com/watch?v=BhYKN21olBw', u'9 - Brain Damage'),
            ('https://www.youtube.com/watch?v=mh-LTSGjFsE', u'9 - 10 - Закон Гука и энергия упругой деформации'),
            ('https://www.youtube.com/watch?v=p15KNqWUZ-c', u'Сергей Гуриев - Экономика красоты и счастья - 2012'),
            ('https://www.youtube.com/watch?v=OHCobJjMHuM', u'Творческая дистанционка от Димы Зицера - 2020-03-20'),
            ('https://www.youtube.com/watch?v=dSVdjmabpgg', u'HBO - Welcome to Chechnya - 2020'),
            # ('https://www.youtube.com/watch?v=lYTdewh-dhY', u'Открытая Россия - Семья - Фильм о Рамзане Кадырове - 2015'),
            ('https://www.youtube.com/watch?v=2nTmeuXQT5w', u'2020 - Математический марафон'),
            ('https://www.youtube.com/watch?v=vF1UGmi5m8s', u'2019 - Дудь - Беслан'),
            ('https://www.youtube.com/watch?v=-TSD1cX2htQ', u'2019 - Новая Газета - Беслан'),
        ]:
            dstFile = os.path.join(path, u'GetAClass', u'%s.mp4' % name)
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
            ('https://www.youtube.com/watch?v=iWr6U3-rynQ', u'Кинематика - Плоское движение точек твердого тела'),
            ('https://www.youtube.com/watch?v=W6zOwbHkA8g', u'Термодинамика - Адиабатный процесс'),
            ('https://www.youtube.com/watch?v=RXvNehmSfl8', u'Статика - Условия равновесия тела'),
            ('https://www.youtube.com/watch?v=YPTGHZZ6H0I', u'Термодинамика - Теплоёмкость'),
            ('https://www.youtube.com/watch?v=7ZpPP_LZYNM', u'Термодинамика - Молярная теплоёмкость'),
            ('https://www.youtube.com/watch?v=b_LlqXeABQU', u'Термодинамика - Удельная теплоёмкость'),
            ('https://www.youtube.com/watch?v=KAcCPNDmRe8', u'Статика - Момент силы'),
            ('https://www.youtube.com/watch?v=0hFWeR8ybxs', u'Последовательное и параллельное соединение проводников'),
            ('https://www.youtube.com/watch?v=vUkOstwz1kA', u'Постоянный ток - Закон Ома для участка цепи'),
            ('https://www.youtube.com/watch?v=487Z6jJVngQ', u'Постоянный ток - Электрическое сопротивление проводника'),
            ('https://www.youtube.com/watch?v=frJYMkK6lFk', u'Постоянный ток - Напряжение'),
            ('https://www.youtube.com/watch?v=At9OP9pQqCE', u'Постоянный ток - Сила тока'),
            ('https://www.youtube.com/watch?v=Hp3dJNEXW00', u'Постоянный ток - Электрический ток'),
            ('https://www.youtube.com/watch?v=hxfowwBlDWg', u'Термодинамика - Количество теплоты'),
            ('https://www.youtube.com/watch?v=2QrBqGvGCKA', u'Термодинамика - Циклические процессы'),
            ('https://www.youtube.com/watch?v=iDDGCf9eyes', u'Термодинамика - Тепловые машины'),
            ('https://www.youtube.com/watch?v=piKLPtzJ1sk', u'МКТ - Графики газовых процессов'),
            ('https://www.youtube.com/watch?v=emwG8AVHciM', u'МКТ - Основные термодинамические процессы'),
            ('https://www.youtube.com/watch?v=ewDWrUCY8sk', u'Геометрическая оптика - Скорость света'),
            ('https://www.youtube.com/watch?v=tEfEaBmYPrI', u'Геометрическая оптика - Плоское зеркало'),
            ('https://www.youtube.com/watch?v=lrBE5EHwbqg', u'Кинематика - Относительность механического движения'),
            ('https://www.youtube.com/watch?v=cMBrpdpOAfU', u'Геометрическая оптика - Законы преломления'),
            ('https://www.youtube.com/watch?v=AuqJHgDFJmY', u'Геометрическая оптика - Законы отражения'),
            ('https://www.youtube.com/watch?v=GpuqosemhBk', u'Кинематика - Поступательное и вращательное движение твёрдого тела'),
            ('https://www.youtube.com/watch?v=uVL3SoDDMNg', u'Геометрическая оптика - Фокусное расстояние и оптическая сила линзы'),
            ('https://www.youtube.com/watch?v=vjmyDrCSFm8', u'Геометрическая оптика - Построение изображений в тонких линзах'),
            ('https://www.youtube.com/watch?v=8Vm_svrry9A', u'Геометрическая оптика - Формула тонкой линзы'),
            ('https://www.youtube.com/watch?v=gy29hTFu54E', u'Геометрическая оптика - Действительный и мнимый источники'),
            ('https://www.youtube.com/watch?v=c1cqOmLOQ9M', u'Геометрическая оптика - Тонкие линзы'),
            ('https://www.youtube.com/watch?v=fQCZkmd9MUk', u'Геометрическая оптика - Действительное и мнимое изображения'),
            ('https://www.youtube.com/watch?v=fvRCNxAjgQ4', u'Геометрическая оптика - Показатель преломления'),
            ('https://www.youtube.com/watch?v=pxc2NUAroLI', u'Геометрическая оптика - Образование тени и полутени'),
            ('https://www.youtube.com/watch?v=sxCkJ_4sT9U', u'Геометрическая оптика - Распространение света'),
            ('https://www.youtube.com/watch?v=utJyyEPMXBU', u'Законы сохранения в механике - Внутренние и внешние силы'),
            ('https://www.youtube.com/watch?v=wsVmAedcD2A', u'Законы сохранения в механике - Неупругий удар'),
            ('https://www.youtube.com/watch?v=RfO-7rPHRTg', u'Общее - Плотность'),
            ('https://www.youtube.com/watch?v=PXyIVNgxfvM', u'МКТ - Основное уравнение МКТ'),
            ('https://www.youtube.com/watch?v=kr8kkIszQbM', u'Термодинамика - Внутренняя энергия и способы её изменения'),
            ('https://www.youtube.com/watch?v=LlPHqQ3UaS4', u'Термодинамика - Внутренняя энергия идеального газа'),
            ('https://www.youtube.com/watch?v=-IFzslacWrI', u'Законы сохранения в механике - Абсолютно упругий удар'),
            ('https://www.youtube.com/watch?v=dqijLBR1qZc', u'Законы сохранения в механике - Закон сохранения импульса'),
            ('https://www.youtube.com/watch?v=CBz4S4gKMfY', u'Законы сохранения в механике - Импульс'),
            ('https://www.youtube.com/watch?v=T72IA5QmUZU', u'Термодинамика - Работа газа'),
            ('https://www.youtube.com/watch?v=lao0b2VD-Bk', u'Термодинамика - Первое начало термодинамики'),
            ('https://www.youtube.com/watch?v=XJS1llpnZK8', u'МКТ - Уравнение Менделеева-Клапейрона для идеального газа'),
            ('https://www.youtube.com/watch?v=ivwYzV9Ar2k', u'МКТ - Смеси газов. Закон Дальтона'),
            ('https://www.youtube.com/watch?v=2nMyiIQtgvM', u'МКТ - Идеальный газ'),
            ('https://www.youtube.com/watch?v=Jo_EXQzgHT0', u'МКТ - Основные положения МКТ и их опытное обоснование'),
            ('https://www.youtube.com/watch?v=OBArlSVHl70', u'МКТ - Изобарный процесс'),
            ('https://www.youtube.com/watch?v=n12aZKl-fWE', u'МКТ - Изохорный процесс'),
            ('https://www.youtube.com/watch?v=RETZXUDfDhc', u'МКТ - Изотермический процесс'),
            ('https://www.youtube.com/watch?v=oFrkSRFOvcE', u'Механика жидкостей и газов - Сила Архимеда'),
            ('https://www.youtube.com/watch?v=DFuQya7Oe9U', u'Динамика - Закон Всемирного тяготения'),
            ('https://www.youtube.com/watch?v=MxfuBo6ih_M', u'Динамика - Третий закон Ньютона'),
            ('https://www.youtube.com/watch?v=kgfpqLNrjuk', u'Динамика - Второй закон Ньютона'),
            ('https://www.youtube.com/watch?v=niJFMDiuMj8', u'Динамика - Первый закон Ньютона'),
            ('https://www.youtube.com/watch?v=d5QhXjgW8tw', u'Общее - Масса'),
            ('https://www.youtube.com/watch?v=M0pnXB_cEMY', u'Динамика - Силы'),
        ]:
            dstFile = os.path.join(path, u'Foxford', u'%s.mp4' % name)
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
            dstFile = os.path.join(path, u'CrashCoursePhysics', u'%s.mp4' % name)
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
            ('https://www.youtube.com/watch?v=yvZoJ9oA2T0', u'Подготовка к ЕГЭ по физике. Занятие 01'),
            ('https://www.youtube.com/watch?v=znsFzrsHXcw', u'Подготовка к ЕГЭ по физике. Занятие 02'),
            ('https://www.youtube.com/watch?v=woiO_HENO20', u'Подготовка к ЕГЭ по физике. Занятие 03'),
            ('https://www.youtube.com/watch?v=cPP9sPWmNds', u'Подготовка к ЕГЭ по физике. Занятие 04'),
            ('https://www.youtube.com/watch?v=9zUxpWaRnN0', u'Подготовка к ЕГЭ по физике. Занятие 05'),
            ('https://www.youtube.com/watch?v=2vZfPKmfeCs', u'Подготовка к ЕГЭ по физике. Занятие 06'),
            ('https://www.youtube.com/watch?v=lkRIteVb0lU', u'Подготовка к ЕГЭ по физике. Занятие 07'),
            ('https://www.youtube.com/watch?v=E3tFXjh5WFY', u'Подготовка к ЕГЭ по физике. Занятие 08'),
            ('https://www.youtube.com/watch?v=9XIZffuvibY', u'Подготовка к ЕГЭ по физике. Занятие 09'),
            ('https://www.youtube.com/watch?v=ScpikkktFeM', u'Подготовка к ЕГЭ по физике. Занятие 10'),
            ('https://www.youtube.com/watch?v=E214eHekXGA', u'Подготовка к ЕГЭ по физике. Занятие 11'),
            ('https://www.youtube.com/watch?v=E77nKXA3XGM', u'Подготовка к ЕГЭ по физике. Занятие 12'),
            ('https://www.youtube.com/watch?v=Yso604wZlls', u'Подготовка к ЕГЭ по физике. Занятие 13'),
            ('https://www.youtube.com/watch?v=f4i99JCpDaE', u'Подготовка к ЕГЭ по физике. Занятие 14'),
            ('https://www.youtube.com/watch?v=JPQe2wTsq34', u'Подготовка к ЕГЭ по физике. Занятие 15'),
            ('https://www.youtube.com/watch?v=o2rI59dasHc', u'Подготовка к ЕГЭ по физике. Занятие 16'),
            ('https://www.youtube.com/watch?v=XrAvEu7dU4o', u'Подготовка к ЕГЭ по физике. Занятие 17'),
            ('https://www.youtube.com/watch?v=un39S9MGUtQ', u'Подготовка к ЕГЭ по физике. Занятие 18'),
            ('https://www.youtube.com/watch?v=DEVHbDMiTA8', u'Подготовка к ЕГЭ по физике. Занятие 19'),
            ('https://www.youtube.com/watch?v=-mHpFMPXgfs', u'Подготовка к ЕГЭ по физике. Занятие 20'),
            ('https://www.youtube.com/watch?v=ieZkxvs-134', u'Подготовка к ЕГЭ по физике. Занятие 21'),
            ('https://www.youtube.com/watch?v=Dc_yG7EAuls', u'Подготовка к ЕГЭ по физике. Занятие 22'),
            ('https://www.youtube.com/watch?v=TdKHj4ZKM9o', u'Подготовка к ЕГЭ по физике. Занятие 23'),
            ('https://www.youtube.com/watch?v=2kOmU6WItv8', u'Подготовка к ЕГЭ по физике. Занятие 24'),
            ('https://www.youtube.com/watch?v=pc0wzU-wTMg', u'Подготовка к ЕГЭ по физике. Занятие 25'),
        ]:
            dstFile = os.path.join(path, u'Горбушин', u'%s.mp4' % name)
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
            log.debug('Using default replacements'):
            replacements = [
                (ur'^Физика[\.:] ', u''),
                (ur'  +', u' '),
                (ur' Центр онлайн-обучения «Фоксфорд»$', u''),
                (ur'\.$', u''),
            ]

        self._Replacements = replacements

    def Canonize(self, title):
        canonized = unicode(title)
        for pattern, replacement in self._Replacements:
            canonized = re.sub(pattern, replacement, canonized)
        canonized = canonized.strip()
        return canonized


class YoutubePlaylist(object):
    def __init__(self, url):
        self._Url = url
        self._TitleCanonizer = TitleCanonizer()

    def ListVideos(self):
        log.info('Looking for videos in %s', self._Url)
        searchPrefix = 'window["ytInitialData"] = '
        count = 0
        for line in requests.get(self._Url).content.split('\n'):
            if line.strip().startswith(searchPrefix):
                l = line.strip()[len(searchPrefix):].strip(';')
                for contentItem in json.loads(l)['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']:
                    try:
                        index = int(contentItem['playlistVideoRenderer']['index']['simpleText'])
                        url = 'https://www.youtube.com/watch?v=%s' % contentItem['playlistVideoRenderer']['videoId']
                        title = contentItem['playlistVideoRenderer']['title']['runs'][0]['text']
                        log.debug('  #%02d %s, %s', index, self._TitleCanonizer.Canonize(title), url)
                        count += 1
                        log.debug('%s', json.dumps(contentItem, separators=(",", ":"), sort_keys=True, indent=4, ensure_ascii=False))
                        yield index, url
                    except Exception as e:
                        log.error('Error %s on %s', e, json.dumps(contentItem, separators=(",", ":"), sort_keys=True, indent=4, ensure_ascii=False))
                        raise
        assert index == count
        log.info('Found %d videos for %s', count, self._Url)
