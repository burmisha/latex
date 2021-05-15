import itertools

import generators.variant as variant
from generators.helpers import UnitValue, letter_variants, Fraction

from library.logging import colorize_json

import logging
log = logging.getLogger(__name__)


@variant.solution_space(20)
@variant.text('''
    Установите каждой букве в соответствие ровно одну цифру и запишите ответ (только цифры, без других символов).

    {lv.Questions}.

    {lv.Options}.
''')
@variant.answer_test('{lv.Answer}')
@variant.arg(lv=letter_variants(
    {
        'разность потенциалов': '$U$',
        'электрическое сопротивление резистора': '$R$',
        'удельное сопротивление проводника': '$\\rho$',
        'сила тока': '$\\mathcal{I}$',
        'длина проводника': '$l$',
        'площадь поперечного сечения проводника': '$S$',
    },
    ['$D$', '$k$', '$\\lambda$'],
    answers_count=3,
    mocks_count=2,
))
@variant.answer_short('{lv.Answer}')
class Definitions01(variant.VariantTask):
    pass


@variant.solution_space(20)
@variant.text('''
    Установите каждой букве в соответствие ровно одну цифру и запишите ответ (только цифры, без других символов).

    {lv.Questions}.

    {lv.Options}.
''')
@variant.answer_test('{lv.Answer}')
@variant.arg(lv=letter_variants(
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
))
@variant.answer_short('{lv.Answer}')
class Definitions02(variant.VariantTask):
    pass


@variant.solution_space(20)
@variant.text('''
    Установите каждой букве в соответствие ровно одну цифру и запишите ответ (только цифры, без других символов).

    {lv.Questions}.

    {lv.Options}.
''')
@variant.answer_test('{lv.Answer}')
@variant.arg(lv=letter_variants(
    {

        'закон Ома': '$\\mathcal{I} R = U$',
        'электрическое сопротивление резистора': '$R = \\rho \\frac lS$',
        'эквивалентное сопротивление 2 резисторов (параллельно)': '$\\frac{R_1R_2}{R_1 + R_2}$',
        'эквивалентное сопротивление 2 резисторов (последовательно)': '$R_1 + R_2$',
    },
    ['$\\frac{2R_1R_2}{R_1 + R_2}$', '$\\frac{R_1 + R_2} 2$', '$\\sqrt{R_1R_2}$', '$\\rho = R l S$', '$R = \\rho \\frac Sl$', '$\\frac{\\mathcal{I}} R = U$' ],
    answers_count=2,
    mocks_count=3,
))
@variant.answer_short('{lv.Answer}')
class Definitions03(variant.VariantTask):
    pass


@variant.solution_space(20)
@variant.text('''
    Установите каждой букве в соответствие ровно одну цифру и запишите ответ (только цифры, без других символов).

    {lv.Questions}.

    {lv.Options}.
''')
@variant.answer_test('{lv.Answer}')
@variant.arg(lv=letter_variants(
    {

        'эквивалентное сопротивление 3 резисторов (параллельно)': '$\\frac{R_1R_2R_3}{R_1R_2 + R_2R_3 + R_3R_1}$',
        'эквивалентное сопротивление 3 резисторов (последовательно)': '$R_1 + R_2 + R_3$',
    },
    ['$\\frac{R_1R_2R_3}{R_1 + R_2 + R_3}$', '$\\frac{R_1 + R_2 + R_3}3$', '$\\frac 3{\\frac 1{R_1} + \\frac 1{R_2} + \\frac 1{R_3}}$', '$\\sqrt{\\frac{R_1^2 + R_2^2 + R_3^2}3}$',],
    answers_count=2,
    mocks_count=3,
))
@variant.answer_short('{lv.Answer}')
class Definitions04(variant.VariantTask):
    pass


@variant.solution_space(20)
@variant.text('''
    Напротив физических величин укажите их обозначения и единицы измерения в СИ:
    \\begin{{enumerate}}
        \\item {v_1},
        \\item {v_2},
        \\item {v_3},
        \\item {v_4}.
    \\end{{enumerate}}
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
    \\begin{{enumerate}}
        \\item {v_1},
        \\item {v_2},
        \\item {v_3}.
    \\end{{enumerate}}
''')
@variant.arg(v_1=['правило Кирхгофа для замкнутого контура', 'правило Кирхгофа для узла цепи'])
@variant.arg(v_2=['закон Ома для однородного участка цепи', 'сопротивление резистора через удельное сопротивление'])
@variant.arg(v_3=['закон Ома для неоднородного участка цепи', 'ЭДС (определение)'])
class Definitions06(variant.VariantTask):
    pass


