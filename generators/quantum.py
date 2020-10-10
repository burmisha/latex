# -*- coding: utf-8 -*-

import math
import itertools

import generators.variant as variant

import logging
log = logging.getLogger(__name__)


@variant.text(u'''
    Сколько фотонов испускает за {minutes} минут лазер,
    если мощность его излучения {power:Value:e}.
    Длина волны излучения {length:Value:e}.
''')
@variant.answer_short(u'''
    N = \\frac{ Pt\\lambda }{ hc }
       = \\frac{
            {power:Value} \\cdot {minutes} \\cdot 60 \\units{ с } \\cdot {length:Value}
         }{
            {Consts.h:Value} \\cdot {Consts.c:Value}
         }
       \\approx { {approx:.2f} }\\cdot10^{ {answerPower} }\\units{ фотонов }
''')
@variant.arg(minutes=[5, 10, 20, 30, 40, 60, 120])
@variant.arg(power=[u'P = %d мВт' % P for P in [15, 40, 75, 200]])
@variant.arg(length=[u'\\lambda = %d нм' % lmbd for lmbd in [500, 600, 750]])
class Fotons(variant.VariantTask):
    def GetUpdate(self, power=None, minutes=None, length=None, **kws):
        answer = 1. * power.Value * minutes * length.Value / 6.626 * 2 / (10 ** 5)
        return dict(
            answerValue=answer,
            answerPower=15 + 5,
            approx=float(answer)
        )


@variant.text(u'''
    В ядре электрически нейтрального атома {nuclons} частиц.
    Вокруг ядра обращается {electrons} электронов.
    Сколько в ядре этого атома протонов и нейтронов?
''')
@variant.answer(u'$Z = {protons}$ протонов и $A - Z = {neutrons}$ нейтронов')
@variant.arg(nuclons__electrons=[
    (108, 47),  # Al
    (65, 29),  # Cu
    (63, 29),  # Cu
    (121, 51),  # Sb
    (123, 51),  # Cu
    (190, 78),  # Pt
])
class KernelCount(variant.VariantTask):
    def GetUpdate(self, nuclons=None, electrons=None, **kws):
        return dict(
            neutrons=nuclons - electrons,
            protons=electrons,
        )


@variant.text(u'Запишите реакцию ${fallType}$-распада {element}.')
@variant.arg(fallType__element=[
    ('\\alpha', '\ce{^{238}_{92}U}'),
    ('\\alpha', '\ce{^{144}_{60}Nd}'),
    ('\\alpha', '\ce{^{147}_{62}Sm}'),
    ('\\alpha', '\ce{^{148}_{62}Sm}'),
    ('\\alpha', '\ce{^{180}_{74}W}'),
    ('\\alpha', '\ce{^{153}_{61}Eu}'),
    ('\\beta', '\ce{^{137}_{55}Cs}'),
    ('\\beta', '\ce{^{22}_{11}Na}'),
])
class RadioFall(variant.VariantTask):
    pass


@variant.text(u'''
    Какой период полураспада радиоактивного изотопа,
    если за {time} ч в среднем распадается {delta} атомов из {total}?
''')
@variant.answer_short(u'''
    N(t) = N_0\\cdot 2^{ -\\frac t{ \\tau_\\frac12 }  }
    \\implies \\log_2\\frac N{ N_0 } = - \\frac t{ \\tau_\\frac 12 }
    \\implies \\tau_\\frac 12 = - \\frac t { \\log_2\\frac N{ N_0 } }
                              =   \\frac t { \\log_2\\frac { N_0 } }N }
    = \\frac{
        {time} \\units{ ч }
    }
    {
        \\log_2\\frac{ {total} }{ {total} - {delta} }
    }
    \\approx {T:Value}.
''')
@variant.arg(time__delta__total=[
    (12, 7500, 8000),
    (24, 75000, 80000),
    (6, 3500, 4000),
    (8, 37500, 40000),
    (8, 300, 400),
])
class RadioFall2(variant.VariantTask):
    def GetUpdate(self, time=None, total=None, delta=None, **kws):
        return dict(
            T=u'%.1f ч' % (time / math.log(total / (total - delta), 2)),
        )


@variant.text(u'''
    Определите длину волны лучей, фотоны которых имеют энергию
    равную кинетической энергии электрона, ускоренного напряжением {V:Value|e}.
''')
@variant.arg(V=[u'%d В' % v for v in [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]])
class Quantum1119(variant.VariantTask):  # 1119 Рымкевич
    pass


@variant.text(u'''
    Лучше всего нейтронное излучение ослабляет вода: в 4 раза лучше бетона и в 3 раза лучше свинца.
    Толщина слоя половинного ослабления $\\gamma$-излучения для воды равна {d1:Value|e}.
    Во сколько раз ослабит нейтронное излучение слой воды толщиной {d:Task|e}?
''')
@variant.arg(d1=[u'3 см'])
@variant.arg(d=[u'%s = %d см' % (l, v) for l, v in itertools.product(['l', 'h', 'd'], [15, 30, 60, 120])])
class Quantum1120(variant.VariantTask):  # 1120 Рымкевич
    pass
