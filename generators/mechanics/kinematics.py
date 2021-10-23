import generators.variant as variant
from generators.helpers import Consts, UnitValue, Decimal

@variant.text('''
    Запишите определения, формулы и физические законы (можно сокращать, но не упустите ключевое):
    \\begin{enumerate}
        \\item {item_1},
        \\item {item_2},
        \\item {item_3},
        \\item {item_4}.
    \\end{enumerate}
''')
@variant.arg(item_1=[
    'основная задача механики',
    'механическое движение',
    'материальная точка',
    'система отсчёта',
    'поступательное движение',
])
@variant.arg(item_2=[
    'траектория',
    'путь',
    'перемещение',
    'равномерное прямолинейное движение',
])
@variant.arg(item_3=[
    'перемещение при равномерном прямолинейном движении (векторно)',
    'положение тела при равномерном прямолинейном движении (векторно)',
])
@variant.arg(item_4=[
    'перемещение при равномерном прямолинейном движении (в проекциях)',
    'положение тела при равномерном прямолинейном движении (в проекциях)',
])
class Theory_1(variant.VariantTask):
    pass


@variant.text('''
    Запишите определения, формулы и физические законы (можно сокращать, но не упустите ключевое):
    \\begin{enumerate}
        \\item {item_1},
        \\item {item_2},
        \\item {item_3}.
    \\end{enumerate}
''')
@variant.arg(item_1=[
    'основная задача механики',
    'материальная точка',
    'система отсчёта',
])
@variant.arg(item_2=[
    'механическое движение',
    'поступательное движение',
])
@variant.arg(item_3=[
    'траектория',
    'путь',
    'перемещение',
])
class Theory_1_simple(variant.VariantTask):
    pass


@variant.text('''
    Положив $\\vec a = {i1}\\vec i + {j1} \\vec j, \\vec b = {i2}\\vec i + {j2} \\vec j$,
    \\begin{enumerate}
        \\item найдите сумму векторов $\\vec a + \\vec b$,
        \\item постройте сумму векторов $\\vec a + \\vec b$ на чертеже,
        \\item определите модуль суммы векторов $\\modul{{\\vec a + \\vec b}}$,
        \\item вычислите разность векторов $\\vec a - \\vec b.$
    \\end{enumerate}
''')
@variant.arg(i1=[2, -2, 3, -3])
@variant.arg(i2=[3, -3, 4, -4])
@variant.arg(j1=[4, -4, 2, -2])
@variant.arg(j2=[2, -2, 3, -3])
@variant.answer_short(
    '\\vec a + \\vec b = {i3}\\vec i + {j3}\\vec i, '
    '\\vec a - \\vec b = {i4}\\vec i + {j4}\\vec i, '
    '\\modul{{\\vec a + \\vec b}} = \\sqrt{{\\sqr{i3} + \\sqr{j3}}} \\approx {modul}.'
)
class Vectors_SumAndDiff(variant.VariantTask):
    def GetUpdate(self, i1=None, j1=None, i2=None, j2=None):
        return dict(
            i3=i1 + i2,
            j3=j1 + j2,
            i4=i1 - i2,
            j4=j1 - j2,
            modul='%.2f' % ((i1 + i2) ** 2 + (j1 + j2) ** 2) ** 0.5
        )


@variant.text('''
    Небольшой лёгкий самолёт взлетел из аэропорта, пролетел {l_1:Value:e} строго на {where_1}, потом повернул и пролетел {l_2:Value:e} на {where_2},
    а после по прямой вернулся обратно в аэропорт. Определите путь и модуль перемещения самолёта, считая Землю плоской.
''')
@variant.arg(where_1=['север', 'юг'])
@variant.arg(where_2=['запад', 'восток'])
@variant.arg(l_1__l_2=[
    ('l_1 = 30 км', 'l_2 = 40 км'),
    ('l_1 = 40 км', 'l_2 = 30 км'),
    ('l_1 = 24 км', 'l_2 = 7 км'),
    ('l_1 = 7 км', 'l_2 = 24 км'),
    ('l_1 = 12 км', 'l_2 = 5 км'),
    ('l_1 = 5 км', 'l_2 = 12 км'),
])
class Chernoutsan_1_2(variant.VariantTask):
    pass


@variant.text('''
    {who} плавает в бассейне длиной {l:Value:e}: от одного бортика к другому и обратно.
    Определите {whose} перемещение, если {whose} путь к текущему моменту составил {s:Value:e}.
''')
@variant.arg(who=['Саша', 'Валя', 'Женя'])
@variant.arg(whose=['её', 'его'])
@variant.arg(l=('l = {} м', [25, 50]))
@variant.arg(s=('s = {} м', range(150, 350, 20)))
@variant.answer_short('{d:Value}')
class Chernoutsan_1_2_1(variant.VariantTask):
     def GetUpdate(self, who=None, whose=None, l=None, s=None):
        d = s.Value % (2 * l.Value)
        d = min(d, 2 * l.Value - d)
        return dict(
            d='d = %d м' % d
        )


