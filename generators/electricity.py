# -*- coding: utf-8 -*-

import itertools
import logging
import collections

import problems
import variant

log = logging.getLogger(__name__)

import fractions


class ForceTask(variant.VariantTask):
    def __call__(self, charges=['2', '4'], letter='l', distance='3'):
        # answer = kqq/r**2
        value = fractions.Fraction(
            numerator=int(charges[0]) * int(charges[1]) * 9,
            denominator=int(distance) ** 2,
        )
        power = 9 - 9 - 9 + 4

        answer = u'''
            $F  = k\\frac{{q_1q_2}}{{{letter}^2}}
                = 9 \\cdot 10^9 \\funits{{Н $\\cdot$ м$^2$}}{{Кл$^2$}} \\cdot \\frac{{
                    {charges[0]}\\cdot 10^{{-9}}\\units{{Кл}}
                    \\cdot
                    {charges[1]}\\cdot 10^{{-9}}\\units{{Кл}}
                }}{{
                    \\left({distance} \\cdot 10^{{-2}}\\units{{м}}\\right)^2
                }}
                = \\frac{{{value.numerator}}}{{{value.denominator}}}\\cdot10^{{{power}}}\\units{{Н}}
                  \\approx {{{approx:.2f}}}\\cdot10^{{{power}}}\\units{{Н}}
            $'''.format(
            value=value,
            power=power,
            letter=letter,
            approx=float(value),
            charges=charges,
            distance=distance,
        ).replace('.', '{,}')
        return problems.task.Task(u'''
            С какой силой взаимодействуют 2 точечных заряда $q_1={charges[0]}\\units{{нКл}}$ и $q_2={charges[1]}\\units{{нКл}}$,
            находящиеся на расстоянии ${letter}={distance}\\units{{см}}$?
        '''.format(
            charges=charges,
            letter=letter,
            distance=distance,
        ),
        answer=answer
        )

    def All(self):
        for first, second, letter, distance in itertools.product(range(2, 5), range(2, 5), ['r', 'l', 'd'], [2, 3, 5, 6]):
            if first != second:
                yield self.__call__(charges=[first, second], letter=letter, distance=distance)


class ExchangeTask(variant.VariantTask):
    def __call__(self, charges=['+q', '+q'], letter='l'):
        q1 = int(''.join(c for c in charges[0] if c.isdigit() or c in ['+', '-']))
        q2 = int(''.join(c for c in charges[1] if c.isdigit() or c in ['+', '-']))
        letter1 = ''.join(c for c in charges[0] if c.isalpha())
        letter2 = ''.join(c for c in charges[1] if c.isalpha())
        assert q1 != q2
        assert letter1 == letter2
        answer = u'''
            \\begin{{align*}}
            F   &= k\\frac{{q_1q_2}}{{{letter}^2}} = k\\frac{{({charges[0]})\\cdot({charges[1]})}}{{{letter}^2}},
            \\text{{{res[0]}}};
            \\\\
            q'_1 = q'_2 = \\frac{{q_1 + q_2}}2 = \\frac{{({charges[0]}) + ({charges[1]})}}2 \\implies
            F'  &= k\\frac{{q'_1q'_2}}{{{letter}^2}}
                = k\\frac{{
                        \\left(\\frac{{({charges[0]}) + ({charges[1]})}}2\\right)^2
                    }}{{
                        {letter}^2
                    }},
            \\text{{{res[1]}}}.
            \\end{{align*}}
        '''.format(
            charges=charges,
            letter=letter,
            res=[
                u'притяжение' if q1 * q2 < 0 else u'отталкивание',
                u'отталкивание',
            ]
        )
        return problems.task.Task(u'''
            Два одинаковых маленьких проводящих заряженных шарика находятся
            на расстоянии~${letter}$ друг от друга.
            Заряд первого равен~${charges[0]}$, второго~---${charges[1]}$.
            Шарики приводят в соприкосновение, а после опять разводят на то же самое расстояние~${letter}$.
            Каким стал заряд каждого из шариков?
            Определите характер (притяжение или отталкивание)
            и силу взаимодействия шариков до и после соприкосновения.
        '''.format(
            letter=letter,
            charges=charges,
        ),
        answer=answer,
        )

    def All(self):
        signs = ['+', '-']
        chargeLetters = ['q', 'Q']
        chargeSizes = range(2, 6)
        for fs, ss, cl, fc, sc, l in itertools.product(signs, signs, chargeLetters, chargeSizes, chargeSizes, ['l', 'd', 'r']):
            if fc != sc:
                yield self.__call__(
                    letter=l,
                    charges=[
                        '{}{}{}'.format(fs, fc, cl),
                        '{}{}{}'.format(ss, sc, cl),
                    ],
                )