@variant.solution_space(80)
@variant.text('''
    Получите выражение:
    \\begin{{enumerate}}
        \\item {v_1},
        \\item {v_2},
        \\item {v_3},
        \\item {v_4}.
    \\end{{enumerate}}
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
    \\begin{{enumerate}}
        \\item {v_1},
        \\item {v_2},
        \\item {v_3},
        \\item {v_4}.
    \\end{{enumerate}}
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
    def GetUpdate(self, R=None, U=None, **kws):
        return dict(
            I='\\eli = %d А' % (U.Value / R.Value),
        )


@variant.solution_space(20)
@variant.text('''
    Женя собирает электрическую цепь из {N:V:e} одинаковых резисторов, каждый сопротивлением {R:V:e}.
    Какое эквивалентное сопротивление этой цепи получится, если все резисторы подключены {how}, ответ выразите в омах.
''')
@variant.answer_test('{r.Value}')
@variant.answer_short('{r:Task}')
@variant.arg(R=('R = {} Ом', [160, 240, 320]))
@variant.arg(N=('N = {}', [10, 20, 40]))
@variant.arg(how=['параллельно', 'последовательно'])
class r_from_R_N(variant.VariantTask):
    def GetUpdate(self, R=None, N=None, how=None, **kws):
        answer = {
            'параллельно': R.Value / N.Value,
            'последовательно': R.Value * N.Value,
        }[how]
        return dict(
            r='r = %d Ом' % answer,
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
    def GetUpdate(self, R1=None, R2=None, I=None, how=None, **kws):
        answer = {
            'параллельно': 1. * (R1.Value * R2.Value) / (R1.Value + R2.Value) * I.Value,
            'последовательно': 1. * (R1.Value + R2.Value) * I.Value,
        }[how]
        return dict(
            U='U = %d В' % int(answer + 0.5),
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
    def GetUpdate(self, a=None, b=None, **kws):
        return dict(
            ratio=Fraction() / b / a,
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
    def GetUpdate(self, R=None, N=None, which=None, **kws):
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
    '{P:L} &= \\frac{ {U:L}^2 }{R:L:s} = \\frac{U:Value|sqr|s}{R:Value:s} = {P:Value}',
])
@variant.arg(R=['%s = %d Ом' % (rLetter, rValue) for rLetter, rValue in itertools.product(['r', 'R'], [5, 12, 18, 30])])
@variant.arg(U=['%s = %d В' % (uLetter, uValue) for uLetter, uValue in itertools.product(['U', 'V'], [120, 150, 180, 240])])
class P_from_R_U(variant.VariantTask):
    def GetUpdate(self, R=None, U=None, **kws):
        return dict(
            I='\\eli = %.2f А' % (1. * U.Value / R.Value),
            P='P = %.2f Вт' % (1. * U.Value ** 2 / R.Value),
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
    def GetUpdate(self, R=None, I=None, U=None, **kws):
        return dict(
            U='U = %d В' % (I.Value * R.Value),
            P='P = %d Вт' % (I.Value ** 2 * R.Value),
        )


@variant.solution_space(180)
@variant.text('''
    Замкнутая электрическая цепь состоит из ЭДС {E:Task:e} и сопротивлением ${r:L}$
    и резистора {R:Task:e}. Определите ток, протекающий в цепи. Какая тепловая энергия выделится на резисторе за время
    {t:Task:e}? Какая работа будет совершена ЭДС за это время? Каков знак этой работы? Чему равен КПД цепи?
    Вычислите значения для 2 случаев: ${r:L}=0$ и {r:Task:e}.
''')
@variant.answer_align([
    '''{I1:L} &= \\frac{E:L:s}{R:L:s} = \\frac{E:Value:s}{R:Value:s} = {I1_ratio:LaTeX}\\units{ А } \\approx {I1:Value}, ''',
    '''{I2:L} &= \\frac{E:L:s}{ {R:L} + {r:L} } = \\frac{E:Value:s}{ {R:Value} + {r:Value} } = {I2_ratio:LaTeX}\\units{ А } \\approx {I2:Value}, ''',
    '''{Q1:L} &= {I1:L}^2{R:L}{t:L} = \\sqr{ \\frac{E:L:s}{R:L:s} } {R:L} {t:L}
        = \\sqr{ \\frac{E:Value:s}{R:Value:s} } * {R:Value} * {t:Value} = {Q1_ratio:LaTeX}\\units{ Дж } \\approx {Q1:Value}, ''',
    '''{Q2:L} &= {I2:L}^2{R:L}{t:L} = \\sqr{ \\frac{E:L:s}{ {R:L} + {r:L} } } {R:L} {t:L}
        = \\sqr{ \\frac{E:Value:s}{ {R:Value} + {r:Value} } } * {R:Value} * {t:Value} = {Q2_ratio:LaTeX}\\units{ Дж } \\approx {Q2:Value}, ''',
    '''{A1:L} &= q_1{E:L} = {I1:L}{t:L}{E:L} = \\frac{E:L:s}{R:L:s} {t:L} {E:L}
        = \\frac{ {E:L}^2 {t:L} }{R:L|s} = \\frac{ {E:Value|sqr} * {t:Value} }{R:Value:s}
        = {A1_ratio:LaTeX}\\units{ Дж } \\approx {A1:Value}, \\text{ положительна }, ''',
    '''{A2:L} &= q_2{E:L} = {I2:L}{t:L}{E:L} = \\frac{E:L:s}{ {R:L} + {r:L} } {t:L} {E:L}
        = \\frac{ {E:L}^2 {t:L} }{ {R:L} + {r:L} } = \\frac{ {E:Value|sqr} * {t:Value} }{ {R:Value} + {r:Value} }
        = {A2_ratio:LaTeX}\\units{ Дж } \\approx {A2:Value}, \\text{ положительна }, ''',
    '''{eta1:L} &= \\frac{Q1:L:s}{A1:L:s} = \\ldots = \\frac{R:L:s}{R:L:s} = {eta1:Value}, ''',
    '''{eta2:L} &= \\frac{Q2:L:s}{A2:L:s} = \\ldots = \\frac{R:L:s}{ {R:L} + {r:L} } = {eta_2_ratio:LaTeX} \\approx {eta2:Value}.''',
])
@variant.arg(E=['\\ele = %d В' % E for E in [1, 2, 3, 4]])
@variant.arg(R=['R = %d Ом' % R for R in [10, 15, 24, 30]])
@variant.arg(r=['r = %d Ом' % r for r in [10, 20, 30, 60]])
@variant.arg(t=['\\tau = %d с' % t for t in [2, 5, 10]])
class Om_eta_full(variant.VariantTask):
    def GetUpdate(self, r=None, R=None, E=None, t=None, **kws):
        I1_ratio = Fraction(numerator=E.Value, denominator=R.Value)
        I2_ratio = Fraction(numerator=E.Value, denominator=R.Value + r.Value)
        eta_2_ratio = Fraction(numerator=R.Value, denominator=R.Value + r.Value)
        Q1_ratio = I1_ratio * I1_ratio * R.Value * t.Value
        Q2_ratio = I2_ratio * I2_ratio * R.Value * t.Value
        A1_ratio = I1_ratio * E.Value * t.Value
        A2_ratio = I2_ratio * E.Value * t.Value
        return dict(
            I1_ratio=I1_ratio,
            I2_ratio=I2_ratio,
            I1='\\eli_1 = %.2f А' % float(I1_ratio),
            I2='\\eli_2 = %.2f А' % float(I2_ratio),
            Q1_ratio=Q1_ratio,
            Q2_ratio=Q2_ratio,
            A1_ratio=A1_ratio,
            A2_ratio=A2_ratio,
            Q1='Q_1 = %.3f Дж' % float(Q1_ratio),
            Q2='Q_2 = %.3f Дж' % float(Q2_ratio),
            A1='A_1 = %.3f Дж' % float(A1_ratio),
            A2='A_2 = %.3f Дж' % float(A2_ratio),
            eta_2_ratio=eta_2_ratio,
            eta1='\\eta_1 = 1',
            eta2='\\eta_2 = %.2f' % float(eta_2_ratio),
        )


@variant.text('''
    Лампочки, сопротивления которых {R1:Task:e} и {R2:Task:e}, поочерёдно подключённные к некоторому источнику тока,
    потребляют одинаковую мощность. Найти внутреннее сопротивление источника и КПД цепи в каждом случае.
''')
@variant.answer_align([
    '''
    P_1 &= \\sqr{ \\frac{E:L:s}{ {R1:L} + {r:L} } }{R1:L},
    P_2  = \\sqr{ \\frac{E:L:s}{ {R2:L} + {r:L} } }{R2:L},
    P_1 = P_2 \\implies ''',
    '''
    &\\implies {R1:L} \\sqr{ {R2:L} + {r:L} } = {R2:L} \\sqr{ {R1:L} + {r:L} } \\implies ''',
    '''
    &\\implies {R1:L} {R2:L}^2 + 2 {R1:L} {R2:L} {r:L} + {R1:L} {r:L}^2 =
                {R2:L} {R1:L}^2 + 2 {R2:L} {R1:L} {r:L} + {R2:L} {r:L}^2  \\implies ''',
    '''&\\implies {r:L}^2 ({R2:L} - {R1:L}) = {R2:L}^2 {R2:L} - {R1:L}^2 {R2:L} \\implies ''',
    '''&\\implies {r:L}
        = \\sqrt{ {R1:L} {R2:L} \\frac{ {R2:L} - {R1:L} }{ {R2:L} - {R1:L} } }
        = \\sqrt{ {R1:L} {R2:L} }
        = \\sqrt{ {R1:Value} * {R2:Value} }
        = {r:Value}. '''
   ,
   '''{eta1:L}
        &= \\frac{R1:L:s}{ {R1:L} + {r:L} }
        = \\frac{ {R1:L|sqrt} }{ {R1:L|sqrt} + {R2:L|sqrt} }
        = {eta1:Value}, '''
   ,
   '''{eta2:L}
        &= \\frac{R2:L:s}{ {R2:L} + {r:L} }
        = \\frac{R2:L|sqrt|s}{ {R2:L|sqrt} + {R1:L|sqrt} }
        = {eta2:Value}''',
])
@variant.arg(R1__R2=[('R_1 = %.2f Ом' % R_1, 'R_2 = %.2f Ом' % R_2) for R_1, R_2 in [
    (0.25, 16), (0.25, 64), (0.25, 4),
    (0.5, 18),  (0.5, 2),   (0.5, 4.5),
    (1, 4),     (1, 9),     (1, 49),
    (3, 12),    (3, 48),
    (4, 36),    (4, 100),
    (5, 45),    (5, 80),
    (6, 24),    (6, 54),
]])
class r_eta_from_Rs(variant.VariantTask):
    def GetUpdate(self, R1=None, R2=None, **kws):
        r = UnitValue('r = %.1f Ом' % ((1. * R1.Value * R2.Value) ** 0.5))
        return dict(
            R1=R1,
            R2=R2,
            r=r,
            eta1='\\eta_1 = %.3f ' % (1. * R1.Value / (R1.Value + r.Value)),
            eta2='\\eta_2 = %.3f ' % (1. * R2.Value / (R2.Value + r.Value)),
            E='\\ele = 1 В',
        )


@variant.text('''
    Определите ток, протекающий через резистор {R:Task:e} и разность потенциалов на нём (см. рис. на доске),
    если {r1:Task:e}, {r2:Task:e}, {E1:Task:e}, {E2:Task:e}.
''')
@variant.arg(R=['R = %d Ом' % RValue for RValue in [10, 12, 15, 18, 20]])
@variant.arg(r1=['r_1 = %d Ом' % r1Value for r1Value in [1, 2, 3]])
@variant.arg(r2=['r_2 = %d Ом' % r2Value for r2Value in [1, 2, 3]])
@variant.arg(E1=['\\ele_1 = %d В' % E1Value for E1Value in [20, 30, 40, 60]])
@variant.arg(E2=['\\ele_2 = %d В' % E2Value for E2Value in [20, 30, 40, 60]])
@variant.answer_tex('''
    Обозначим на рисунке все токи: направление произвольно, но его надо зафиксировать. Всего на рисунке 3 контура и 2 узла.
    Поэтому можно записать $3 - 1 = 2$ уравнения законов Кирхгофа для замкнутого контура и $2 - 1 = 1$ — для узлов
    (остальные уравнения тоже можно записать, но они не дадут полезной информации, а будут лишь следствиями уже записанных).

    Отметим на рисунке 2 контура (и не забуем указать направление) и 1 узел (точка «1»ы, выделена жирным). Выбор контуров и узлов не критичен: получившаяся система может быть чуть проще или сложнее, но не слишком.

    \\begin{ tikzpicture }[circuit ee IEC, thick]
        \\draw  (0, 0) to [current direction={ near end, info=$\\eli_1$ }] (0, 3)
                to [battery={ rotate=-180,info={ $\\ele_1, r_1 $ } }]
                (3, 3)
                to [battery={ info'={ $\\ele_2, r_2 $ } }]
                (6, 3) to [current direction'={ near start, info=$\\eli_2$ }] (6, 0) -- (0, 0)
                (3, 0) to [current direction={ near start, info=$\\eli$ }, resistor={ near end, info=$R$ }] (3, 3);
        \\draw [-{ Latex },color=red] (1.2, 1.7) arc [start angle = 135, end angle = -160, radius = 0.6];
        \\draw [-{ Latex },color=blue] (4.2, 1.7) arc [start angle = 135, end angle = -160, radius = 0.6];
        \\node [contact,color=green!71!black] (bottomc) at (3, 0) {  };
        \\node [below] (bottom) at (3, 0) { $2$ };
        \\node [above] (top) at (3, 3) { $1$ };
    \\end{ tikzpicture }

    \\begin{ align* }
        &\\begin{ cases }
            { \\color{ red } \\ele_1 = \\eli_1 r_1 - \\eli R }, \\\\
            { \\color{ blue } -\\ele_2 = -\\eli_2 r_2 + \\eli R }, \\\\
            { \\color{ green!71!black } - \\eli - \\eli_1 - \\eli_2 = 0 };
        \\end{ cases }
        \\qquad \\implies \\qquad
        \\begin{ cases }
            \\eli_1 = \\frac{ \\ele_1 + \\eli R }{ r_1 }, \\\\
            \\eli_2 = \\frac{ \\ele_2 + \\eli R }{ r_2 }, \\\\
            \\eli + \\eli_1 + \\eli_2 = 0;
        \\end{ cases } \\implies \\\\
        &\\implies
         \\eli + \\frac{ \\ele_1 + \\eli R }{ r_1 } + \\frac{ \\ele_2 + \\eli R }{ r_2 } = 0, \\\\
        &\\eli\\cbr{ 1 + \\frac{ R }{ r_1 } + \\frac{ R }{ r_2 } } + \\frac{ \\ele_1 }{ r_1 } + \\frac{ \\ele_2 }{ r_2 } = 0, \\\\
        &\\eli
            = - \\frac{ \\frac{ \\ele_1 }{ r_1 } + \\frac{ \\ele_2 }{ r_2 } }{ 1 + \\frac{ R }{ r_1 } + \\frac{ R }{ r_2 } }
            = - \\frac{ \\frac{E1:V|s}{r1:V|s} + \\frac{E2:V|s}{r2:V|s} }{ 1 + \\frac{R:V|s}{r1:V|s} + \\frac{R:V|s}{r2:V|s} }
            = - {I_ratio:LaTeX}\\units{ А }
            \\approx {I:Value}, \\\\
        &U  = \\varphi_2 - \\varphi_1 = \\eli R
            = - \\frac{ \\frac{ \\ele_1 }{ r_1 } + \\frac{ \\ele_2 }{ r_2 } }{ 1 + \\frac{ R }{ r_1 } + \\frac{ R }{ r_2 } } R
            \\approx {U:Value}.
    \\end{ align* }
    Оба ответа отрицательны, потому что мы изначально «не угадали» с направлением тока. Расчёт же показал,
    что ток через резистор $R$ течёт в противоположную сторону: вниз на рисунке, а потенциал точки 1 больше потенциала точки 2,
    а электрический ток ожидаемо течёт из точки с большим потенциалов в точку с меньшим.

    Кстати, если продолжить расчёт и вычислить значения ещё двух токов (формулы для $\\eli_1$ и $\\eli_2$, куда подставлять, выписаны выше),
    то по их знакам можно будет понять: угадали ли мы с их направлением или нет.
'''
)
class Kirchgof_double(variant.VariantTask):
    def GetUpdate(self, R=None, r1=None, r2=None, E1=None, E2=None, **kws):
        I_ratio = (
            Fraction(numerator=E1.Value, denominator=r1.Value) + Fraction(numerator=E2.Value, denominator=r2.Value)
        ) / (
            Fraction(base_value=1) + Fraction(numerator=R.Value, denominator=r1.Value) + Fraction(numerator=R.Value, denominator=r2.Value)
        )

        I = '\\eli = -%.1f А' % float(I_ratio)
        U = 'U = -%.1f В' % float(I_ratio * R.Value)
        return dict(
            I_ratio=I_ratio,
            I=I,
            U=U,
        )


@variant.text('''
    Определите ток, протекающий через резистор $R_{index}$, разность потенциалов на нём (см. рис.)
    и выделяющуюся на нём мощность, если известны $r_1, r_2, \\ele_1, \\ele_2, R_1, R_2$.

    \\begin{ tikzpicture }[circuit ee IEC, thick]
        \\draw  (0, 0) -- ++(up:2)
                to [
                    battery={ very near start, rotate={rotate1}, info={ $\\ele_1, r_1 $ } },
                    resistor={ midway, info=$R_1$ },
                    battery={ very near end, rotate={rotate2}, info={ $\\ele_2, r_2 $ } }
                ] ++(right:5)
                -- ++(down:2)
                to [resistor={ info=$R_2$ }] ++(left:5);
    \\end{ tikzpicture }
''')
@variant.arg(index=[1, 2])
@variant.arg(rotate1=[0, -180])
@variant.arg(rotate2=[0, -180])
@variant.answer_tex('''
    Нетривиальных узлов нет, поэтому все законы Кирхгофа для узлов будут иметь вид
    $\\eli-\\eli=0$ и ничем нам не помогут. Впрочем, если бы мы обозначили токи на разных участках контура $\\eli_1, \\eli_2, \\eli_3, \\ldots$,
    то именно эти законы бы помогли понять, что все эти токи равны: $\\eli_1 - \\eli_2 = 0$ и т.д.
    Так что запишем закон Кирхгофа для единственного замкнутого контура:

    \\begin{ tikzpicture }[circuit ee IEC, thick]
        \\draw  (0, 0) -- ++(up:2)
                to [
                    battery={ very near start, rotate={rotate1}, info={ $\\ele_1, r_1 $ } },
                    resistor={ midway, info=$R_1$ },
                    battery={ very near end, rotate={rotate2}, info={ $\\ele_2, r_2 $ } }
                ] ++(right:5)
                -- ++(down:2)
                to [resistor={ info=$R_2$ }, current direction={ near end, info=$\\eli$ }] ++(left:5);
        \\draw [-{ Latex }] (2, 1.4) arc [start angle = 135, end angle = -160, radius = 0.6];
    \\end{ tikzpicture }

    \\begin{ align* }
        &{sign1} \\ele_1 + {sign2} \\ele_2 = \\eli R_1 + \\eli r_2 + \\eli R_2 + \\eli r_1, \\\\
        &{sign1} \\ele_1 + {sign2} \\ele_2 = \\eli (R_1 + r_2 + R_2 + r_1), \\\\
        &\\eli = \\frac{ {sign1} \\ele_1 + {sign2} \\ele_2 }{ R_1 + r_2 + R_2 + r_1 }, \\\\
        &U_{index} = \\eli R_{index} = \\frac{ {sign1} \\ele_1 + {sign2} \\ele_2 }{ R_1 + r_2 + R_2 + r_1 } * R_{index}, \\\\
        &P_{index} = \\eli^2 R_{index} = \\frac{ \\sqr{ {sign1} \\ele_1 + {sign2} \\ele_2 } R_{index} }{ \\sqr{ R_1 + r_2 + R_2 + r_1 } }.
    \\end{ align* }

    Отметим, что это ответ для тока $\\eli$ меняет знак, если отметить его на рисунке в другую сторону.
    А вот выбор направления контура — не повлияет на ответ.
''')
class Kirchgof_plain(variant.VariantTask):
    def GetUpdate(self, index=None, rotate1=None, rotate2=None, **kws):
        signs = {
            0: '-',
            -180: '',
        }
        return dict(
            sign1=signs[rotate1],
            sign2=signs[rotate2],
        )


@variant.text('''
    Два резистора сопротивлениями $R_1={a}R$ и $R_2={b}R$ подключены {how} к источнику напряжения.
    Определите, в каком резисторе выделяется большая тепловая мощность и во сколько раз?
''')
@variant.arg(a=[3, 5, 7])
@variant.arg(b=[2, 4, 6, 8])
@variant.arg(how=['параллельно', 'последовательно'])
@variant.answer('Подключены {how}, поэтому  ${equals1} \\implies \\frac{ P_2 }{ P_1 } = {equals2} = {ratio:LaTeX}$.')
class Compare_power(variant.VariantTask):  # Вишнякова - 17
    def GetUpdate(self, a=None, b=None, how=None, **kws):
        if how == 'параллельно':
            equals1 = 'U_1 = U_2 = U'
            equals2 = '\\frac{ \\frac{ U_2^2 }{ R_2 } }{ \\frac{ U_1^2 }{ R_1 } } = \\frac{ U^2R_1 }{ U^2R_2 } = \\frac{ R_1 }{ R_2 }'
            ratio = Fraction(numerator=a, denominator=b)
        elif how == 'последовательно':
            equals1 = '\\eli_1 = \\eli_2 = \\eli'
            equals2 = '\\frac{ \\eli_2^2 R_2 }{ \\eli_1^2 R_1 } = \\frac{ \\eli_2^2R_2 }{ \\eli_1R_1 } = \\frac{ R_2 }{ R_1 }'
            ratio = Fraction(numerator=b, denominator=a)

        return dict(
            equals1=equals1,
            equals2=equals2,
            ratio=ratio,
        )


@variant.text('''
    Если батарею замкнуть на резистор сопротивлением $R_1$, то в цепи потечёт ток $\\eli_1$,
    а если на другой $R_2$ — то $\\eli_2$. Определите:
    \\begin{{itemize}}
        \\item ЭДС батареи,
        \\item внутреннее сопротивление батареи,
        \\item ток короткого замыкания.
    \\end{{itemize}}
''')
@variant.no_args
@variant.answer_tex('''
    Запишем закон Ома для полной цепи 2 раза для обеих способов подключения
    (короткое замыкание рассмотрим позже).

    \\begin{ align* }
        &\\begin{ cases }
            \\ele = \\eli_1(R_1 + r), \\\\
            \\ele = \\eli_2(R_2 + r); \\\\
        \\end{ cases } \\\\
        &\\eli_1(R_1 + r) = \\eli_2(R_2 + r), \\\\
        &\\eli_1 R_1 + \\eli_1r = \\eli_2 R_2 + \\eli_2r, \\\\
        &\\eli_1 R_1 - \\eli_2 R_2 = - \\eli_1r  + \\eli_2r = (\\eli_2 - \\eli_1)r, \\\\
        r &= \\frac{ \\eli_1 R_1 - \\eli_2 R_2 }{ \\eli_2 - \\eli_1 }, \\\\
        \\ele &= \\eli_1(R_1 + r)
            = \\eli_1\\cbr{ R_1 + \\frac{ \\eli_1 R_1 - \\eli_2 R_2 }{ \\eli_2 - \\eli_1 } }
            = \\eli_1 * \\frac{ R_1\\eli_2 - R_1\\eli_1 + \\eli_1 R_1 - \\eli_2 R_2 }{ \\eli_2 - \\eli_1 } \\\\
            &= \\eli_1 * \\frac{ R_1\\eli_2 - \\eli_2 R_2 }{ \\eli_2 - \\eli_1 }
            = \\frac{ \\eli_1 \\eli_2 (R_1 - R_2) }{ \\eli_2 - \\eli_1 }
            \\equiv \\frac{ \\eli_1 \\eli_2 (R_2 - R_1) }{ \\eli_1 - \\eli_2 }.
    \\end{ align* }

    Короткое замыкание означает, что сопротивление внешней нагрузки 0:
    $$
        \\eli_\\text{ к. з. } = \\frac \\ele { 0 + r } = \\frac \\ele r
            = \\frac{ \\cfrac{ \\eli_1 \\eli_2 (R_1 - R_2) }{ \\eli_2 - \\eli_1 } }{ \\cfrac{ \\eli_1 R_1 - \\eli_2 R_2 }{ \\eli_2 - \\eli_1 } }
            = \\frac{ \\eli_1 \\eli_2 (R_1 - R_2) }{ \\eli_1 R_1 - \\eli_2 R_2 }
            \\equiv \\frac{ \\eli_1 \\eli_2 (R_2 - R_1) }{ \\eli_2 R_2 - \\eli_1 R_1 }.
    $$
''')
class Short_i(variant.VariantTask):  # Вишнякова - 7
    pass


@variant.text('''
    Определите ток, протекающий через резистор {R:Task:e} и разность потенциалов на нём (см. рис.),
    если {E1:Task:e}, {E2:Task:e}, {r1:Task:e}, {r2:Task:e}.

    \\begin{ tikzpicture }[circuit ee IEC, thick]
        \\draw  (0, 0) to [battery={ rotate=-180,info={ $\\ele_1, r_1 $ } }] (0, 3)
                -- (5, 3)
                to [battery={ rotate=-180, info'={ $\\ele_2, r_2 $ } }] (5, 0)
                -- (0, 0)
                (2.5, 0) to [resistor={ info=$R$ }] (2.5, 3);
    \\end{ tikzpicture }
''')
@variant.arg(R=['R = %d Ом' % RValue for RValue in [10, 12, 15, 18, 20]])
@variant.arg(r1=['r_1 = %d Ом' % r1Value for r1Value in [1, 2, 3]])
@variant.arg(r2=['r_2 = %d Ом' % r2Value for r2Value in [2, 4, 6]])
@variant.arg(E1=['\\ele_1 = %d В' % E1Value for E1Value in [6, 12, 18]])
@variant.arg(E2=['\\ele_2 = %d В' % E2Value for E2Value in [5, 15, 25]])
@variant.answer_tex('''
    Выберем 2 контура и один узел, запишем для них законы Кирхгофа:

    \\begin{ tikzpicture }[circuit ee IEC, thick]
        \\draw  (0, 0) to [battery={ rotate=-180,info={ $\\ele_1, r_1 $ } }, current direction={ near end, info=$\\eli_1$ }] (0, 3)
                -- (5, 3)
                to [battery={ rotate=-180, info'={ $\\ele_2, r_2 $ } }, current direction={ near end, info=$\\eli_2$ }] (5, 0)
                -- (0, 0)
                (2.5, 0) to [resistor={ info=$R$ }, current direction'={ near end, info=$\\eli$ }] (2.5, 3);
        \\draw [-{ Latex },color=red] (0.8, 1.9) arc [start angle = 135, end angle = -160, radius = 0.6];
        \\draw [-{ Latex },color=blue] (3.5, 1.9) arc [start angle = 135, end angle = -160, radius = 0.6];
        \\node [contact,color=green!71!black] (topc) at (2.5, 3) {  };
        \\node [above] (top) at (2.5, 3) { $1$ };
    \\end{ tikzpicture }

    \\begin{ align* }
        &\\begin{ cases }
            { \\color{ red } {E1:L} = \\eli_1 {r1:L} + {I:L} {R:L} }, \\\\
            { \\color{ blue } {E2:L} = \\eli_2 {r2:L} - {I:L} {R:L} }, \\\\
            { \\color{ green!71!black } {I:L} - \\eli_1 - \\eli_2 = 0 };
        \\end{ cases }
        \\qquad \\implies \\qquad
        \\begin{ cases }
            \\eli_1 = \\frac{ {E1:L} - {I:L} {R:L} }{r1:L:s}, \\\\
            \\eli_2 = \\frac{ {E2:L} + {I:L} {R:L} }{r2:L:s}, \\\\
            {I:L} - \\eli_1 - \\eli_2 = 0;
        \\end{ cases } \\implies \\\\
        &\\implies {I:L} - \\frac{ {E1:L} - {I:L} {R:L} }{r1:L:s} + \\frac{ {E2:L} + {I:L} {R:L} }{r2:L:s} = 0, \\\\
        &{I:L}\\cbr{ 1 + \\frac{R:L:s}{r1:L:s} + \\frac{R:L:s}{r2:L:s} } - \\frac{E1:L:s}{r1:L:s} + \\frac{E2:L:s}{r2:L:s} = 0, \\\\
        &{I:L}
            = \\frac{ \\frac{E1:L:s}{r1:L:s} - \\frac{E2:L:s}{r2:L:s} }{ 1 + \\frac{R:L:s}{r1:L:s} + \\frac{R:L:s}{r2:L:s} }
            = \\frac{ \\frac{E1:V:s}{r1:V:s} - \\frac{E2:V:s}{r2:V:s} }{ 1 + \\frac{R:V:s}{r1:V:s} + \\frac{R:V:s}{r2:V:s} }
            = {I_ratio:LaTeX}\\units{ А }
            \\approx {I:Value}, \\\\
        &U  = {I:L} {R:L} = \\frac{ \\frac{E1:L:s}{r1:L:s} - \\frac{E2:L:s}{r2:L:s} }{ 1 + \\frac{R:L:s}{r1:L:s} + \\frac{R:L:s}{r2:L:s} } R
            \\approx {U:Value}.
    \\end{ align* }
'''
)
class Kirchgof_double_2(variant.VariantTask):
    pass
    def GetUpdate(self, R=None, r1=None, r2=None, E1=None, E2=None, **kws):
        I_ratio = (
            Fraction(numerator=E1.Value, denominator=r1.Value) - Fraction(numerator=E2.Value, denominator=r2.Value)
        ) / (
            Fraction(base_value=1) + Fraction(numerator=R.Value, denominator=r1.Value) + Fraction(numerator=R.Value, denominator=r2.Value)
        )

        I = '\\eli = %.3f А' % float(I_ratio)
        U = 'U = %.3f В' % float(I_ratio * R.Value)
        return dict(
            I_ratio=I_ratio,
            I=I,
            U=U,
        )


@variant.text('''
    Определите ток $\\eli_{index}$, протекающий через резистор $R_{index}$ (см. рис.),
    направление этого тока и разность потенциалов $U_{index}$ на этом резисторе,
    если {R1:Task:e}, {R2:Task:e}, {R3:Task:e}, {E1:Task:e}, {E2:Task:e}, {E3:Task:e}.
    Внутренним сопротивлением всех трёх ЭДС пренебречь.
    Ответы получите в виде несократимых дробей, а также определите приближённые значения.

    \\begin{ tikzpicture }[circuit ee IEC, thick]
        \\foreach \\contact/\\x in { 1/0, 2/3, 3/6 }
        {
            \\node [contact] (top contact \\contact) at (\\x, 0) {  };
            \\node [contact] (bottom contact \\contact) at (\\x, 4) {  };
        }
        \\draw  (bottom contact 1) -- (bottom contact 2) -- (bottom contact 3);
        \\draw  (top contact 1) -- (top contact 2) -- (top contact 3);
        \\draw  (bottom contact 1) to [resistor={ near start, info={R1:Letter:e} }, battery={ near end, info={E1:Letter:e} }] (top contact 1);
        \\draw  (bottom contact 2) to [resistor={ near start, info={R2:Letter:e} }, battery={ near end, info={E2:Letter:e} }] (top contact 2);
        \\draw  (bottom contact 3) to [resistor={ near start, info={R3:Letter:e} }, battery={ near end, info={E3:Letter:e} }] (top contact 3);
    \\end{ tikzpicture }

''')
@variant.arg(index=[1, 2, 3])
@variant.arg(R1=('R_1 = {} Ом', [2, 3, 4]))
@variant.arg(R2=('R_2 = {} Ом', [5, 6, 8]))
@variant.arg(R3=('R_3 = {} Ом', [10, 12, 15]))
@variant.arg(E1=('\\ele_1 = {} В', [4, 5]))
@variant.arg(E2=('\\ele_2 = {} В', [3, 6]))
@variant.arg(E3=('\\ele_3 = {} В', [2, 8]))
@variant.answer_tex('''
    План:
    \\begin{{itemize}}
        \\item отметим на рисунке произвольно направления токов (если получим отрицательный ответ, значит не угадали направление и только),
        \\item выберем и обозначим на рисунке контуры (здесь всего 3, значит будет нужно $3-1=2$), для них запишем законы Кирхгофа,
        \\item выберем и выделим на рисунке нетривиальные узлы (здесь всего 2, значит будет нужно $2-1=1$), для него запишем закон Кирхгофа,
        \\item попытаемся решить получившуюся систему. В конкретном решении мы пытались первым делом найти {I2:L:e}, но, возможно, в вашем варианте будет быстрее решать систему в другом порядке. Мы всё же проделаем всё в лоб, подробно и целиком.
    \\end{{itemize}}


    \\begin{ tikzpicture }[circuit ee IEC, thick]
        \\foreach \\contact/\\x in { 1/0, 2/3, 3/6 }
        {
            \\node [contact] (top contact \\contact) at (\\x, 0) {  };
            \\node [contact] (bottom contact \\contact) at (\\x, 4) {  };
        }
        \\draw  (bottom contact 1) -- (bottom contact 2) -- (bottom contact 3);
        \\draw  (top contact 1) -- (top contact 2) -- (top contact 3);
        \\draw  (bottom contact 1) to [resistor={ near start, info={R1:Letter:e} }, current direction'={ midway, info={I1:Letter:e} }, battery={ near end, info={E1:Letter:e} }] (top contact 1);
        \\draw  (bottom contact 2) to [resistor={ near start, info={R2:Letter:e} }, current direction'={ midway, info={I2:Letter:e} }, battery={ near end, info={E2:Letter:e} }] (top contact 2);
        \\draw  (bottom contact 3) to [resistor={ near start, info={R3:Letter:e} }, current direction'={ midway, info={I3:Letter:e} }, battery={ near end, info={E3:Letter:e} }] (top contact 3);
        \\draw [-{ Latex },color=red] (1.2, 2.5) arc [start angle = 135, end angle = -160, radius = 0.6];
        \\draw [-{ Latex },color=blue] (4.2, 2.5) arc [start angle = 135, end angle = -160, radius = 0.6];
        \\node [contact,color=green!71!black] (bottomc) at (bottom contact 2) {  };
    \\end{ tikzpicture }

    \\begin{ align* }
        &\\begin{ cases }
            { \\color{ red } {I1:L}{R1:L} - {I2:L}{R2:L} = {E1:L} - {E2:L} }, \\\\
            { \\color{ blue } {I2:L}{R2:L} - {I3:L}{R3:L} = {E2:L} - {E3:L} }, \\\\
            { \\color{ green!71!black } {I1:L} + {I2:L} + {I3:L} = 0 };
        \\end{ cases }
        \\qquad \\implies \\qquad
        \\begin{ cases }
            {I1:L} = \\frac{ {E1:L} - {E2:L} + {I2:L}{R2:L} }{R1:L:s}, \\\\
            {I3:L} = \\frac{ {I2:L}{R2:L} - {E2:L} + {E3:L} }{R3:L:s}, \\\\
            {I1:L} + {I2:L} + {I3:L} = 0, \\\\
        \\end{ cases } \\implies \\\\
        \\implies
            &{I2:L} + \\frac{ {E1:L} - {E2:L} + {I2:L}{R2:L} }{R1:L:s} + \\frac{ {I2:L}{R2:L} - {E2:L} + {E3:L} }{R3:L:s} = 0, \\\\
        &   {I2:L}\\cbr{ 1 + \\frac{R2:L:s}{R1:L:s} + \\frac{R2:L:s}{R3:L:s} } + \\frac{ {E1:L} - {E2:L} }{R1:L:s} + \\frac{ {E3:L} - {E2:L} }{R3:L:s} = 0, \\\\
        &   {I2:L} = \\cfrac{ \\cfrac{ {E2:L} - {E1:L} }{R1:L:s} + \\cfrac{ {E2:L} - {E3:L} }{R3:L:s} }{ 1 + \\cfrac{R2:L:s}{R1:L:s} + \\cfrac{R2:L:s}{R3:L:s} }
            = \\cfrac{ \\cfrac{ {E2:V} - {E1:V} }{R1:V:s} + \\cfrac{ {E2:V} - {E3:V} }{R3:V:s} }{ 1 + \\cfrac{R2:V:s}{R1:V:s} + \\cfrac{R2:V:s}{R3:V:s} }
            = {I2_ratio:LaTeX}\\units{ А } \\approx {I2:Value}, \\\\
        &   {U2:L} = {I2:L}{R2:L} = \\cfrac{ \\cfrac{ {E2:L} - {E1:L} }{R1:L:s} + \\cfrac{ {E2:L} - {E3:L} }{R3:L:s} }{ 1 + \\cfrac{R2:L:s}{R1:L:s} + \\cfrac{R2:L:s}{R3:L:s} } * {R2:L}
            = \\cfrac{ \\cfrac{ {E2:V} - {E1:V} }{R1:V:s} + \\cfrac{ {E2:V} - {E3:V} }{R3:V:s} }{ 1 + \\cfrac{R2:V:s}{R1:V:s} + \\cfrac{R2:V:s}{R3:V:s} } * {R2:V}
            = {I2_ratio:LaTeX}\\units{ А } * {R2:V} = {U2_ratio:LaTeX}\\units{ В } \\approx {U2:Value}.
    \\end{ align* }

    Одну пару силы тока и напряжения получили. Для некоторых вариантов это уже ответ, но не у всех.
    Для упрощения записи преобразуем (чтобы избавитсья от 4-этажной дроби) и подставим в уже полученные уравнения:

    \\begin{ align* }
    {I2:L}
        &=
        \\frac{ \\frac{ {E2:L} - {E1:L} }{R1:L:s} + \\frac{ {E2:L} - {E3:L} }{R3:L:s} }{ 1 + \\frac{R2:L:s}{R1:L:s} + \\frac{R2:L:s}{R3:L:s} }
        =
        \\frac{ ({E2:L} - {E1:L}){R3:L} + ({E2:L} - {E3:L}){R1:L} }{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} },
        \\\\
    {I1:L}
        &=  \\frac{ {E1:L} - {E2:L} + {I2:L}{R2:L} }{R1:L:s}
        =   \\frac{ {E1:L} - {E2:L} + \\cfrac{ ({E2:L} - {E1:L}){R3:L} + ({E2:L} - {E3:L}){R1:L} }{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} } * {R2:L} }{R1:L:s} = \\\\
        &=  \\frac{
            {E1:L}{R1:L}{R3:L} + {E1:L}{R2:L}{R3:L} + {E1:L}{R2:L}{R1:L}
            - {E2:L}{R1:L}{R3:L} - {E2:L}{R2:L}{R3:L} - {E2:L}{R2:L}{R1:L}
            + {E2:L}{R3:L}{R2:L} - {E1:L}{R3:L}{R2:L} + {E2:L}{R1:L}{R2:L} - {E3:L}{R1:L}{R2:L}
        }{ {R1:L} * \\cbr{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} } }
        = \\\\ &=
        \\frac{
            {E1:L}\\cbr{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} - {R3:L}{R2:L} }
            + {E2:L}\\cbr{ - {R1:L}{R3:L} - {R2:L}{R3:L} - {R2:L}{R1:L} + {R3:L}{R2:L} + {R1:L}{R2:L} }
            - {E3:L}{R1:L}{R2:L}
        }{ {R1:L} * \\cbr{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} } }
        = \\\\ &=
        \\frac{
            {E1:L}\\cbr{ {R1:L}{R3:L} + {R2:L}{R1:L} }
            + {E2:L}\\cbr{ - {R1:L}{R3:L} }
            - {E3:L}{R1:L}{R2:L}
        }{ {R1:L} * \\cbr{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} } }
        =
        \\frac{
            {E1:L}\\cbr{ {R3:L} + {R2:L} } - {E2:L}{R3:L} - {E3:L}{R2:L}
        }{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} }
        = \\\\ &=
        \\frac{
            ({E1:L} - {E3:L}){R2:L} + ({E1:L} - {E2:L}){R3:L}
        }{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} }
        =
        \\frac{
            \\cfrac{ {E1:L} - {E3:L} }{R3:L:s} + \\cfrac{ {E1:L} - {E2:L} }{R2:L:s}
        }{ \\cfrac{R1:L:s}{R2:L:s} + 1 + \\cfrac{R1:L:s}{R3:L:s} }
        =
        \\frac{
            \\cfrac{ {E1:V} - {E3:V} }{R3:V:s} + \\cfrac{ {E1:V} - {E2:V} }{R2:V:s}
        }{ \\cfrac{R1:V:s}{R2:V:s} + 1 + \\cfrac{R1:V:s}{R3:V:s} }
        = {I1_ratio:LaTeX}\\units{ А } \\approx {I1:Value}. \\\\
    {U1:L}
        &=
        {I1:L}{R1:L}
        =
        \\frac{
            \\cfrac{ {E1:L} - {E3:L} }{R3:L:s} + \\cfrac{ {E1:L} - {E2:L} }{R2:L:s}
        }{ \\cfrac{R1:L:s}{R2:L:s} + 1 + \\cfrac{R1:L:s}{R3:L:s} } * {R1:L}
        =
        {I1_ratio:LaTeX}\\units{ А } * {R1:V} = {U1_ratio:LaTeX}\\units{ В } \\approx {U1:Value}.
    \\end{ align* }

    Если вы проделали все эти вычисления выше вместе со мной, то
    \\begin{{itemize}}
        \\item вы совершили ошибку, выбрав неверный путь решения:
        слишком длинное решение, очень легко ошибиться в индексах, дробях, знаках или потерять какой-то множитель,
        \\item можно было выразить из исходной системы другие токи и получить сразу нажный вам,
        а не какой-то 2-й,
        \\item можно было сэкономить: все три резистора и ЭДС соединены одинаково,
        поэтому ответ для 1-го резистора должен отличаться лишь перестановкой индексов (этот факт крайне полезен при проверке ответа, у нас всё сошлось),
        я специально подгонял выражение для {I1:L:e} к этому виду, вынося за скобки и преобразуя дробь,
        \\item вы молодец, потому что не побоялись и получили верный ответ грамотным способом,
    \\end{{itemize}}
    так что переходим к третьему резистору. Будет похоже, но кого это когда останавливало...

    \\begin{ align* }
    {I3:L}
        &=  \\frac{ {I2:L}{R2:L} - {E2:L} + {E3:L} }{R3:L:s}
        =
        \\cfrac{
            \\cfrac{
                ({E2:L} - {E1:L}){R3:L} + ({E2:L} - {E3:L}){R1:L}
            }{
                {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L}
            } * {R2:L} - {E2:L} + {E3:L} }{R3:L:s}
        = \\\\ &=
        \\frac{
            {E2:L}{R3:L}{R2:L} - {E1:L}{R3:L}{R2:L} + {E2:L}{R1:L}{R2:L} - {E3:L}{R1:L}{R2:L}
            - {E2:L}{R1:L}{R3:L} - {E2:L}{R2:L}{R3:L} - {E2:L}{R2:L}{R1:L}
            + {E3:L}{R1:L}{R3:L} + {E3:L}{R2:L}{R3:L} + {E3:L}{R2:L}{R1:L}
        }{ \\cbr{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} } * {R3:L} }
        = \\\\ &=
        \\frac{
            - {E1:L}{R3:L}{R2:L} - {E2:L}{R1:L}{R3:L} + {E3:L}{R1:L}{R3:L} + {E3:L}{R2:L}{R3:L}
        }{ \\cbr{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} } * {R3:L} }
        =
        \\frac{
            - {E1:L}{R2:L} - {E2:L}{R1:L} + {E3:L}{R1:L} + {E3:L}{R2:L}
        }{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} }
        = \\\\ &=
        \\frac{
            {R1:L}({E3:L} - {E2:L}) + {R2:L}({E3:L} - {E1:L})
        }{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} }
        =
        \\frac{
            \\cfrac{ {E3:L} - {E2:L} }{R2:L:s} + \\cfrac{ {E3:L} - {E1:L} }{R1:L:s}
        }{ \\cfrac{R3:L:s}{R2:L:s} + \\cfrac{R3:L:s}{R1:L:s} + 1 }
        =
        \\frac{
            \\cfrac{ {E3:V} - {E2:V} }{R2:V:s} + \\cfrac{ {E3:V} - {E1:V} }{R1:V:s}
        }{ \\cfrac{R3:V:s}{R2:V:s} + \\cfrac{R3:V:s}{R1:V:s} + 1 }
        = {I3_ratio:LaTeX}\\units{ А } \\approx {I3:Value}. \\\\
    {U3:L}
        &=
        {I3:L}{R3:L}
        =
        \\frac{
            \\cfrac{ {E3:L} - {E2:L} }{R2:L:s} + \\cfrac{ {E3:L} - {E1:L} }{R1:L:s}
        }{ \\cfrac{R3:L:s}{R2:L:s} + \\cfrac{R3:L:s}{R1:L:s} + 1 } * {R3:L}
        =
        {I3_ratio:LaTeX}\\units{ А } * {R3:V} = {U3_ratio:LaTeX}\\units{ В } \\approx {U3:Value}.
    \\end{ align* }

    Положительные ответы говорят, что мы угадали на рисунке направление тока (тут нет нашей заслуги, повезло),
    отрицательные — что не угадали (и в этом нет ошибки), и ток течёт в противоположную сторону.
    Напомним, что направление тока — это направление движения положительных зарядов,
    а в металлах носители заряда — электроны, которые заряжены отрицательно.
