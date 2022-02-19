import itertools

import generators.variant as variant
from generators.helpers import UnitValue, Fraction, n_times
from decimal import Decimal

@variant.lv_variant_task(
    {
        'разность потенциалов': '$U$',
        'электрическое сопротивление резистора': '$R$',
        'удельное сопротивление проводника': '$\\rho$',
        'сила тока': '$\\eli$',
        'длина проводника': '$l$',
        'площадь поперечного сечения проводника': '$S$',
    },
    ['$D$', '$k$', '$\\lambda$'],
    answers_count=3,
    mocks_count=2,
)
class Definitions01(variant.VariantTask):
    pass


@variant.lv_variant_task(
    {

        'разность потенциалов': 'вольт',
        'электрическое сопротивление резистора': 'ом',
        'электрический заряд': 'кулон',
        'сила тока': 'ампер',
        'длина проводника': 'метр',
    },
    ['генри', 'ватт', 'сименс'],
    answers_count=3,
    mocks_count=2,
)
class Definitions02(variant.VariantTask):
    pass


@variant.lv_variant_task(
    {

        'закон Ома': '$\\eli R = U$',
        'электрическое сопротивление резистора': '$R = \\rho \\frac lS$',
        'эквивалентное сопротивление 2 резисторов (параллельно)': '$\\frac{R_1R_2}{R_1 + R_2}$',
        'эквивалентное сопротивление 2 резисторов (последовательно)': '$R_1 + R_2$',
    },
    ['$\\frac{2R_1R_2}{R_1 + R_2}$', '$\\frac{R_1 + R_2} 2$', '$\\sqrt{R_1R_2}$', '$\\rho = R l S$', '$R = \\rho \\frac Sl$', '$\\frac{\\eli} R = U$' ],
    answers_count=2,
    mocks_count=3,
)
class Definitions03(variant.VariantTask):
    pass


@variant.lv_variant_task(
    {

        'эквивалентное сопротивление 3 резисторов (параллельно)': '$\\frac{R_1R_2R_3}{R_1R_2 + R_2R_3 + R_3R_1}$',
        'эквивалентное сопротивление 3 резисторов (последовательно)': '$R_1 + R_2 + R_3$',
    },
    ['$\\frac{R_1R_2R_3}{R_1 + R_2 + R_3}$', '$\\frac{R_1 + R_2 + R_3}3$', '$\\frac 3{\\frac 1{R_1} + \\frac 1{R_2} + \\frac 1{R_3}}$', '$\\sqrt{\\frac{R_1^2 + R_2^2 + R_3^2}3}$',],
    answers_count=2,
    mocks_count=3,
)
class Definitions04(variant.VariantTask):
    pass


@variant.solution_space(20)
@variant.text('''
    Напротив физических величин укажите их обозначения и единицы измерения в СИ:
    \\begin{enumerate}
        \\item {v_1},
        \\item {v_2},
        \\item {v_3},
        \\item {v_4}.
    \\end{enumerate}
''')
@variant.arg(v_1=['сила тока', 'разность потенциалов', 'напряжение'])
@variant.arg(v_2=['работа тока', 'мощность тока'])
@variant.arg(v_3=['удельное сопротивление', 'ЭДС'])
@variant.arg(v_4=['внутреннее сопротивление полной цепи', 'внешнее сопротивление полной цепи'])
class Definitions05(variant.VariantTask):
    pass


@variant.solution_space(40)
@variant.text('''
    Запишите физический закон или формулу:
    \\begin{enumerate}
        \\item {v_1},
        \\item {v_2},
        \\item {v_3}.
    \\end{enumerate}
''')
@variant.arg(v_1=['правило Кирхгофа для замкнутого контура', 'правило Кирхгофа для узла цепи'])
@variant.arg(v_2=['закон Ома для однородного участка цепи', 'сопротивление резистора через удельное сопротивление'])
@variant.arg(v_3=['закон Ома для неоднородного участка цепи', 'ЭДС (определение)'])
class Definitions06(variant.VariantTask):
    pass


@variant.solution_space(80)
@variant.text('''
    Получите выражение:
    \\begin{enumerate}
        \\item {v_1},
        \\item {v_2},
        \\item {v_3},
        \\item {v_4}.
    \\end{enumerate}
''')
@variant.arg(v_1=[
    'силы тока через выделяемую мощность и сопротивление резистора',
    'силы тока через выделяемую мощность и напряжение на резисторе',
    'силы тока через выделяемую мощность и разность потенциалов на резисторе',
])
@variant.arg(v_2=[
    'силы тока через выделенную теплоту и сопротивление резистора',
    'силы тока через выделенную теплоту и напряжение на резисторе',
    'силы тока через выделенную теплоту и разность потенциалов на резисторе',
])
@variant.arg(v_3=[
    'напряжение на резисторе через выделяемую мощность и сопротивление резистора',
    'напряжение на резисторе через выделяемую мощность и силу тока через него',
])
@variant.arg(v_4=[
    'напряжение на резисторе через выделенную в нём теплоту и сопротивление резистора',
    'напряжение на резисторе через выделенную в нём теплоту и силу тока через него',
])
class Definitions08(variant.VariantTask):
    pass


