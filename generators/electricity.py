# -*- coding: utf-8 -*-

import itertools
import fractions

import generators.variant as variant
from generators.value import Consts, UnitValue

import logging
log = logging.getLogger(__name__)


@variant.text('''
    С какой силой взаимодействуют 2 точечных заряда {first:Task:e} и {second:Task:e},
    находящиеся на расстоянии {distance:Task:e}?
''')
@variant.answer_short('''
    F
        = k\\frac{ {first:L}{second:L} }{ {distance:L}^2 }
        = {Consts.k:Value} * \\frac{ {first:Value} *{second:Value} }{ {distance:Value|sqr} }
        = \\frac{ {value.numerator} }{ {value.denominator} } * 10^{ {power} }\\units{ Н }
          \\approx { {approx:.2f} } * 10^{ {power} }\\units{ Н }
''')
@variant.arg(first__second=[('q_1 = %d нКл' % f, 'q_2 = %d нКл' % s) for f in range(2, 5) for s in range(2, 5) if f != s])
@variant.arg(distance=['%s = %d см' % (l, d) for d in [2, 3, 5, 6] for l in ['r', 'l', 'd'] ])
class ForceTask(variant.VariantTask):
    def GetUpdate(self, first=None, second=None, distance=None, **kws):
        # answer = kqq/r**2
        value = fractions.Fraction(
            numerator=first.Value * second.Value * Consts.k.Value,
            denominator=distance.Value ** 2,
        )
        return dict(
            value=value,
            power=Consts.k.Power - first.Power - second.Power - 2 * distance.Power,
            approx=float(value),
            distance=distance,
        )


@variant.text('''
    Два одинаковых маленьких проводящих заряженных шарика находятся
    на расстоянии~${letter}$ друг от друга.
    Заряд первого равен~${charges[0]}$, второго~---${charges[1]}$.
    Шарики приводят в соприкосновение, а после опять разводят на то же самое расстояние~${letter}$.
    Каким стал заряд каждого из шариков?
    Определите характер (притяжение или отталкивание)
    и силу взаимодействия шариков до и после соприкосновения.
''')
@variant.answer_align([
    'F &= k\\frac{ q_1 q_2 }{ {letter}^2 } = k\\frac{ ({charges[0]}) * ({charges[1]}) }{ {letter}^2 }, \\text{ {res[0]} };',
    '''
    q'_1 = q'_2 = \\frac{ q_1 + q_2 }2 = \\frac{ {charges[0]} + {charges[1]} }2 \\implies
    F'  &= k\\frac{ q'_1 q'_2 }{ {letter}^2 }
        = k\\frac{ \\sqr{ \\frac{ ({charges[0]}) + ({charges[1]}) }2 } }{ {letter}^2 },
    \\text{ {res[1]} }.'''
])
@variant.arg(first_charge__second_charge=[(fc, sc) for fc in range(2, 6) for sc in range(2, 6) if fc != sc])
@variant.arg(sign_1=['+', '-'])
@variant.arg(sign_2=['+', '-'])
@variant.arg(chargeLetter=['q', 'Q'])
@variant.arg(letter=['l', 'd', 'r'])
class ExchangeTask(variant.VariantTask):
    def GetUpdate(self, sign_1=None, sign_2=None, chargeLetter=None, letter=None, first_charge=None, second_charge=None, **kws):
        charges = [
            '{}{}{}'.format(sign_1, first_charge, chargeLetter),
            '{}{}{}'.format(sign_2, second_charge, chargeLetter),
        ]
        return dict(
            res=[
                'притяжение' if first_charge * second_charge < 0 else 'отталкивание',
                'отталкивание',
            ],
            charges=charges,
        )


