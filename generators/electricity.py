# -*- coding: utf-8 -*-

import itertools
import fractions

import variant
from value import UnitValue

import logging
log = logging.getLogger(__name__)


@variant.text(u'''
    С какой силой взаимодействуют 2 точечных заряда $q_1={charges[0]}\\units{ нКл }$ и $q_2={charges[1]}\\units{ нКл }$,
    находящиеся на расстоянии ${letter}={distance}\\units{ см }$?
''')
@variant.answer_short(u'''
    F
        = k\\frac{ q_1q_2 }{ {letter}^2 }
        = 9 \\cdot 10^9 \\funits{ Н $\\cdot$ м$^2$ }{ Кл$^2$ } \\cdot \\frac{
            {charges[0]}\\cdot 10^{ -9 }\\units{ Кл }
            \\cdot
            {charges[1]}\\cdot 10^{ -9 }\\units{ Кл }
         }{
            \\left({distance} \\cdot 10^{ -2 }\\units{ м }\\right)^2
         }
        = \\frac{ {value.numerator} }{ {value.denominator} }\\cdot10^{ {power} }\\units{ Н }
          \\approx { {approx:.2f} }\\cdot10^{ {power} }\\units{ Н }
''')
@variant.args(
    first__second=[(f, s) for f in range(2, 5) for s in range(2, 5) if f != s],
    letter=['r', 'l', 'd'],
    distance=[2, 3, 5, 6],
)
class ForceTask(variant.VariantTask):
    def GetUpdate(self, first=None, second=None, letter=None, distance=None, **kws):
        # answer = kqq/r**2
        charges = [first, second]
        value = fractions.Fraction(
            numerator=int(charges[0]) * int(charges[1]) * 9,
            denominator=int(distance) ** 2,
        )
        power = 9 - 9 - 9 + 4
        return dict(
            charges=charges,
            value=value,
            power=power,
            letter=letter,
            approx=float(value),
            distance=distance,
        )


@variant.text(u'''
    Два одинаковых маленьких проводящих заряженных шарика находятся
    на расстоянии~${letter}$ друг от друга.
    Заряд первого равен~${charges[0]}$, второго~---${charges[1]}$.
    Шарики приводят в соприкосновение, а после опять разводят на то же самое расстояние~${letter}$.
    Каким стал заряд каждого из шариков?
    Определите характер (притяжение или отталкивание)
    и силу взаимодействия шариков до и после соприкосновения.
''')
@variant.answer_align([
    u'''
    F   &= k\\frac{ q_1 q_2 }{ {letter}^2 } = k\\frac{ ({charges[0]})\\cdot({charges[1]}) }{ {letter}^2 },
    \\text{ {res[0]} };
    ''',
    u'''
    q'_1 = q'_2 = \\frac{ q_1 + q_2 }2 = \\frac{ {charges[0]} + {charges[1]} }2 \\implies
    F'  &= k\\frac{ q'_1 q'_2 }{ {letter}^2 }
        = k\\frac{ \\sqr{ \\frac{ ({charges[0]}) + ({charges[1]}) }2 } }{ {letter}^2 },
    \\text{ {res[1]} }.'''
])
@variant.args(
    first_charge__second_charge=[(fc, sc) for fc in range(2, 6) for sc in range(2, 6) if fc != sc],
    sign_1=['+', '-'],
    sign_2=['+', '-'],
    chargeLetter=['q', 'Q'],
    letter=['l', 'd', 'r'],
)
class ExchangeTask(variant.VariantTask):
    def GetUpdate(self, sign_1=None, sign_2=None, chargeLetter=None, letter=None, first_charge=None, second_charge=None, **kws):
        charges = [
            '{}{}{}'.format(sign_1, first_charge, chargeLetter),
            '{}{}{}'.format(sign_2, second_charge, chargeLetter),
        ]
        return dict(
            res=[
                u'притяжение' if first_charge * second_charge < 0 else u'отталкивание',
                u'отталкивание',
            ],
            charges=charges,
        )


