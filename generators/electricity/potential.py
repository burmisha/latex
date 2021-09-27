import generators.variant as variant
from generators.helpers import Consts

@variant.solution_space(80)
@variant.text('''
    В однородном электрическом поле напряжённостью {E:Task:e}
    переместили заряд {q:Task:e} в направлении силовой линии
    на {l:Task:e}. Определите
    \\begin{itemize}
        \\item работу поля,
        \\item изменение потенциальной энергии заряда.
        % \\item напряжение между начальной и конечной точками перемещения.
    \\end{itemize}
''')
@variant.answer_align([
    'A &= F * {l:L} * \\cos \\alpha = {E:L}{q:L} * {l:L} * 1 = {E:L}{q:L}{l:L} = {E:Value} * {q:Value} * {l:Value} = {A:V},',
    '\\Delta E_\\text{пот.} &= -A = {dE:V}'
])
@variant.arg(q=['%s = %d нКл' % (ql, qv) for ql in ['Q', 'q'] for qv in [-10, 10, -25, 25, -40, 40]])
@variant.arg(l=['%s = %d см' % (ll, lv) for ll in ['l', 'r', 'd'] for lv in [2, 4, 5, 10]])
@variant.arg(E=['E = %d кВ / м' % ev for ev in [2, 4, 20]])
class A_from_Q_E_l(variant.VariantTask):  # Рымкевич 728(737)
    def GetUpdate(self, l=None, q=None, E=None):
        A = 1. * E.Value * q.Value * l.Value / 100
        dE = -A
        return dict(
            A=f'{A:.1f} мкДж',
            dE=f'{dE:.1f} мкДж',
        )


@variant.solution_space(40)
@variant.text('''
    Напряжение между двумя точками, лежащими на одной линии напряжённости
    однородного электрического поля, равно {U:Task:e}.
    Расстояние между точками {l:Task:e}. Какова напряжённость этого поля?
''')
@variant.arg(U=['%s = %d кВ' % (ul, uv) for ul in ['U', 'V'] for uv in [2, 3, 4, 5, 6]])
@variant.arg(l=['%s = %d см' % (ll, lv) for ll in ['l', 'r', 'd'] for lv in [10, 20, 30, 40]])
@variant.answer_short('''
    E_x = -\\frac{\\Delta \\varphi}{\\Delta x} \\implies
    E = \\frac{U:L:s}{l:L:s} = \\frac{U:V:s}{l:V:s} = {E:V}.
''')
class E_from_U_l(variant.VariantTask):  # Рымкевич 735(737)
    def GetUpdate(self, U=None, l=None):
        return dict(
            E='%.1f кВ / м' % (1. * U.Value / l.Value * 100),
        )


@variant.text('''
    Найти напряжение между точками $A$ и $B$ в однородном электрическом поле
    (см. рис. на доске), если $AB={l:Task}$, ${alpha:L}={alpha:Value}^\\circ$,
    {E:Task:e}. Потенциал какой из точек $A$ и $B$ больше?
''')
@variant.arg(l=['%s = %d см' % (ll, lv) for ll in ['l', 'r', 'd'] for lv in [4, 6, 8, 10, 12]])
@variant.arg(alpha=['%s = %d' % (al, av) for al in ['\\alpha', '\\varphi'] for av in [30, 45, 60]])
@variant.arg(E=['E = %d В / м' % ev for ev in [30, 50, 60, 100, 120]])
class Potential737(variant.VariantTask):  # Рымкевич 737(739)
    pass


@variant.solution_space(40)
@variant.text('При какой скорости {what} его кинетическая энергия равна {E:Task:e}?')
@variant.arg(E=('E_\\text{{к}} = {} эВ', [4, 8, 20, 30, 40, 50, 200, 400, 600, 1000]))
@variant.arg(what=['электрона', 'позитрона', 'протона', 'нейтрона'])
class v_from_Ev_m(variant.VariantTask):  # 2335 Gendenshteyn
    pass


