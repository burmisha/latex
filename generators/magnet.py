# -*- coding: utf-8 -*-

import itertools

import variant
import value

import logging
log = logging.getLogger(__name__)


@variant.text(u'''
    Верно ли, что
    \\begin{{itemize}}
        \item   если распилить постоянный магнит на 2, то мы получим 2 магнита:
                один только с южным полюсом, а второй — только с северным,
        \item   линии магнитного поля всегда замкнуты,
        \item   линии магнитного поля могут пересекаться в полюсах магнитов,
        \item   линии магнитного всегда начинаются у северного полюса и заканчиваются у южного,
        \item   Северный географическию полюс Земли в точности совпадает с южным магнитным полюсом Земли?
    \\end{{itemize}}
''')
@variant.args(None)
class ConstMagnet0(variant.VariantTask):
    pass


@variant.text(u'''
    Для постоянного магнита, изображённого на рис. 1{variant})
    изобразите линии индукции магнитного поля
    и укажите, как соориентируются магнитные стрелки в точках {points}.
''')
@variant.args(
    variant=[u'а', u'б', u'в', u'г'],
    points=[u' и '.join(points) for points in itertools.combinations('ABCD', 2)],
)
class ConstMagnet1(variant.VariantTask):
    pass


@variant.text(u'''
    Магнитная стрелка вблизи длинного прямолинейного проводника
    повёрнута в точке ${point}$ северным полюсом {direction} (см. рис. 2{variant}).
    Сделайте рисунок, укажите направление протекания электрического тока,
    изобразите линии индукции магнитного поля.
''')
@variant.args(
    variant__direction__point=itertools.chain(
        itertools.product(
            [u'а', u'б'],
            [u'налево', u'направо'],
            'AB',
        ),
        itertools.product(
            [u'в', u'г'],
            [u'вверх', u'вниз'],
            'AB',
        ),
    )
)
class ConstMagnet2(variant.VariantTask):
    pass


@variant.text(u'''
    Кольцевой ток (виток с током) ориентирован как указано на рисунке 3{variant}).
    Изобразите линии индукции магнитного поля.
    Укажите, как соориентируется магнитная стрелка в точках {points}.
    Как нужно расположить ещё один кольцевой ток, чтобы между ними возникло {what}
    (сделайте отдельный рисунок с витками, укажите направления протекания тока и направление сил)?
''')
@variant.args(
    variant=[u'а', u'б', u'в', u'г'],
    points=[u' и '.join(points) for points in itertools.combinations('ABCD', 2)],
    what=[u'притяжение', u'отталкивание'],
)
class ConstMagnet3(variant.VariantTask):
    pass


@variant.text(u'''
    Проводник длиной {l:Task:e} согнули под прямым углом так, что одна сторона угла оказалась равной {a:Task:e},
    и поместили в однородное магнитное поле с индукцией {B:Task:e} обеими сторонами перпендикулярно линиям индукции.
    Какая сила будет действовать на этот проводник при пропусканиии по нему тока {I:Task:e}?
''')
@variant.answer(u'''
    \\begin{{align*}}
        F
            &= \\sqrt{{F_a^2 + F_b^2}} = \\sqrt{{(\\mathcal{{I}}Ba)^2 + (\\mathcal{{I}}Bb)^2}}
            = \\mathcal{{I}}B\\sqrt{{a^2 + b^2}} = \\mathcal{{I}}B\\sqrt{{a^2 + (l - a)^2}} =                       \\\\
            &= {I:Value}\\cdot {B:Value} \\cdot \\sqrt{{ {a:Value:s}^2 + \\left({l:Value} - {a:Value}\\right)^2}}
            = {F:Value}.
    \\end{{align*}}
''')
@variant.args(
    l__a=[(u'l = %d см' % (a + b), u'a = %d см' % a) for a, b in [
        (30, 40), (40, 30), (3, 4), (4, 3),
        (120, 50), (50, 120), (12, 5), (5, 12),
        (70, 240), (240, 70), (7, 24), (24, 7),
    ]],
    B=[u'B = %d мТл' % B for B in [2, 5, 10]],
    I=[u'\\mathcal{I} = %d А' % I for I in [10, 20, 40, 50]],
)
class Chernoutsan11_01(variant.VariantTask):
    def GetUpdate(self, l=None, a=None, B=None, I=None, **kws):
        return {
            'F': u'F = %.2f мН' % ((1.0 * a.Value ** 2 + (1.0 * l.Value - a.Value) ** 2) ** 0.5 / 100 * I.Value * B.Value),
        }


@variant.text(u'''
    В однородном горизонтальном магнитном поле с индукцией {B:Task:e} находится проводник,
    расположенный также горизонтально и перпендикулярно полю.
    Какой ток необходимо пустить по проводнику, чтобы он завис?
    Масса единицы длины проводника {rho:Task:e}, {g:Task:e}.
''')
@variant.answer(u'''
    $$
        mg = B\\mathcal{{I}}l, m=\\rho l
        \\implies \\mathcal{{I}}
            = \\frac{{g\\rho}}{{B}}
            = \\frac{{{g:Value} \\cdot {rho:Value}}}{B:Value:s}
            = {I:Value}.
    $$
''')
@variant.args(
    B=[u'B = %d мТл' % B for B in [10, 20, 50, 100]],
    rho=[u'\\rho = %d кг / м' % r for r in [5, 10, 20, 40, 100]],   # TODO: г / м
)
class Chernoutsan11_02(variant.VariantTask):
    def GetUpdate(self, rho=None, B=None, **kws):
        g = value.Consts.g_ten
        return {
            'g': g,
            'I': u'\\mathcal{I} = %f кА' % (1.0 * g.Value * rho.Value / B.Value),
        }


@variant.text(u'''
    Определите работу, которую совершает сила Ампера при перемещении проводника длиной {l:Task:e}
    с током силой {I:Task:e} в однородном магнитном поле индукцией {B:Task:e} на расстояние {d:Task:e}.
    Проводник перпендикулярен линиям поля и движется в направлении силы Ампера.
''')
@variant.answer(u'''
    $$
        A   = F\\cdot d = B\\mathcal{{I}} l \\cdot d
            = {B:Value} \\cdot {I:Value} \\cdot {l:Value} \\cdot {d:Value}
            = {A:Value}.
    $$
''')
@variant.args(
    l=[u'l = %d см' % l for l in [20, 30, 40, 50]],
    I=[u'\\mathcal{I} = %d А' % I for I in [5, 10, 20]],
    B=[u'B = %f Тл' % B for B in [0.1, 0.2, 0.5]],
    d=[u'd = %d см' % d for d in [20, 50, 80]],
)
class Chernoutsan11_5(variant.VariantTask):
    def GetUpdate(self, B=None, I=None, l=None, d=None, **kws):
        return {
            'A': u'A = %.5f Дж' % (10 ** (-4) * 1.0 * B.Value * I.Value * l.Value * d.Value),
        }
