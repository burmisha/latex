# -*- coding: utf-8 -*-

import generators.variant as variant

import logging
log = logging.getLogger(__name__)


@variant.text(u'''
    Запишите определения, формулы и физические законы (можно сокращать, но не упустите ключевое):
    \\begin{{enumerate}}
        \\item {item_1},
        \\item {item_2},
        \\item {item_3},
        \\item {item_4}.
    \\end{{enumerate}}
''')
@variant.arg(item_1=[
    u'основная задача механики',
    u'механическое движение',
    u'материальная точка',
    u'система отсчёта',
    u'поступательное движение',
])
@variant.arg(item_2=[
    u'траектория',
    u'путь',
    u'перемещение',
    u'равномерное прямолинейное движение',
])
@variant.arg(item_3=[
    u'перемещение при равномерном прямолинейном движении (векторно)',
    u'положение тела при равномерном прямолинейном движении (векторно)',
])
@variant.arg(item_4=[
    u'перемещение при равномерном прямолинейном движении (в проекциях)',
    u'положение тела при равномерном прямолинейном движении (в проекциях)',
])
class Theory_1(variant.VariantTask):
    pass


@variant.text(u'''
    Запишите определения, формулы и физические законы (можно сокращать, но не упустите ключевое):
    \\begin{{enumerate}}
        \\item {item_1},
        \\item {item_2},
        \\item {item_3}.
    \\end{{enumerate}}
''')
@variant.arg(item_1=[
    u'основная задача механики',
    u'материальная точка',
    u'система отсчёта',
])
@variant.arg(item_2=[
    u'механическое движение',
    u'поступательное движение',
])
@variant.arg(item_3=[
    u'траектория',
    u'путь',
    u'перемещение',
])
class Theory_1_simple(variant.VariantTask):
    pass


@variant.text(u'''
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


@variant.text(u'''
    Небольшой лёгкий самолёт взлетел из аэропорта, пролетел {l_1:Value:e} строго на {where_1}, потом повернул и пролетел {l_2:Value:e} на {where_2},
    а после по прямой вернулся обратно в аэропорт. Определите путь и модуль перемещения самолёта, считая Землю плоской.
''')
@variant.arg(where_1=[u'север', u'юг'])
@variant.arg(where_2=[u'запад', u'восток'])
@variant.arg(l_1__l_2=[
    (u'l_1 = 30 км', u'l_2 = 40 км'),
    (u'l_1 = 40 км', u'l_2 = 30 км'),
    (u'l_1 = 24 км', u'l_2 = 7 км'),
    (u'l_1 = 7 км', u'l_2 = 24 км'),
    (u'l_1 = 12 км', u'l_2 = 5 км'),
    (u'l_1 = 5 км', u'l_2 = 12 км'),
])
class Chernoutsan_1_2(variant.VariantTask):
    pass


@variant.text(u'''
    {who} плавает в бассейне длиной {l:Value:e}: от одного бортика к другому и обратно.
    Определите {whose} перемещение, если {whose} путь к текущему моменту составил {s:Value:e}.
''')
@variant.arg(who=[u'Саша', u'Валя', u'Женя'])
@variant.arg(whose=[u'её', u'его'])
@variant.arg(l=[u'l = %d м' % l for l in [25, 50]])
@variant.arg(s=[u's = %d м' % s for s in range(150, 350, 20)])
@variant.answer_short('{d:Value}')
class Chernoutsan_1_2_1(variant.VariantTask):
     def GetUpdate(self, l=None, s=None, **kws):
        d = s.Value % (2 * l.Value)
        d = min(d, 2 * l.Value - d)
        return dict(
            d=u'd = %d м' % d
        )


@variant.text(u'''
    Женя и Валя едут на {what}: Женя движется на {where_1} со скоростью {v_1:Value:e}, Валя — на {where_2} со скоростью {v_2:Value:e}.
    Определите скорость Вали относительно Жени. Сделайте рисунок («вид сверху»), подпишите кто где, укажите скорости (в т.ч. направление).
''')
@variant.arg(what=[u'велосипедах', u'мотоциклах', u'лошадях'])
@variant.arg(where_1=[u'север', u'юг', u'запад', u'восток'])
@variant.arg(where_2=[u'север', u'юг', u'запад', u'восток'])
@variant.arg(v_1__v_2=[
    (u'v_1 = 3 м / с', u'v_2 = 4 м / с'),
    (u'v_1 = 12 м / с', u'v_2 = 5 м / с'),
    (u'v_1 = 4 км / ч', u'v_2 = 3 км / ч'),
    (u'v_1 = 5 км / ч', u'v_2 = 12 км / ч'),
])
class Vectors_SpeedSum(variant.VariantTask):
    pass
