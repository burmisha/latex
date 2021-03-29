import itertools

import generators.variant as variant
from generators.helpers import Consts, Fraction


@variant.text('''
    С какой силой взаимодействуют 2 точечных заряда {first:Task:e} и {second:Task:e},
    находящиеся на расстоянии {distance:Task:e}?
''')
@variant.answer_short('''
    F
        = k\\frac{ {first:L}{second:L} }{ {distance:L}^2 }
        = {Consts.k:Value} * \\frac{ {first:Value} *{second:Value} }{ {distance:Value|sqr} }
        = {value:LaTeX} * 10^{ {power} }\\units{ Н }
          \\approx { {approx:.2f} } * 10^{ {power} }\\units{ Н }
''')
@variant.arg(first__second=[('q_1 = %d нКл' % f, 'q_2 = %d нКл' % s) for f in range(2, 5) for s in range(2, 5) if f != s])
@variant.arg(distance=['%s = %d см' % (l, d) for d in [2, 3, 5, 6] for l in ['r', 'l', 'd'] ])
class ForceTask(variant.VariantTask):
    def GetUpdate(self, first=None, second=None, distance=None, **kws):
        # answer = kqq/r**2
        value = Fraction() * first.Value * second.Value * Consts.k.Value / (distance.Value ** 2)
        return dict(
            value=value,
            power=Consts.k.Power - first.Power - second.Power - 2 * distance.Power,
            approx=float(value._fraction),
            distance=distance,
        )


@variant.text('''
    Два одинаковых маленьких проводящих заряженных шарика находятся на расстоянии~${letter}$ друг от друга.
    Заряд первого равен~${charges[0]}$, второго~--- ${charges[1]}$.
    Шарики приводят в соприкосновение, а после опять разводят на расстояние~${n}{letter}$.
    \\begin{{itemize}}
        \\item Каким стал заряд каждого из шариков?
        \\item Определите характер (притяжение или отталкивание) и силу взаимодействия шариков до и после соприкосновения.
        \\item Как изменилась сила взаимодействия шариков после соприкосновения?
    \\end{{itemize}}
''')
@variant.answer_align([
    'F &= k\\frac{ q_1 q_2 }{ \\sqr{ {n} {letter} } } = k\\frac{ ({charges[0]}) * ({charges[1]}) }{ \\sqr{ {n} {letter} } }, \\text{ {res[0]} };',
    '''
    q'_1 = q'_2 = \\frac{ q_1 + q_2 }2 = \\frac{ {charges[0]} + {charges[1]} }2 \\implies
    F'  &= k\\frac{ q'_1 q'_2 }{ {letter}^2 }
        = k\\frac{ \\sqr{ \\frac{ ({charges[0]}) + ({charges[1]}) }2 } }{ {n}^2 * {letter}^2 },
    \\text{ {res[1]} }.'''
])
@variant.arg(first_charge__second_charge=[(fc, sc) for fc in range(3, 9, 2) for sc in range(2, 10, 2)])
@variant.arg(n=[2, 3, 4])
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
    и укажите её направление в двух точках: ${firstCoords}$ и ${secondCoords}$.
''')
@variant.arg(firstPoint__secondPoint=list(itertools.product(['up', 'down'], ['right', 'left'])))
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
    а $q_2$~--- $E_2={values[1]}\\funits{ В }{ м }$.
    Угол между векторами $\\vect{ E_1 }$ и $\\vect{ E_2 }$ равен ${angleLetter}$.
    Определите величину суммарного электрического поля в точке $A$,
    создаваемого обоими зарядами $q_1$ и $q_2$.
    Сделайте рисунки и вычислите значение для двух значений угла ${angleLetter}$:
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



@variant.solution_space(0)
@variant.text('''
    \\begin{{enumerate}}
        \\item Запишите (формулой) {first}.
        \\item Зарисуйте электрическое поле точечного {second} электрического заряда.
        \\item Запишите формулу для вычисления {third} электрического поля точечного заряда.
        \\item Запишите принцип суперпозиции (правило сложения) {fourth}.
    \\end{{enumerate}}
''')
@variant.arg(first=['закон Кулона (в вакууме)', 'закон сохранения электрического заряда'])
@variant.arg(second=['положительного', 'отрицательного'])
@variant.arg(third=['потенциала', 'напряжённости'])
@variant.arg(fourth=['потенциалов', 'напряжённостей'])
class Definitions01(variant.VariantTask):
    pass

