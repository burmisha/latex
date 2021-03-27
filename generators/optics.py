# -*- coding: utf-8 -*-

import generators.variant as variant
from generators.helpers import Consts

import logging
log = logging.getLogger(__name__)


@variant.text('''
    Длина волны света в~вакууме {lmbd:Task:e}.
    Какова частота этой световой волны?
    Какова длина этой волны в среде с показателем преломления {n:Task:e}?
    Может ли человек увидеть такую волну света, и если да, то какой именно цвет соответствует этим волнам в вакууме и в этой среде?
''')
@variant.arg(n=['n = 1.%d' % n for n in [3, 4, 5, 6, 7]])
@variant.arg(lmbd=['\\lambda = %d нм' % lmbd for lmbd in [400, 500, 600, 700]])
@variant.answer_align([
    '''\\nu &= \\frac 1T = \\frac 1{ \\lambda/c } = \\frac c\\lambda = \\frac{Consts.c:Value|s}{lmbd:Value|s} \\approx {nu:Value},''',
    '''\\nu' = \\nu &\\cbr{ \\text{ или } T' = T } \\implies \\lambda' = v'T' = \\frac vn T = \\frac{ vt }n = \\frac \\lambda n = \\frac{lmbd:Value|s}{n:Value|s} \\approx {lmbd_1:Value}.''',
    '&\\text{ 380 нм---фиол---440---син---485---гол---500---зел---565---жёл---590---оранж---625---крас---780 нм }',
])
@variant.solution_space(180)
class Gendenshteyn_11_11_18(variant.VariantTask):
    def GetUpdate(self, n=None, lmbd=None, **kws):
        return dict(
            nu=Consts.c.Div(lmbd, units='Гц', powerShift=3),
            lmbd_1=lmbd.Div(n, units='м', precisionInc=2),
        )


@variant.text('''
    Установка для наблюдения интерференции состоит
    из двух когерентных источников света и экрана.
    Расстояние между источниками {l:Task:e},
    а от каждого источника до экрана — {L:Task:e}.
    Сделайте рисунок и укажите положение нулевого максимума освещенности,
    а также определите расстояние между первым {text} и нулевым максимумом.
    Длина волны падающего света составляет {lmbd:Task:e}.
''')
@variant.arg(l=['l = %d мкм' % l for l in [400, 500, 600]])
@variant.arg(L=['L = %d м' % L for L in [2, 4, 5, 6]])
@variant.arg(lmbd=['\\lambda = %d нм' % lmbd for lmbd in [400, 500, 600]])
@variant.arg(text=['максимумом', 'минимумом'])
@variant.solution_space(180)
class Vishnyakova_example_11(variant.VariantTask):
    # d_1^2=L^2 + (h - l/2)^2
    # Вычитаем, приближаем
    # h=lambda L/l = 3,6 мм.
    pass


@variant.text('''
    На стеклянную пластинку ({n1:Task:e}) нанесена прозрачная пленка ({n2:Task:e}).
    На плёнку нормально к поверхности падает монохроматический свет с длиной волны {lmbd:Task:e}.
    Какова должна быть минимальная толщина пленки, если в результате интерференции свет имеет {text} интенсивность?
''')
@variant.solution_space(180)
@variant.arg(n1=['\\hat n = 1.%d' % n1 for n1 in [5, 6]])
@variant.arg(n2=['n = 1.%d' % n2 for n2 in [2, 4, 7, 8]])
@variant.arg(lmbd=['\\lambda = %d нм' % lmbd for lmbd in [400, 500, 600]])
@variant.arg(text=['наибольшую', 'наименьшую'])
class Belolipetsky_5_196(variant.VariantTask):
    pass
