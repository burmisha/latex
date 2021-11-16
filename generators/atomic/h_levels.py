import generators.variant as variant
from generators.helpers import UnitValue, Consts


@variant.solution_space(150)
@variant.text('''
    При переходе электрона в атоме с одной стационарной орбиты на другую
    излучается фотон с энергией ${E:Value}$.
    Какова длина волны этой линии спектра?
    Постоянная Планка ${Consts.h:Task}$, скорость света ${Consts.c:Task}$.
''')
@variant.answer_short('''
    E = h\\nu = h \\frac c\\lambda
    \\implies \\lambda = \\frac{hc}E
        = \\frac{{Consts.h:Value} * {Consts.c:Value|s}}{E:Value|s}
        = {lmbd:Value}.
''')
@variant.arg(E=('E = {} 10^{{-19}} Дж', ['4.04', '5.05', '2.02', '7.07', '1.01', '0.55']))
class Lambda_from_E(variant.VariantTask):  # Вишнякова - Базовый курс 5.2 - задача 01
    def GetUpdate(self, E=None):
        lmbd = Consts.c * Consts.h / E
        mul = 10 ** 9
        return dict(lmbd=f'\\lambda = {lmbd.SI_Value * mul:.2f} нм')


@variant.solution_space(150)
@variant.text('''
    Излучение какой длины волны поглотил атом водорода, если полная энергия в атоме увеличилась на ${E:Value}$?
    Постоянная Планка ${Consts.h:Task}$, скорость света ${Consts.c:Task}$.
''')
@variant.answer_short('''
    E = h\\nu = h \\frac c\\lambda
    \\implies \\lambda = \\frac{hc}E
        = \\frac{{Consts.h:Value} * {Consts.c:Value|s}}{E:Value|s}
        = {lmbd:Value}.
''')
@variant.arg(E=['E = %d 10^{-19} Дж' % E for E in [2, 3, 4, 6]])
class Lambda_from_E_2(variant.VariantTask):  # Вишнякова - Базовый курс 5.2 - задача 02
    def GetUpdate(self, E=None):
        lmbd = Consts.h * Consts.c / E
        mul = 10 ** 9
        return dict(lmbd=f'\\lambda = {lmbd.SI_Value * mul:.2f} нм')


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