@variant.solution_space(40)
@variant.text('''
    Получите выражение:
    \\begin{enumerate}
        \\item {v_1},
        \\item {v_2},
        \\item {v_3},
        \\item {v_4}.
    \\end{enumerate}
''')
@variant.arg(v_1=['длины проводника через его сопротивление', 'площади поперечного сечения проводника через его сопротивление'])
@variant.arg(v_2=['сопротивление из закона Ома', 'удельное сопротивление из закона Ома'])
@variant.arg(v_3=['внутреннее сопротивление цепи из закона Ома для полной цепи', 'внешнее сопротивление цепи из закона Ома для полной цепи'])
@variant.arg(v_4=[
    'эквивалентное сопротивление $n$ резисторов, соединённых последовательно, каждый сопротивлением $R$',
    'эквивалентное сопротивление $n$ резисторов, соединённых параллельно, каждый сопротивлением $R$',
])
class Definitions07(variant.VariantTask):
    pass


@variant.solution_space(20)
@variant.text('''
    На резистор сопротивлением {R:V:e} подали напряжение {U:V:e}.
    Определите ток, который потечёт через резистор, ответ выразите в амперах.
''')
@variant.answer_test('{I.Value}')
@variant.answer_short('{I:L} = \\frac{U:L:s}{R:L:s} = \\frac{U:Value:s}{R:Value:s} = {I:Value}')
@variant.arg(R=('R = {} Ом', [3, 5, 10, 15, 20, 30]))
@variant.arg(U=('U = {} В', [120, 180, 240]))
class I_from_U_R(variant.VariantTask):
    def GetUpdate(self, R=None, U=None):
        return dict(
            I=(U / R).SetLetter('\\eli'),
        )


@variant.solution_space(20)
@variant.text('''
    Женя собирает электрическую цепь из {N:V:e} одинаковых резисторов, каждый сопротивлением {R:V:e}.
    Какое эквивалентное сопротивление этой цепи получится, если все резисторы подключены {how}, ответ выразите в омах.
''')
@variant.answer_test('{r.Value}')
@variant.answer_short('{r:Task}')
@variant.arg(R='R = 160/240/320 Ом')
@variant.arg(N='N = 10/20/40')
@variant.arg(how=['параллельно', 'последовательно'])
class r_from_R_N(variant.VariantTask):
    def GetUpdate(self, R=None, N=None, how=None):
        r = {
            'параллельно': R / N,
            'последовательно': R * N,
        }[how]
        return dict(
            r=r.SetLetter('r'),
        )

@variant.solution_space(20)
@variant.text('''
    Два резистора сопротивлениями {R1:Task:e} и {R2:Task:e} подключены {how} и на них подано напряжение.
    Определите, какое напряжение них подали, если в цепи идёт {I:Task:e}. Ответ выразите в вольтах и округлите до целого.
''')
@variant.answer_test('{U.Value}')
@variant.answer_short('{U:Task}')
@variant.arg(R1=('R_1 = {} кОм', [4, 10, 15]))
@variant.arg(R2=('R_2 = {} кОм', [2, 6, 12, 20]))
@variant.arg(I=('\\eli = {} мА', [2, 3, 5]))
@variant.arg(how=['параллельно', 'последовательно'])
class U_from_R1_R2_I(variant.VariantTask):
    def GetUpdate(self, R1=None, R2=None, I=None, how=None):
        answer = {
            'параллельно': (R1.Value * R2.Value) / (R1.Value + R2.Value) * I.Value,
            'последовательно': (R1.Value + R2.Value) * I.Value,
        }[how]
        return dict(
            U='U = %d В' % int(answer + Decimal('0.5')),
        )


