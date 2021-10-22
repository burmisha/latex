import itertools

import generators.variant as variant
from generators.helpers import Consts, Fraction, n_times, n_word, permute


def sign_to_mult(line):
    return {
        '+': 1,
        '-': -1,
    }[line[0]]


@variant.text('''
    С какой силой взаимодействуют 2 точечных заряда {first:Task:e} и {second:Task:e},
    находящиеся на расстоянии {distance:Task:e}?
''')
@variant.answer_short('''
    F
        = k\\frac{{first:L}{second:L}}{{distance:L}^2}
        = {Consts.k:V} * \\frac{{first:V} * {second:V}}{{distance:V|sqr}}
        \\approx {F:V}
''')
@variant.arg(first__second=[('q_1 = %d нКл' % f, 'q_2 = %d нКл' % s) for f in range(2, 5) for s in range(2, 5) if f != s])
@variant.arg(distance=['%s = %d см' % (l, d) for d in [2, 3, 5, 6] for l in ['r', 'l', 'd'] ])
class ForceTask(variant.VariantTask):
    def GetUpdate(self, first=None, second=None, distance=None):
        F = Consts.k * first * second / distance / distance  # kqq/r**2
        mul = 10 ** 6
        return dict(
            F=f'F = {F.SI_Value * mul:.3f} мкН',
        )