class FieldTaskGenerator(variant.VariantTask):
    def __call__(self, charges=['+q', '+q'], points=['up', 'left'], letter='l'):
        allPoints = {
            'up': '(0; {})'.format(letter),
            'down': '(0; -{})'.format(letter),
            'left': '(-2{}; 0)'.format(letter),
            'right': '(2{}; 0)'.format(letter),
        }
        return problems.task.Task(u'''
            На координатной плоскости в точках $(-{letter}; 0)$ и $({letter}; 0)$
            находятся заряды, соответственно, ${charges[0]}$ и ${charges[1]}$.
            Сделайте рисунок, определите величину напряжённости электрического поля
            в точках ${firstPoint}$ и ${secondPoint}$ и укажите её направление.
        '''.format(
            letter=letter,
            charges=charges,
            firstPoint=allPoints[points[0]],
            secondPoint=allPoints[points[1]],
        ))

    def All(self):
        for charges in [['+q', '-q'], ['-q', '-q'], ['+Q', '+Q'], ['-Q', '+Q']]:
            for firstPoint in ['up', 'down']:
                for secondPoint in ['right', 'left']:
                    for letter in ['a', 'l', 'r', 'd']:
                        yield self.__call__(
                            charges=charges,
                            letter=letter,
                            points=[firstPoint, secondPoint],
                        )


class SumTask(variant.VariantTask):
    def __call__(self, angleLetter='\\alpha', values=[12, 5], angles=[60, 90]):
        return problems.task.Task(u'''
            Заряд $q_1$ создает в точке $A$ электрическое поле
            по величине равное~$E_1={values[0]}\\funits{{В}}{{м}}$,
            а $q_2$~---$E_2={values[1]}\\funits{{В}}{{м}}$.
            Угол между векторами $\\vect{{E_1}}$ и $\\vect{{E_2}}$ равен ${angle}$.
            Определите величину суммарного электрического поля в точке $A$,
            создаваемого обоими зарядами $q_1$ и $q_2$.
            Сделайте рисунок и вычислите её значение для двух значений угла ${angle}$:
            ${angle}_1={angles[0]}^\\circ$ и ${angle}_2={angles[1]}^\\circ$.
        '''.format(
            angle=angleLetter,
            values=values,
            angles=angles,
        ))

    def All(self):
        for values, angles in [
            ((120, 50), (90, 180)),
            ((50, 120), (0, 90)),
            ((500, 500), (0, 120)),
            ((200, 200), (0, 60)),
            ((24, 7), (90, 180)),
            ((7, 24), (0, 90)),
            ((72, 72), (0, 120)),
            ((250, 250), (0, 60)),
            ((300, 400), (90, 180)),
            ((300, 400), (0, 90)),
        ]:
            for angleLetter in ['\\alpha', '\\varphi']:
                yield self.__call__(
                    angleLetter=angleLetter,
                    values=values,
                    angles=angles
                )


# LetterValue = collections.namedtuple('LetterValue', ['Letter', 'Value'])

class Units(object):
    def __init__(self, basic=None, standard=None, power=None):
        self.Basic = basic
        self.Standard = standard
        self.Power = power


class LetterValue(object):
    def __init__(self, Letter=None, Value=None, units=None):
        self.Letter = Letter
        self.Value = Value
        self.Units = units

    def __format__(self, format):
        value = self.Value
        if value < 0:
            value = '({})'.format(value)
        if format == 'Task':
            return u'{self.Letter}={self.Value}{self.Units.Basic}'.format(self=self)
        elif format == 'Answer':
            return u'{value} \\cdot 10^{{{self.Units.Power}}} \\cdot {self.Units.Standard}'.format(self=self, value=value)
        else:
            raise RuntimeError('Error on format %r' % format)


