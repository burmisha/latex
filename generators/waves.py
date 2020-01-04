# -*- coding: utf-8 -*-
import math

import itertools
import logging

import problems
import variant
from value import UnitValue

log = logging.getLogger(__name__)


class Waves00(variant.VariantTask):
    def __call__(self):
        text = u'''
            Укажите, верны ли утверждения:
            \\begin{itemize}
                \\item механические волны переносят вещество,
                \\item механические волны переносят энергию,
                \\item источником механических волны служат колеблющиеся тела,
                \\item продольные волны могут распространяться только в твёрдых телах,
                \\item в твёрдых телах могут распространяться поперечные волны,
                \\item скорость распространения волны равна произведению её длины на её частоту,
                \\item звуковая волна~--- поперечная волна,
                \\item волна на поверхности озера~--- поперечная волна (или же поверхностная).
            \\end{itemize}
            (4 из 8~--- это «–»)
        '''
        answer = u'''нет, да, да, нет, да, да, нет, да'''
        return problems.task.Task(text, answer=answer, solutionSpace=20)

    def All(self):
        yield self.__call__()


class Waves01(variant.VariantTask):
    def __call__(self, nu=None, alpha=None):
        text = u'''
            Частота собственных малых колебаний пружинного маятника равна ${nu:Task}$.
            Чему станет равен период колебаний, если массу пружинного маятника увеличить в ${alpha}$ раз?
        '''.format(nu=nu, alpha=alpha)
        T1 = UnitValue(u'T\' = %.2f с' % (math.sqrt(int(alpha)) / int(nu.Value)))
        answer = u'''$
            T'  = 2\\pi\\sqrt{{\\frac {{m'}}k}} 
                = 2\\pi\\sqrt{{\\frac {{\\alpha m}}k}}
                = \\sqrt{{\\alpha}} \\cdot 2\\pi\\sqrt{{\\frac mk}}
                = \\sqrt{{\\alpha}} \\cdot T
                = T\\sqrt{{\\alpha}}
                = \\frac 1\\nu \\cdot\\sqrt{{\\alpha}} 
                = \\frac {{\\sqrt{{\\alpha}}}}\\nu
                = \\frac {{\\sqrt{{{alpha}}}}}{nu:Value:s}
                = {T1:Value}
        $'''.format(alpha=alpha, nu=nu, T1=T1)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for nu, alpha in itertools.product(
            [u'2', u'4', u'5', u'8'],
            [u'4', u'16', u'25'],
        ):
            yield self.__call__(
                nu=UnitValue(u'\\nu = %s Гц' % nu),
                alpha=alpha,
            )


class Waves02(variant.VariantTask):
    def __call__(self, m=None, v=None):
        text = u'''
            Тело массой ${m:Task}$ совершает гармонические колебания.
            При этом амплитуда колебаний его скорости равна ${v:Task}$. 
            Определите запас полной механической энергии колебательной системы
            и амплитуду колебаний потенциальной энергии.
        '''.format(m=m, v=v)
        E = UnitValue(u'%.3f Дж' % (0.001 * m.Value * (v.Value ** 2) / 2))
        E2 = UnitValue(u'%.3f Дж' % (0.001 * m.Value * (v.Value ** 2) / 2 / 2))
        answer = u'''
            \\begin{{align*}}
                E_{{\\text{{полная механическая}}}} 
                    &= E_{{\\text{{max кинетическая}}}} 
                    = \\frac{{m v_{{\\max}}^2}}2
                    = \\frac{{{m:Value} \\cdot \\sqr{v:Value:s}}}2
                    = {E:Value},
                \\\\
                A_{{E_{{\\text{{потенциальная}}}}}} &= \\frac {{E_{{\\text{{полная механическая}}}}}}2 = {E2:Value}.
            \\end{{align*}}
        '''.format(m=m, v=v, E=E, E2=E2)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for mLetter, mValue, v in itertools.product(
            [u'm', u'M'],
            [100, 200, 250, 400],
            [1, 2, 4, 5],
        ):
            yield self.__call__(
                m=UnitValue(u'%s = %d г' % (mLetter, mValue)),
                v=UnitValue(u'v = %d м / с' % v),
            )