@variant.text(u'''
    На координатной плоскости в точках $(-{letter}; 0)$ и $({letter}; 0)$
    находятся заряды, соответственно, ${charges[0]}$ и ${charges[1]}$.
    Сделайте рисунок, определите величину напряжённости электрического поля
    в точках ${firstCoords}$ и ${secondCoords}$ и укажите её направление.
''')
@variant.args(
    firstPoint__secondPoint=itertools.product(['up', 'down'], ['right', 'left']),
    charges=[['+q', '-q'], ['-q', '-q'], ['+Q', '+Q'], ['-Q', '+Q']],
    letter=['a', 'l', 'r', 'd'],
)
class FieldTaskGenerator(variant.VariantTask):
    def GetUpdate(self, firstPoint=None, secondPoint=None, letter='l', **kws):
        coords = {
            'up': '(0; {})'.format(letter),
            'down': '(0; -{})'.format(letter),
            'left': '(-2{}; 0)'.format(letter),
            'right': '(2{}; 0)'.format(letter),
        }
        return dict(
            firstCoords=coords[firstPoint],
            secondCoords=coords[secondPoint],
        )


@variant.text(u'''
    Заряд $q_1$ создает в точке $A$ электрическое поле
    по величине равное~$E_1={values[0]}\\funits{ В }{ м }$,
    а $q_2$~---$E_2={values[1]}\\funits{ В }{ м }$.
    Угол между векторами $\\vect{ E_1 }$ и $\\vect{ E_2 }$ равен ${angleLetter}$.
    Определите величину суммарного электрического поля в точке $A$,
    создаваемого обоими зарядами $q_1$ и $q_2$.
    Сделайте рисунок и вычислите её значение для двух значений угла ${angleLetter}$:
    ${angleLetter}_1={angles[0]}^\\circ$ и ${angleLetter}_2={angles[1]}^\\circ$.
''')
@variant.args(
    values__angles=[
        ((120, 50), (90, 180)),
        ((50, 120), (0, 90)),
        ((500, 500), (0, 120)),
        ((200, 200), (0, 60)),
        ((24, 7), (90, 180)),
        ((7, 24), (0, 90)),
        ((72, 72), (0, 120)),
        ((250, 250), (0, 60)),
        ((300, 400), (90, 180)),
        ((300, 400), (0, 90)),
    ],
    angleLetter=['\\alpha', '\\varphi'],
)
class SumTask(variant.VariantTask):
    pass


@variant.text(u'''
    В однородном электрическом поле напряжённостью {E:Task:e}
    переместили заряд {q:Task:e} в направлении силовой линии
    на {l:Task:e}. Определите работу поля, изменение потенциальной энергии заряда,
    напряжение между начальной и конечной точками перемещения.
''')
@variant.answer_short(u'''
    A   = {E.Letter}{q.Letter}{l.Letter}
        = {E:Value} \\cdot {q:Value} \\cdot {l:Value}
        = {A:.2f} \\cdot 10^{ -7 } \\units{ Дж }
''')
@variant.args(
    q=[u'%s = %d нКл' % (ql, qv) for ql in ['Q', 'q'] for qv in [-10, 10, -25, 25, -40, 40]],
    l=[u'%s = %d см' % (ll, lv) for ll in ['l', 'r', 'd'] for lv in [2, 4, 5, 10]],
    E=[u'E = %d кВ / м' % ev for ev in [2, 4, 20]],
)
class Potential728(variant.VariantTask):  # 728(737) - Rymkevich
    def GetUpdate(self, l=None, q=None, E=None, **kws):
        return dict(
            A=1. * E.Value * q.Value * l.Value,
        )


@variant.text(u'''
    Напряжение между двумя точками, лежащими на одной линии напряжённости однородного электрического поля,
    равно ${U.Letter}={U:Value}$. Расстояние между точками ${l.Letter}={l:Value}$.
    Какова напряжённость этого поля?
''')
@variant.args(
    U=[u'%s = %d кВ' % (ul, uv) for ul in ['U', 'V'] for uv in [2, 3, 4, 5, 6]],
    l=[u'%s = %d см' % (ll, lv) for ll in ['l', 'r', 'd'] for lv in [10, 20, 30, 40]],
)
class Potential735(variant.VariantTask):  # 735(737) - Rymkevich
    pass