'''
)
class Kirchgof_triple(variant.VariantTask):
    def GetUpdate(self, R1=None, R2=None, R3=None, E1=None, E2=None, E3=None, **kws):
        I1_ratio = (
            Fraction(numerator=E1.Value - E3.Value, denominator=R3.Value)
            + Fraction(numerator=E1.Value - E2.Value, denominator=R2.Value)
        ) / (
            Fraction(numerator=R1.Value, denominator=R2.Value)
            + Fraction(numerator=R1.Value, denominator=R3.Value)
            + 1
        )
        I2_ratio = (
            Fraction(numerator=E2.Value - E1.Value, denominator=R1.Value)
            + Fraction(numerator=E2.Value - E3.Value, denominator=R3.Value)
        ) / (
            Fraction(numerator=R2.Value, denominator=R1.Value)
            + Fraction(numerator=R2.Value, denominator=R3.Value)
            + 1
        )
        I3_ratio = (
            Fraction(numerator=E3.Value - E1.Value, denominator=R1.Value)
            + Fraction(numerator=E3.Value - E2.Value, denominator=R2.Value)
        ) / (
            Fraction(numerator=R3.Value, denominator=R1.Value)
            + Fraction(numerator=R3.Value, denominator=R2.Value)
            + 1
        )
        I1 = '\\eli_1 = %.2f А' % float(I1_ratio)
        I2 = '\\eli_2 = %.2f А' % float(I2_ratio)
        I3 = '\\eli_3 = %.2f А' % float(I3_ratio)
        U1_ratio = I1_ratio * R1.Value
        U2_ratio = I2_ratio * R2.Value
        U3_ratio = I3_ratio * R3.Value
        U1 = 'U_1 = %.2f В' % float(U1_ratio)
        U2 = 'U_2 = %.2f В' % float(U2_ratio)
        U3 = 'U_3 = %.2f В' % float(U3_ratio)
        return dict(
            I1_ratio=I1_ratio,
            I2_ratio=I2_ratio,
            I3_ratio=I3_ratio,
            I1=I1,
            I2=I2,
            I3=I3,
            U1_ratio=U1_ratio,
            U2_ratio=U2_ratio,
            U3_ratio=U3_ratio,
            U1=U1,
            U2=U2,
            U3=U3,
        )


@variant.solution_space(180)
@variant.text('''
    При подключении к источнику тока с ЭДС равным {E:Value:e}
    резистора сопротивлением {R1:Value:e} в цепи течёт ток силой {I1:Value:e}.
    После этого {how} с первым проводником подключают ещё один сопротивлением {R2:Value:e}.
    Определите
    \\begin{{itemize}}
        \\item внутреннее сопротивление источника тока,
        \\item новую силу тока в цепи,
        \\item мощность тока во втором проводнике.
    \\end{{itemize}}
