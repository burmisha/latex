# -*- coding: utf-8 -*-

import itertools
import logging

import problems
import variant
from value import UnitValue

log = logging.getLogger(__name__)


class Ch_3_1(variant.VariantTask):
    def __call__(self, masses=None, speeds=None):
        text = u'''
            Шарики массами {m1:ShortTask:e} и {m2:ShortTask:e} 
            движутся параллельно друг другу в одном направлении
            со скоростями {v1:ShortTask:e} и {v2:ShortTask:e} соответсвенно.
            Сделайте рисунок и укажите направления скоростей и импульсов.
            Определите импульс каждого из шариков, а также их суммарный импульс.
        '''.format(m1=masses[0], m2=masses[1], v1=speeds[0], v2=speeds[1])

        p1 = UnitValue(u'p_1 = %d кг м / с' % (masses[0].Value * speeds[0].Value))
        p2 = UnitValue(u'p_2 = %d кг м / с' % (masses[1].Value * speeds[1].Value))
        p = UnitValue(u'p = %d кг м / с' % (masses[0].Value * speeds[0].Value + masses[1].Value * speeds[1].Value))
        answer = u'''
            \\begin{{align*}}
                {p1:Letter} &= {m1:Letter}{v1:Letter} = {m1:Value}\\cdot{v1:Value} = {p1:Value}, \\\\
                {p2:Letter} &= {m2:Letter}{v2:Letter} = {m2:Value}\\cdot{v2:Value} = {p2:Value}, \\\\
                {p:Letter} &= {p1:Letter} + {p2:Letter} = {m1:Letter}{v1:Letter} + {m2:Letter}{v2:Letter} = {p:Value}.
            \\end{{align*}}
        '''.format(m1=masses[0], m2=masses[1], v1=speeds[0], v2=speeds[1], p1=p1, p2=p2, p=p)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for m1, m2, v1, v2 in itertools.product(
            [1, 2, 3, 4],
            [1, 2, 3, 4],
            [2, 4, 5, 10],
            [3, 6, 8],
        ):
            if m1 != m2 and v1 != v2:
                yield self.__call__(
                    masses=[
                        UnitValue(u'm_1 = %d кг' % m1),
                        UnitValue(u'm_2 = %d кг' % m2),
                    ],
                    speeds=[
                        UnitValue(u'v_1 = %d м / с' % v1),
                        UnitValue(u'v_2 = %d м / с' % v2),
                    ],
                )


class Ch_3_2(variant.VariantTask):
    def __call__(self, m=None, speeds=None):
        text = u'''
            Два шарика, масса каждого из которого составляет {m:ShortTask:e},
            движутся навстречу друг другу.
            Скорость одного из них {v1:ShortTask:e}, а другого~--- {v2:ShortTask:e}.
            Сделайте рисунок, укажите направления скоростей и импульсов.
            Определите импульс каждого из шариков, а также их суммарный импульс.
        '''.format(m=m, v1=speeds[0], v2=speeds[1])

        p1 = UnitValue(u'p_1 = %d кг м / с' % (m.Value * speeds[0].Value))
        p2 = UnitValue(u'p_2 = %d кг м / с' % (m.Value * speeds[1].Value))
        p = UnitValue(u'p = %d кг м / с' % (m.Value * speeds[0].Value - m.Value * speeds[1].Value))
        answer = u'''
            \\begin{{align*}}
                {p1:Letter} &= {m:Letter}{v1:Letter} = {m:Value}\\cdot{v1:Value} = {p1:Value}, \\\\
                {p2:Letter} &= {m:Letter}{v2:Letter} = {m:Value}\\cdot{v2:Value} = {p2:Value}, \\\\
                {p:Letter} &= {p1:Letter} - {p2:Letter} = {m:Letter}({v1:Letter} - {v2:Letter}) = {p:Value}.
            \\end{{align*}}
        '''.format(m=m, v1=speeds[0], v2=speeds[1], p1=p1, p2=p2, p=p)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for m, v1, v2 in itertools.product(
            [2, 5, 10],
            [1, 2, 5, 10],
            [3, 6, 8],
        ):
            yield self.__call__(
                m=UnitValue(u'm = %d кг' % m),
                speeds=[
                    UnitValue(u'v_1 = %d м / с' % v1),
                    UnitValue(u'v_2 = %d м / с' % v2),
                ],
            )


