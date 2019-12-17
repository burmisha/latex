# -*- coding: utf-8 -*-

import itertools
import logging

import problems
import variant
from variant import UnitValue as UV

log = logging.getLogger(__name__)


class Ch_8_6(variant.VariantTask):
    def __call__(self, Q=None):
        text = u'''
            Сколько льда при температуре $0\\celsius$ можно расплавить,
            сообщив ему энергию {Q:ShortTask:e}? 
            Здесь (и во всех следующих задачах) используйте табличные значения из учебника.
        '''.format(Q=Q)

        return problems.task.Task(text)

    def All(self):
        for Q in itertools.product(
             [2, 3, 4, 5, 6, 7, 8, 9],
        ):
            yield self.__call__(
                Q=UV(u'Q = %d МДж' % Q),
            )


class Ch_8_7(variant.VariantTask):
    def __call__(self, m=None, metall=None):
        text = u'''
            Какое количество теплоты выделится при затвердевании {m:ShortTask:e} расплавленного {metall} при температуре плавления?
        '''.format(m=m, metall=metall)

        return problems.task.Task(text)

    def All(self):
        for m, metall in itertools.product(
             [15, 20, 25, 30, 50, 75],
             [
                u'свинца',
                u'меди',
                u'алюминия',
                u'стали',
             ]
        ):
            yield self.__call__(
                m=UV(u'm = %d кг' % m),
                metall=metall,
            )


class Ch_8_10(variant.VariantTask):
    def __call__(self, m=None, t=None):
        text = u'''
            Какое количество теплоты необходимо для превращения воды массой {m:ShortTask:e} при $t = {t}\\celsius$
            в пар при температуре $t_{{100}} = 100\\celsius$?
        '''.format(m=m, t=t)

        return problems.task.Task(text)

    def All(self):
        for m, t in itertools.product(
             [2, 3, 4, 5, 15],
             [20, 30, 40, 50, 60, 70],
        ):
            yield self.__call__(
                m=UV(u'm = %d кг' % m),
                t=t,
            )


class Ch_8_13(variant.VariantTask):
    def __call__(self, Q=None, t=None):
        text = u'''
            Воду температурой $t = {t}\\celsius$ нагрели и превратили в пар при температуре $t_{{100}} = 100\\celsius$,
            потратив {Q:ShortTask:e}. Определите массу воды.
        '''.format(Q=Q, t=t)

        return problems.task.Task(text)

    def All(self):
        for Q, t in itertools.product(
             [2000, 2500, 4000, 5000],
             [10, 30, 40, 50, 60, 70],
        ):
            yield self.__call__(
                Q=UV(u'Q = %d кДж' % Q),
                t=t,
            )


class Ch_8_35(variant.VariantTask):
    def __call__(self, metall=None, T=None, t=None):
        text = u'''
            {metall} тело температурой $T = {T}\\celsius$ опустили 
            в воду температурой $t = {t}\\celsius$, масса которой равна массе тела.
            Определите, какая температура установится в сосуде.
        '''.format(metall=metall, T=T, t=t)

        return problems.task.Task(text)

    def All(self):
        for metall, T, t in itertools.product(
             [
                u'Стальное',
                u'Алюминиевое',
                u'Цинковое'
            ],
             [70, 80, 90, 100],
             [10, 20, 30],
        ):
            yield self.__call__(
                metall=metall,
                T=T,
                t=t,
            )

