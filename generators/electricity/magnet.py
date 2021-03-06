# -*- coding: utf-8 -*-

import itertools

import generators.variant as variant
from generators.helpers import Consts

import logging
log = logging.getLogger(__name__)


@variant.text('''
    Верно ли, что
    \\begin{itemize}
        \\item   если распилить постоянный магнит на 2, то мы получим 2 магнита:
                один только с южным полюсом, а второй — только с северным,
        \\item   линии магнитного поля всегда замкнуты,
        \\item   линии магнитного поля могут пересекаться в полюсах магнитов,
        \\item   линии магнитного всегда начинаются у северного полюса и заканчиваются у южного,
        \\item   Северный географическию полюс Земли в точности совпадает с южным магнитным полюсом Земли?
    \\end{itemize}
''')
@variant.no_args
class ConstMagnet0(variant.VariantTask):
    pass


@variant.text('''
    Для постоянного магнита, изображённого на рис. 1{variant})
    изобразите линии индукции магнитного поля
    и укажите, как соориентируются магнитные стрелки в точках {points}.
''')
@variant.arg(variant=['а', 'б', 'в', 'г'])
@variant.arg(points=[' и '.join(points) for points in itertools.combinations('ABCD', 2)])
class ConstMagnet1(variant.VariantTask):
    pass


@variant.text('''
    Магнитная стрелка вблизи длинного прямолинейного проводника
    повёрнута в точке ${point}$ северным полюсом {direction} (см. рис. 2{variant}).
    Сделайте рисунок, укажите направление протекания электрического тока,
    изобразите линии индукции магнитного поля.
''')
@variant.arg(variant__direction__point=itertools.chain(
    itertools.product(
        ['а', 'б'],
        ['налево', 'направо'],
        'AB',
    ),
    itertools.product(
        ['в', 'г'],
        ['вверх', 'вниз'],
        'AB',
    ),
))
class ConstMagnet2(variant.VariantTask):
    pass


@variant.text('''
    Кольцевой ток (виток с током) ориентирован как указано на рисунке 3{variant}).
    Изобразите линии индукции магнитного поля.
    Укажите, как соориентируется магнитная стрелка в точках {points}.
    Как нужно расположить ещё один кольцевой ток, чтобы между ними возникло {what}
    (сделайте отдельный рисунок с витками, укажите направления протекания тока и направление сил)?
''')
@variant.arg(variant=['а', 'б', 'в', 'г'])
@variant.arg(points=[' и '.join(points) for points in itertools.combinations('ABCD', 2)])
@variant.arg(what=['притяжение', 'отталкивание'])
class ConstMagnet3(variant.VariantTask):
    pass


@variant.text('''
    Проводник длиной {l:Task|e} согнули под прямым углом так, что одна сторона угла оказалась равной {a:Task|e},
    и поместили в однородное магнитное поле с индукцией {B:Task|e} обеими сторонами перпендикулярно линиям индукции.
    Какая сила будет действовать на этот проводник при пропусканиии по нему тока {I:Task|e}?
''')
@variant.answer_align([
    '''F &= \\sqrt{F_a^2 + F_b^2} = \\sqrt{\\sqr{{I:L}Ba} + \\sqr{{I:L}Bb}}
            = {I:L}B\\sqrt{a^2 + b^2} = {I:L}B\\sqrt{a^2 + (l - a)^2} = ''',
    '&= {I:Value} * {B:Value} * \\sqrt{{a:Value|sqr} + \\sqr{{l:Value} - {a:Value}}} = {F:Value}.',
])
@variant.arg(l__a=[('l = %d см' % (a + b), 'a = %d см' % a) for a, b in [
    (30, 40), (40, 30), (3, 4), (4, 3),
    (120, 50), (50, 120), (12, 5), (5, 12),
    (70, 240), (240, 70), (7, 24), (24, 7),
]])
@variant.arg(B=['B = %d мТл' % B for B in [2, 5, 10]])
@variant.arg(I=['\\mathcal{I} = %d А' % I for I in [10, 20, 40, 50]])
class Chernoutsan11_01(variant.VariantTask):
    def GetUpdate(self, l=None, a=None, B=None, I=None, **kws):
        return dict(
            F='F = %.2f мН' % ((1.0 * a.Value ** 2 + (1.0 * l.Value - a.Value) ** 2) ** 0.5 / 100 * I.Value * B.Value),
        )


@variant.text('''
    В однородном горизонтальном магнитном поле с индукцией {B:Task|e} находится проводник,
    расположенный также горизонтально и перпендикулярно полю.
    Какой ток необходимо пустить по проводнику, чтобы он завис?
    Масса единицы длины проводника {rho:Task|e}, {Consts.g_ten:Task|e}.
''')
@variant.answer_short('''
        mg = B{I:L} l, m=\\rho l
        \\implies {I:L}
            = \\frac{g\\rho}B
            = \\frac{{Consts.g_ten:Value} * {rho:Value}}{B:Value|s}
            = {I:Value}.
''')
@variant.arg(B=['B = %d мТл' % B for B in [10, 20, 50, 100]])
@variant.arg(rho=['\\rho = %d кг / м' % r for r in [5, 10, 20, 40, 100]])   # TODO: г / м
class Chernoutsan11_02(variant.VariantTask):
    def GetUpdate(self, rho=None, B=None, **kws):
        return dict(
            I='\\mathcal{I} = %f кА' % (1.0 * Consts.g_ten.Value * rho.Value / B.Value),
        )


@variant.text('''
    Определите работу, которую совершает сила Ампера при перемещении проводника длиной {l:Task|e}
    с током силой {I:Task|e} в однородном магнитном поле индукцией {B:Task|e} на расстояние {d:Task|e}.
    Проводник перпендикулярен линиям поля и движется в направлении силы Ампера.
''')
@variant.answer_short('''
    A   = F * d = B {I:L} l * d
        = {B:Value} * {I:Value} * {l:Value} * {d:Value}
        = {A:Value}.
''')
@variant.arg(l=['l = %d см' % l for l in [20, 30, 40, 50]])
@variant.arg(I=['\\mathcal{I} = %d А' % I for I in [5, 10, 20]])
@variant.arg(B=['B = %f Тл' % B for B in [0.1, 0.2, 0.5]])
@variant.arg(d=['d = %d см' % d for d in [20, 50, 80]])
class Chernoutsan11_5(variant.VariantTask):
    def GetUpdate(self, B=None, I=None, l=None, d=None, **kws):
        return dict(
            A='A = %.5f Дж' % (10 ** (-4) * 1.0 * B.Value * I.Value * l.Value * d.Value),
        )
