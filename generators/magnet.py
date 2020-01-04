# -*- coding: utf-8 -*-

import itertools
import logging
import collections

import problems
import variant
from value import UnitValue

log = logging.getLogger(__name__)

import fractions


class ConstMagnet0(variant.VariantTask):
    def __call__(self):
        text = u'''
            Верно ли, что
            \\begin{itemize}
                \item   если распилить постоянный магнит на 2, то мы получим 2 магнита:
                        один только с южным полюсом, а второй — только с северным,
                \item   линии магнитного поля всегда замкнуты,
                \item   линии магнитного поля могут пересекаться в полюсах магнитов,
                \item   линии магнитного всегда начинаются у северного полюса и заканчиваются у южного,
                \item   Северный географическию полюс Земли в точности совпадает с южным магнитным полюсом Земли?
            \\end{itemize}
        '''
        return problems.task.Task(text)

    def All(self):
        yield self.__call__()


class ConstMagnet1(variant.VariantTask):
    def __call__(self, variant=None, points=None):
        text = u'''
            Для постоянного магнита, изображнного на рис. 1{variant})
            изобразите линии индукции магнитного поля
            и укажите, как соориентируется магнитная стрелка в точках {points}.
        '''.format(variant=variant, points=u' и '.join(points))
        return problems.task.Task(text)

    def All(self):
        for variant, points in itertools.product(
            [u'а', u'б', u'в', u'г'],
            list(itertools.combinations('ABCD', 2)),
        ):
            yield self.__call__(variant=variant, points=points)


class ConstMagnet2(variant.VariantTask):
    def __call__(self, variant=None, direction=None, point=None):
        text = u'''
            Магнитная стрелка вблизи длинного прямолинейного проводника
            повёрнута в точке ${point}$ северным полюсом {direction} (см. рис. 2{variant}).
            Сделайте рисунок, укажите направление протекания электрического тока,
            изобразите линии индукции магнитного поля.
        '''.format(variant=variant, direction=direction, point=point)
        return problems.task.Task(text)

    def All(self):
        for variant, direction, point in itertools.chain(
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
        ):
            yield self.__call__(variant=variant, direction=direction, point=point)


class ConstMagnet3(variant.VariantTask):
    def __call__(self, variant=None, direction=None, points=None, what=None):
        text = u'''
            Кольцевой ток (виток с током) ориентирован как указано на рисунке 3{variant}).
            Изобразите линии индукции магнитного поля.
            Укажите, как соориентируется магнитная стрелка в точках {points}.
            Как нужно расположить ещё один кольцевой ток, чтобы между ними возникло {what}
            (сделайте отдельный рисунок с витками, укажите направления протекания тока и направление сил)?
        '''.format(variant=variant, what=what, points=points)
        return problems.task.Task(text)

    def All(self):
        for variant, points, what in itertools.product(
            [u'а', u'б', u'в', u'г'],
            list(itertools.combinations('ABCD', 2)),
            [u'притяжение', u'отталкивание'],
        ):
            yield self.__call__(
                variant=variant,
                what=what,
                points=u' и '.join(points),
            )


