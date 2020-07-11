# -*- coding: utf-8 -*-

import logging
import os
import re
import requests
import time

log = logging.getLogger(__name__)


try:
    import pafy # http://np1.github.io/pafy/
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
        return bestStream


class GetAClass(object):
    def __init__(self):
        self.YoutubeDownloader = YoutubeDownloader()

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
            ('https://www.youtube.com/watch?v=lYTdewh-dhY', u'Открытая Россия - Семья - Фильм о Рамзане Кадырове - 2015'),
        ]:
            dstFile = os.path.join(path, u'GetAClass', u'%s.mp4' % name)
            if os.path.exists(dstFile):
                log.debug('Skipping %s as %s exists', url, name)
            else:
                log.info('Downloading %s to %s', url, dstFile)
                bestStream = self.YoutubeDownloader.GetBestStream(url, preftype='mp4')
                bestStream.download(filepath=dstFile)


class Gorbushin(object):
    def __init__(self):
        self.YoutubeDownloader = YoutubeDownloader()

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
                log.info('Skipping %s', name)
            else:
                log.info('Downloading %s to %s', url, dstFile)
                bestStream = self.YoutubeDownloader.GetBestStream(url)
                data = requests.get(bestStream.url).content
                with open(dstFile, 'w') as f:
                    f.write(data)