@variant.text(u'''
    Найти напряжение между точками $A$ и $B$ в однородном электрическом поле (см. рис. на доске), если
    $AB={l.Letter}={l:Value}$,
    ${alpha.Letter}={alpha:Value}^\\circ$,
    ${E.Letter}={E:Value}$.
    Потенциал какой из точек $A$ и $B$ больше?
''')
@variant.args(
    l=[u'%s = %d см' % (ll, lv) for ll in ['l', 'r', 'd'] for lv in [4, 6, 8, 10, 12]],
    alpha=[u'%s = %d' % (al, av) for al in ['\\alpha', '\\varphi'] for av in [30, 45, 60]],
    E=[u'E = %d В / м' % ev for ev in [30, 50, 60, 100, 120]],
)
class Potential737(variant.VariantTask):  # 737(739) - Rymkevich
    pass


@variant.text(u'''
    При какой скорости электрона его кинетическая энергия равна $E_\\text{ к } = {E}\\units{ эВ }?$
''')
@variant.args(
    E=[4, 8, 20, 30, 40, 50, 200, 400, 600, 1000],
)
class Potential2335(variant.VariantTask):  # 2335 Gendenshteyn
    pass


@variant.text(u'''
    Электрон $e^-$ вылетает из точки, потенциал которой ${V.Letter} = {V:Value}$,
    со скоростью ${v.Letter} = {v:Value}$ в направлении линий напряжённости поля.
    Будет поле ускорять или тормозить электрон?
    Каков потенциал точки, дойдя до которой электрон остановится?
''')
@variant.args(
    v=[u'v = %d000000 м / с' % vv for vv in [3, 4, 6, 10, 12]],
    V=[u'\\varphi = %d В' % Vv for Vv in [200, 400, 600, 800, 1000]],
)
class Potential1621(variant.VariantTask):  # 1621 Goldfarb
    pass


@variant.text(u'''
    Определите ёмкость конденсатора, если при его зарядке до напряжения
    {U:Task:e} он приобретает заряд {Q:Task:e}.
    Чему при этом равны заряды обкладок конденсатора (сделайте рисунок)?
''')
@variant.answer_short(u'''
    {Q:Letter} = {C:Letter}{U:Letter} \\implies
    {C:Letter} = \\frac{Q:Letter:s}{U:Letter:s} = \\frac{Q:Value:s}{U:Value:s} = {C:Value}.
    \\text{ Заряды обкладок: ${Q:Letter}$ и $-{Q:Letter}$ }
''')
@variant.args(
    U=[u'%s = %d кВ' % (Ul, Uv) for Ul in ['U', 'V'] for Uv in [2, 3, 5, 6, 12, 15, 20]],
    Q=[u'%s = %d нКл' % (ql, qv) for ql in ['Q', 'q'] for qv in [4, 6, 15, 18, 24, 25]],
)
class Rymkevich748(variant.VariantTask):
    def GetUpdate(self, U=None, Q=None, **kws):
        return dict(
            C=u'C = %.2f пФ' % (1. * Q.Value / U.Value)
        )