@variant.text('''
    На координатной плоскости в точках $(-{letter}; 0)$ и $({letter}; 0)$
    находятся заряды, соответственно, ${charges[0]}$ и ${charges[1]}$.
    Сделайте рисунок, определите величину напряжённости электрического поля
    в точках ${firstCoords}$ и ${secondCoords}$ и укажите её направление.
''')
@variant.arg(firstPoint__secondPoint=itertools.product(['up', 'down'], ['right', 'left']))
@variant.arg(charges=[['+q', '-q'], ['-q', '-q'], ['+Q', '+Q'], ['-Q', '+Q']])
@variant.arg(letter=['a', 'l', 'r', 'd'])
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


@variant.text('''
    Заряд $q_1$ создает в точке $A$ электрическое поле
    по величине равное~$E_1={values[0]}\\funits{ В }{ м }$,
    а $q_2$~---$E_2={values[1]}\\funits{ В }{ м }$.
    Угол между векторами $\\vect{ E_1 }$ и $\\vect{ E_2 }$ равен ${angleLetter}$.
    Определите величину суммарного электрического поля в точке $A$,
    создаваемого обоими зарядами $q_1$ и $q_2$.
    Сделайте рисунок и вычислите её значение для двух значений угла ${angleLetter}$:
    ${angleLetter}_1={angles[0]}^\\circ$ и ${angleLetter}_2={angles[1]}^\\circ$.
''')
@variant.arg(values__angles=[
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
])
@variant.arg(angleLetter=['\\alpha', '\\varphi'])
class SumTask(variant.VariantTask):
    pass


@variant.text('''
    В однородном электрическом поле напряжённостью {E:Task:e}
    переместили заряд {q:Task:e} в направлении силовой линии
    на {l:Task:e}. Определите работу поля, изменение потенциальной энергии заряда,
    напряжение между начальной и конечной точками перемещения.
''')
@variant.answer_short('''
    A   = {E:L}{q:L}{l:L}
        = {E:Value} * {q:Value} * {l:Value}
        = {A:.2f} * 10^{ -7 } \\units{ Дж }
''')
@variant.arg(q=['%s = %d нКл' % (ql, qv) for ql in ['Q', 'q'] for qv in [-10, 10, -25, 25, -40, 40]])
@variant.arg(l=['%s = %d см' % (ll, lv) for ll in ['l', 'r', 'd'] for lv in [2, 4, 5, 10]])
@variant.arg(E=['E = %d кВ / м' % ev for ev in [2, 4, 20]])
class Potential728(variant.VariantTask):  # 728(737) - Rymkevich
    def GetUpdate(self, l=None, q=None, E=None, **kws):
        return dict(
            A=1. * E.Value * q.Value * l.Value,
        )


@variant.text('''
    Напряжение между двумя точками, лежащими на одной линии напряжённости однородного электрического поля,
    равно {U:Task:e}. Расстояние между точками {l:Task:e}.
    Какова напряжённость этого поля?
''')
@variant.arg(U=['%s = %d кВ' % (ul, uv) for ul in ['U', 'V'] for uv in [2, 3, 4, 5, 6]])
@variant.arg(l=['%s = %d см' % (ll, lv) for ll in ['l', 'r', 'd'] for lv in [10, 20, 30, 40]])
class Potential735(variant.VariantTask):  # 735(737) - Rymkevich
    pass


@variant.text('''
    Найти напряжение между точками $A$ и $B$ в однородном электрическом поле (см. рис. на доске), если
    $AB={l:Task}$,
    ${alpha:L}={alpha:Value}^\\circ$,
    {E:Task:e}.
    Потенциал какой из точек $A$ и $B$ больше?
''')
@variant.arg(l=['%s = %d см' % (ll, lv) for ll in ['l', 'r', 'd'] for lv in [4, 6, 8, 10, 12]])
@variant.arg(alpha=['%s = %d' % (al, av) for al in ['\\alpha', '\\varphi'] for av in [30, 45, 60]])
@variant.arg(E=['E = %d В / м' % ev for ev in [30, 50, 60, 100, 120]])
class Potential737(variant.VariantTask):  # 737(739) - Rymkevich
    pass