''')
@variant.arg(r=('r = {} Ом', [1, 2, 3]))
@variant.arg(how=['параллельно', 'последовательно'])
@variant.arg(R1=('R_1 = {} Ом', [6, 12, 20]))
@variant.arg(R2=('R_2 = {} Ом', [5, 10, 15]))
@variant.arg(I1=('\\eli_1 = {} А', [2, 3, 5, 7, 11]))
@variant.answer_align([
    '{I1:L} &= \\frac{E:L:s}{ {R1:L} + {r:L} } \\implies {r:L} = \\frac{E:L:s}{I1:L:s} - {R1:L} = \\frac{E:V:s}{I1:V:s} - {R1:V} = {r:V},',
    'R\' &= {R_formula} = {R_ratio:LaTeX}\\units{ Ом },',
    '{I2:L} &= \\frac{E:L:s}{ R\' + {r:L} } = {I2_ratio:LaTeX}\\units{ А } \\approx {I2:V},',
    '{P2:L} &= {P_formula} = {P2_ratio:LaTeX}\\units{ Вт } \\approx {P2:V}.',
])
class Update_external_R(variant.VariantTask):
    def GetUpdate(self, r=None, how=None, R1=None, R2=None, I1=None, **kws):
        E_value = I1.Value * (r.Value + R1.Value)
        E = '\\ele = %d В' % E_value
        if how == 'параллельно':
            R_formula = f'\\frac{{ {R1:L}{R2:L} }}{{ {R1:L} + {R2:L} }}'
            R_ratio = Fraction(numerator=R1.Value * R2.Value, denominator=R1.Value + R2.Value)
            I2_ratio = Fraction(numerator=E_value) / (R_ratio + r.Value)
            P_formula = f'\\frac{{ U_2^2 }}{R2:L:s} \\equiv \\frac{{ \\sqr{{ \\eli_2 R\' }} }}{R2:L:s}'
            P2_ratio = (I2_ratio * R_ratio * I2_ratio * R_ratio) / R2.Value
        elif how == 'последовательно':
            R_formula = f'{R1:L} + {R2:L}'
            R_ratio = Fraction(numerator=R1.Value + R2.Value)
            I2_ratio = Fraction(numerator=E_value) / (R_ratio + r.Value)
            P_formula = f'\\eli_2^2 {R2:L:s}'
            P2_ratio = I2_ratio * I2_ratio * R2.Value

        return dict(
            E=E,
            R_formula=R_formula,
            R_ratio=R_ratio,
            I2_ratio=I2_ratio,
            I2='\\eli_2 = %.2f А' % float(I2_ratio),
            P_formula=P_formula,
            P2_ratio=P2_ratio,
            P2='P\'_2 = %.1f Вт' % float(P2_ratio),
        )


@variant.text('''
    Определите эквивалентное сопротивление цепи на рисунке (между выделенными на рисунке контактами),
    если известны сопротивления всех резисторов: {R1:Task:e}, {R2:Task:e}, {R3:Task:e}, {R4:Task:e}.
    При каком напряжении поданном на эту цепь, в ней потечёт ток равный {I:Task:e}?

    \\begin{ tikzpicture }[rotate={rotate}, circuit ee IEC, thick]
        \\node [contact]  (contact1) at (-1.5, 0) {  };
        \\draw  (0, 0) to [resistor={ info=$R_1$ }] ++(left:1.5);
        \\draw  (0, 0) -- ++(up:1.5) to [resistor={ near start, info=$R_2$ }, resistor={ near end, info=$R_3$ }] ++(right:3);
        \\draw  (0, 0) to [resistor={ info=$R_4$ }] ++(right:3) -- ++(up:1.5);
        {appendix}
    \\end{ tikzpicture }