@variant.text('''
    {what} вылетает из точки, потенциал которой {V:Task:e},
    со скоростью {v:Task:e} параллельно линиям напряжённости однородного электрического поля.
    % Будет поле его ускорять или тормозить?
    В некоторой точке частица остановилась. Каков потенциал этой точки?
    Вдоль и против поля влетела изначально частица?
''')
@variant.arg(v=['v = %d000000 м / с' % vv for vv in [3, 4, 6, 10, 12]])
@variant.arg(V=['\\varphi = %d В' % Vv for Vv in [200, 400, 600, 800, 1000]])
@variant.arg(what=['Электрон $e^-$', 'Позитрон $e^+$'])
@variant.answer_align([
    'A_\\text{внешних сил} &= \\Delta E_\\text{кин.} \\implies A_\\text{эл. поля} = 0 - \\frac{mv^2}2.',
    'A_\\text{эл. поля} &= q(\\varphi_1 - \\varphi_2) \\implies'
    '\\varphi_2 = \\varphi_1 - \\frac{A_\\text{эл. поля}}q = \\varphi_1 - \\frac{- \\frac{mv^2}2}q = \\varphi_1 + \\frac{mv^2}{2q} = ',
    '&= {V:Value} + \\frac{{Consts.m_e:V} * {v:V|sqr}}{2 {sign} * {Consts.e:V}} \\approx {V2:V}.'
])
class Phi_from_static_e(variant.VariantTask):  # Гольдфарб 16.21, Вишнякова 3.1.7
    def GetUpdate(self, v=None, V=None, what=None):
        sign = {
            'электрон': -1,
            'позитрон': 1,
        }[what.split()[0].lower()]
        power = Consts.m_e.Power + 2 * v.Power - Consts.e.Power
        V2 = V.Value + 1. / 2 * sign * Consts.m_e.Value * (v.Value ** 2) / Consts.e.Value * (10 ** power)
        return dict(
            V2=f'\\varphi_2 = {V2:.1f} В',
            sign=' * (-1) ' if sign == -1 else ''
        )


@variant.solution_space(120)
@variant.text('''
    {what} вылетает из точки, потенциал которой {V:Task:e},
    со скоростью {v:Task:e} параллельно линиям напряжённости однородного электрического поля.
    % Будет поле его ускорять или тормозить?
    В некоторой точке частица остановилась. Каков потенциал этой точки?
    Вдоль и против поля влетела изначально частица?
''')
@variant.arg(v=['v = %d000000 м / с' % vv for vv in [3, 4, 6, 10, 12]])
@variant.arg(V=['\\varphi = %d В' % Vv for Vv in [200, 400, 600, 800, 1000]])
@variant.arg(what=['Электрон $e^-$', 'Позитрон $e^+$'])
@variant.answer_align([
    'A_\\text{внешних сил} &= \\Delta E_\\text{кин.} \\implies A_\\text{эл. поля} = 0 - \\frac{mv^2}2.',
    'A_\\text{эл. поля} &= q(\\varphi_1 - \\varphi_2) \\implies'
    '\\varphi_2 = \\varphi_1 - \\frac{A_\\text{эл. поля}}q = \\varphi_1 - \\frac{- \\frac{mv^2}2}q = \\varphi_1 + \\frac{mv^2}{2q} = ',
    '&= {V:Value} + \\frac{{Consts.m_e:V} * {v:V|sqr}}{2 {sign} * {Consts.e:V}} \\approx {V2:V}.'
])
class Phi_from_static_e(variant.VariantTask):  # 1621 Goldfarb
    def GetUpdate(self, v=None, V=None, what=None):
        sign = {
            'электрон': -1,
            'позитрон': 1,
        }[what.split()[0].lower()]
        power = Consts.m_e.Power + 2 * v.Power - Consts.e.Power
        V2 = V.Value + 1. / 2 * sign * Consts.m_e.Value * (v.Value ** 2) / Consts.e.Value * (10 ** power)
        return dict(
            V2=f'\\varphi_2 = {V2:.1f} В',
            sign=' * (-1) ' if sign == -1 else ''
        )


