# -*- coding: utf-8 -*-
import math

import itertools
import logging

import problems
import variant
from value import UnitValue

log = logging.getLogger(__name__)

class Gendenshteyn_11_11_18(variant.VariantTask):
    def __call__(
        self,
        n=None,
        lmbd=None,
    ):
        text = u'''
            Длина волны света в~вакууме {lmbd:Task:e}. 
            Какова частота этой световой волны?
            Какова длина этой волны в среде с показателем преломления {n:Task:e}?
            Какой цвет соответствует этим длинам волн в вакууме и в этой среде?
        '''.format(
            lmbd=lmbd,
            n=n,
        )
        return problems.task.Task(text, solutionSpace=180)

    def All(self):
        for n, lmbd in itertools.product(
            [3, 4, 5, 6, 7],
            [400, 500, 600, 700],
        ):
            yield self.__call__(
                n=UnitValue(u'n = 1.%d' % n),
                lmbd=UnitValue(u'\\lambda = %d нм' % lmbd),
            )


class Vishnyakova_example_11(variant.VariantTask):
    def __call__(
        self,
        l=None,
        L=None,
        lmbd=None,
        text=None,
    ):
        text = u'''
            Установка для наблюдения интерференции состоит
            из двух когерентных источников света и экрана.
            Расстояние между источниками {l:Task:e},
            а от каждого источника до экрана — {L:Task:e}.
            Сделайте рисунок и укажите положение нулевого максимума освещенности,
            а также определите расстояние между первым {text} и нулевым максимумом. 
            Длина волны падающего света составляет {lmbd:Task:e}. 
        '''.format(
            l=l,
            L=L,
            lmbd=lmbd,
            text=text,
        )
        # d_1^2=L^2 + (h - l/2)^2
        # Вычитаем, приближаем
        # h=lambda L/l = 3,6 мм. 
        return problems.task.Task(text, solutionSpace=180)

    def All(self):
        for l, L, lmbd, text in itertools.product(
            [400, 500, 600],
            [2, 4, 5, 6],
            [400, 500, 600],
            [u'максимумом', u'минимумом'],
        ):
            yield self.__call__(
                l=UnitValue(u'l = %d мкм' % l),
                L=UnitValue(u'L = %d м' % L),
                lmbd=UnitValue(u'\\lambda = %d нм' % lmbd),
                text=text,
            )


class Belolipetsky_5_196(variant.VariantTask):
    def __call__(
        self,
        n1=None,
        n2=None,
        lmbd=None,
        text=None,
    ):
        text = u'''
            На стеклянную пластинку ({n1:Task:e}) нанесена прозрачная пленка ({n2:Task:e}). 
            На плёнку нормально к поверхности падает монохроматический свет с длиной волны {lmbd:Task:e}. 
            Какова должна быть минимальная толщина пленки, если в результате интерференции свет имеет {text} интенсивность?
        '''.format(
            n1=n1,
            n2=n2,
            lmbd=lmbd,
            text=text,
        )
        return problems.task.Task(text, solutionSpace=180)

    def All(self):
        for n1, n2, lmbd, text in itertools.product(
            [5, 6],
            [2, 4, 7, 8],
            [400, 500, 600],
            [u'наибольшую', u'наименьшую'],
        ):
            yield self.__call__(
                n1=UnitValue(u'\\hat n = 1.%d' % n1),
                n2=UnitValue(u'n = 1.%d' % n2),
                lmbd=UnitValue(u'\\lambda = %d нм' % lmbd),
                text=text,
            )