''')
@variant.arg(rotate=[0, 90, 180, 270])
@variant.arg(second_node=[0, 1])
@variant.arg(R1=('R_1 = {} Ом', [1, 2]))
@variant.arg(R2=('R_2 = {} Ом', [3, 4, 5]))
@variant.arg(R3=('R_3 = {} Ом', [1, 2, 3]))
@variant.arg(R4=('R_4 = {} Ом', [2, 3, 4]))
@variant.arg(I=('\\eli = {} А', [2, 5, 10]))
@variant.answer_short('R={R_ratio:LaTeX}\\units{ Ом } \\approx {R:V} \\implies U = \\eli R \\approx {U:V}.')
class Circuit_four(variant.VariantTask):
    def GetUpdate(self, rotate=None, second_node=None, R1=None, R2=None, R3=None, R4=None, I=None, **kws):
        if second_node == 0:
            appendix = '\\draw  (3, 1.5) -- ++(right:0.5); \\node [contact] (contact2) at (3.5, 1.5) {  };'
            R_ratio = Fraction(numerator=(R2.Value + R3.Value) * R4.Value, denominator=R2.Value + R3.Value + R4.Value) + R1.Value
        elif second_node == 1:
            appendix = '\\draw  (1.5, 1.5) -- ++(up:1); \\node [contact] (contact2) at (1.5, 2.5) {  };'
            R_ratio = Fraction(numerator=R2.Value * (R3.Value + R4.Value), denominator=R2.Value + R3.Value + R4.Value) + R1.Value
        return dict(
            appendix=appendix,
            R_ratio=R_ratio,
            R='R = %.2f Ом' % float(R_ratio),
            U='U = %.1f В' % (I.Value * float(R_ratio)),
        )



@variant.text('''
    Определите показания амперметра ${index_a}$ (см. рис.) и разность потенциалов на резисторе ${index_r}$,
    если сопротивления всех резисторов равны: $R_1 = R_2 = R_3 = R_4 = R_5 = R_6 = {R:Task}$,
    а напряжение, поданное на цепь, равно {U:Task:e}.
    Ответы получите в виде несократимых дробей, а также определите приближённые значения. Амперметры считать идеальными.

    \\begin{ tikzpicture }[circuit ee IEC, thick]
        \\node [contact]  (left contact) at (3, 0) {  };
        \\node [contact]  (right contact) at (9, 0) {  };
        \\draw  (left contact) -- ++(up:2) to [resistor={ very near start, info=$R_2$ }, amperemeter={ midway, info=$1$ }, resistor={ very near end, info=$R_3$ } ] ++(right:6) -- (right contact);
        \\draw  (left contact) -- ++(down:2) to [resistor={ very near start, info=$R_5$ }, resistor={ midway, info=$R_6$ }, amperemeter={ very near end, info=$3$ }] ++(right:6) -- (right contact);
        \\draw  (left contact) ++(left:3) to [resistor={ info=$R_1$ }] (left contact) to [amperemeter={ near start, info=$2$ }, resistor={ near end , info=$R_4$ }] (right contact) -- ++(right:0.5);
    \\end{ tikzpicture }