class Waves03(variant.VariantTask):
    def __call__(self, first=None, second=None, lmbd=None, n1=None, n2=None):
        text = u'''
            Определите расстояние между {first} и {second} гребнями волн,
            если длина волны равна {lmbd:Value:e}. Сколько между ними ещё уместилось гребней?
        '''.format(first=first, second=second, lmbd=lmbd)
        l = UnitValue(u'l = %d м' % ((n2 - n1) * lmbd.Value))
        answer = u'''$
            l 
                = (n_2 - n_1) \\cdot \\lambda 
                = \\cbr{{{n2} - {n1}}} \\cdot {lmbd:Value}
                = {l:Value},
            \\quad
            n = n_2 - n_1 - 1 = {n2} - {n1} - 1 = {n}
        $'''.format(lmbd=lmbd, n1=n1, n2=n2, n=n2 - n1 - 1, l=l)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for (first, n1), (second, n2), lmbd in itertools.product(
            [
                (u'первым', 1),
                (u'вторым', 2),
                (u'третьим', 3),
            ],
            [
                (u'шестым', 6),
                (u'седьмым', 7),
                (u'восьмым', 8),
                (u'девятым', 9),
                (u'десятым', 10),
            ],
            [3, 4, 5, 6],
        ):
            yield self.__call__(
                first=first,
                second=second,
                lmbd=UnitValue(u'\\lambda = %d м' % lmbd),
                n1=n1,
                n2=n2,
            )


class Waves04(variant.VariantTask):
    def __call__(self, T=None, lmbd=None):
        text = u'''
            Определите скорость звука в среде, если источник звука, 
            колеблющийся с периодом {T:Value:e}, возбуждает волны длиной
            {lmbd:Value:e}.
        '''.format(T=T, lmbd=lmbd)
        v = UnitValue(u'v = %.1f м / c' % (1000. * lmbd.Value / T.Value))
        answer = u'''$
            \\lambda 
                = vT \\implies v 
                = \\frac{{\\lambda}}{{T}}
                = \\frac{lmbd:Value:s}{T:Value:s}
                = {v:Value:s}
        $'''.format(T=T, lmbd=lmbd, v=v)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for lmbd, T in itertools.product(
            [1.2, 1.5, 2.1, 2.4],
            [2, 3, 4, 5, 6],
        ):
            yield self.__call__(
                T=UnitValue(u'T = %d мc' % T),
                lmbd=UnitValue(u'\\lambda = %.1f м' % lmbd),
            )


class Waves05(variant.VariantTask):
    def __call__(self, N=None, t=None, v=None):
        text = u'''
            Мимо неподвижного наблюдателя прошло {N:Value:e} гребней волн за {t:Value:e},
            начиная с первого. Каковы длина, период и частота волны, 
            если скорость распространения волн {v:Value:e}?
        '''.format(N=N, t=t, v=v)
        lmbd = UnitValue(u'\\lambda = %.2f м' % (1. * v.Value * t.Value / (N.Value - 1)))
        T = UnitValue(u'T = %.2f с' % (1. * t.Value / (N.Value - 1)))
        nu = UnitValue(u'\\nu = %.2f Гц' % (1. * (N.Value - 1) / t.Value))
        lmbd_1 = UnitValue(u'\\lambda = %.2f м' % (1. * v.Value * t.Value / N.Value))
        T_1 = UnitValue(u'T = %.2f с' % (1. * t.Value / N.Value))
        nu_1 = UnitValue(u'\\nu = %.2f Гц' % (1. * N.Value / t.Value))
        answer = u'''
            \\begin{{align*}}
                \\lambda &= \\frac L{{N-1}} = \\frac {{vt}}{{N-1}} = \\frac {{{v:Value}\\cdot{t:Value}}}{{{N:Value} - 1}} = {lmbd:Value}, \\\\
                T &= \\frac {{\\lambda}}{{v}} = \\frac {{vt}}{{\\cbr{{N-1}}v}} = \\frac {{t}}{{N-1}} =  \\frac {t:Value:s}{{{N:Value} - 1}} = {T:Value}, \\\\
                \\nu &= \\frac 1T = \\frac {{N-1}}{{t}} = \\frac {{{N:Value} - 1}}{t:Value:s} = {nu:Value}. \\\\
                &\\text{{Если же считать гребни целиком, т.е. не вычитать единицу:}} \\\\
                \\lambda' &= \\frac L{{N}} = \\frac {{vt}}{{N}} = \\frac {{{v:Value}\\cdot{t:Value}}}{N:Value:s} = {lmbd_1:Value}, \\\\
                T' &= \\frac {{\\lambda'}}{{v}} = \\frac {{vt}}{{Nv}} = \\frac tN =  \\frac {t:Value:s}{N:Value:s} = {T_1:Value}, \\\\
                \\nu' &= \\frac 1{{T'}} = \\frac {{N}}{{t}} = \\frac {N:Value:s}{t:Value:s} = {nu_1:Value}.
            \\end{{align*}}
        '''.format(lmbd=lmbd, T=T, nu=nu, lmbd_1=lmbd_1, T_1=T_1, nu_1=nu_1, v=v, N=N, t=t)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for N, t, v in itertools.product(
            [4, 5, 6],
            [5, 6, 8, 10],
            [1, 2, 3, 4, 5],
        ):
            yield self.__call__(
                N=UnitValue(u'N = %d' % N),
                t=UnitValue(u't = %d c' % t),
                v=UnitValue(u'v = %d м / с' % v),
            )