@variant.text(u'''
    На конденсаторе указано: {C:Task:e}, {U:Task:e}.
    Удастся ли его использовать для накопления заряда {Q:Task:e}?
''')
@variant.answer_short(u'''
    {Q_new:Letter} = {C:Letter}{U:Letter} = {C:Value} \\cdot {U:Value} = {Q:Value}
    \\implies {Q_new:Letter} {sign} {Q:Letter} \\implies \\text{ {result} }
''')
@variant.args(
    U=[u'%s = %d кВ' % (Ul, Uv) for Ul in ['U', 'V'] for Uv in [200, 300, 400, 450]],
    Q=[u'%s = %d нКл' % (Ql, Qv) for Ql in ['Q', 'q'] for Qv in [30, 50, 60]],
    C=[u'C = %d пФ' % Cv for Cv in [50, 80, 100, 120, 150]],
)
class Rymkevich750(variant.VariantTask):
    def GetUpdate(self, U=None, Q=None, C=None, **kws):
        resultQ = C.Value * U.Value
        if resultQ >= Q.Value:
            sign = '\\ge'
            result = u'удастся'
        else:
            sign = '\\less'
            result = u'не удастся'
        return dict(
            Q_new=u'%s_{max} = %d нКл' % (Q.Letter, resultQ),
            sign=sign,
            result=result,
        )


@variant.text(u'''
    Как и во сколько раз изменится ёмкость плоского конденсатора при уменьшении площади пластин в {a} раз
    и уменьшении расстояния между ними в {b} раз?
''')
@variant.answer_short(u'''
    \\frac{ C' }{ C }
        = \\frac{ \\eps_0\\eps \\frac S{a} }{ \\frac d{b} } \\Big/ \\frac{ \\eps_0\\eps S }{ d }
        = \\frac{  {b}  }{  {a}  } {sign} 1 \\implies \\text{ {result} }
''')
@variant.args(
    a=[2, 3, 4, 5, 6, 7, 8],
    b=[2, 3, 4, 5, 6, 7, 8],
)
class Rymkevich751(variant.VariantTask):
    def GetUpdate(self, a=None, b=None, **kws):
        value = fractions.Fraction(numerator=b, denominator=a)
        if value == 1:
            sign = '='
            result = u'не изменится'
        else:
            if value > 1:
                sign = '>'
                result = u'увеличится'
            elif value < 1:
                sign = '<'
                result = u'уменьшится'
                value = 1 / value
            result += u' в $\\frac{value.numerator}{value.denominator}$ раз'.format(value=value)
        return dict(
            sign=sign,
            result=result,
        )


@variant.text(u'''
    Электрическая ёмкость конденсатора равна {C:Task:e},
    при этом ему сообщён заряд {Q:Task:e}. Какова энергия заряженного конденсатора?
''')
@variant.answer_short(u'''
    {W:Letter}
    = \\frac{ {Q:Letter}^2 }{ 2{C:Letter} }
    = \\frac{ \\sqr{Q:Value:s} }{ 2 \\cdot {C:Value} }
    = {W:Value}
''')
@variant.args(
    Q=[u'%s = %s нКл' % (Ql, Qv) for Ql in ['Q', 'q'] for Qv in [300, 500, 800, 900]],
    C=[u'С = %s пФ' % Cv for Cv in [200, 400, 600, 750]],
)
class Rymkevich762(variant.VariantTask):
    def GetUpdate(self, C=None, Q=None, **kws):
        return dict(
            W=u'W = %.2f мкДж' % (1. * Q.Value ** 2 / 2 / C.Value),
        )


@variant.text(u'''
    Два конденсатора ёмкостей {C1:Task:e} и {C2:Task:e} последовательно подключают
    к источнику напряжения {U:Task:e} (см. рис.). Определите заряды каждого из конденсаторов.
''')
@variant.answer_short(u'''
    Q_1
        = Q_2
        = C{U:Letter}
        = \\frac{ {U:Letter} }{ \\frac1{ C_1 } + \\frac1{ C_2 } }
        = \\frac{ C_1C_2{U:Letter} }{ C_1 + C_2 }
        = \\frac{
            {C1:Value} \\cdot {C2:Value} \\cdot {U:Value}
         }{
            {C1:Value} + {C2:Value}
         }
        = {Q:Value}
''')
@variant.args(
    C1__C2=[(u'С_1 = %s нФ' % C1, u'С_2 = %s нФ' % C2) for C1 in [20, 30, 40, 60] for C2 in [20, 30, 40, 60] if C1 != C2],
    U=[u'%s = %s В' % (Ul, Uv) for  Ul in ['U', 'V'] for Uv in [150, 200, 300, 400, 450]],
)
class Cond1(variant.VariantTask):
    def GetUpdate(self, C1=None, C2=None, U=None, **kws):
        return dict(
            Q=u'Q = %.2f нКл' % (1. * C1.Value * C2.Value * U.Value / (C1.Value + C2.Value)),
        )


