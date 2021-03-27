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
@variant.arg(l=['l = %d м' % l for l in [25, 50]])
@variant.arg(s=['s = %d м' % s for s in range(150, 350, 20)])
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