class Ch1238(variant.VariantTask):
    def __call__(self, nu_1=None, nu_2=None):
        v = UnitValue(u'v = 320 м / с')
        c = UnitValue(u'c = 300 Мм / с')
        text = u'''
            Сравните длины звуковой волны частотой ${nu_1:Task}$ и радиоволны частотой ${nu_2:Task}$. 
            Какая больше, во сколько раз? Скорость звука примите равной ${v:Task}$.
        '''.format(nu_1=nu_1, nu_2=nu_2, v=v)
        l_1 = UnitValue(u'%.2f м' % (320. / nu_1.Value))
        l_2 = UnitValue(u'%.2f м' % (300. / nu_2.Value))
        n = UnitValue('%.2f' % ((300. / nu_2.Value) / (320. / nu_1.Value)))
        answer = u'''$
            \\lambda_1 
                = v T_1 = v \\cdot \\frac 1{{\\nu_1}} = \\frac{{v}}{{\\nu_1}} 
                = \\frac{v:Value:s}{nu_1:Value:s} = {l_1:Value},
            \\quad
            \\lambda_2 
                = c T_2 = c \\cdot \\frac 1{{\\nu_2}} = \\frac{{c}}{{\\nu_2}} 
                = \\frac{c:Value:s}{nu_2:Value:s} = {l_2:Value},
            \\quad n = \\frac{{\\lambda_2}}{{\\lambda_1}} \\approx {n:Value}
        $'''.format(nu_1=nu_1, nu_2=nu_2, v=v, c=c, l_1=l_1, l_2=l_2, n=n)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for nu_1, nu_2 in itertools.product(
            [150, 200, 300, 500],
            [200, 500, 800],
        ):
            yield self.__call__(
                nu_1=UnitValue(u'\\nu_1 = %s Гц' % nu_1),
                nu_2=UnitValue(u'\\nu_2 = %s МГц' % nu_2),
            )


class Ch1240(variant.VariantTask):
    def __call__(self, l=None, delta=None, frac=None):
        text = u'''
            Чему равна длина волны, если две точки среды, находящиеся на расстоянии ${l:Task}$,
            совершают колебания с разностью фаз ${delta}$?
        '''.format(l=l, delta=delta)
        lmbd = UnitValue(u'\\lambda = %.2f см' % (1. * l.Value / frac))
        answer = u'''$
            \\frac l\\lambda = \\frac \\varphi{{2\\pi}} + k (k\\in\\mathbb{{N}})
            \\implies 
            \\lambda 
                = \\frac l{{\\frac \\varphi{{2\\pi}} + k}}
                = \\frac {{2\\pi l}}{{\\varphi + 2\\pi k}},
            \\quad
            \\lambda_0 = \\frac {{2\\pi l}}{{\\varphi}} = {lmbd:Value}
        $'''.format(lmbd=lmbd)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for l, (delta, frac) in itertools.product(
            [20, 25, 40, 50, 75],
            [
                (u'\\frac{\\pi}{8}', 1. / 16),
                (u'\\frac{2\\pi}{5}', 1. / 5),
                (u'\\frac{3\\pi}{8}', 3. / 16),
                (u'\\frac{\\pi}{2}', 1. / 4),
                (u'\\frac{3\\pi}{4}', 3. / 8),
            ],
        ):
            yield self.__call__(
                l=UnitValue(u'l = %d см' % l),
                delta=delta,
                frac=frac,
            )
