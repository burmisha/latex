# -*- coding: utf-8 -*-

import variant

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
@variant.arg(free=[u'свободные колебания', u'вынужденные колебания'])
@variant.arg(const=[u'незатухающие колебания', u'затухающие колебания'])
class Nu01(variant.VariantTask):
    pass


@variant.text(u'Определите частоту колебаний, если их период составляет {T:Task:e}.')
@variant.answer_short(u'\\nu = \\frac 1T = \\frac 1{T:Value:s} = {nu:Value}')
@variant.arg(T=[u'T = %d мс' % T for T in [2, 4, 5, 10, 20, 40, 50]])
class Nu02(variant.VariantTask):
    def GetUpdate(self, T=None, **kws):
        return dict(
            nu=u'''\\nu = %d Гц''' % (1000 / T.Value),
        )


@variant.text(u'''
    Определите период колебаний, если их частота составляет {nu:Task:e}.
    Сколько колебаний произойдёт за {t:Task:e}?
''')
@variant.answer_align([
    u'T &= \\frac 1\\nu = \\frac 1{nu:Value:s} = {T:Value},',
    u'N &= \\nu t = {nu:Value|cdot}{t:Value} = {N:Value}.',
])
@variant.arg(nu=[u'\\nu = %d кГц' % nu for nu in [2, 4, 5, 10, 20, 40, 50]])
@variant.arg(t=[u't = %d мин' % t for t in [1, 2, 3, 5, 10]])
class Nu03(variant.VariantTask):
    def GetUpdate(self, nu=None, t=None, **kws):
        return dict(
            T=u'T = %.3f мc' % (1. / nu.Value),
            N=u'N = %d колебаний' % (nu.Value * 1000 * t.Value * 60),
        )


@variant.text(u'''
    Амплитуда колебаний точки составляет {A:Task:e}, а частота~--- {nu:Task:e}.
    Определите, какой путь преодолеет эта точка за {t:Task:e}.
''')
@variant.answer_short(u'''
    s
        = 4A \\cdot N = 4A \\cdot \\frac tT = 4A \\cdot t\\nu
        = 4 \\cdot {A:Value} \\cdot {t:Value} \\cdot {nu:Value}
        = {s:Value}
''')
@variant.arg(A=[u'A = %d см' % A for A in [2, 3, 5, 10, 15]])
@variant.arg(nu=[u'\\nu = %d Гц' % nu for nu in [2, 5, 6, 10, 20]])
@variant.arg(t=[u't = %d с' % t for t in [10, 40, 80]])
class Nu04(variant.VariantTask):
    def GetUpdate(self, A=None, nu=None, t=None, **kws):
        return dict(
            s=u's = %.1f м' % (4. * A.Value / 100 * t.Value * nu.Value),
        )


@variant.text(u'''
    Изобразите график гармонических колебаний, амплитуда которых составляла бы
    {A:Task:e}, а период {T:Task:e}.
''')
@variant.arg(A=[u'A = %d см' % A for A in [1, 2, 3, 5, 6, 15, 30, 40, 75]])
@variant.arg(T=[u'T = %d с' % T for T in [2, 4, 6, 8, 10]])
class Nu05(variant.VariantTask):
    pass
