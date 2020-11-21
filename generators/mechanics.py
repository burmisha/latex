# -*- coding: utf-8 -*-

import generators.variant as variant

import logging
log = logging.getLogger(__name__)

# соответсвенно
@variant.text(u'''
    Шарики массами {m1:Value:e} и {m2:Value:e}
    движутся параллельно друг другу в одном направлении
    со скоростями {v1:Value:e} и {v2:Value:e} соответсвенно.
    Сделайте рисунок и укажите направления скоростей и импульсов.
    Определите импульс каждого из шариков, а также их суммарный импульс.
''')
@variant.answer_align([
    u'{p1:Letter} &= {m1:Letter}{v1:Letter} = {m1:Value|cdot}{v1:Value} = {p1:Value},',
    u'{p2:Letter} &= {m2:Letter}{v2:Letter} = {m2:Value|cdot}{v2:Value} = {p2:Value},',
    u'{p:Letter} &= {p1:Letter} + {p2:Letter} = {m1:Letter}{v1:Letter} + {m2:Letter}{v2:Letter} = {p:Value}.',
])
@variant.arg(m1__m2=[(u'm_1 = %d кг' % m1, u'm_2 = %d кг' % m2) for m1 in [1, 2, 3, 4] for m2 in [1, 2, 3, 4] if m1 != m2])
@variant.arg(v1=[u'v_1 = %d м / с' % v1 for v1 in [2, 4, 5, 10]])
@variant.arg(v2=[u'v_2 = %d м / с' % v2 for v2 in[3, 6, 8]])
@variant.answer_test('{p:Value}')
class Ch_3_1(variant.VariantTask):
    def GetUpdate(self, m1=None, m2=None, v1=None, v2=None, **kws):
        return dict(
            p1=u'p_1 = %d кг м / с' % (m1.Value * v1.Value),
            p2=u'p_2 = %d кг м / с' % (m2.Value * v2.Value),
            p=u'p = %d кг м / с' % (m1.Value * v1.Value + m2.Value * v2.Value),
        )


@variant.text(u'''
    Два шарика, масса каждого из которого составляет {m:Value:e},
    движутся навстречу друг другу.
    Скорость одного из них {v1:Value:e}, а другого~--- {v2:Value:e}.
    Сделайте рисунок, укажите направления скоростей и импульсов.
    Определите импульс каждого из шариков, а также их суммарный импульс.
''')
@variant.answer_align([
    u'{p1:Letter} &= {m:Letter}{v1:Letter} = {m:Value|cdot}{v1:Value} = {p1:Value},',
    u'{p2:Letter} &= {m:Letter}{v2:Letter} = {m:Value|cdot}{v2:Value} = {p2:Value},',
    u'{p:Letter} &= {p1:Letter} - {p2:Letter} = {m:Letter}({v1:Letter} - {v2:Letter}) = {p:Value}.',
])
@variant.arg(m=[u'm = %d кг' % m for m in [2, 5, 10]])
@variant.arg(v1=[u'v_1 = %d м / с' % v1 for v1 in [1, 2, 5, 10]])
@variant.arg(v2=[u'v_2 = %d м / с' % v2 for v2 in [3, 6, 8]])
class Ch_3_2(variant.VariantTask):
    def GetUpdate(self, m=None, v1=None, v2=None, **kws):
        return dict(
            p1=u'p_1 = %d кг м / с' % (m.Value * v1.Value),
            p2=u'p_2 = %d кг м / с' % (m.Value * v2.Value),
            p=u'p = %d кг м / с' % (m.Value * v1.Value - m.Value * v2.Value),
        )


@variant.text(u'''
    Два одинаковых шарика массами по {m:Value:e}
    движутся во взаимно перпендикулярных направлениях.
    Скорости шариков составляют {v1:Value:e} и {v2:Value:e}.
    Сделайте рисунок, укажите направления скоростей и импульсов.
    Определите импульс каждого из шариков и полный импульс системы.
''')
@variant.answer_align([
    u'{p1:Letter} &= {m:Letter}{v1:Letter} = {m:Value|cdot}{v1:Value} = {p1:Value},',
    u'{p2:Letter} &= {m:Letter}{v2:Letter} = {m:Value|cdot}{v2:Value} = {p2:Value},',
    u'{p:Letter} &= \\sqrt{ {p1:Letter}^2 + {p2:Letter}^2 } = {m:Letter}\\sqrt{ {v1:Letter}^2 + {v2:Letter}^2 } = {p:Value}.',
])
@variant.arg(v1__v2__v=[(
    u'v_1 = %d м / с' % v1,
    u'v_2 = %d м / с' % v2,
    u'v = %d м / с' % v3,
) for v1, v2, v3 in [
    (3, 4, 5),
    (5, 12, 13),
    (7, 24, 25),
]])
@variant.arg(m=[u'm = %d кг' % m for m in [2, 5, 10]])
class Ch_3_3(variant.VariantTask):
    def GetUpdate(self, m=None, v1=None, v2=None, v=None, **kws):
        return dict(
            p1=u'p_1 = %d кг м / с' % (m.Value * v1.Value),
            p2=u'p_2 = %d кг м / с' % (m.Value * v2.Value),
            p=u'p = %d кг м / с' % (m.Value * v.Value),
        )


@variant.text(u'''
    Паровоз массой {M:Task:e}, скорость которого равна {v:Task:e},
    сталкивается с двумя неподвижными вагонами массой {m:Task:e} каждый и сцепляется с ними.
    Запишите (формулами, не числами) импульсы каждого из тел до и после сцепки и после,
    а также определите скорость их совместного движения.
''')
@variant.answer_align([
    u"\\text{ ЗСИ: } &M\\cdot v + m \\cdot 0 + m \\cdot 0 =  M \\cdot v' + m \\cdot v' + m \\cdot v' \\implies",
    u"&\\implies v' = v\\cdot \\frac{ M }{ M + 2m } = {v:Value|cdot} \\frac{M:Value|s}{ {M:Value} + 2 \\cdot {m:Value} } \\approx {u:Value}.",
])
@variant.arg(M=[u'M = %d т' % M for M in [120, 150, 210]])
@variant.arg(m=[u'm = %d т' % m for m in [30, 40, 50]])
@variant.arg(v=[u'v = %.2f м / с' % v for v in [0.2, 0.4, 0.6]])
class Ch_3_24(variant.VariantTask):
    def GetUpdate(self, m=None, M=None, v=None, **kws):
        return dict(
            u=u'v\' = %.2f м / с' % (1.0 * v.Value * M.Value / (M.Value + 2 * m.Value)),
        )


@variant.text(u'''
    Два тела двигаются навстречу друг другу. Скорость каждого из них составляет {v:Task:e}.
    После соударения тела слиплись и продолжили движение уже со скоростью {u:Task:e}.
    Определите отношение масс тел.
''')
@variant.arg(v=[u'v = %f м / с' % v for v in [3, 4, 5, 6]])
@variant.arg(u=[u'u = %.1f м / с' % u for u in [1.0, 1.5, 2.0]])
class Ch_3_26(variant.VariantTask):
    pass


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
