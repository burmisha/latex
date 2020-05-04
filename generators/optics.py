# -*- coding: utf-8 -*-

import variant

import logging
log = logging.getLogger(__name__)


@variant.text(u'''
    Длина волны света в~вакууме {lmbd:Task:e}.
    Какова частота этой световой волны?
    Какова длина этой волны в среде с показателем преломления {n:Task:e}?
    Может ли человек увидеть такую волну света, и если да, то какой именно цвет соответствует этим волнам в вакууме и в этой среде?
''')
@variant.args({
    'n': [u'n = 1.%d' % n for n in [3, 4, 5, 6, 7]],
    'lmbd': [u'\\lambda = %d нм' % lmbd for lmbd in [400, 500, 600, 700]],
})
@variant.solution_space(180)
class Gendenshteyn_11_11_18(variant.VariantTask):
    pass

@variant.text(u'''
    Установка для наблюдения интерференции состоит
    из двух когерентных источников света и экрана.
    Расстояние между источниками {l:Task:e},
    а от каждого источника до экрана — {L:Task:e}.
    Сделайте рисунок и укажите положение нулевого максимума освещенности,
    а также определите расстояние между первым {text} и нулевым максимумом.
    Длина волны падающего света составляет {lmbd:Task:e}.
''')
@variant.args({
    'l': [u'l = %d мкм' % l for l in [400, 500, 600]],
    'L': [u'L = %d м' % L for L in [2, 4, 5, 6]],
    'lmbd': [u'\\lambda = %d нм' % lmbd for lmbd in [400, 500, 600]],
    'text': [u'максимумом', u'минимумом'],
})
@variant.solution_space(180)
class Vishnyakova_example_11(variant.VariantTask):
    # d_1^2=L^2 + (h - l/2)^2
    # Вычитаем, приближаем
    # h=lambda L/l = 3,6 мм.
    pass

@variant.text(u'''
    На стеклянную пластинку ({n1:Task:e}) нанесена прозрачная пленка ({n2:Task:e}).
    На плёнку нормально к поверхности падает монохроматический свет с длиной волны {lmbd:Task:e}.
    Какова должна быть минимальная толщина пленки, если в результате интерференции свет имеет {text} интенсивность?
''')
@variant.solution_space(180)
@variant.args({
    'n1': [u'\\hat n = 1.%d' % n1 for n1 in [5, 6]],
    'n2': [u'n = 1.%d' % n2 for n2 in [2, 4, 7, 8]],
    'lmbd': [u'\\lambda = %d нм' % lmbd for lmbd in [400, 500, 600]],
    'text': [u'наибольшую', u'наименьшую'],
})
class Belolipetsky_5_196(variant.VariantTask):
    pass
