# -*- coding: utf-8 -*-

import variant
from value import UnitValue

import logging
log = logging.getLogger(__name__)


TableValues = {
    'water': {
        'c': UnitValue(u'4200 Дж / кг К'),
        'lmbd': UnitValue(u'340 кДж / кг'),
        'L': UnitValue(u'2.3 МДж / кг'),
    },
    'lead': {  # свинец
        'lmbd': UnitValue(u'25 кДж / кг'),
    },
    'aluminum': { # алюминий
        'c': UnitValue(u'920 Дж / кг К'),
        'lmbd': UnitValue(u'390 кДж / кг'),
    },
    'copper': { # медь
        'lmbd': UnitValue(u'210 кДж / кг'),
    },
    'steel': { # сталь
        'c': UnitValue(u'500 Дж / кг К'),
        'lmbd': UnitValue(u'84 кДж / кг'),
    },
    'zinc': { # цинк
        'c': UnitValue(u'400 Дж / кг К'),
    },
}

@variant.text(u'''
    Сколько льда при температуре $0\\celsius$ можно расплавить,
    сообщив ему энергию {Q:Value:e}?
    Здесь (и во всех следующих задачах) используйте табличные значения из учебника.
''')
@variant.answer(u'''$
    Q 
        = \\lambda m \\implies m
        = \\frac Q{{\\lambda}}
        = \\frac {Q:Value:s}{lmbd:Value:s}
        \\approx {m:Value}
$''')
@variant.args({
    'Q': [u'Q = %d МДж' % Q for Q in [2, 3, 4, 5, 6, 7, 8, 9]],
})
class Ch_8_6(variant.VariantTask):
    def GetUpdate(self, Q=None, **kws):
        lmbd = TableValues['water']['lmbd']
        return {
            'lmbd': lmbd,
            'm': u'm = %.1f кг' % (1000. * Q.Value / lmbd.Value),
        }

@variant.text(u'''
    Какое количество теплоты выделится при затвердевании {m:Value:e} расплавленного {metall} при температуре плавления?
''')
@variant.answer(u'''$
    Q
        = - \\lambda m
        = - {lmbd:Value} \\cdot {m:Value}
        = - {Q:Value} \\implies \\abs{{Q}} = {Q:Value}
$''')
@variant.args({
     'm': [u'm = %d кг' % m for m in [15, 20, 25, 30, 50, 75]],
     ('metall', 'lmbd'): [
        (u'свинца', TableValues['lead']['lmbd']),
        (u'меди', TableValues['copper']['lmbd']),
        (u'алюминия', TableValues['aluminum']['lmbd']),
        (u'стали', TableValues['steel']['lmbd']),
     ],
})
class Ch_8_7(variant.VariantTask):
    def GetUpdate(self, m=None, metall=None, lmbd=None, **kws):
        return {
            'Q': u'Q = %.1f МДж' % (0.001 * m.Value * lmbd.Value),
        }

@variant.text(u'''
    Какое количество теплоты необходимо для превращения воды массой {m:Value:e} при $t = {t}\\celsius$
    в пар при температуре $t_{{100}} = 100\\celsius$?
''')
@variant.answer(u'''$
    Q
        = cm\\Delta t + Lm
        = m\\cbr{{c(t_{{100}} - t) + L}}
        = {m:Value} \\cdot \\cbr{{{c:Value}\\cbr{{100\\celsius - {t}\\celsius}} + {L:Value}}}
        = {Q:Value}
$''')
@variant.args({
    'm': [u'm = %d кг' % m for m in [2, 3, 4, 5, 15]],
    't': [20, 30, 40, 50, 60, 70],
})
class Ch_8_10(variant.VariantTask):
    def GetUpdate(self, m=None, t=None, **kws):
        c = TableValues['water']['c']
        L = TableValues['water']['L']
        return {
            'c': c,
            'L': L,
            'Q': u'Q = %.2f МДж' % (m.Value * ((100. - t) * c.Value / 10 ** 6 + L.Value)),
        }


@variant.text(u'''
    Воду температурой $t = {t}\\celsius$ нагрели и превратили в пар при температуре $t_{{100}} = 100\\celsius$,
    потратив {Q:Value:e}. Определите массу воды.
''')
@variant.answer(u'''$
    Q
        = cm\\Delta t + Lm
        = m\\cbr{{c(t_{{100}} - t) + L}}
    \\implies
    m = \\frac{{Q}}{{c(t_{{100}} - t) + L}}
        = \\frac {Q:Value:s}{{{c:Value}\\cbr{{100\\celsius - {t}\\celsius}} + {L:Value}}}
        \\approx {m:Value}
$''')
@variant.args(
{
     'Q': [u'Q = %d кДж' % Q for Q in [2000, 2500, 4000, 5000]],
     't': [10, 30, 40, 50, 60, 70],
})
class Ch_8_13(variant.VariantTask):
    def GetUpdate(self, Q=None, t=None, **kws):
        c =  TableValues['water']['c']
        L = TableValues['water']['L']
        return {
            'c': c,
            'L': L,
            'm': u'Q = %.2f кг' % (1000. * Q.Value / ((100. - t) * c.Value + 1. * L.Value * 10 ** 6)),
        }


@variant.text(u'''
    {metall} тело температурой $T = {T}\\celsius$ опустили
    в воду температурой $t = {t}\\celsius$, масса которой равна массе тела.
    Определите, какая температура установится в сосуде.
''')
@variant.answer(u'''\\begin{{align*}}
    Q_1 + Q_2 &= 0, \\\\
    Q_1 &= c_1 m_1 \\Delta t_1 = c_1 m (\\theta - t_1), \\\\
    Q_2 &= c_2 m_2 \\Delta t_2 = c_2 m (\\theta - t_2), \\\\
    c_1 m (\\theta - t_1) + c_2 m (\\theta - t_2) &= 0, \\\\
    c_1 (\\theta - t_1) + c_2 (\\theta - t_2) &= 0, \\\\
    c_1 \\theta - c_1 t_1 + c_2 \\theta - c_2 t_2 &= 0, \\\\
    (c_1 + c_2)\\theta &= c_1 t_1 + c_2 t_2, \\\\
    \\theta &= \\frac{{c_1 t_1 + c_2 t_2}}{{c_1 + c_2}}
        = \\frac{{{c1:Value} \\cdot {t1}\\celsius + {c2:Value} \\cdot {t2}\\celsius}}{{{c1:Value} + {c2:Value}}}
        \\approx {theta} \\celsius.
\\end{{align*}}''')
@variant.args({
    ('metall', 'c'): [
        (u'Стальное', TableValues['steel']['c']),
        (u'Алюминиевое', TableValues['aluminum']['c']),
        (u'Цинковое', TableValues['zinc']['c']),
    ],
    'T': [70, 80, 90, 100],
    't': [10, 20, 30],
})
class Ch_8_35(variant.VariantTask):
    def GetUpdate(self, metall=None, T=None, t=None, c=None, **kws):
        c_water = TableValues['water']['c']
        return {
            'c1': c_water,
            'c2': c,
            't1': t,
            't2': T,
            'theta': '%.1f' % ((1. * c_water.Value * t + 1. * c.Value * T) / (1. * c_water.Value + 1. * c.Value)),
        }