@variant.solution_space(40)
@variant.text('''
    Валя проводит эксперименты c 2 кусками одинаковой {which} проволки, причём второй кусок в {a} длиннее первого.
    В одном из экспериментов Валя подаёт на первый кусок проволки напряжение в {b} раз больше, чем на второй.
    Определите отношение сил тока в двух проволках в этом эксперименте: второй к первой.
    В ответе укажите простую дробь или целое число.
''')
@variant.answer_test('{ratio:Basic}')
@variant.answer_short('{ratio:LaTeX}')
@variant.arg(a=[2, 3, 4, 5, 6, 7, 8, 9, 10])
@variant.arg(b=[2, 3, 4, 5, 6, 7, 8, 9, 10])
@variant.arg(which=['медной', 'стальной', 'алюминиевой'])
class I_ratio(variant.VariantTask):
    def GetUpdate(self, a=None, b=None, which=None):
        return dict(
            ratio=Fraction(1) / b / a,
        )


@variant.solution_space(40)
@variant.text('''
    Юлия проводит эксперименты c 2 кусками одинаковой {which} проволки, причём второй кусок в {times_a} длиннее первого.
    В одном из экспериментов Юлия подаёт на первый кусок проволки напряжение в {times_b} раз больше, чем на второй.
    Определите отношения в двух проволках в этом эксперименте (второй к первой):
    \\begin{itemize}
        \\item отношение сил тока,
        \\item отношение выделяющихся мощностей.
    \\end{itemize}
''')
# @variant.answer_test('{ratio:Basic}')
@variant.answer_short(
    'R_2 = {a}R_1, U_1 = {b}U_2 \\implies '
    ' \\eli_2 / \\eli_1 = \\frac{U_2 / R_2}{U_1 / R_1} = \\frac{U_2}{U_1} * \\frac{R_1}{R_2} = {ratio_i:LaTeX},'
    ' P_2 / P_1 = \\frac{U_2^2 / R_2}{U_1^2 / R_1} = \\sqr{\\frac{U_2}{U_1}} * \\frac{R_1}{R_2} = {ratio_P:LaTeX}.')
@variant.arg(a__times_a=n_times(2, 3, 4, 5, 6, 7, 8, 9, 10))
@variant.arg(b__times_b=n_times(2, 3, 4, 5, 6, 7, 8, 9, 10))
@variant.arg(which=['медной', 'стальной', 'алюминиевой'])
class P_ratio(variant.VariantTask):
    def GetUpdate(self, a=None, times_a=None, b=None, times_b=None, which=None):
        return dict(
            ratio_i=Fraction(1) / b / a,
            ratio_P=Fraction(1) / b / b / a,
        )


@variant.solution_space(20)
@variant.text('''
    В распоряжении Маши имеется {N} одинаковых резисторов, каждый сопротивлением {R:V:e}.
    Какое {which} эквивалентное сопротивление она может из них получить? Использовать все резисторы при этом не обязательно, ответ укажите в омах.
''')
@variant.answer_test('{r.Value}')
@variant.answer_short('{r:Task}')
@variant.arg(R=('R = {} кОм', [2, 3, 4]))
@variant.arg(N=[10, 20, 40])
@variant.arg(which=['наименьшее', 'наибольшее'])
class R_best_from_R_N(variant.VariantTask):
    def GetUpdate(self, R=None, N=None, which=None):
        answer = {
            'наименьшее': R.Value * 1000 / N,
            'наибольшее': R.Value * 1000 * N,
        }[which]
        return dict(
            r='r = %d Ом' % answer,
        )


@variant.solution_space(60)
@variant.text('''
    На резистор сопротивлением {R:Task:e} подали напряжение {U:Task:e}.
    Определите ток, который потечёт через резистор, и мощность, выделяющуюся на нём.
''')
@variant.answer_align([
    '{I:L} &= \\frac{U:L:s}{R:L:s} = \\frac{U:Value:s}{R:Value:s} = {I:Value}, ',
    '{P:L} &= \\frac{{U:L}^2}{R:L:s} = \\frac{U:Value|sqr|s}{R:Value:s} = {P:Value}',
])
@variant.arg(R=['%s = %d Ом' % (rLetter, rValue) for rLetter, rValue in itertools.product(['r', 'R'], [5, 12, 18, 30])])
@variant.arg(U=['%s = %d В' % (uLetter, uValue) for uLetter, uValue in itertools.product(['U', 'V'], [120, 150, 180, 240])])
class P_from_R_U(variant.VariantTask):
    def GetUpdate(self, R=None, U=None):
        return dict(
            I='\\eli = %.2f А' % (U.Value / R.Value),
            P='P = %.2f Вт' % (U.Value ** 2 / R.Value),
        )


