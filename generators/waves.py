# -*- coding: utf-8 -*-

import itertools
import logging

import problems
import variant
from variant import LetterValue, Units, UnitValue

log = logging.getLogger(__name__)


class Waves01(variant.VariantTask):
    def __call__(self, nu=None, alpha=None):
        text = u'''
            Частота собственных малых колебаний пружинного маятника равна ${nu:Task}$.
            Чему станет равен период колебаний, если массу пружинного маятника увеличить в ${alpha}$ раз?
        '''.format(nu=nu, alpha=alpha)
        return problems.task.Task(text)

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
        return problems.task.Task(text)

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


class Ch1238(variant.VariantTask):
    def __call__(self, nu_1=None, nu_2=None):
        text = u'''
            Сравните длины звуковой волны частотой ${nu_1:Task}$ и радиоволны частотой ${nu_2:Task}$. 
            Какая больше, во сколько раз? Скорость звука примите равной ${v:Task}$.
        '''.format(nu_1=nu_1, nu_2=nu_2, v=UnitValue(u'v = 320 м / с'))
        return problems.task.Task(text)

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
    def __call__(self, l=None, delta=None):
        text = u'''
            Чему равна длина волны, если две точки среды, находящиеся на расстоянии ${l:Task}$,
            совершают колебания с разностью фаз ${delta}$?
        '''.format(l=l, delta=delta)
        return problems.task.Task(text)

    def All(self):
        for l, delta in itertools.product(
            [20, 25, 40, 50, 75],
            [
                u'\\frac{\\pi}{8}',
                u'\\frac{2\\pi}{5}',
                u'\\frac{3\\pi}{8}',
                u'\\frac{\\pi}{2}',
                u'\\frac{3\\pi}{4}',
            ],
        ):
            yield self.__call__(
                l=UnitValue(u'l = %d см' % l),
                delta=delta,
            )