@variant.solution_space(120)
@variant.text('''
    Три одинаковых положительных точечных заряда по ${q}$ каждый находятся
    на одной прямой так, что расстояние между каждыми двумя соседними равно ${n}{r}$.
    Какую минимальную работу необходимо совершить, чтобы перевести эти заряды в положение,
    при котором они образуют {what} ${r}$? Сделайте рисунки и получите ответ (формулой).
''')
@variant.arg(q=['q', 'Q'])
@variant.arg(r=['l', 'r', 'd'])
@variant.arg(n=[2, 3])
@variant.arg(what=[
    'равносторонний треугольник со стороной',
    'прямоугольный равнобедренный треугольник с катетом',
    'прямоугольный равнобедренный треугольник с гипотенузой',
])
class A_from_motion(variant.VariantTask):  # Вишнякова 3.1.8
    pass


@variant.solution_space(90)
@variant.text('''
    На рисунке показано расположение трёх металлических пластин и указаны их потенциалы.
    Размеры пластин кораздо больше расстояния между ними. Отмечены также ось и начало координат.
    Дорисуйте на рисунке электрическое поле и постройте графики зависимости от координаты $x$:
    \\begin{enumerate}
        \\item проекции напряжённости электрического поля,
        \\item потенциала электрического поля.
    \\end{enumerate}
    \\begin{tikzpicture}
        \\draw[-{Latex}] (0, 0) -- (0, 3.5) node[below right] {$x$};
        \\draw[thick]
            (-0.05, 0.5) -- (0.05, 0.5)     (0, 0.5) node[left] {$-{d:V}$}     (0.5, 0.5) -- (4, 0.5) node[right] {{phi_1:V:e}}
            (-0.05, 1.5) -- (0.05, 1.5)     (0, 1.5) node[left] {$0$}         (0.5, 1.5) -- (4, 1.5) node[right] {{zero:V:e}}
            (-0.05, 2.5) -- (0.05, 2.5)     (0, 2.5) node[left] {${d:V}$}    (0.5, 2.5) -- (4, 2.5) node[right] {{phi_2:V:e}};
    \\end{tikzpicture}
''')
@variant.arg(d=('d = {} см', [2, 3]))
@variant.arg(phi_1=('\\varphi_1 = {} В', [-90, -30, 30, 90, 150]))
@variant.arg(phi_2=('\\varphi_1 = {} В', [-120, -60, 60, 120]))
class E_phi_graphs(variant.VariantTask):
    def GetUpdate(self, d=None, phi_1=None, phi_2=None):
        return dict(
            zero='0 В',
        )


@variant.solution_space(0)
@variant.text('''
    \\begin{enumerate}
        \\item Запишите {first}.
        \\item Из теоремы Гаусса выведите (нужен рисунок, применение и результат) формулу для напряженности электростатического поля {what}.
        \\item Зарисуйте электрическое поле точечного {second} электрического заряда.
        \\item Запишите формулу для вычисления {third} электрического поля точечного заряда в диэлектрике.
        \\item Запишите принцип суперпозиции (правило сложения) {fourth}.
    \\end{enumerate}
''')
@variant.arg(first=['теорему Гаусса', 'закон Кулона (в диэлектрике)', 'закон сохранения электрического заряда'])
@variant.arg(what=['снаружи равномерно заряженной сферы', 'внутри равномерно заряженной сферы', 'около равномерно заряженной бесконечной плоскости'])
@variant.arg(second=['положительного', 'отрицательного'])
@variant.arg(third=['потенциала', 'напряжённости'])
@variant.arg(fourth=['потенциалов', 'напряжённостей'])
class Definitions01(variant.VariantTask):
    pass