@variant.solution_space(60)
@variant.text('''
    Через резистор сопротивлением {R:Task:e} протекает электрический ток {I:Task:e}.
    Определите, чему равны напряжение на резисторе и мощность, выделяющаяся на нём.
''')
@variant.answer_align([
    '{U:L} &= {I:L} {R:L} = {I:Value} * {R:Value} = {U:Value}, ',
    '{P:L} &= {I:L}^2{R:L} = {I:Value|sqr} * {R:Value} = {P:Value}',
])
@variant.arg(R=['%s = %d Ом' % (rLetter, rValue) for rLetter, rValue in itertools.product(['r', 'R'], [5, 12, 18, 30])])
@variant.arg(I=['\\eli = %.2f А' % iValue for iValue in [2, 3, 4, 5, 6, 8, 10, 15]])
class P_from_R_I(variant.VariantTask):
    def GetUpdate(self, R=None, I=None, U=None):
        return dict(
            U='U = %d В' % (I.Value * R.Value),
            P='P = %d Вт' % (I.Value ** 2 * R.Value),
        )


@variant.text('''
    Два резистора сопротивлениями $R_1={a}R$ и $R_2={b}R$ подключены {how} к источнику напряжения.
    Определите, в каком резисторе выделяется большая тепловая мощность и во сколько раз?
''')
@variant.arg(a=[3, 5, 7])
@variant.arg(b=[2, 4, 6, 8])
@variant.arg(how=['параллельно', 'последовательно'])
@variant.answer('Подключены {how}, поэтому  ${equals1} \\implies \\frac{P_2}{P_1} = {equals2} = {ratio:LaTeX}$.')
class Compare_power(variant.VariantTask):  # Вишнякова - 17
    def GetUpdate(self, a=None, b=None, how=None):
        if how == 'параллельно':
            equals1 = 'U_1 = U_2 = U'
            equals2 = '\\frac{\\frac{U_2^2}{R_2}}{\\frac{U_1^2}{R_1}} = \\frac{U^2R_1}{U^2R_2} = \\frac{R_1}{R_2}'
            ratio = Fraction(numerator=a, denominator=b)
        elif how == 'последовательно':
            equals1 = '\\eli_1 = \\eli_2 = \\eli'
            equals2 = '\\frac{\\eli_2^2 R_2}{\\eli_1^2 R_1} = \\frac{\\eli_2^2R_2}{\\eli_1R_1} = \\frac{R_2}{R_1}'
            ratio = Fraction(numerator=b, denominator=a)

        return dict(
            equals1=equals1,
            equals2=equals2,
            ratio=ratio,
        )


@variant.text('''
    Определите эквивалентное сопротивление цепи на рисунке (между выделенными на рисунке контактами),
    если известны сопротивления всех резисторов: {R1:Task:e}, {R2:Task:e}, {R3:Task:e}, {R4:Task:e}.
    При каком напряжении поданном на эту цепь, в ней потечёт ток равный {I:Task:e}?

    \\begin{tikzpicture}[rotate={rotate}, circuit ee IEC, thick]
        \\node [contact]  (contact1) at (-1.5, 0) {};
        \\draw  (0, 0) to [resistor={info=$R_1$}] ++(left:1.5);
        \\draw  (0, 0) -- ++(up:1.5) to [resistor={near start, info=$R_2$}, resistor={near end, info=$R_3$}] ++(right:3);
        \\draw  (0, 0) to [resistor={info=$R_4$}] ++(right:3) -- ++(up:1.5);
        {appendix}
    \\end{tikzpicture}
''')
@variant.arg(rotate=[0, 90, 180, 270])
@variant.arg(second_node=[0, 1])
@variant.arg(R1=('R_1 = {} Ом', [1, 2]))
@variant.arg(R2=('R_2 = {} Ом', [3, 4, 5]))
@variant.arg(R3=('R_3 = {} Ом', [1, 2, 3]))
@variant.arg(R4=('R_4 = {} Ом', [2, 3, 4]))
@variant.arg(I=('\\eli = {} А', [2, 5, 10]))
@variant.answer_short('R={R_ratio:LaTeX}\\units{Ом} \\approx {R:V} \\implies U = \\eli R \\approx {U:V}.')
class Circuit_four(variant.VariantTask):
    def GetUpdate(self, rotate=None, second_node=None, R1=None, R2=None, R3=None, R4=None, I=None):
        if second_node == 0:
            appendix = '\\draw  (3, 1.5) -- ++(right:0.5); \\node [contact] (contact2) at (3.5, 1.5) {};'
            R_ratio = (R2.frac_value + R3.frac_value) * R4.frac_value / (R2.frac_value + R3.frac_value + R4.frac_value) + R1.frac_value
        elif second_node == 1:
            appendix = '\\draw  (1.5, 1.5) -- ++(up:1); \\node [contact] (contact2) at (1.5, 2.5) {};'
            R_ratio = R2.frac_value * (R3.frac_value + R4.frac_value) / (R2.frac_value + R3.frac_value + R4.frac_value) + R1.frac_value
        return dict(
            appendix=appendix,
            R_ratio=R_ratio,
            R='R = %.2f Ом' % float(R_ratio),
            U='U = %.1f В' % (I.frac_value * R_ratio),
        )


