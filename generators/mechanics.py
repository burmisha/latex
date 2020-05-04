# -*- coding: utf-8 -*-

import variant

import logging
log = logging.getLogger(__name__)


@variant.text(u'''
    Шарики массами {m1:Value:e} и {m2:Value:e}
    движутся параллельно друг другу в одном направлении
    со скоростями {v1:Value:e} и {v2:Value:e} соответсвенно.
    Сделайте рисунок и укажите направления скоростей и импульсов.
    Определите импульс каждого из шариков, а также их суммарный импульс.
''')
@variant.answer(u'''
    \\begin{{align*}}
        {p1:Letter} &= {m1:Letter}{v1:Letter} = {m1:Value}\\cdot{v1:Value} = {p1:Value}, \\\\
        {p2:Letter} &= {m2:Letter}{v2:Letter} = {m2:Value}\\cdot{v2:Value} = {p2:Value}, \\\\
        {p:Letter} &= {p1:Letter} + {p2:Letter} = {m1:Letter}{v1:Letter} + {m2:Letter}{v2:Letter} = {p:Value}.
    \\end{{align*}}
''')
@variant.args({
    (u'm1', u'm2'): [(u'm_1 = %d кг' % m1, u'm_2 = %d кг' % m2) for m1 in [1, 2, 3, 4] for m2 in [1, 2, 3, 4] if m1 != m2],
    u'v1': [u'v_1 = %d м / с' % v1 for v1 in [2, 4, 5, 10]],
    u'v2': [u'v_2 = %d м / с' % v2 for v2 in[3, 6, 8]],
})
class Ch_3_1(variant.VariantTask):
    def GetUpdate(self, m1=None, m2=None, v1=None, v2=None, **kws):
        return {
            'p1': u'p_1 = %d кг м / с' % (m1.Value * v1.Value),
            'p2': u'p_2 = %d кг м / с' % (m2.Value * v2.Value),
            'p': u'p = %d кг м / с' % (m1.Value * v1.Value + m2.Value * v2.Value),
        }


@variant.text(u'''
    Два шарика, масса каждого из которого составляет {m:Value:e},
    движутся навстречу друг другу.
    Скорость одного из них {v1:Value:e}, а другого~--- {v2:Value:e}.
    Сделайте рисунок, укажите направления скоростей и импульсов.
    Определите импульс каждого из шариков, а также их суммарный импульс.
''')
@variant.answer(u'''
    \\begin{{align*}}
        {p1:Letter} &= {m:Letter}{v1:Letter} = {m:Value}\\cdot{v1:Value} = {p1:Value}, \\\\
        {p2:Letter} &= {m:Letter}{v2:Letter} = {m:Value}\\cdot{v2:Value} = {p2:Value}, \\\\
        {p:Letter} &= {p1:Letter} - {p2:Letter} = {m:Letter}({v1:Letter} - {v2:Letter}) = {p:Value}.
    \\end{{align*}}
''')
@variant.args({
    'm': [u'm = %d кг' % m for m in [2, 5, 10]],
    'v1': [u'v_1 = %d м / с' % v1 for v1 in [1, 2, 5, 10]],
    'v2': [u'v_2 = %d м / с' % v2 for v2 in [3, 6, 8]],
})
class Ch_3_2(variant.VariantTask):
    def GetUpdate(self, m=None, v1=None, v2=None, **kws):
        return {
            'p1': u'p_1 = %d кг м / с' % (m.Value * v1.Value),
            'p2': u'p_2 = %d кг м / с' % (m.Value * v2.Value),
            'p': u'p = %d кг м / с' % (m.Value * v1.Value - m.Value * v2.Value),
        }


@variant.text(u'''
    Два одинаковых шарика массами по {m:Value:e}
    движутся во взаимно перпендикулярных направлениях.
    Скорости шариков составляют {v1:Value:e} и {v2:Value:e}.
    Сделайте рисунок, укажите направления скоростей и импульсов.
    Определите импульс каждого из шариков и полный импульс системы.
''')
@variant.answer(u'''\\begin{{align*}}
    {p1:Letter} &= {m:Letter}{v1:Letter} = {m:Value}\\cdot{v1:Value} = {p1:Value}, \\\\
    {p2:Letter} &= {m:Letter}{v2:Letter} = {m:Value}\\cdot{v2:Value} = {p2:Value}, \\\\
    {p:Letter}
        &= \\sqrt{{{p1:Letter}^2 + {p2:Letter}^2}}
        = {m:Letter}\\sqrt{{{v1:Letter}^2 + {v2:Letter}^2}} = {p:Value}.
\\end{{align*}}''')
@variant.args({
    'm': [u'm = %d кг' % m for m in [2, 5, 10]],
    ('v1', 'v2', 'v'): [(
        u'v_1 = %d м / с' % v1,
        u'v_2 = %d м / с' % v2,
        u'v = %d м / с' % v3,
    ) for v1, v2, v3 in [
        (3, 4, 5),
        (5, 12, 13),
        (7, 24, 25),
    ]],
})
class Ch_3_3(variant.VariantTask):
    def GetUpdate(self, m=None, v1=None, v2=None, v=None, **kws):
        return {
            'p1': u'p_1 = %d кг м / с' % (m.Value * v1.Value),
            'p2': u'p_2 = %d кг м / с' % (m.Value * v2.Value),
            'p': u'p = %d кг м / с' % (m.Value * v.Value),
        }


@variant.text(u'''
    Паровоз массой {M:Task:e}, скорость которого равна {v:Task:e},
    сталкивается с двумя неподвижными вагонами массой {m:Task:e} каждый и сцепляется с ними.
    Запишите (формулами, не числами) импульсы каждого из тел до и после сцепки и после,
    а также определите скорость их совместного движения.
''')
@variant.answer(u'''\\begin{{align*}}
    \\text{{ЗСИ: }} &M\\cdot v + m\\cdot 0 + m \\cdot 0 =  M\\cdot v' + m\\cdot v' + m \\cdot v' \\implies \\\\
    &\\implies v' = v\\cdot \\frac{{M}}{{M + 2m}}
      = {v:Value}\\cdot \\frac{{{M:Value}}}{{{M:Value} + 2 \\cdot {m:Value}}} \\approx {u:Value}.
\\end{{align*}}''')
@variant.args({
    'M': [u'M = %d т' % M for M in [120, 150, 210]],
    'm': [u'm = %d т' % m for m in [30, 40, 50]],
    'v': [u'v = %.2f м / с' % v for v in [0.2, 0.4, 0.6]],
})
class Ch_3_24(variant.VariantTask):
    def GetUpdate(self, m=None, M=None, v=None, **kws):
        return {
            'u': u'v\' = %.2f м / с' % (1.0 * v.Value * M.Value / (M.Value + 2 * m.Value)),
        }


@variant.text(u'''
    Два тела двигаются навстречу друг другу. Скорость каждого из них составляет {v:Task:e}.
    После соударения тела слиплись и продолжили движение уже со скоростью {u:Task:e}.
    Определите отношение масс тел.
''')
@variant.args({
    'v': [u'v = %f м / с' % v for v in [3, 4, 5, 6]],
    'u': [u'u = %.1f м / с' % u for u in [1.0, 1.5, 2.0]],
})
class Ch_3_26(variant.VariantTask):
    pass
