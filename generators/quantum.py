# -*- coding: utf-8 -*-

import math

import variant

import logging
log = logging.getLogger(__name__)


@variant.text(u'''
    Сколько фотонов испускает за {minutes} минут лазер,
    если мощность его излучения {power} мВт.
    Длина волны излучения {length} нм.
''')
@variant.answer(u'''$
    N = \\frac{{Pt\\lambda}}{{hc}}
       = \\frac{{
            {power} \\cdot 10^{{-3}} \\units{{Вт}} \\cdot {minutes} \\cdot 60 \\units{{с}} \\cdot {length} \\cdot 10^{{-9}} \\units{{м}}
        }}{{
            6{{,}}626 \\cdot 10^{{-34}} \\units{{Дж}} \\cdot \\units{{с}} \\cdot 3 \\cdot 10^{{8}} \\funits{{м}}{{с}}
        }}
       \\approx {{{approx:.2f}}}\\cdot10^{{{answerPower}}}\\units{{фотонов}}
$''')
@variant.args({
    'minutes': [5, 10, 20, 30, 40, 60, 120],
    'power': [15, 40, 75, 200],
    'length': [500, 600, 750],
})
class Fotons(variant.VariantTask):
    def GetUpdate(self, **kws):
        res = {
            'answerValue': 1. * kws['power']  * kws['minutes'] * kws['length'] / 6.626 * 2 / (10 ** 5),
            'answerPower': 15 + 5,
        }
        res['approx'] = float(res['answerValue'])
        return res


@variant.text(u'''
    В ядре электрически нейтрального атома {nuclons} частиц.
    Вокруг ядра обращается {electrons} электронов.
    Сколько в ядре этого атома протонов и нейтронов?
''')
@variant.answer(u'''
    $Z = {protons}$ протонов и $A - Z = {neutrons}$ нейтронов
''')
@variant.args({
    ('nuclons', 'electrons'): [
        (108, 47),  # Al
        (65, 29),  # Cu
        (63, 29),  # Cu
        (121, 51),  # Sb
        (123, 51),  # Cu
        (190, 78),  # Pt
    ],
})
class KernelCount(variant.VariantTask):
    def GetUpdate(self, **kws):
        return {
            'neutrons': kws['nuclons'] - kws['electrons'],
            'protons': kws['electrons'],
        }


@variant.text(u'''Запишите реакцию ${fallType}$-распада \ce{{{element}}}.''')
@variant.args({
    ('fallType', 'element'): [
        ('\\alpha', '^{238}_{92}U'),
        ('\\alpha', '^{144}_{60}Nd'),
        ('\\alpha', '^{147}_{62}Sm'),
        ('\\alpha', '^{148}_{62}Sm'),
        ('\\alpha', '^{180}_{74}W'),
        ('\\alpha', '^{153}_{61}Eu'),
        ('\\beta', '^{137}_{55}Cs'),
        ('\\beta', '^{22}_{11}Na'),
    ]
})
class RadioFall(variant.VariantTask):
    pass


@variant.text(u'''
    Какой период полураспада радиоактивного изотопа,
    если за {time} ч в среднем распадается {delta} атомов из {total}?
''')
@variant.answer(u'''$
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
$''')
@variant.args({
    ('time', 'delta', 'total'): [
        (12, 7500, 8000),
        (24, 75000, 80000),
        (6, 3500, 4000),
        (8, 37500, 40000),
        (8, 300, 400),
    ],
})
class RadioFall2(variant.VariantTask):
    def GetUpdate(self, **kws):
        return {
            'value': 1. * kws['time'] / math.log(kws['total'] / (kws['total'] - kws['delta']), 2),
        }


@variant.text(u'''
    Определите длину волны лучей,
    фотоны которых имеют энергию равную кинетической энергии электрона,
    ускоренного напряжением ${V}\\units{{В}}$.
''')
@variant.args({
    'V': [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610],
})
class Quantum1119(variant.VariantTask):  # 1119 Рымкевич
    pass

@variant.text(u'''
    Лучше всего нейтронное излучение ослабляет вода: в 4 раза лучше бетона и в 3 раза лучше свинца.
    Толщина слоя половинного ослабления $\\gamma$-излучения для воды равна $3\\units{{см}}$.
    Во сколько раз ослабит нейтронное излучение слой воды толщиной ${letter} = {value}\\units{{см}}?$
''')
@variant.args({
    'letter': ['l', 'h', 'd'],
    'value': [15, 30, 60, 120],
})
class Quantum1120(variant.VariantTask):  # 1120 Рымкевич
    pass
