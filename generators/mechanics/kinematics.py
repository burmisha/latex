import generators.variant as variant


@variant.text('''
    Запишите определения, формулы и физические законы (можно сокращать, но не упустите ключевое):
    \\begin{{enumerate}}
        \\item {item_1},
        \\item {item_2},
        \\item {item_3},
        \\item {item_4}.
    \\end{{enumerate}}
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
    \\begin{{enumerate}}
        \\item {item_1},
        \\item {item_2},
        \\item {item_3}.
    \\end{{enumerate}}
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
    \\begin{{enumerate}}
        \\item найдите сумму векторов $\\vec a + \\vec b$,
        \\item постройте сумму векторов $\\vec a + \\vec b$ на чертеже,
        \\item определите модуль суммы векторов $\\modul{{\\vec a + \\vec b}}$,
        \\item вычислите разность векторов $\\vec a - \\vec b.$
    \\end{{enumerate}}
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
    def GetUpdate(self, i1=None, j1=None, i2=None, j2=None, **kws):
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
     def GetUpdate(self, l=None, s=None, **kws):
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
    \\begin{{itemize}}
        \\item какую скорость при этом удастся достичь,
        \\item какой путь за это время будет пройден,
        \\item среднюю скорость за всё время движения, если после начального ускорения продолжить движение равномерно ещё в течение времени ${n}{t:L}$
    \\end{{itemize}}
''')
@variant.arg(who=['Валя', 'Женя', 'Саша'])
@variant.arg(what=['велосипеде', 'мотоцикле', 'лошади'])
@variant.arg(t=('t = {} c', [2, 3, 4, 5, 10]))
@variant.arg(a=('a = {} м / с^2', ['0.5', '1.5', '2', '2.5']))
@variant.arg(n=[2, 3])
class A_plus_V(variant.VariantTask):
    pass


@variant.text('''
    Какой путь тело пройдёт за {which} секунду после начала свободного падения?
    Какую скорость в {point} этой секунды оно имеет?
''')
@variant.arg(n__which=[(2, 'вторую'), (3, 'третью'), (4, 'четвёртую'), (5, 'пятую'), (6, 'шестую')])
@variant.arg(point=['начале', 'конце'])
class V_and_S_from_g_and_t(variant.VariantTask):
    pass


@variant.solution_space(80)
@variant.text('''
    Карусель {what} {l:V:e} равномерно совершает {n} оборотов в минуту. Определите
    \\begin{{itemize}} 
        \\item период и частоту её обращения, 
        \\item скорость и ускорение крайних её точек.
    \\end{{itemize}}
''')
@variant.arg(what=['радиусом', 'диаметром'])
@variant.arg(l=('l = {} м', [2, 3, 4, 5]))
@variant.arg(n=[5, 6, 10])
class All_from_l_and_n(variant.VariantTask):
    pass


@variant.text('''
    {who} стоит на обрыве над рекой и методично и строго горизонтально кидает в неё камушки.
    За этим всем наблюдает экспериментатор Глюк, который уже выяснил, что камушки падают в реку спустя {t:Value:e} после броска,
    а вот дальность полёта оценить сложнее: придётся лезть в воду. Выручите Глюка и определите:
    \\begin{{itemize}}
        \\item высоту обрыва (вместе с ростом {who2}).
        \\item дальность полёта камушков (по горизонтали) и их скорость при падении, приняв начальную скорость броска равной {v:Task:e}.
    \\end{{itemize}}
    Сопротивлением воздуха пренебречь.
''')
@variant.arg(who=['Даша', 'Маша', 'Миша', 'Паша'])
@variant.arg(t=('t = {} с', ['1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8']))
@variant.arg(v=('v = {} м / с', ['12', '13', '14', '15', '16', '17', '18']))
class Stones_into_river(variant.VariantTask):
    def GetUpdate(self, who=None, t=None, v=None, **kws):
        return dict(
            who2 = who[:3] + 'и'
        )