@variant.text(u'''
    На резистор сопротивлением {R:Task:e} подали напряжение {U:Task:e}.
    Определите ток, который потечёт через резистор, и мощность, выделяющуюся на нём.
''')
@variant.answer_align([
    u'{I:Letter} &= \\frac{U:Letter:s}{R:Letter:s} = \\frac{U:Value:s}{R:Value:s} = {I:Value}, ',
    u'{P:Letter} &= \\frac{ {U:Letter}^2 }{R:Letter:s} = \\frac{U:Value|sqr|s}{R:Value:s} = {P:Value}',
])
@variant.args(
    R=[u'%s = %d Ом' % (rLetter, rValue) for rLetter, rValue in itertools.product(['r', 'R'], [5, 12, 18, 30])],
    U=[u'%s = %d В' % (uLetter, uValue) for uLetter, uValue in itertools.product(['U', 'V'], [120, 150, 180, 240])],
)
class Rezistor1_v1(variant.VariantTask):
    def GetUpdate(self, R=None, U=None, **kws):
        return dict(
            I=u'\\mathcal{I} = %.2f А' % (1. * U.Value / R.Value),
            P=u'P = %.2f Вт' % (1. * U.Value ** 2 / R.Value),
        )


@variant.text(u'''
    Через резистор сопротивлением {R:Task:e} протекает электрический ток {I:Task:e}.
    Определите, чему равны напряжение на резисторе и мощность, выделяющаяся на нём.
''')
@variant.answer_align([
    u'{U:Letter} &= {I:Letter}{R:Letter} = {I:Value} \\cdot {R:Value} = {U:Value}, ',
    u'{P:Letter} &= {I:Letter}^2{R:Letter} = {I:Value|sqr|cdot} {R:Value} = {P:Value}',
])
@variant.args(
    R=[u'%s = %d Ом' % (rLetter, rValue) for rLetter, rValue in itertools.product(['r', 'R'], [5, 12, 18, 30])],
    I=[u'\\mathcal{I} = %.2f А' % iValue for iValue in [2, 3, 4, 5, 6, 8, 10, 15]],
)
class Rezistor1_v2(variant.VariantTask):
    def GetUpdate(self, R=None, I=None, U=None, **kws):
        return dict(
            U=u'U = %d В' % (I.Value * R.Value),
            P=u'P = %d Вт' % (I.Value ** 2 * R.Value),
        )