@variant.text('''
    Женя и Валя едут на {what}: Женя движется на {where_1} со скоростью {v_1:Value:e}, Валя — на {where_2} со скоростью {v_2:Value:e}.
    Определите скорость Вали относительно Жени. Сделайте рисунок («вид сверху»), подпишите кто где, укажите скорости (в т.ч. направление).
''')
@variant.arg(what=['велосипедах', 'мотоциклах', 'лошадях'])
@variant.arg(where_1=['север', 'юг', 'запад', 'восток'])
@variant.arg(where_2=['север', 'юг', 'запад', 'восток'])
@variant.arg(v_1__v_2=[
    ('v_1 = 3 м / с', 'v_2 = 4 м / с'),
    ('v_1 = 12 м / с', 'v_2 = 5 м / с'),
    ('v_1 = 4 км / ч', 'v_2 = 3 км / ч'),
    ('v_1 = 5 км / ч', 'v_2 = 12 км / ч'),
])
class Vectors_SpeedSum(variant.VariantTask):
    pass


@variant.text('''
    Электрон летит прямолинейно из точки $A$ в точку $B$, за ним при этом наблюдает экспериментатор Глюк.
    Глюк заметил, что первую {part} {what} электрон равномерно двигался со скоростью {v1:V:e},
    затем его практически мгновенно ускорило электрическое поле
    и остаток {what} электрон вновь равномерно двигался со скоростью {v2:V:e}.
    Определите среднюю скорость электрона. Ответ выразите в м/с и округлите до тысяч.
''')
@variant.arg(part__denominator=[('половину', 2), ('треть', 3), ('четверть', 4)])
@variant.arg(v1=('v_1 = {} 10^5 км / ч', [2, 4]))
@variant.arg(v2=('v_2 = {} 10^5 км / ч', [3, 6]))
@variant.arg(what=['времени', 'пути'])
class AvgSpeed_electron(variant.VariantTask):
    pass


@variant.text('''
    {who} стартует на {what} и в течение {t:Task:e} двигается с постоянным ускорением {a:V:e}.
    Определите
    \\begin{itemize}
        \\item какую скорость при этом удастся достичь,
        \\item какой путь за это время будет пройден,
        \\item среднюю скорость за всё время движения, если после начального ускорения продолжить движение равномерно ещё в течение времени ${n}{t:L}$
    \\end{itemize}
''')
@variant.arg(who=['Валя', 'Женя', 'Саша'])
@variant.arg(what=['велосипеде', 'мотоцикле', 'лошади'])
@variant.arg(t=('t = {} c', [2, 3, 4, 5, 10]))
@variant.arg(a=('a = {} м / с^2', ['0.5', '1.5', '2', '2.5']))
@variant.arg(n=[2, 3])
@variant.answer_align([
    'v &= v_0 + a t = at = {a:Value} * {t:Value} = {v:Value},',
    's_x &= v_0t + \\frac{a t^2}2 = \\frac{a t^2}2 = \\frac{{a:Value} * {t:Value:sqr}}2 = {s:Value},',
    'v_\\text{сред.} &= \\frac{s_\\text{общ}}{t_\\text{общ.}} = \\frac{s_x + v * {n}t}{t + {n}t} = \\frac{\\frac{a t^2}2 + at * {n}t}{t (1 + {n})} =',
    '&= at * \\frac{\\frac 12 + {n}}{1 + {n}} = {a:Value} * {t:Value} * \\frac{\\frac 12 + {n}}{1 + {n}} \\approx {v_avg:Value}.'
])
class A_plus_V(variant.VariantTask):
    def GetUpdate(self, who=None, what=None, t=None, a=None, n=None):
        return dict(
            v='v = %.1f м / с' % (t.Value * a.Value) ,
            s='s_x = %.1f м' % (t.Value ** 2 * a.Value / 2) ,
            v_avg='v_\\text{сред.} = %.2f м / c' % (float(t.Value * a.Value) * (1 / 2 + n) / (1 + n)) ,
        )