class Potential728(variant.VariantTask):
    def __call__(self, l=None, q=None, E=None):
        # 728(737) - Rymkevich
        answer = u'''
            \\begin{{align*}}
            A   = {E.Letter}{q.Letter}{l.Letter} 
                = {E:Answer} \\cdot {q:Answer} \\cdot {l:Answer}
                = {A:.2f} \\cdot 10^{{-7}} \\units{{Дж}}
            \\end{{align*}}
        '''.format(
            A=1. * E.Value * q.Value * l.Value,
            E=E,
            q=q,
            l=l,
        )
        return problems.task.Task(u'''
            В однородном электрическом поле напряжённостью ${E:Task}$
            переместили заряд ${q:Task}$ в направлении силовой линии
            на ${l:Task}$. Определите работу поля, изменение потенциальной энергии заряда,
            напряжение между начальной и конечной точками перемещения.
        '''.format(
            l=l,
            q=q,
            E=E,
        ),
        answer=answer,
        )

    def All(self):
        for ql, qv, ll, lv, ev in itertools.product(['Q', 'q'], [-10, 10, -25, 25, -40, 40], ['l', 'r', 'd'], [2, 4, 5, 10], [2, 4, 20]):
            yield self.__call__(
                E=LetterValue(Letter='E', Value=ev, units=Units(basic=u'\\funits{кВ}{м}', standard=u'\\funits{В}{м}', power=3)),
                q=LetterValue(Letter=ql, Value=qv, units=Units(basic=u'\\units{нКл}',  standard=u'\\units{Кл}', power=-9)),
                l=LetterValue(Letter=ll, Value=lv, units=Units(basic=u'\\units{см}',  standard=u'\\units{м}', power=-2)),
            )


class Potential735(variant.VariantTask):
    def __call__(self, l=None, U=None):
        # 735(737) - Rymkevich
        return problems.task.Task(u'''
            Напряжение между двумя точками, лежащими на одной линии напряжённости однородного электрического поля,
            равно ${U.Letter}={U.Value}\\units{{кВ}}$. Расстояние между точками ${l.Letter}={l.Value}\\units{{см}}$. 
            Какова напряжённость этого поля?
        '''.format(
            l=l,
            U=U,
        ))

    def All(self):
        for ul, uv, ll, lv in itertools.product(['U', 'V'], [2, 3, 4, 5, 6], ['l', 'r', 'd'], [10, 20, 30, 40]):
            yield self.__call__(
                U=LetterValue(Letter=ul, Value=uv),
                l=LetterValue(Letter=ll, Value=lv),
            )


class Potential737(variant.VariantTask):
    def __call__(self, l=None, alpha=None, E=None):
        # 737(739) - Rymkevich
        return problems.task.Task(u'''
            Найти напряжение между точками $A$ и $B$ в однородном электрическом поле (см. рис. на доске), если 
            $AB={l.Letter}={l.Value}\\units{{см}}$,
            ${alpha.Letter}={alpha.Value}^\\circ$,
            ${E.Letter}={E.Value}\\funits{{В}}{{м}}$.
            Потенциал какой из точек $A$ и $B$ больше?
        '''.format(
            l=l,
            alpha=alpha,
            E=E,
        ))

    def All(self):
        for ll, lv, al, av, ev in itertools.product(['l', 'r', 'd'], [4, 6, 8, 10, 12], ['\\alpha', '\\varphi'], [30, 45, 60], [30, 50, 60, 100, 120]):
            yield self.__call__(
                l=LetterValue(Letter=ll, Value=lv),
                alpha=LetterValue(Letter=al, Value=av),
                E=LetterValue(Letter='E', Value=ev),
            )


class Potential2335(variant.VariantTask):
    def __call__(self, E=None):
        # 2335 Gendenshteyn
        return problems.task.Task(u'''
            При какой скорости электрона его кинетическая энергия равна $E_\\text{{к}} = {E}\\units{{эВ}}?$
        '''.format(
            E=E,
        ))

    def All(self):
        for E in [4, 8, 20, 30, 40, 50, 200, 400, 600, 1000]:
            yield self.__call__(
                E=E,
            )


class Potential1621(variant.VariantTask):
    def __call__(self, v=None, V=None):
        # 1621 Goldfarb
        return problems.task.Task(u'''
            Электрон $e^-$ вылетает из точки, потенциал которой ${V.Letter} = {V.Value}\\units{{В}},$
            со скоростью ${v.Letter} = {v.Value}\\cdot 10^6\\funits{{м}}{{c}}$ в направлении линий напряжённости поля.
            Будет поле ускорять или тормозить электрон?
            Каков потенциал точки, дойдя до которой электрон остановится?
        '''.format(
            v=v,
            V=V,
        ))

    def All(self):
        for vv, Vv, in itertools.product([3, 4, 6, 10, 12], [200, 400, 600, 800, 1000]):
            yield self.__call__(
                v=LetterValue(Letter='v', Value=vv),
                V=LetterValue(Letter='\\varphi', Value=Vv),
            )