''')
@variant.arg(index_a=[1, 2, 3])
@variant.arg(index_r=[1, 2, 3, 4, 5, 6])
@variant.arg(R=('R = {} Ом', [2, 4, 5, 10]))
@variant.arg(U=('U = {} В', [30, 60, 90, 120, 150]))
@variant.answer_align([
    'R_0 &= R + \\frac 1{ \\frac 1{ R + R } + \\frac 1{ R } + \\frac 1{ R + R } } = R + \\frac 1{ \\frac 2R } = \\frac 32 R,',
    '\\eli &= \\frac U{ R_0 } = \\frac { 2U }{ 3R },',
    'U_1 &= \\eli R_1 = \\frac { 2U }{ 3R } * R = \\frac 23 U = {U1:Value},',
    'U_{ 23 } &= U_{ 56 } = U_4 = U - \\eli R_1 = U - \\frac { 2U }{ 3R } * R = \\frac U3 = {U4:Value},',
    '\\eli_2 &= \\frac{ U_4 }{ R_4 } = \\frac{ U }{ 3R } \\approx {I2:Value},',
    '\\eli_1 &= \\frac{ U_{ 23 } }{ R_{ 23 } } = \\frac{ \\frac U3 }{ R + R } = \\frac U{ 6R } \\approx {I1:Value},',
    '\\eli_3 &= \\frac{ U_{ 56 } }{ R_{ 56 } } = \\frac{ \\frac U3 }{ R + R } = \\frac U{ 6R } \\approx {I3:Value},',
    'U_2 &= \\eli_1 R_2 = \\frac U{ 6R } * R = \\frac U6 = {U2:Value},',
    'U_3 &= \\eli_1 R_3 = \\frac U{ 6R } * R = \\frac U3 = {U3:Value},',
    'U_5 &= \\eli_3 R_5 = \\frac U{ 6R } * R = \\frac U5 = {U5:Value},',
    'U_6 &= \\eli_3 R_6 = \\frac U{ 6R } * R = \\frac U6 = {U6:Value}.',
])
class Circuit_six(variant.VariantTask):
    def GetUpdate(self, R=None, U=None, index_a=None, index_r=None, **kws):
        U1 = Fraction(numerator=2 * U.Value, denominator=3)
        U2 = Fraction(numerator=U.Value, denominator=6)
        U3 = Fraction(numerator=U.Value, denominator=6)
        U4 = Fraction(numerator=U.Value, denominator=3)
        U5 = Fraction(numerator=U.Value, denominator=6)
        U6 = Fraction(numerator=U.Value, denominator=6)
        I1 = Fraction(numerator=U.Value, denominator=6 * R.Value)
        I2 = Fraction(numerator=U.Value, denominator=3 * R.Value)
        I3 = Fraction(numerator=U.Value, denominator=6 * R.Value)
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
