# -*- coding: utf-8 -*-

import itertools
import logging
import math

import problems
import variant

log = logging.getLogger(__name__)


class Fotons(variant.VariantTask):
    def __call__(self, minutes=30, power=2, length=750):
        answerValue = 1. * power  * minutes * length / 6.626 * 2 / (10 ** 5)
        answerPower = 15 + 5

        answer = u'''
            $N = \\frac{{Pt\\lambda}}{{hc}}
               = \\frac{{
                    {power} \\cdot 10^{{-3}} \\units{{Вт}} \\cdot {minutes} \\cdot 60 \\units{{с}} \\cdot {length} \\cdot 10^{{-9}} \\units{{м}}
                }}{{
                    6{{,}}626 \\cdot 10^{{-34}} \\units{{Дж}} \\cdot \\units{{с}} \\cdot 3 \\cdot 10^{{8}} \\funits{{м}}{{с}}
                }}
               \\approx {{{approx:.2f}}}\\cdot10^{{{answerPower}}}\\units{{фотонов}}
            $'''.format(
            answerPower=answerPower,
            approx=float(answerValue),
            minutes=minutes,
            power=power,
            length=length,
        ).replace('.', '{,}')

        return problems.task.Task(u'''
            Сколько фотонов испускает за {minutes} минут лазер,
            если мощность его излучения {power} мВт.
            Длина волны излучения {length} нм.
        '''.format(
            minutes=minutes,
            power=power,
            length=length,
        ),
        answer=answer,
        )

    def All(self):
        for minutes, power, length in itertools.product(
            [5, 10, 20, 30, 40, 60, 120],
            [15, 40, 75, 200],
            [500, 600, 750],
        ):
            yield self.__call__(
                minutes=minutes,
                power=power,
                length=length,
            )

class KernelCount(variant.VariantTask):
    def __call__(self, nuclons=108, electrons=47):
        answer = u'''$Z = {protons}$ протонов и $A - Z = {neutrons}$ нейтронов'''.format(
            protons=electrons,
            neutrons=nuclons - electrons,
        )
        return problems.task.Task(u'''
            В ядре электрически нейтрального атома {nuclons} частиц.
            Вокруг ядра обращается {electrons} электронов.
            Сколько в ядре этого атома протонов и нейтронов?
        '''.format(
            nuclons=nuclons,
            electrons=electrons,
        ),
        answer=answer,
        )

    def All(self):
        for nuclons, electrons in [
            (108, 47),  # Al
            (65, 29),  # Cu
            (63, 29),  # Cu
            (121, 51),  # Sb
            (123, 51),  # Cu
            (190, 78),  # Pt
        ]:
            yield self.__call__(
                nuclons=nuclons,
                electrons=electrons,
            )


class RadioFall(variant.VariantTask):
    def __call__(self, fallType='alpha', element='^{238}_{92}U'):
        typeFmt = {
            'alpha': '\\alpha',
            'beta': '\\beta',
        }[fallType]
        return problems.task.Task(u'''
            Запишите реакцию ${typeFmt}$-распада \ce{{{element}}}.
        '''.format(
            typeFmt=typeFmt,
            element=element,
        ))

    def All(self):
        for fallType, element in [
            ('alpha', '^{238}_{92}U'),
            ('alpha', '^{144}_{60}Nd'),
            ('alpha', '^{147}_{62}Sm'),
            ('alpha', '^{148}_{62}Sm'),
            ('alpha', '^{180}_{74}W'),
            ('alpha', '^{153}_{61}Eu'),
            ('beta', '^{137}_{55}Cs'),
            ('beta', '^{22}_{11}Na'),
        ]:
            yield self.__call__(
                fallType=fallType,
                element=element,
            )


class RadioFall2(variant.VariantTask):
    def __call__(self, time=12, delta=7500, total=8000):
        value = 1. * time / math.log(total / (total - delta), 2)
        answer = u'''
            $
            N(t) = N_0\\cdot 2^{{-\\frac t{{\\tau_\\frac12}}}}
            \\implies \\log_2\\frac N{{N_0}} = - \\frac t{{\\tau_\\frac 12}}
            \\implies \\tau_\\frac 12 = - \\frac t {{\\log_2\\frac N{{N_0}}}} 
                                      =   \\frac t {{\\log_2\\frac {{N_0}}N}}
            = \\frac{{
                {time} \\units{{ч}}
            }}
            {{
                \\log_2\\frac{{{total}}}{{{total} - {delta}}}
            }}
            \\approx {value:.1f}\\units{{ч}}
            $
        '''.format(
            value=value,
            total=total,
            time=time,
            delta=delta,
        ).replace('.', '{,}')
        return problems.task.Task(u'''
            Какой период полураспада радиоактивного изотопа,
            если за {time} ч в среднем распадается {delta} атомов из {total}?
        '''.format(
            time=time,
            delta=delta,
            total=total,
        ),
        answer=answer,
        )

    def All(self):
        for time, delta, total in [
            (12, 7500, 8000),
            (24, 75000, 80000),
            (6, 3500, 4000),
            (8, 37500, 40000),
            (8, 300, 400),
        ]:
            yield self.__call__(
                time=time,
                delta=delta,
                total=total,
            )