class Rymkevich748(variant.VariantTask):
    def __call__(self, U=None, q=None):
        return problems.task.Task(u'''
            Определите ёмкость конденсатора, если при его зарядке до напряжения
            ${U:Task}$ он приобретает заряд ${q:Task}$. 
            Чему при этом равны заряды обкладок конденсатора (сделайте рисунок)?
        '''.format(U=U, q=q),
        )

    def All(self):
        for Ul, Uv, ql, qv in itertools.product(['U', 'V'], [2, 3, 5, 6, 12, 15, 20], ['Q', 'q'], [4, 6, 15, 18, 24, 25]):
            yield self.__call__(
                U=LetterValue(Letter=Ul, Value=Uv, units=Units(basic=u'\\units{кВ}', standard=u'\\units{В}', power=3)),
                q=LetterValue(Letter=ql, Value=qv, units=Units(basic=u'\\units{нКл}', standard=u'\\units{Кл}', power=-9)),
            )


class Rymkevich750(variant.VariantTask):
    def __call__(self, U=None, Q=None, C=None):
        return problems.task.Task(u'''
            На конденсаторе указано: ${C:Task}$, ${U:Task}$.
            Удастся ли его использовать для накопления заряда ${Q:Task}$?
        '''.format(U=U, Q=Q, C=C),
        )

    def All(self):
        for Ul, Uv, Ql, Qv, Cv in itertools.product(['U', 'V'], [200, 300, 400, 450], ['Q', 'q'], [30, 50, 60], [50, 80, 100, 120, 150]):
            yield self.__call__(
                U=LetterValue(Letter=Ul, Value=Uv, units=Units(basic=u'\\units{кВ}', standard=u'\\units{В}', power=3)),
                Q=LetterValue(Letter=Ql, Value=Qv, units=Units(basic=u'\\units{нКл}', standard=u'\\units{Кл}', power=-9)),
                C=LetterValue(Letter='C', Value=Cv, units=Units(basic=u'\\units{пФ}', standard=u'\\units{Ф}', power=-12)),
            )


class Rymkevich751(variant.VariantTask):
    def __call__(self, a=None, b=None):
        return problems.task.Task(u'''
            Как и во сколько раз изменится ёмкость плоского конденсатора при уменьшении площади пластин в {a} раз
            и уменьшении расстояния между ними в {b} раз?
        '''.format(a=a, b=b),
        )

    def All(self):
        for a, b in itertools.product([2, 3, 4, 5, 6, 7, 8], [2, 3, 4, 5, 6, 7, 8]):
            yield self.__call__(a=a, b=b)


class Rymkevich762(variant.VariantTask):
    def __call__(self, C=None, Q=None):
        return problems.task.Task(u'''
            Электрическая ёмкость конденсатора равна ${C:Task}$,
            при этом ему сообщён заряд ${Q:Task}$. Какова энергия заряженного конденсатора?
        '''.format(C=C, Q=Q),
        )

    def All(self):
        for Ql, Qv, Cv in itertools.product(['Q', 'q'], [300, 500, 800, 900], [200, 400, 600, 750]):
            yield self.__call__(
                Q=LetterValue(Letter=Ql, Value=Qv, units=Units(basic=u'\\units{нКл}', standard=u'\\units{Кл}', power=-9)),
                C=LetterValue(Letter='C', Value=Cv, units=Units(basic=u'\\units{пФ}', standard=u'\\units{Ф}', power=-12)),
            )


class Cond1(variant.VariantTask):
    def __call__(self, C=None, U=None):
        return problems.task.Task(u'''
            Два конденсатора ёмкостей ${C[0]:Task}$ и ${C[1]:Task}$ последовательно подключают
            к источнику напряжения ${U:Task}$ (см. рис.). Определите заряды каждого из конденсаторов.
        '''.format(C=C, U=U),
        )

    def All(self):
        for Ul, Uv, C1, C2 in itertools.product(['U', 'V'], [150, 200, 300, 400, 450], [20, 30, 40, 60], [20, 30, 40, 60]):
            if C1 == C2:
                continue
            yield self.__call__(
                U=LetterValue(Letter=Ul, Value=Uv, units=Units(basic=u'\\units{В}', standard=u'\\units{В}', power=0)),
                C=[
                    LetterValue(Letter='C_1', Value=C1, units=Units(basic=u'\\units{нФ}', standard=u'\\units{Ф}', power=-9)),
                    LetterValue(Letter='C_2', Value=C2, units=Units(basic=u'\\units{нФ}', standard=u'\\units{Ф}', power=-9)),
                ],
            )
