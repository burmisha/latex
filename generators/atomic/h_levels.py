import generators.variant as variant
from generators.helpers import UnitValue, Consts, Fraction, n_times


@variant.solution_space(150)
@variant.text('''
    Кратко опишите {what} и укажите проблемы этой теории (какой наблюдаемый эффект она не способна описать),
    сделайте необходимые рисунки.
''')
@variant.arg(what=[
    'модель атома Томсона',
    'модель атома Резерфорда',
    'планетарную модель атома',
    'модель атома Бора',
])
class Theory01(variant.VariantTask):
    pass



@variant.solution_space(80)
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
@variant.arg(E='E = 4.04/5.05/2.02/7.07/1.01/0.55 10^{-19} Дж')
class Lambda_from_E(variant.VariantTask):  # Вишнякова - Базовый курс 5.2
    def GetUpdate(self, E=None):
        lmbd = (Consts.h * Consts.c / E).IncPrecision(2).SetLetter('\\lambda').As('нм')
        return dict(lmbd=lmbd)


@variant.solution_space(80)
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
@variant.arg(E='E = 2/3/4/6 10^{-19} Дж')
class Lambda_from_E_2(variant.VariantTask):  # Вишнякова - Базовый курс 5.2
    def GetUpdate(self, E=None):
        lmbd = (Consts.h * Consts.c / E).IncPrecision(2).SetLetter('\\lambda').As('нм')
        return dict(lmbd=lmbd)


@variant.solution_space(80)
@variant.text('''
    Электрон в некотором атоме переходит из стационарного состояния с энергией {E1:V:e}
    в другое стационарного состояния с энергией {E2:V:e}.
    \\begin{itemize}
        \\item Определите, происходит при этом поглощение или излучение кванта света?
        \\item Чему равна энергия этого фотона?
        \\item Чему равна частота этого фотона?
        \\item Чему равна длина волны этого кванта света?
    \\end{itemize}
''')
@variant.arg(E1='E_1 = -1.15/-2.35/-3.55 10^{-19} Дж')
@variant.arg(E2='E_2 = -1.75/-2.85/-3.95 10^{-19} Дж')
class TwoLevels(variant.VariantTask):  # Генденштейн-11-29-8
    pass



@variant.solution_space(80)
@variant.text('''
    В некотором атоме есть 3 энергетических уровня с энергиями {E1:Task:e}, {E2:Task:e} и {E3:Task:e}.
    Электрон находится на втором ({E2:L:e}). Определите энергию фотона, который может быть {what} таким атомом.
''')
@variant.arg(E1='E_1 = -1.1/-1.2/-1.3/-1.4/-1.5 10^{-19} Дж')
@variant.arg(E2='E_2 = -2.2/-2.5/-2.7/-2.9 10^{-19} Дж')
@variant.arg(E3='E_3 = -3.1/-3.4/-3.7 10^{-19} Дж')
@variant.arg(what='испущен/поглощён')
class MedianLevels(variant.VariantTask):
    # TODO: reorder E
    pass


@variant.solution_space(150)
@variant.text('''
    Сделайте схематичный рисунок энергетических уровней атома водорода
    и отметьте на нём первый (основной) уровень и последующие.
    Сколько различных длин волн может испустить атом водорода,
    находящийся в {n}-м возбуждённом состоянии (рассмотрите и сложные переходы)? 
    Отметьте все соответствующие переходы на рисунке и укажите,
    при каком переходе (среди отмеченных) {what} излучённого фотона {minmax}.
''')
@variant.answer_short('N = {N}, \\text{ {answer} }')
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
            N=n * (n - 1) // 2,
            answer=answer,
        )


@variant.text('''
    Во сколько раз уменьшается радиус орбиты электрона в атоме водорода,
    если при переходе атома из одного стационарного состояния в другое
    кинетическая энергия электрона увеличивается в {n_word}?
''')
@variant.solution_space(80)
@variant.arg(n__n_word=n_times(3, 4, 8, 9, 12, 16))
@variant.answer_short(
    'm_e \\frac{v^2}r = k\\frac{e^2}{r^2} \\implies mv^2 = k\\frac{e^2} r \\implies {E_k:L} = k\\frac{e^2}{2r} \\implies {n}',
)
class Chernoutsan_13_73(variant.VariantTask):
    def GetUpdate(self, *, n=None, n_word=None):
        return dict(
            E_k='E_{\\text{кин.}} = 1 Дж',
        )


@variant.text('''
    Во сколько раз увеличилась кинетическая энергия электрона в атоме водорода при переходе
    из одного стационарного состояния в другое, если угловая скорость вращения по орбите увеличилась в {n_word}?
    (Считая, что такие уровни существуют, что можно обсудить отдельно).
''')
@variant.solution_space(80)
@variant.arg(n__n_word=n_times(5, 6, 8, 10, 12))
@variant.answer_short(
    'm_e \\frac{v^2}r = k\\frac{e^2}{r^2}, v = \\omega r \\implies m_e v^2 = k\\frac{e^2}{r} = k\\frac{e^2\\omega}{ v } \\implies v^3 =  k\\frac{e^2}{ m_e } \\omega \\implies {nn:.2f}'
)
class Chernoutsan_13_74(variant.VariantTask):
    def GetUpdate(self, *, n=None, n_word=None):
        return dict(
            E_k='E_{\\text{кин.}} = 1 Дж',
            nn = n ** (2 / 3),
        )


@variant.text('''
    Во сколько раз увеличивается угловая скорость вращения электрона в атоме водорода,
    если при переходе атома из одного стационарного состояния в другое радиус орбиты электрона уменьшается в {n_word}?
    (Считая, что такие уровни существуют, что можно обсудить отдельно).
''')
@variant.solution_space(80)
@variant.arg(n__n_word=n_times(2, 3, 4, 5, 6, 7, 8))
@variant.answer_short(
    'm_e \\frac{v^2}r = k\\frac{e^2}{r^2}, v = \\omega r \\implies m_e \\omega^2 r = k\\frac{e^2}{r^2} \\implies \\omega = \\sqrt{ k\\frac{e^2}{ m_e } } r^{-\\frac 32} \\implies {nn:.2f}'
)
class Chernoutsan_13_75(variant.VariantTask):
    def GetUpdate(self, *, n=None, n_word=None):
        return dict(
            nn = n ** (3 / 2),
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