@variant.text('''
    Два одинаковых маленьких проводящих заряженных шарика находятся на расстоянии~${letter}$ друг от друга.
    Заряд первого равен~${charges[0]}$, второго~--- ${charges[1]}$.
    Шарики приводят в соприкосновение, а после опять разводят на расстояние~${n}{letter}$.
    \\begin{itemize}
        \\item Каким стал заряд каждого из шариков?
        \\item Определите характер (притяжение или отталкивание) и силу взаимодействия шариков до и после соприкосновения.
        \\item Как изменилась сила взаимодействия шариков после соприкосновения?
    \\end{itemize}
''')
@variant.answer_align([
    'F &= k\\frac{\\abs{q_1}\\abs {q_2}}{\\sqr{{n} {letter}}}'
    '   = k\\frac{\\abs{{charges[0]}} * \\abs{{charges[1]}}}{{n}^2 * {letter}^2}, \\text{{res[0]}};',
    '''
    q'_1 &= q'_2, q_1 + q_2 = q'_1 + q'_2 \\implies  q'_1 = q'_2 = \\frac{q_1 + q_2}2 = \\frac{{charges[0]} + {charges[1]}}2 = {q_ratio:LaTeX}{chargeLetter} \\implies''',
    '''
    \\implies F'  &= k\\frac{\\abs{q'_1}\\abs{q'_2}}{\\sqr{{n} {letter}}}
        = k\\frac{\\sqr{{q_ratio:LaTeX}{chargeLetter}}}{{n}^2 * {letter}^2},
    \\text{{res[1]}},''',
    '\\frac{F\'}F &= \\frac{\\sqr{{q_ratio:LaTeX}{chargeLetter}}}{{n}^2 * \\abs{{charges[0]}} * \\abs{{charges[1]}}} = {ratio:LaTeX}.'
])
@variant.arg(first_charge__second_charge=[(fc, sc) for fc in range(3, 9, 2) for sc in range(2, 10, 2)])
@variant.arg(n=[2, 3, 4])
@variant.arg(sign_1=['+', '-'])
@variant.arg(sign_2=['+', '-'])
@variant.arg(chargeLetter=['q', 'Q'])
@variant.arg(letter=['l', 'd', 'r'])
class ExchangeTask(variant.VariantTask):
    def GetUpdate(self, sign_1=None, sign_2=None, chargeLetter=None, letter=None, first_charge=None, second_charge=None, n=None):
        charges = [
            '{}{}{}'.format(sign_1, first_charge, chargeLetter),
            '{}{}{}'.format(sign_2, second_charge, chargeLetter),
        ]
        q_ratio = Fraction(1) * (sign_to_mult(sign_1) * first_charge + sign_to_mult(sign_2) * second_charge) / 2
        ratio = Fraction(1) * q_ratio * q_ratio / first_charge / second_charge / (n ** 2)
        return dict(
            res=[
                'отталкивание' if (sign_to_mult(sign_1) == sign_to_mult(sign_2)) else 'притяжение',
                'отталкивание',
            ],
            charges=charges,
            ratio=ratio,
            q_ratio=q_ratio,
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
    def GetUpdate(self, firstPoint=None, secondPoint=None, charges=None, letter=None):
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
    по величине равное~$E_1={values[0]}\\funits{В}{м}$,
    а $q_2$~--- $E_2={values[1]}\\funits{В}{м}$.
    Угол между векторами $\\vect{E_1}$ и $\\vect{E_2}$ равен ${angleLetter}$.
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
    \\begin{enumerate}
        \\item Запишите (формулой) {first}.
        \\item Зарисуйте электрическое поле точечного {second} электрического заряда.
        \\item Запишите формулу для вычисления {third} электрического поля точечного заряда.
        \\item Запишите принцип суперпозиции (правило сложения) {fourth}.
    \\end{enumerate}
''')
@variant.arg(first=['закон Кулона (в вакууме)', 'закон сохранения электрического заряда'])
@variant.arg(second=['положительного', 'отрицательного'])
@variant.arg(third=['потенциала', 'напряжённости'])
@variant.arg(fourth=['потенциалов', 'напряжённостей'])
class Definitions01(variant.VariantTask):
    pass


@variant.solution_space(60)
@variant.text('''
    Как изменится сила кулоновского взаимодействия между двумя точечными зарядами,
    если их, первоначально покоившихся в керосине, поместить в вакуум,
    увеличив при этом расстояние между ними в {n_text}?
''')
@variant.arg(n__n_text=n_times(2, 3, 4, 5, 6, 7, 8))
class F_ratio_from_e_and_r(variant.VariantTask):  # Вишнякова 3.1.1
    pass


@variant.solution_space(60)
@variant.text('''
    Два точечных заряда взаимодействуют в среде с диэлектрической
    проницаемостью {e1:V:e} на расстояние {r1:V:e}.
    На каком расстоянии друг от друга нужно поместить эти заряды
    в среде с диэлектрической проницаемостью {e2:V:e},
    чтобы сила их взаимодействия осталась прежней?
''')
@variant.arg(e1=('\\vareps_1 = {}', [6, 12, 18, 54]))
@variant.arg(e2=('\\vareps_2 = {}', [3, 9, 27, 81]))
@variant.arg(r1=('r_1 = {} мм', [10, 15, 25, 40, 80]))
class R_from_r_e1_e2(variant.VariantTask):  # Вишнякова 3.1.2
    pass


@variant.solution_space(80)
@variant.text('''
    В вакууме вдоль одной прямой расположены {n_text} {sign} заряда так,
    что расстояние между соседними зарядами равно ${r}$. Сделайте рисунок,
    и определите силу, действующую на крайний заряд.
    Модули всех зарядов равны ${q}$ (${q} > 0$).
''')
@variant.arg(n__n_text=n_word(3, 4))
@variant.arg(r=['a', 'l', 'd', 'r'])
@variant.arg(q=['q', 'Q'])
@variant.arg(sign=['положительных', 'отрицательных'])
@variant.answer_short('F = \\sum_i F_i = \\ldots = {ratio:LaTeX} \\frac{k{q}^2}{{r}^2}.')
class F_from_many_q(variant.VariantTask):  # Вишнякова 3.1.3
    def GetUpdate(self, n=None, n_text=None, r=None, q=None, sign=None):
        if n == 3:
            ratio = Fraction(1) + Fraction(1) / 4
        elif n == 4:
            ratio = Fraction(1) + Fraction(1) / 4 + Fraction(1) / 9
        return dict(
            ratio=ratio,
        )


@variant.solution_space(80)
@variant.text('''
    Маленький шарик массой {m:V} подвешен на длинной непроводящей нити
    и помещён в горизонтальное однородное электрическое поле с напряжённостью {E:V:e}.
    При этом шарик отклонился на угол ${alpha}\\degrees$.
    Определите, каким зарядом обладает шарик. {Consts.g_ten:Task:e}.
''')
@variant.arg(m=('m = {} мг', [200, 400, 500, 800]))
@variant.arg(E=('E = {} кВ / м', [50, 100, 200]))
@variant.arg(alpha=[2, 4, 5, 10])
class Q_from_alpha(variant.VariantTask):  # Вишнякова 3.1.4
    pass


@variant.solution_space(80)
@variant.text('''
    Электрическое поле создаётся двумя положительными точечными зарядами
    {q1:Task:e} и {q2:Task:e}. Чему равно расстояние между этими зарядами,
    если известно, что точка, где напряжённость электрического поля равна нулю,
    находится на расстоянии {d:V} от первого заряда?
''')
@variant.arg(q1=('q_1 = {} нКл', [2, 10, 16, 24]))
@variant.arg(q2=('q_2 = {} нКл', [1, 4, 12, 20, 30]))
@variant.arg(d=('d = {} см', [5, 10, 15, 20]))
class R_from_d(variant.VariantTask):  # Вишнякова 3.1.5
    pass


@variant.solution_space(100)
@variant.text('''
    Небольшое заряженное тело начинает скользить без трения по наклонной плоскости
    с высоты {H:Task:e}. Заряд тела {q2:Task:e}, угол наклона плоскости $\\alpha={alpha}\\degrees$.
    В вершине прямого угла находится точесный отрицательный заряд {q1:Task:e}. найти массу тела,
    если его кинетическая энергия в нижней точке наклонной плоскости
    равна {E_k:Task:e}. Ответ приведите в граммах. {Consts.e_0:Task:e}
''')
@variant.arg(H=('H = {} см', [20, 40, 80]))
@variant.arg(q1=('q_1 = {} мкКл', [2, -5, 10]))
@variant.arg(q2=('q_2 = {} мкКл', [-3, 4, -5]))
@variant.arg(alpha=[10, 15, 20])
@variant.arg(E_k=('E_\\text{{кин.}} = {} мДж', [50, 80, 120, 150]))
class E_kin_prism(variant.VariantTask):  # Вишнякова 3.1.6
    pass


@variant.solution_space(80)
@variant.text('''
    Точки $A$, $B$ и $C$ образуют треугольник со сторонами $BC = {a:V:e}$, $AC = {b:V:e}$ и $AB = {c:V:e}$.
    В точках $A$ и $C$ находятся 2 точечных заряда: {qe:V:e} и {qc:V:e}.
    Определите потенциал в третьей вершине треугольника.
    {Consts.e_0:Task:e}, {Consts.k:Task:e}.
''')
@variant.arg(a__b__c=
    permute('6 см', '8 см', '9 см')
    + permute('5 см', '11 см', '13 см')
    + permute('8 см', '23 см', '25 см')
)
@variant.arg(qa=('q_A = {} мкКл', [-3, -2, 3, 4, 5, 6]))
@variant.arg(qc=('q_C = {} мкКл', [-6, -5, -4, -3, -2, 3, 4]))
class KulonDiel(variant.VariantTask):  # Вишнякова 3.1.9
    pass


@variant.solution_space(80)
@variant.text('''
    Два равных по величине положительных точечных заряда $q$ расположены
    в вакууме в точках $A$ и $B$. Длина отрезка $AB = {n}L$.
    Точка $С$ — середина отрезка $AB$, а точка $D$ лежит на отрезке $BC$,
    причём $CD = \\frac Lm$. Определите, какой заряд необходимо
    поместить в точку $C$, чтобы {what} электрического поля в точке $D$ {what_do} нулю.
''')
@variant.arg(m=[2, 3, 4])
@variant.arg(n=[2, 3])
@variant.arg(what__what_do=[('напряжённость', 'стала'), ('потенциал', 'стал'),])
class KulonDiel(variant.VariantTask):  # Вишнякова 3.1.10
    pass