class Ch_3_3(variant.VariantTask):
    def __call__(self, m=None, speeds=None):
        text = u'''
            Два одинаковых шарика массами по {m:ShortTask:e}
            движутся во взаимно перпендикулярных направлениях.
            Скорости шариков составляют {v1:ShortTask:e} и {v2:ShortTask:e}.
            Сделайте рисунок, укажите направления скоростей и импульсов.
            Определите импульс каждого из шариков и полный импульс системы.
        '''.format(m=m, v1=speeds[0], v2=speeds[1])

        p1 = UnitValue(u'p_1 = %d кг м / с' % (m.Value * speeds[0].Value))
        p2 = UnitValue(u'p_2 = %d кг м / с' % (m.Value * speeds[1].Value))
        p = UnitValue(u'p = %d кг м / с' % (m.Value * speeds[2].Value))
        answer = u'''
            \\begin{{align*}}
                {p1:Letter} &= {m:Letter}{v1:Letter} = {m:Value}\\cdot{v1:Value} = {p1:Value}, \\\\
                {p2:Letter} &= {m:Letter}{v2:Letter} = {m:Value}\\cdot{v2:Value} = {p2:Value}, \\\\
                {p:Letter} 
                    &= \\sqrt{{{p1:Letter}^2 + {p2:Letter}^2}} 
                    = {m:Letter}\\sqrt{{{v1:Letter}^2 + {v2:Letter}^2}} = {p:Value}.
            \\end{{align*}}
        '''.format(m=m, v1=speeds[0], v2=speeds[1], p1=p1, p2=p2, p=p)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for m, (v1, v2, v3) in itertools.product(
            [2, 5, 10],
            [
                (3, 4, 5),
                (5, 12, 13),
                (7, 24, 25),
            ],
        ):
            yield self.__call__(
                m=UnitValue(u'm = %d кг' % m),
                speeds=[
                    UnitValue(u'v_1 = %d м / с' % v1),
                    UnitValue(u'v_2 = %d м / с' % v2),
                    UnitValue(u'%d м / с' % v3),
                ],
            )

class Ch_3_24(variant.VariantTask):
    def __call__(self, m=None, M=None, v=None):
        text = u'''
            Паровоз массой {M:Task:e}, скорость которого равна {v:Task:e}, 
            сталкивается с двумя неподвижными вагонами массой {m:Task:e} каждый и сцепляется с ними.
            Запишите (формулами, не числами) импульсы каждого из тел до и после сцепки и после,
            а также определите скорость их совместного движения.
        '''.format(m=m, M=M, v=v)

        u = UnitValue(u'%.2f м / с' % (1.0 * v.Value * M.Value / (M.Value + 2 * m.Value)))
        answer = u'''
            \\begin{{align*}}
                \\text{{ЗСИ: }} &M\\cdot v + m\\cdot 0 + m \\cdot 0 =  M\\cdot v' + m\\cdot v' + m \\cdot v' \\implies \\\\
                &\\implies v' = v\\cdot \\frac{{M}}{{M + 2m}} 
                  = {v:Value}\\cdot \\frac{{{M:Value}}}{{{M:Value} + 2 \\cdot {m:Value}}} \\approx {u:Value}.
            \\end{{align*}}
        '''.format(m=m, M=M, v=v, u=u)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for M, m, v in itertools.product(
            [120, 150, 210],
            [30, 40, 50],
            [0.2, 0.4, 0.6],
        ):
            yield self.__call__(
                M=UnitValue(u'M = %d т' % M),
                m=UnitValue(u'm = %d т' % m),
                v=UnitValue(u'v = %.2f м / с' % v),
            )


class Ch_3_26(variant.VariantTask):
    def __call__(self, v=None, u=None):
        text = u'''
            Два тела двигаются навстречу друг другу. Скорость каждого из них составляет {v:Task:e}. 
            После соударения тела слиплись и продолжили движение уже со скоростью {u:Task:e}. 
            Определите отношение масс тел.
        '''.format(v=v, u=u)

        return problems.task.Task(text)

    def All(self):
        for v, u in itertools.product(
            [3, 4, 5, 6],
            [1.0, 1.5, 2.0],
        ):
            yield self.__call__(
                v=UnitValue(u'v = %f м / с' % v),
                u=UnitValue(u'u = %.1f м / с' % u),
            )
