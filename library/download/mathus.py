from library.download.multiple import DownloadItem

import os


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


HOST = 'http://mathus.ru'


def get_items():
    for part_index, (part_name, files) in enumerate(MATHUS_PHYS_CONFIG, 1):
        for index, (url_suffix, name) in enumerate(files, 1):
            assert url_suffix.endswith('.pdf')
            assert '/' not in name
            filename = f'{index:02d}-{name}'.replace(' ', '-').replace('.', '') + '.pdf'
            yield DownloadItem(
                filename=os.path.join(f'{part_index:02d}-{part_name}', filename),
                url=f'{HOST}{url_suffix}',
            )