@variant.text(u'''
    Замкнутая электрическая цепь состоит из ЭДС {E:Task:e} и сопротивлением ${r:Letter}$
    и резистора {R:Task:e}. Определите ток, протекающий в цепи. Какая тепловая энергия выделится на резисторе за время
    {t:Task:e}? Какая работа будет совершена ЭДС за это время? Каков знак этой работы? Чему равен КПД цепи? Вычислите значения для 2 случаев:
    ${r:Letter}=0$ и {r:Task:e}.
''')
@variant.answer_align([
    u'''{I1:Letter} &= \\frac{E:Letter:s}{R:Letter:s} = \\frac{E:Value:s}{R:Value:s} = {I1:Value}, ''',
    u'''{I2:Letter} &= \\frac{E:Letter:s}{ {R:Letter} + {r:Letter} } = \\frac{E:Value:s}{ {R:Value} + {r:Value} } = {I2:Value}, ''',
    u'''{Q1:Letter} &= {I1:Letter}^2{R:Letter}{t:Letter} = \\sqr{ \\frac{E:Letter:s}{R:Letter:s} } {R:Letter} {t:Letter}
        = \\sqr{ \\frac{E:Value:s}{R:Value:s} } \\cdot {R:Value|cdot} \\cdot {t:Value} = {Q1:Value}, ''',
    u'''{Q2:Letter} &= {I2:Letter}^2{R:Letter}{t:Letter} = \\sqr{ \\frac{E:Letter:s}{ {R:Letter} + {r:Letter} } } {R:Letter} {t:Letter}
        = \\sqr{ \\frac{E:Value:s}{ {R:Value} + {r:Value} } } \\cdot {R:Value} \\cdot {t:Value} = {Q2:Value}, ''',
    u'''{A1:Letter} &= {I1:Letter}{t:Letter}{E:Letter} = \\frac{E:Letter:s}{ {R:Letter} } {t:Letter} {E:Letter}
        = \\frac{ {E:Letter}^2 {t:Letter} }{R:Letter|s} = \\frac{ {E:Value|sqr|cdot} {t:Value} }{R:Value:s}
        = {A1:Value}, \\text{ положительна }, ''',
    u'''{A2:Letter} &= {I2:Letter}{t:Letter}{E:Letter} = \\frac{E:Letter:s}{ {R:Letter} + {r:Letter} } {t:Letter} {E:Letter}
        = \\frac{ {E:Letter}^2 {t:Letter} }{ {R:Letter} + {r:Letter} } = \\frac{ {E:Value|sqr|cdot} {t:Value} }{ {R:Value} + {r:Value} }
        = {A2:Value}, \\text{ положительна }, ''',
    u'''{eta1:Letter} &= \\frac{Q1:Letter:s}{A1:Letter:s} = \\ldots = \\frac{R:Letter:s}{R:Letter:s} = 1, ''',
    u'''{eta2:Letter} &= \\frac{Q2:Letter:s}{A2:Letter:s} = \\ldots = \\frac{R:Letter:s}{ {R:Letter} + {r:Letter} } = {eta2:Value}''',
])
@variant.args(
    E=[u'\\mathcal{E} = %d В' % E for E in [1, 2, 3, 4]],
    R=[u'R = %d Ом' % R for R in [10, 15, 24, 30]],
    r=[u'r = %d Ом' % r for r in [10, 20, 30, 60]],
    t=[u'\\tau = %d с' % t for t in [2, 5, 10]],
)
class Rezistor2(variant.VariantTask):
    def GetUpdate(self, r=None, R=None, E=None, t=None, **kws):
        I1 = UnitValue(u'\\mathcal{I}_1 = %.2f А' % (1. * E.Value / R.Value))
        I2 = UnitValue(u'\\mathcal{I}_2 = %.2f А' % (1. * E.Value / (R.Value + r.Value)))
        Q1 = UnitValue(u'Q_1 = %.3f Дж' % (1. * I1.Value ** 2 * R.Value * t.Value))
        Q2 = UnitValue(u'Q_2 = %.3f Дж' % (1. * I2.Value ** 2 * R.Value * t.Value))
        A1 = UnitValue(u'A_1 = %.3f Дж' % (1. * I1.Value * E.Value * t.Value))
        A2 = UnitValue(u'A_2 = %.3f Дж' % (1. * I2.Value * E.Value * t.Value))
        return dict(
            I1=I1,
            I2=I2,
            Q1=Q1,
            Q2=Q2,
            A1=A1,
            A2=A2,
            eta1=u'\\eta_1 = %.2f' % (1. * Q1.Value / A1.Value),
            eta2=u'\\eta_2 = %.2f' % (1. * Q2.Value / A2.Value),
        )


