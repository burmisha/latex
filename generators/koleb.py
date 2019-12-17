# -*- coding: utf-8 -*-

import itertools
import logging

import problems
import variant
from variant import UnitValue

log = logging.getLogger(__name__)


class Nu01(variant.VariantTask):
    def __call__(self, free=None, const=None):
        text = u'''
            Запишите определения:
            \\begin{itemize}
                \\item гармонические колебания,
        '''
        if free:
            text += u'''\item   свободные колебания,'''
        else:
            text += u'''\item   вынужденные колебания,'''
        if const:
            text += u'''\item   незатухающие колебания,'''
        else:
            text += u'''\item   затухающие колебания.'''
        text += u'''
            \\end{itemize}
        '''
        return problems.task.Task(text)

    def All(self):
        for free, const in itertools.product(
            [False, True],
            [False, True],
        ):
            yield self.__call__(free=free, const=const)


class Nu02(variant.VariantTask):
    def __call__(self, T=None):
        text = u'''
            Определите частоту колебаний, если их период составляет {T:Task:e}.
        '''.format(T=T)
        return problems.task.Task(text)

    def All(self):
        for T in itertools.product(
            [2, 4, 5, 10, 20, 40, 50],
        ):
            yield self.__call__(T=UnitValue(u'T = %d мс' % T))


class Nu03(variant.VariantTask):
    def __call__(self, nu=None, t=None):
        text = u'''
            Определите период колебаний, если их частота составляет {nu:Task:e}.
            Сколько колебаний произойдёт за {t:Task:e}?
        '''.format(nu=nu, t=t)
        return problems.task.Task(text)

    def All(self):
        for nu, t in itertools.product(
            [2, 4, 5, 10, 20, 40, 50],
            [1, 2, 3, 5, 10],
        ):
            yield self.__call__(
                nu=UnitValue(u'\\nu = %d кГц' % nu),
                t=UnitValue(u't = %d мин' % t),
            )


class Nu04(variant.VariantTask):
    def __call__(self, A=None, nu=None, t=None):
        text = u'''
            Амплитуда колебаний точки составляет {A:Task:e}, а частота~--- {nu:Task:e}.
            Определите, какой путь преодолеет эта точка за {t:Task:e}.
        '''.format(A=A, nu=nu, t=t)
        return problems.task.Task(text)

    def All(self):
        for A, nu, t in itertools.product(
            [2, 3, 5, 10, 15],
            [2, 5, 6, 10, 20],
            [10, 40, 80],
        ):
            yield self.__call__(
                A=UnitValue(u'A = %d см' % A),
                nu=UnitValue(u'\\nu = %d Гц' % nu),
                t=UnitValue(u't = %d с' % t),
            )
