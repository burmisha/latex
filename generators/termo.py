# -*- coding: utf-8 -*-

import itertools
import logging

import problems
import variant
from value import UnitValue

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

class Ch_8_6(variant.VariantTask):
    def __call__(self, Q=None):
        text = u'''
            Сколько льда при температуре $0\\celsius$ можно расплавить,
            сообщив ему энергию {Q:ShortTask:e}?
            Здесь (и во всех следующих задачах) используйте табличные значения из учебника.
        '''.format(Q=Q)
        lmbd = TableValues['water']['lmbd']
        m = UnitValue(u'%.1f кг' % (1000. * Q.Value / lmbd.Value))
        answer = u'''$
            Q = \\lambda m \\implies m
                = \\frac Q{{\\lambda}}
                = \\frac {Q:Value:s}{lmbd:Value:s}
                \\approx {m:Value}
        $'''.format(Q=Q, lmbd=lmbd, m=m)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for Q in itertools.product(
             [2, 3, 4, 5, 6, 7, 8, 9],
        ):
            yield self.__call__(
                Q=UnitValue(u'Q = %d МДж' % Q),
            )


class Ch_8_7(variant.VariantTask):
    def __call__(self, m=None, metall=None, lmbd=None):
        text = u'''
            Какое количество теплоты выделится при затвердевании {m:ShortTask:e} расплавленного {metall} при температуре плавления?
        '''.format(m=m, metall=metall)
        Q = UnitValue(u'Q = %.1f МДж' % (0.001 * m.Value * lmbd.Value))
        answer = u'''$
            Q
                = - \\lambda m
                = - {lmbd:Value} \\cdot {m:Value}
                = - {Q:Value} \\implies \\abs{{Q}} = {Q:Value}
        $'''.format(m=m, lmbd=lmbd, Q=Q)

        return problems.task.Task(text, answer=answer)

    def All(self):
        for m, (metall, lmbd) in itertools.product(
             [15, 20, 25, 30, 50, 75],
             [
                (u'свинца', TableValues['lead']['lmbd']),
                (u'меди', TableValues['copper']['lmbd']),
                (u'алюминия', TableValues['aluminum']['lmbd']),
                (u'стали', TableValues['steel']['lmbd']),
             ]
        ):
            yield self.__call__(
                m=UnitValue(u'm = %d кг' % m),
                metall=metall,
                lmbd=lmbd,
            )


class Ch_8_10(variant.VariantTask):
    def __call__(self, m=None, t=None):
        text = u'''
            Какое количество теплоты необходимо для превращения воды массой {m:ShortTask:e} при $t = {t}\\celsius$
            в пар при температуре $t_{{100}} = 100\\celsius$?
        '''.format(m=m, t=t)
        c = TableValues['water']['c']
        L = TableValues['water']['L']
        Q = UnitValue(u'Q = %.2f МДж' % (m.Value * ((100. - t) * c.Value / 10 ** 6 + L.Value)))
        answer = u'''$
            Q
                = cm\\Delta t + Lm
                = m\\cbr{{c(t_{{100}} - t) + L}}
                = {m:Value} \\cdot \\cbr{{{c:Value}\\cbr{{100\\celsius - {t}\\celsius}} + {L:Value}}}
                = {Q:Value}
        $'''.format(m=m, t=t, c=c, L=L, Q=Q)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for m, t in itertools.product(
             [2, 3, 4, 5, 15],
             [20, 30, 40, 50, 60, 70],
        ):
            yield self.__call__(
                m=UnitValue(u'm = %d кг' % m),
                t=t,
            )


class Ch_8_13(variant.VariantTask):
    def __call__(self, Q=None, t=None):
        text = u'''
            Воду температурой $t = {t}\\celsius$ нагрели и превратили в пар при температуре $t_{{100}} = 100\\celsius$,
            потратив {Q:ShortTask:e}. Определите массу воды.
        '''.format(Q=Q, t=t)
        c = TableValues['water']['c']
        L = TableValues['water']['L']
        m = UnitValue(u'Q = %.2f кг' % (1000. * Q.Value / ((100. - t) * c.Value + 1. * L.Value * 10 ** 6)))
        answer = u'''$
            Q
                = cm\\Delta t + Lm
                = m\\cbr{{c(t_{{100}} - t) + L}}
            \\implies
            m = \\frac{{Q}}{{c(t_{{100}} - t) + L}}
                = \\frac {Q:Value:s}{{{c:Value}\\cbr{{100\\celsius - {t}\\celsius}} + {L:Value}}}
                \\approx {m:Value}
        $'''.format(m=m, t=t, c=c, L=L, Q=Q)

        return problems.task.Task(text, answer=answer)

    def All(self):
        for Q, t in itertools.product(
             [2000, 2500, 4000, 5000],
             [10, 30, 40, 50, 60, 70],
        ):
            yield self.__call__(
                Q=UnitValue(u'Q = %d кДж' % Q),
                t=t,
            )


class Ch_8_35(variant.VariantTask):
    def __call__(self, metall=None, T=None, t=None, c=None):
        text = u'''
            {metall} тело температурой $T = {T}\\celsius$ опустили
            в воду температурой $t = {t}\\celsius$, масса которой равна массе тела.
            Определите, какая температура установится в сосуде.
        '''.format(metall=metall, T=T, t=t)
        c_water = TableValues['water']['c']
        theta = (1. * c_water.Value * t + 1. * c.Value * T) / (1. * c_water.Value + 1. * c.Value)
        answer = u'''
            \\begin{{align*}}
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
            \\end{{align*}}
        '''.format(c1=c_water, t1=t, c2=c, t2=T, theta='%.1f' % theta)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for (metall, c), T, t in itertools.product(
             [
                (u'Стальное', TableValues['steel']['c']),
                (u'Алюминиевое', TableValues['aluminum']['c']),
                (u'Цинковое', TableValues['zinc']['c']),
            ],
             [70, 80, 90, 100],
             [10, 20, 30],
        ):
            yield self.__call__(
                metall=metall,
                T=T,
                t=t,
                c=c,
            )

