import itertools

import generators.variant as variant
from generators.helpers import UnitValue


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
class Rezistor1_v1(variant.VariantTask):
    def GetUpdate(self, R=None, U=None, **kws):
        return dict(
            I='\\mathcal{I} = %.2f А' % (1. * U.Value / R.Value),
            P='P = %.2f Вт' % (1. * U.Value ** 2 / R.Value),
        )


@variant.text('''
    Через резистор сопротивлением {R:Task:e} протекает электрический ток {I:Task:e}.
    Определите, чему равны напряжение на резисторе и мощность, выделяющаяся на нём.
''')
@variant.answer_align([
    '{U:L} &= {I:L}{R:L} = {I:Value} * {R:Value} = {U:Value}, ',
    '{P:L} &= {I:L}^2{R:L} = {I:Value|sqr} * {R:Value} = {P:Value}',
])
@variant.arg(R=['%s = %d Ом' % (rLetter, rValue) for rLetter, rValue in itertools.product(['r', 'R'], [5, 12, 18, 30])])
@variant.arg(I=['\\mathcal{I} = %.2f А' % iValue for iValue in [2, 3, 4, 5, 6, 8, 10, 15]])
class Rezistor1_v2(variant.VariantTask):
    def GetUpdate(self, R=None, I=None, U=None, **kws):
        return dict(
            U='U = %d В' % (I.Value * R.Value),
            P='P = %d Вт' % (I.Value ** 2 * R.Value),
        )


@variant.text('''
    Замкнутая электрическая цепь состоит из ЭДС {E:Task:e} и сопротивлением ${r:L}$
    и резистора {R:Task:e}. Определите ток, протекающий в цепи. Какая тепловая энергия выделится на резисторе за время
    {t:Task:e}? Какая работа будет совершена ЭДС за это время? Каков знак этой работы? Чему равен КПД цепи? Вычислите значения для 2 случаев:
    ${r:L}=0$ и {r:Task:e}.
''')
@variant.answer_align([
    '''{I1:L} &= \\frac{E:L:s}{R:L:s} = \\frac{E:Value:s}{R:Value:s} = {I1:Value}, ''',
    '''{I2:L} &= \\frac{E:L:s}{ {R:L} + {r:L} } = \\frac{E:Value:s}{ {R:Value} + {r:Value} } = {I2:Value}, ''',
    '''{Q1:L} &= {I1:L}^2{R:L}{t:L} = \\sqr{ \\frac{E:L:s}{R:L:s} } {R:L} {t:L}
        = \\sqr{ \\frac{E:Value:s}{R:Value:s} } * {R:Value} * {t:Value} = {Q1:Value}, ''',
    '''{Q2:L} &= {I2:L}^2{R:L}{t:L} = \\sqr{ \\frac{E:L:s}{ {R:L} + {r:L} } } {R:L} {t:L}
        = \\sqr{ \\frac{E:Value:s}{ {R:Value} + {r:Value} } } * {R:Value} * {t:Value} = {Q2:Value}, ''',
    '''{A1:L} &= {I1:L}{t:L}{E:L} = \\frac{E:L:s}{ {R:L} } {t:L} {E:L}
        = \\frac{ {E:L}^2 {t:L} }{R:L|s} = \\frac{ {E:Value|sqr} * {t:Value} }{R:Value:s}
        = {A1:Value}, \\text{ положительна }, ''',
    '''{A2:L} &= {I2:L}{t:L}{E:L} = \\frac{E:L:s}{ {R:L} + {r:L} } {t:L} {E:L}
        = \\frac{ {E:L}^2 {t:L} }{ {R:L} + {r:L} } = \\frac{ {E:Value|sqr} * {t:Value} }{ {R:Value} + {r:Value} }
        = {A2:Value}, \\text{ положительна }, ''',
    '''{eta1:L} &= \\frac{Q1:L:s}{A1:L:s} = \\ldots = \\frac{R:L:s}{R:L:s} = 1, ''',
    '''{eta2:L} &= \\frac{Q2:L:s}{A2:L:s} = \\ldots = \\frac{R:L:s}{ {R:L} + {r:L} } = {eta2:Value}''',
])
@variant.arg(E=['\\mathcal{E} = %d В' % E for E in [1, 2, 3, 4]])
@variant.arg(R=['R = %d Ом' % R for R in [10, 15, 24, 30]])
@variant.arg(r=['r = %d Ом' % r for r in [10, 20, 30, 60]])
@variant.arg(t=['\\tau = %d с' % t for t in [2, 5, 10]])
class Rezistor2(variant.VariantTask):
    def GetUpdate(self, r=None, R=None, E=None, t=None, **kws):
        I1 = UnitValue('\\mathcal{I}_1 = %.2f А' % (1. * E.Value / R.Value))
        I2 = UnitValue('\\mathcal{I}_2 = %.2f А' % (1. * E.Value / (R.Value + r.Value)))
        Q1 = UnitValue('Q_1 = %.3f Дж' % (1. * I1.Value ** 2 * R.Value * t.Value))
        Q2 = UnitValue('Q_2 = %.3f Дж' % (1. * I2.Value ** 2 * R.Value * t.Value))
        A1 = UnitValue('A_1 = %.3f Дж' % (1. * I1.Value * E.Value * t.Value))
        A2 = UnitValue('A_2 = %.3f Дж' % (1. * I2.Value * E.Value * t.Value))
        return dict(
            I1=I1,
            I2=I2,
            Q1=Q1,
            Q2=Q2,
            A1=A1,
            A2=A2,
            eta1='\\eta_1 = %.2f' % (1. * Q1.Value / A1.Value),
            eta2='\\eta_2 = %.2f' % (1. * Q2.Value / A2.Value),
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
class Rezistor3(variant.VariantTask):
    def GetUpdate(self, R1=None, R2=None, **kws):
        r = UnitValue('r = %.2f Ом' % ((1. * R1.Value * R2.Value) ** 0.5))
        return dict(
            R1=R1,
            R2=R2,
            r=r,
            eta1='\\eta_1 = %.3f ' % (1. * R1.Value / (R1.Value + r.Value)),
            eta2='\\eta_2 = %.3f ' % (1. * R2.Value / (R2.Value + r.Value)),
            E='\\mathcal{E} = 1234 В',
        )


@variant.text('''
    Определите ток, протекающий через резистор {R:Task:e} и разность потенциалов на нём (см. рис. на доске),
    если {r1:Task:e}, {r2:Task:e}, {E1:Task:e}, {E2:Task:e}
''')
@variant.arg(R=['R = %d Ом' % RValue for RValue in [10, 12, 15, 18, 20]])
@variant.arg(r1=['r_1 = %d Ом' % r1Value for r1Value in [1, 2, 3]])
@variant.arg(r2=['r_2 = %d Ом' % r2Value for r2Value in [1, 2, 3]])
@variant.arg(E1=['\\mathcal{E}_1 = %d В' % E1Value for E1Value in [20, 30, 40, 60]])
@variant.arg(E2=['\\mathcal{E}_2 = %d В' % E2Value for E2Value in [20, 30, 40, 60]])
class Rezistor4(variant.VariantTask):
    pass