class Chernoutsan11_01(variant.VariantTask):
    def __call__(self, l=None, a=None, B=None, I=None):
        text = u'''
            Проводник длиной ${l:Task}$ согнули под прямым углом так, что одна сторона угла оказалась равной ${a:Task}$,
            и поместили в однородное магнитное поле с индукцией ${B:Task}$ обеими сторонами перпендикулярно линиям индукции.
            Какая сила будет действовать на этот проводник при пропусканиии по нему тока ${I:Task}$?
        '''.format(l=l, a=a, B=B, I=I)
        F = UnitValue(u'%.2f мН' % ((1.0 * a.Value ** 2 + (1.0 * l.Value - a.Value) ** 2) ** 0.5 / 100 * I.Value * B.Value))
        answer = u'''
            \\begin{{align*}}
                F
                    &= \\sqrt{{F_a^2 + F_b^2}} = \\sqrt{{(\\mathcal{{I}}Ba)^2 + (\\mathcal{{I}}Bb)^2}}
                    = \\mathcal{{I}}B\\sqrt{{a^2 + b^2}} = \\mathcal{{I}}B\\sqrt{{a^2 + (l - a)^2}} =                       \\\\
                    &= {I:Value}\\cdot {B:Value} \\cdot \\sqrt{{ {a:Value:s}^2 + \\left({l:Value} - {a:Value}\\right)^2}}
                    = {F:Value}.
            \\end{{align*}}
        '''.format(l=l, a=a, B=B, I=I, F=F)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for (a, b), B, I in itertools.product(
            [
                (30, 40), (40, 30), (3, 4), (4, 3),
                (120, 50), (50, 120), (12, 5), (5, 12),
                (70, 240), (240, 70), (7, 24), (24, 7),
            ],
            [2, 5, 10],
            [10, 20, 40, 50],
        ):
            yield self.__call__(
                l=UnitValue(u'l = %d см' % (a + b)),
                a=UnitValue(u'a = %d см' % a),
                B=UnitValue(u'B = %d мТл' % B),
                I=UnitValue(u'\\mathcal{I} = %d А' % I),
            )


class Chernoutsan11_02(variant.VariantTask):
    def __call__(self, B=None, rho=None):
        g = UnitValue(u'g = 10 м / c^2')
        text = u'''
            В однородном горизонтальном магнитном поле с индукцией ${B:Task}$ находится проводник,
            расположенный также горизонтально и перпендикулярно полю.
            Какой ток необходимо пустить по проводнику, чтобы он завис?
            Масса единицы длины проводника ${rho:Task}$, ${g:Task}$.
        '''.format(B=B, rho=rho, g=g)
        I = UnitValue(u'%f кА' % (1.0 * g.Value * rho.Value / B.Value))
        answer = u'''
            $$
                mg = B\\mathcal{{I}}l, m=\\rho l
                \\implies \\mathcal{{I}}
                    = \\frac{{g\\rho}}{{B}}
                    = \\frac{{{g:Value} \\cdot {rho:Value}}}{B:Value:s}
                    = {I:Value}.
            $$
        '''.format(B=B, rho=rho, g=g, I=I)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for B, r in itertools.product(
            [10, 20, 50, 100],
            [5, 10, 20, 40, 100],
        ):
            yield self.__call__(
                B=UnitValue(u'B = %d мТл' % B),
                rho=UnitValue(u'\\rho = %d кг / м' % r),  # TODO: г / м
            )


class Chernoutsan11_5(variant.VariantTask):
    def __call__(self, l=None, I=None, B=None, d=None):
        text = u'''
            Определите работу, которую совершает сила Ампера при перемещении проводника длиной ${l:Task}$
            с током силой ${I:Task}$ в однородном магнитном поле индукцией ${B:Task}$ на расстояние ${d:Task}$.
            Проводник перпендикулярен линиям поля и движется в направлении силы Ампера.
        '''.format(B=B, I=I, l=l, d=d)
        A = UnitValue(u'%.5f Дж' % (10 ** (-4) * 1.0 * B.Value * I.Value * l.Value * d.Value))
        answer = u'''
            $$
                A   = F\\cdot d = B\\mathcal{{I}} l \\cdot d
                    = {B:Value} \\cdot {I:Value} \\cdot {l:Value} \\cdot {d:Value}
                    = {A:Value}.
            $$
        '''.format(B=B, I=I, l=l, d=d, A=A)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for l, I, B, d in itertools.product(
            [20, 30, 40, 50],
            [5, 10, 20],
            [0.1, 0.2, 0.5],
            [20, 50, 80],
        ):
            yield self.__call__(
                l=UnitValue(u'l = %d см' % l),
                I=UnitValue(u'\\mathcal{I} = %d А' % I),
                B=UnitValue(u'B = %f Тл' % B),
                d=UnitValue(u'd = %d см' % d),
            )