@variant.text('''
    Какой путь тело пройдёт за {which} секунду после начала свободного падения?
    Какую скорость в {point} этой секунды оно имеет?
''')
@variant.arg(n__which=[(2, 'вторую'), (3, 'третью'), (4, 'четвёртую'), (5, 'пятую'), (6, 'шестую')])
@variant.arg(point=['начале', 'конце'])
@variant.answer_align([
    '{s:Letter} &= -s_y = -(y_2-y_1) = y_1 - y_2 = \\cbr{y_0 + v_{0y}t_1 - \\frac{gt_1^2}2} - \\cbr{y_0 + v_{0y}t_2 - \\frac{gt_2^2}2} =',
    '&= \\frac{gt_2^2}2 - \\frac{gt_1^2}2 = \\frac g2\\cbr{t_2^2 - t_1^2} = {s:Value},',
    '{v:Letter} &= v_{0y} - gt = -gt = {Consts.g_ten:Value} * {t:Value} = -{v:Value}.'
])
class V_and_S_from_g_and_t(variant.VariantTask):
    def GetUpdate(self, n=None, which=None, point=None):
        t_value = {
            'начале': n - 1,
            'конце': n,
        }[point]
        return dict(
            t='t = %d с' % t_value,
            v='v_y = %d м / с' % (t_value * Consts.g_ten.Value),
            s='s = %.1f м' % (((n ** 2) - (n - 1) ** 2) * Consts.g_ten.Value / 2),
        )


@variant.solution_space(80)
@variant.text('''
    Карусель {what} {l:V:e} равномерно совершает {n} оборотов в минуту. Определите
    \\begin{itemize}
        \\item период и частоту её обращения,
        \\item скорость и ускорение крайних её точек.
    \\end{itemize}
''')
@variant.arg(what=['радиусом', 'диаметром'])
@variant.arg(l=('l = {} м', [2, 3, 4, 5]))
@variant.arg(n=[5, 6, 10])
@variant.answer_align([
    't &= {t:Value}, r = {r:Value}, n = {n}\\units{оборотов},',
    'T &= \\frac tN = \\frac{t:Value:s}{{n}} \\approx {T:Value},',
    '\\nu &= \\frac 1T = \\frac{{n}}{t:Value:s} \\approx {nu:Value},',
    'v &= \\frac{2 \\pi r}T = \\frac{2 \\pi r}T =  \\frac{2 \\pi r n}t \\approx {v:Value},',
    'a &= \\frac{v^2}r =  \\frac{4 \\pi^2 r n^2}{t^2} \\approx {a:Value}.'
])
class All_from_l_and_n(variant.VariantTask):
    def GetUpdate(self, what=None, l=None, n=None):
        denominator = {'радиусом': 1, 'диаметром': 2}[what]
        r_ratio = l.frac_value / denominator
        t = UnitValue('t = 60 с')
        r = UnitValue('r = %.1f м' % float(r_ratio))
        return dict(
            t=t,
            r=r,
            T='T = %.2f c' % (t.Value / n),
            nu='\\nu = %.2f Гц' % (Decimal(n) / t.Value),
            v='v = %.2f м / c' % (float(r_ratio) * 2 * Consts.pi * n / float(t.Value)),
            a='a = %.2f м / с^2' % (float(r_ratio) * 4 * (Consts.pi ** 2) * (n ** 2) / (float(t.Value) ** 2)),
        )



@variant.text('''
    {who} стоит на обрыве над рекой и методично и строго горизонтально кидает в неё камушки.
    За этим всем наблюдает экспериментатор Глюк, который уже выяснил, что камушки падают в реку спустя {t:Value:e} после броска,
    а вот дальность полёта оценить сложнее: придётся лезть в воду. Выручите Глюка и определите:
    \\begin{itemize}
        \\item высоту обрыва (вместе с ростом {who2}).
        \\item дальность полёта камушков (по горизонтали) и их скорость при падении, приняв начальную скорость броска равной {v:Task:e}.
    \\end{itemize}
    Сопротивлением воздуха пренебречь.
''')
@variant.arg(who=['Даша', 'Маша', 'Миша', 'Паша'])
@variant.arg(t=('t = {} с', ['1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8']))
@variant.arg(v=('v_0 = {} м / с', ['12', '13', '14', '15', '16', '17', '18']))
@variant.answer_align([
    'y &= y_0 + v_{0y}t - \\frac{gt^2}2 = h - \\frac{gt^2}2, \\qquad y(\\tau) = 0 \\implies h - \\frac{g\\tau^2}2 = 0 \\implies h = \\frac{g\\tau^2}2 \\approx {h:Value}.',
    'x &= x_0 + v_{0x}t = v_0t \\implies L = v_0\\tau \\approx {L:Value}.',
    'v = \\sqrt{v_x^2 + v_y^2} = \\sqrt{v_{0x}^2 + \\sqr{v_{0y} - g\\tau}} = \\sqrt{v_0^2 + \\sqr{g\\tau}} \\approx {v_res:Value}.'
])
class Stones_into_river(variant.VariantTask):
    def GetUpdate(self, who=None, t=None, v=None):
        return dict(
            who2=who[:3] + 'и',
            h='h = %.1f м' % (float(Consts.g_ten.Value) * float(t.Value) ** 2 / 2),
            L='L = %.1f м' % (v.Value * t.Value),
            v_res='v = %.1f м / c' % ((float(v.Value) ** 2 + float(Consts.g_ten.Value * t.Value) ** 2) ** 0.5),
        )