@variant.text(u'''
    Лампочки, сопротивления которых {R1:Task:e} и {R2:Task:e}, поочерёдно подключённные к некоторому источнику тока,
    потребляют одинаковую мощность. Найти внутреннее сопротивление источника и КПД цепи в каждом случае.
''')
@variant.answer_align([
    u'''
    P_1 &= \\sqr{ \\frac{E:Letter:s}{ {R1:Letter} + {r:Letter} } }{R1:Letter},
    P_2  = \\sqr{ \\frac{E:Letter:s}{ {R2:Letter} + {r:Letter} } }{R2:Letter},
    P_1 = P_2 \\implies ''',
    u'''
    &\\implies {R1:Letter} \\sqr{ {R2:Letter} + {r:Letter} } = {R2:Letter} \\sqr{ {R1:Letter} + {r:Letter} } \\implies ''',
    u'''
    &\\implies {R1:Letter} {R2:Letter}^2 + 2 {R1:Letter} {R2:Letter} {r:Letter} + {R1:Letter} {r:Letter}^2 =
                {R2:Letter} {R1:Letter}^2 + 2 {R2:Letter} {R1:Letter} {r:Letter} + {R2:Letter} {r:Letter}^2  \\implies ''',
    u'''&\\imuplies {r:Letter}^2 ({R2:Letter} - {R1:Letter}) = {R2:Letter}^2 {R2:Letter} - {R1:Letter}^2 {R2:Letter} \\implies ''',
    u'''&\\implies {r:Letter}
        = \\sqrt{ {R1:Letter} {R2:Letter} \\frac{ {R2:Letter} - {R1:Letter} }{ {R2:Letter} - {R1:Letter} } }
        = \\sqrt{ {R1:Letter} {R2:Letter} }
        = \\sqrt{ {R1:Value|cdot} {R2:Value} }
        = {r:Value}. '''
   ,
   u'''{eta1:Letter}
        &= \\frac{R1:Letter:s}{ {R1:Letter} + {r:Letter} }
        = \\frac{ {R1:Letter|sqrt} }{ {R1:Letter|sqrt} + {R2:Letter|sqrt} }
        = {eta1:Value}, '''
   ,
   u'''{eta2:Letter}
        &= \\frac{R2:Letter:s}{ {R2:Letter} + {r:Letter} }
        = \\frac{R2:Letter|sqrt|s}{ {R2:Letter|sqrt} + {R1:Letter|sqrt} }
        = {eta2:Value}''',
])
@variant.args(
    R1__R2=[(u'R_1 = %.2f Ом' % R_1, u'R_2 = %.2f Ом' % R_2) for R_1, R_2 in [
        (0.25, 16), (0.25, 64), (0.25, 4),
        (0.5, 18),  (0.5, 2),   (0.5, 4.5),
        (1, 4),     (1, 9),     (1, 49),
        (3, 12),    (3, 48),
        (4, 36),    (4, 100),
        (5, 45),    (5, 80),
        (6, 24),    (6, 54),
    ]],
)
class Rezistor3(variant.VariantTask):
    def GetUpdate(self, R1=None, R2=None, **kws):
        r = UnitValue(u'r = %.2f Ом' % ((1. * R1.Value * R2.Value) ** 0.5))
        return dict(
            R1=R1,
            R2=R2,
            r=r,
            eta1=u'\\eta_1 = %.3f ' % (1. * R1.Value / (R1.Value + r.Value)),
            eta2=u'\\eta_2 = %.3f ' % (1. * R2.Value / (R2.Value + r.Value)),
            E=u'\\mathcal{E} = 1234 В',
        )


@variant.text(u'''
    Определите ток, протекающий через резистор {R:Task:e} и разность потенциалов на нём (см. рис. на доске),
    если {r1:Task:e}, {r2:Task:e}, {E1:Task:e}, {E2:Task:e}
''')
@variant.args(
    R=[u'R = %d Ом' % RValue for RValue in [10, 12, 15, 18, 20]],
    r1=[u'r_1 = %d Ом' % r1Value for r1Value in [1, 2, 3]],
    r2=[u'r_2 = %d Ом' % r2Value for r2Value in [1, 2, 3]],
    E1=[u'\\mathcal{E}_1 = %d В' % E1Value for E1Value in [20, 30, 40, 60]],
    E2=[u'\\mathcal{E}_2 = %d В' % E2Value for E2Value in [20, 30, 40, 60]],
)
class Rezistor4(variant.VariantTask):
    pass
