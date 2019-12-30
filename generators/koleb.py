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
        nu = UnitValue(u'''\\nu = %d Гц''' % (1000 / T.Value))
        answer = u'''
            $\\nu = \\frac 1T = \\frac 1{T:Value:s} = {nu:Value}$
        '''.format(T=T, nu=nu)
        return problems.task.Task(text, answer=answer)

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
        T = UnitValue(u'''T = %.3f мc''' % (1. / nu.Value))
        N = UnitValue(u'''N = %d колебаний''' % (nu.Value * 1000 * t.Value * 60))
        answer = u'''
            \\begin{{align*}}
                T &= \\frac 1\\nu = \\frac 1{nu:Value:s} = {T:Value}, \\\\
                N &= \\nu t = {nu:Value}\\cdot{t:Value} = {N:Value}.
            \\end{{align*}}
        '''.format(T=T, nu=nu, N=N, t=t)
        return problems.task.Task(text, answer=answer)

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
        s = UnitValue(u'%.1f м' % (4. * A.Value / 100 * t.Value * nu.Value))
        answer = u'''$
            s 
                = 4A \\cdot N = 4A \\cdot \\frac tT = 4A \\cdot t\\nu
                = 4 \\cdot {A:Value} \\cdot {t:Value} \\cdot {nu:Value}
                = {s:Value}
        $'''.format(A=A, nu=nu, t=t, s=s)
        return problems.task.Task(text, answer=answer)

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


class Nu05(variant.VariantTask):
    def __call__(self, A=None, T=None):
        text = u'''
            Изобразите график гармонических колебаний, амплитуда которых составляла бы
            {A:Task:e}, а период {T:Task:e}.
        '''.format(A=A, T=T)
        return problems.task.Task(text)

    def All(self):
        for A, T in itertools.product(
            [1, 2, 3, 5, 6, 15, 30, 40, 75],
            [2, 4, 6, 8, 10],
        ):
            yield self.__call__(
                A=UnitValue(u'A = %d см' % A),
                T=UnitValue(u'T = %d с' % T),
            )