@variant.text('''
    При какой скорости электрона его кинетическая энергия равна $E_\\text{ к } = {E:Value}?$
''')
@variant.arg(E=['E = %d эВ' % E for E in [4, 8, 20, 30, 40, 50, 200, 400, 600, 1000]])
class Potential2335(variant.VariantTask):  # 2335 Gendenshteyn
    pass


@variant.text('''
    Электрон $e^-$ вылетает из точки, потенциал которой {V:Task:e},
    со скоростью {v:Task:e} в направлении линий напряжённости поля.
    Будет поле ускорять или тормозить электрон?
    Каков потенциал точки, дойдя до которой электрон остановится?
''')
@variant.arg(v=['v = %d000000 м / с' % vv for vv in [3, 4, 6, 10, 12]])
@variant.arg(V=['\\varphi = %d В' % Vv for Vv in [200, 400, 600, 800, 1000]])
class Potential1621(variant.VariantTask):  # 1621 Goldfarb
    pass


@variant.solution_space(40)
@variant.text('''
    Напротив физических величин укажите их обозначения и единицы измерения в СИ:
    \\begin{{enumerate}}
        \\item ёмкость конденсатора,
        \\item индуктивность.
    \\end{{enumerate}}
''')
@variant.no_args
class Definitions01(variant.VariantTask):
    pass


@variant.solution_space(40)
@variant.text('''
    Запишите формулы, выражающие:
    \\begin{{enumerate}}
        \\item заряд кондесатора через его ёмкость и поданное напряжение,
        \\item энергию кондесатора через {v_1},
        \\item {v_2} колебаний в электромагнитном контуре, состоящем из конденсатора и катушки индуктивности,
    \\end{{enumerate}}
''')
@variant.arg(v_1=['его ёмкость и поданное напряжение', 'его ёмкость и заряд', 'его заряд и поданное напряжение'])
@variant.arg(v_2=['период', 'частоту'])
class Definitions02(variant.VariantTask):
    pass


@variant.text('''
    Определите ёмкость конденсатора, если при его зарядке до напряжения
    {U:Task:e} он приобретает заряд {Q:Task:e}.
    Чему при этом равны заряды обкладок конденсатора (сделайте рисунок и укажите их)?
''')
@variant.answer_short('''
    {Q:L} = {C:L}{U:L} \\implies
    {C:L} = \\frac{Q:L:s}{U:L:s} = \\frac{Q:Value:s}{U:Value:s} = {C:Value}.
    \\text{ Заряды обкладок: ${Q:L}$ и $-{Q:L}$ }
''')
@variant.arg(U=['%s = %d кВ' % (Ul, Uv) for Ul in ['U', 'V'] for Uv in [2, 3, 5, 6, 12, 15, 20]])
@variant.arg(Q=['%s = %d нКл' % (ql, qv) for ql in ['Q', 'q'] for qv in [4, 6, 15, 18, 24, 25]])
class Rymkevich748(variant.VariantTask):
    def GetUpdate(self, U=None, Q=None, **kws):
        return dict(
            C='C = %.2f пФ' % (1. * Q.Value / U.Value)
        )


@variant.solution_space(80)
@variant.text('''
    На конденсаторе указано: {C:Task:e}, {U:Task:e}.
    Удастся ли его использовать для накопления заряда {Q:Task:e}?
''')
@variant.answer_short('''
    {Q_max:L} = {C:L}{U:L} = {C:Value} * {U:Value} = {Q_max:Value}
    \\implies {Q_max:L} {sign} {Q:L} \\implies \\text{ {result} }
''')
@variant.arg(U=['%s = %d В' % (Ul, Uv) for Ul in ['U', 'V'] for Uv in [200, 300, 400, 450]])
@variant.arg(Q=['%s = %d нКл' % (Ql, Qv) for Ql in ['Q', 'q'] for Qv in [30, 50, 60]])
@variant.arg(C=['C = %d пФ' % Cv for Cv in [50, 80, 100, 120, 150]])
class Rymkevich750(variant.VariantTask):
    def GetUpdate(self, U=None, Q=None, C=None, **kws):
        Q_max = C.Value * U.Value / 1000
        if Q_max >= Q.Value:
            sign = '\\ge'
            result = 'удастся'
        else:
            sign = ' < '
            result = 'не удастся'
        return dict(
            Q_max='%s_{ \\text{ max } } = %d нКл' % (Q.Letter, Q_max),
            sign=sign,
            result=result,
        )


