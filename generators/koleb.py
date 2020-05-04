# -*- coding: utf-8 -*-

import variant
from value import UnitValue

import logging
log = logging.getLogger(__name__)


@variant.text(u'''
    Запишите определения:
    \\begin{{itemize}}
        \\item гармонические колебания,
        \\item {free},
        \\item {const}.
    \\end{{itemize}}
''')
@variant.args({
    'free': [u'свободные колебания', u'вынужденные колебания'],
    'const': [u'незатухающие колебания', u'затухающие колебания'],
})
class Nu01(variant.VariantTask):
    pass


@variant.text(u'Определите частоту колебаний, если их период составляет {T:Task:e}.')
@variant.answer(u'$\\nu = \\frac 1T = \\frac 1{T:Value:s} = {nu:Value}$')
@variant.args({
    'T': [u'T = %d мс' % T for T in [2, 4, 5, 10, 20, 40, 50]],
})
class Nu02(variant.VariantTask):
    def GetUpdate(self, **kws):
        T = kws['T']
        return {
            'nu': u'''\\nu = %d Гц''' % (1000 / T.Value),
        }


@variant.text(u'''
    Определите период колебаний, если их частота составляет {nu:Task:e}.
    Сколько колебаний произойдёт за {t:Task:e}?
''')
@variant.answer(u'''
    \\begin{{align*}}
        T &= \\frac 1\\nu = \\frac 1{nu:Value:s} = {T:Value}, \\\\
        N &= \\nu t = {nu:Value}\\cdot{t:Value} = {N:Value}.
    \\end{{align*}}
''')
@variant.args({
    'nu': [u'\\nu = %d кГц' % nu for nu in [2, 4, 5, 10, 20, 40, 50]],
    't': [u't = %d мин' % t for t in [1, 2, 3, 5, 10]],
})
class Nu03(variant.VariantTask):
    def GetUpdate(self, **kws):
        nu = kws['nu']
        t = kws['t']
        return {
            'T': u'T = %.3f мc' % (1. / nu.Value),
            'N': u'N = %d колебаний' % (nu.Value * 1000 * t.Value * 60),
        }


@variant.text(u'''
    Амплитуда колебаний точки составляет {A:Task:e}, а частота~--- {nu:Task:e}.
    Определите, какой путь преодолеет эта точка за {t:Task:e}.
''')
@variant.answer(u'''$
    s
        = 4A \\cdot N = 4A \\cdot \\frac tT = 4A \\cdot t\\nu
        = 4 \\cdot {A:Value} \\cdot {t:Value} \\cdot {nu:Value}
        = {s:Value}
$''')
@variant.args({
    'A': [u'A = %d см' % A for A in [2, 3, 5, 10, 15]],
    'nu': [u'\\nu = %d Гц' % nu for nu in [2, 5, 6, 10, 20]],
    't': [u't = %d с' % t for t in [10, 40, 80]],
})
class Nu04(variant.VariantTask):
    def GetUpdate(self, **kws):
        A = kws['A']
        nu = kws['nu']
        t = kws['t']
        return {
            's': u's = %.1f м' % (4. * A.Value / 100 * t.Value * nu.Value),
        }


@variant.text(u'''
    Изобразите график гармонических колебаний, амплитуда которых составляла бы
    {A:Task:e}, а период {T:Task:e}.
''')
@variant.args({
    'A': [u'A = %d см' % A for A in [1, 2, 3, 5, 6, 15, 30, 40, 75]],
    'T': [u'T = %d с' % T for T in [2, 4, 6, 8, 10]],
})
class Nu05(variant.VariantTask):
    pass