@variant.text('''
    Определите показания амперметра ${index_a}$ (см. рис.) и разность потенциалов на резисторе ${index_r}$,
    если сопротивления всех резисторов равны: $R_1 = R_2 = R_3 = R_4 = R_5 = R_6 = {R:Task}$,
    а напряжение, поданное на цепь, равно {U:Task:e}.
    Ответы получите в виде несократимых дробей, а также определите приближённые значения. Амперметры считать идеальными.

    \\begin{tikzpicture}[circuit ee IEC, thick]
        \\node [contact]  (left contact) at (3, 0) {};
        \\node [contact]  (right contact) at (9, 0) {};
        \\draw  (left contact) -- ++(up:2) to [resistor={very near start, info=$R_2$}, amperemeter={midway, info=$1$}, resistor={very near end, info=$R_3$} ] ++(right:6) -- (right contact);
        \\draw  (left contact) -- ++(down:2) to [resistor={very near start, info=$R_5$}, resistor={midway, info=$R_6$}, amperemeter={very near end, info=$3$}] ++(right:6) -- (right contact);
        \\draw  (left contact) ++(left:3) to [resistor={info=$R_1$}] (left contact) to [amperemeter={near start, info=$2$}, resistor={near end , info=$R_4$}] (right contact) -- ++(right:0.5);
    \\end{tikzpicture}

''')
@variant.arg(index_a=[1, 2, 3])
@variant.arg(index_r=[1, 2, 3, 4, 5, 6])
@variant.arg(R=('R = {} Ом', [2, 4, 5, 10]))
@variant.arg(U=('U = {} В', [30, 60, 90, 120, 150]))
@variant.answer_align([
    'R_0 &= R + \\frac 1{\\frac 1{R+R} + \\frac 1{R:L} + \\frac 1{R+R}} = R + \\frac 1{\\frac 2R} = \\frac 32 R,',
    '\\eli &= \\frac U{R_0} = \\frac {2U}{3R},',
    'U_1 &= \\eli R_1 = \\frac {2U}{3R} * R = \\frac 23 U = {U1:Value},',
    'U_{23} &= U_{56} = U_4 = U - \\eli R_1 = U - \\frac {2U}{3R} * R = \\frac U3 = {U4:Value},',
    '\\eli_2 &= \\frac{U_4}{R_4} = \\frac U{3R} \\approx {I2:Value},',
    '\\eli_1 &= \\frac{U_{23}}{R_{23}} = \\frac{\\frac U3}{R+R} = \\frac U{6R} \\approx {I1:Value},',
    '\\eli_3 &= \\frac{U_{56}}{R_{56}} = \\frac{\\frac U3}{R+R} = \\frac U{6R} \\approx {I3:Value},',
    'U_2 &= \\eli_1 R_2 = \\frac U{6R} * R = \\frac U6 = {U2:Value},',
    'U_3 &= \\eli_1 R_3 = \\frac U{6R} * R = \\frac U3 = {U3:Value},',
    'U_5 &= \\eli_3 R_5 = \\frac U{6R} * R = \\frac U5 = {U5:Value},',
    'U_6 &= \\eli_3 R_6 = \\frac U{6R} * R = \\frac U6 = {U6:Value}.',
])
class Circuit_six(variant.VariantTask):
    def GetUpdate(self, R=None, U=None, index_a=None, index_r=None):
        U1 = 2 * U.frac_value / 3
        U2 = U.frac_value / 6
        U3 = U.frac_value / 6
        U4 = U.frac_value / 3
        U5 = U.frac_value / 6
        U6 = U.frac_value / 6
        I1 = U.frac_value / (6 * R.frac_value)
        I2 = U.frac_value / (3 * R.frac_value)
        I3 = U.frac_value / (6 * R.frac_value)
        return dict(
            U1='U_1 = %.1f В' % float(U1),
            U2='U_2 = %.1f В' % float(U2),
            U3='U_3 = %.1f В' % float(U3),
            U4='U_4 = %.1f В' % float(U4),
            U5='U_5 = %.1f В' % float(U5),
            U6='U_6 = %.1f В' % float(U6),
            I1='\\eli_1 = %.1f А' % float(I1),
            I2='\\eli_2 = %.1f А' % float(I2),
            I3='\\eli_3 = %.1f А' % float(I3),
        )