@variant.solution_space(80)
@variant.text('''
    Как и во сколько раз изменится ёмкость плоского конденсатора при уменьшении площади пластин в {a} раз
    и уменьшении расстояния между ними в {b} раз?
''')
@variant.answer_short('''
    \\frac{ C' }{ C }
        = \\frac{ \\eps_0\\eps \\frac S{a} }{ \\frac d{b} } \\Big/ \\frac{ \\eps_0\\eps S }{ d }
        = \\frac{ {b} }{ {a} } {sign} 1 \\implies \\text{ {result} }
''')
@variant.arg(a=[2, 3, 4, 5, 6, 7, 8])
@variant.arg(b=[2, 3, 4, 5, 6, 7, 8])
class Rymkevich751(variant.VariantTask):
    def GetUpdate(self, a=None, b=None, **kws):
        value = fractions.Fraction(numerator=b, denominator=a)
        if value == 1:
            sign = '='
            result = 'не изменится'
        else:
            if value > 1:
                sign = '>'
                result = 'увеличится'
            elif value < 1:
                sign = '<'
                result = 'уменьшится'
                value = 1 / value
            result += ' в $\\frac{value.numerator}{value.denominator}$ раз'.format(value=value)
        return dict(
            sign=sign,
            result=result,
        )


@variant.solution_space(80)
@variant.text('''
    Электрическая ёмкость конденсатора равна {C:Task:e},
    при этом ему сообщён заряд {Q:Task:e}. Какова энергия заряженного конденсатора?
''')
@variant.answer_short('''
    {W:L}
    = \\frac{ {Q:L}^2 }{ 2{C:L} }
    = \\frac{ \\sqr{Q:Value:s} }{ 2 * {C:Value} }
    = {W:Value}
''')
@variant.arg(Q=['%s = %s нКл' % (Ql, Qv) for Ql in ['Q', 'q'] for Qv in [300, 500, 800, 900]])
@variant.arg(C=['C = %s пФ' % Cv for Cv in [200, 400, 600, 750]])
class Rymkevich762(variant.VariantTask):
    def GetUpdate(self, C=None, Q=None, **kws):
        return dict(
            W='W = %.2f мкДж' % (1. * Q.Value ** 2 / 2 / C.Value),
        )


@variant.text('''
    Два конденсатора ёмкостей {C1:Task:e} и {C2:Task:e} последовательно подключают
    к источнику напряжения {U:Task:e} (см. рис.). Определите заряды каждого из конденсаторов.
''')
@variant.answer_short('''
    Q_1
        = Q_2
        = C{U:L}
        = \\frac{ {U:L} }{ \\frac1{ C_1 } + \\frac1{ C_2 } }
        = \\frac{ C_1C_2{U:L} }{ C_1 + C_2 }
        = \\frac{
            {C1:Value} * {C2:Value} * {U:Value}
         }{
            {C1:Value} + {C2:Value}
         }
        = {Q:Value}
''')
@variant.arg(C1__C2=[('C_1 = %s нФ' % C1, 'C_2 = %s нФ' % C2) for C1 in [20, 30, 40, 60] for C2 in [20, 30, 40, 60] if C1 != C2])
@variant.arg(U=['%s = %s В' % (Ul, Uv) for  Ul in ['U', 'V'] for Uv in [150, 200, 300, 400, 450]])
class Cond1(variant.VariantTask):
    def GetUpdate(self, C1=None, C2=None, U=None, **kws):
        return dict(
            Q='Q = %.2f нКл' % (1. * C1.Value * C2.Value * U.Value / (C1.Value + C2.Value)),
        )


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
