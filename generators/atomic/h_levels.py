import generators.variant as variant
from generators.helpers import UnitValue, Consts, Fraction


@variant.solution_space(150)
@variant.text('''
    При переходе электрона в атоме с одной стационарной орбиты на другую
    излучается фотон с энергией {E:V:e}.
    Какова длина волны этой линии спектра?
    Постоянная Планка {Consts.h:Task:e}, скорость света {Consts.c:Task:e}.
''')
@variant.answer_short('''
    E = h\\nu = h \\frac c{lmbd:L}
    \\implies {lmbd:L} = \\frac{hc}E
        = \\frac{{Consts.h:Value} * {Consts.c:Value|s}}{E:Value|s}
        = {lmbd:Value}.
''')
@variant.arg(E=('E = {} 10^{{-19}} Дж', ['4.04', '5.05', '2.02', '7.07', '1.01', '0.55']))
class Lambda_from_E(variant.VariantTask):  # Вишнякова - Базовый курс 5.2
    def GetUpdate(self, E=None):
        lmbd = (Consts.h * Consts.c / E).IncPrecision(2).SetLetter('\\lambda').As('нм')
        return dict(lmbd=lmbd)


@variant.solution_space(150)
@variant.text('''
    Излучение какой длины волны поглотил атом водорода, если полная энергия в атоме увеличилась на {E:V:e}?
    Постоянная Планка {Consts.h:Task:e}, скорость света {Consts.c:Task:e}.
''')
@variant.answer_short('''
    E = h\\nu = h \\frac c{lmbd:L}
    \\implies {lmbd:L} = \\frac{hc}E
        = \\frac{{Consts.h:Value} * {Consts.c:Value|s}}{E:Value|s}
        = {lmbd:Value}.
''')
@variant.arg(E=['E = %d 10^{-19} Дж' % E for E in [2, 3, 4, 6]])
class Lambda_from_E_2(variant.VariantTask):  # Вишнякова - Базовый курс 5.2
    def GetUpdate(self, E=None):
        lmbd = (Consts.h * Consts.c / E).IncPrecision(2).SetLetter('\\lambda').As('нм')
        return dict(lmbd=lmbd)


@variant.solution_space(150)
@variant.text('''
    Сделайте схематичный рисунок энергетических уровней атома водорода
    и отметьте на нём первый (основной) уровень и последующие.
    Сколько различных длин волн может испустить атом водорода,
    находящийся в {n}-м возбуждённом состоянии?
    Отметьте все соответствующие переходы на рисунке и укажите,
    при каком переходе (среди отмеченных) {what} излучённого фотона {minmax}.
''')
@variant.answer_short('N = {N}, \\text{{answer}}')
@variant.arg(n=[3, 4, 5])
@variant.arg(what__what_sign=[
    ('энергия', 1),
    ('частота', 1),
    ('длина волны', -1),
])
@variant.arg(minmax__minmax_sign=[
    ('минимальна', -1),
    ('максимальна', 1),
])
class H_levels(variant.VariantTask):  # Вишнякова - Базовый курс 5.2 - задача 07
    def GetUpdate(self, n=None, what=None, minmax=None, what_sign=None, minmax_sign=None):
        answer = {
            1: 'самая длинная линия',
            -1: 'самая короткая линия',
        }[what_sign * minmax_sign]
        return dict(
            N=n * (n - 1) / 2,
            answer=answer,
        )


@variant.text('''
    Во сколько раз уменьшается радиус орбиты электрона в атоме водорода,
    если при переходе атома из одного стационарного состояния в другое
    кинетическая энергия электрона увеличивается в {n} раз?
''')
@variant.solution_space(80)
@variant.arg(n=[16])
@variant.answer_align([
    # 'E_{\\text{кин.}} &= \\frac{mv^2} \\implies v = \\sqrt{\\frac {2E_{\\text{кин.} k}} m} \\implies mv = \\sqrt{2 m E_{\\text{кин.}}},',
    'm_e v r &= n h \\implies v = \\frac{n h}{m_e r}'
    'm_e \\frac{v^2}r &= k\\frac{e^2}{r^2} \\implies m_e \\frac{n^2 h^2}{m_e^2 r^3} = k\\frac{e^2}{r^2} \\implies r = \\frac{m_e n^2 h^2}{m_e^2 k e^2}',
    'v &= \\frac{k e^2}{n h} \\implies \\sqrt{ \\frac{2E_k}{m_e} } = \\frac{k e^2}{n h} \\implies \\frac{2E_k}{m_e} = \\frac{k^2 e^4}{n^2 h^2}',
    'r &= \\frac{m_e n^2 h^2}{m_e^2 k e^2} \\implies \\frac{2E_k}{m_e} * r = \\frac{k^2 e^4}{n^2 h^2} * \\frac{m_e n^2 h^2}{m_e^2 k e^2} = k e^2 m_e'

])
class Chernoutsan_13_73(variant.VariantTask):
    def GetUpdate(self, *, n=None):
        return dict(
        )


@variant.text('''
    Во сколько раз увеличилась кинетическая энергия электрона в атоме водорода при переходе
    из одного стационарного состояния в другое, если угловая скорость вращения по орбите увеличилась в {n} раз?
''')
@variant.solution_space(80)
@variant.arg(n=[8])
@variant.answer_align([
])
class Chernoutsan_13_74(variant.VariantTask):
    def GetUpdate(self, *, n=None):
        return dict(
        )


@variant.text('''
    Во сколько раз увеличивается угловая скорость вращения электрона в атоме водорода,
    если при переходе атома из одного стационарного состояния в другое радиус орбиты электрона уменьшается в {n} раза?
''')
@variant.solution_space(80)
@variant.arg(n=[4])
@variant.answer_align([
])
class Chernoutsan_13_75(variant.VariantTask):
    def GetUpdate(self, *, A=None):
        return dict(
        )


@variant.text('''
    Переход атомов водорода из состояния с номером 2 в нормальное состояние сопровождается
    ультрафиолетовым излучением с некоторой длиной волны. Каков номер возбужденного состояния,
    в которое переходят атомы водорода из состояния с номером 2 при поглощении кванта с длиной волны, в 4 раза большей?
''')
@variant.solution_space(80)
@variant.arg(A=('A = {} a', [1]))
@variant.answer_align([
])
class Chernoutsan_13_76(variant.VariantTask):
    def GetUpdate(self, *, A=None):
        return dict(
        )


@variant.text('''
    Каков номер возбужденного состояния, в которое переходит атом водорода из нормального состояния
    при поглощении фотона, энергия которого составляет {share:LaTeX} энергии ионизации атома водорода?
''')
@variant.solution_space(80)
@variant.arg(share=[Fraction(8) / 9])
@variant.answer_align([
])
class Chernoutsan_13_77(variant.VariantTask):
    def GetUpdate(self, *, A=None):
        return dict(
        )
