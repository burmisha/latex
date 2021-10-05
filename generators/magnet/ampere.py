import itertools

import generators.variant as variant
from generators.helpers import Consts

import logging
log = logging.getLogger(__name__)


@variant.text('''
    Проводник массой {m:V:e} и длиной {l:V:e} подвешен на двух нитях горизонтально в однородном горизонтальном магнитном поле индукцией {B:V:e} (см. рис).
    По проводнику протекает электрический ток силой {I:V:e}. Определите, во сколько раз увеличится натяжение нитей, если увеличить {what} в {N} раза.
''')
@variant.solution_space(120)
@variant.arg(m=('m = {} г', [20, 40, 50]))
@variant.arg(l=('l = {} см', [30, 60, 80]))
@variant.arg(I=('\\eli = {} А', [2, 3, 5]))
@variant.arg(B=('B = {} мТл', [20, 40, 50]))
@variant.arg(what=['силу тока', 'индукцию магнитного поля'])
@variant.arg(N=[2, 3, 4])
class Force19(variant.VariantTask):
    pass



@variant.text('''
    Определите работу, которую совершает сила Ампера при перемещении проводника длиной {l:Task|e}
    с током силой {I:Task|e} в однородном магнитном поле индукцией {B:Task|e} на расстояние {d:Task|e}.
    Проводник перпендикулярен линиям поля и движется в направлении силы Ампера.
''')
@variant.answer_short('''
    A   = F * d = B {I:L} l * d
        = {B:V} * {I:V} * {l:V} * {d:V}
        = {A:V}.
''')
@variant.arg(l=('l = {} см', [20, 30, 40, 50]))
@variant.arg(I=('\\eli = {} А', [5, 10, 20]))
@variant.arg(B=('B = {} Тл', [0.1, 0.2, 0.5]))
@variant.arg(d=('d = {} см', [20, 50, 80]))
@variant.solution_space(80)
class Chernoutsan11_5(variant.VariantTask):
    def GetUpdate(self, B=None, I=None, l=None, d=None):
        A = B * I * l * d
        return dict(
            A=f'A = {A.SI_Value:.3f} Дж',
        )


@variant.text('''
    Проводник длиной {l:Task|e} согнули под прямым углом так, что одна сторона угла оказалась равной {a:Task|e},
    и поместили в однородное магнитное поле с индукцией {B:Task|e} обеими сторонами перпендикулярно линиям индукции.
    Какая сила будет действовать на этот проводник при пропускании по нему тока {I:Task|e}?
''')
@variant.answer_align([
    '''F &= \\sqrt{F_a^2 + F_b^2} = \\sqrt{\\sqr{{I:L} Ba} + \\sqr{{I:L} Bb}}
            = {I:L} B\\sqrt{a^2 + b^2} = {I:L} B\\sqrt{a^2 + (l - a)^2} = ''',
    '&= {I:V} * {B:V} * \\sqrt{{a:V|sqr} + \\sqr{{l:V} - {a:V}}} = {F:V}.',
])
@variant.arg(l__a=[('l = %d см' % (a + b), 'a = %d см' % a) for a, b in [
    (30, 40), (40, 30), (3, 4), (4, 3),
    (120, 50), (50, 120), (12, 5), (5, 12),
    (70, 240), (240, 70), (7, 24), (24, 7),
]])
@variant.arg(B=('B = {} мТл', [2, 5, 10]))
@variant.arg(I=('\\eli = {} А', [10, 20, 40, 50]))
class Chernoutsan11_01(variant.VariantTask):
    def GetUpdate(self, l=None, a=None, B=None, I=None):
        c = (1.0 * a.Value ** 2 + (1.0 * l.Value - a.Value) ** 2) ** 0.5 / 100
        F = I * B * c
        return dict(
            F=f'F = {F.SI_Value * 1000:.2f} мН',
        )


@variant.text('''
    В однородном горизонтальном магнитном поле с индукцией {B:Task|e} находится проводник,
    расположенный также горизонтально и перпендикулярно полю.
    Какой ток необходимо пустить по проводнику, чтобы он завис?
    Масса единицы длины проводника {rho:Task|e}, {g:Task|e}.
''')
@variant.answer_short('''
        mg = B{I:L} l, m=\\rho l
        \\implies {I:L}
            = \\frac{g\\rho}B
            = \\frac{{g:V} * {rho:V}}{B:V|s}
            = {I:V}.
''')
@variant.arg(B=('B = {} мТл', [10, 20, 50, 100]))
@variant.arg(rho=('\\rho = {} г / м', [5, 10, 20, 40, 100]))
class Chernoutsan11_02(variant.VariantTask):
    def GetUpdate(self, rho=None, B=None):
        g = Consts.g_ten
        I = g * rho / B
        return dict(
            I=f'\\eli = {I.SI_Value:.1f} А',
            g=g,
        )
