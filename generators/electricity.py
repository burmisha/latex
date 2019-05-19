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
    def __init__(self, basic=None, standard=None, power=0):
        self.Basic = basic
        self.Standard = standard
        self.Power = power
        if self.Power == 0:
            assert self.Standard is not None
            if not self.Basic:
                self.Basic = self.Standard
            assert self.Basic == self.Standard
        else:
            assert self.Basic != self.Standard


class LetterValue(object):
    def __init__(self, Letter=None, Value=None, units=None):
        self.Letter = Letter
        self.Value = Value
        self.Units = units

    def __repr__(self):
        return ' '.join([
            'Letter: %r' % [self.Letter, type(self.Letter)],
            'Value: %r' % [self.Value, type(self.Value)],
            'Units: %r' % [self.Units, type(self.Units)],
        ])

    def __format__(self, format):
        if isinstance(self.Value, int):
            fmt = '{:d}'
        else:
            fmt = '{:.2f}'
        if self.Value < 0:
            fmt = '(%s)' % fmt
        value = fmt.format(self.Value).replace('.', '{,}')
        if ':' in format:
            format, suffix = format.split(':')
        else:
            suffix = None
        if format == 'Task':
            result = u'{self.Letter}={self.Value}{self.Units.Basic}'.format(self=self)
        elif format == 'Letter':
            result = u'{self.Letter}'.format(self=self)
        elif format == 'Value':
            result = u'{self.Value}'.format(self=self).replace('.', '{,}')
        elif format == 'ShortAnswer':
            result = u'{value}{self.Units.Basic}'.format(self=self, value=value)
        elif format == 'Answer':
            if self.Units.Power != 0:
                result = u'{value} \\cdot 10^{{{self.Units.Power}}} {self.Units.Standard}'.format(self=self, value=value)
            else:
                result = u'{value} {self.Units.Standard}'.format(self=self, value=value)
        else:
            raise RuntimeError('Error on format %r' % format)

        if suffix == 's':
            result = u'{ ' + result + ' }'

        return result


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
        for vv, Vv in itertools.product([3, 4, 6, 10, 12], [200, 400, 600, 800, 1000]):
            yield self.__call__(
                v=LetterValue(Letter='v', Value=vv),
                V=LetterValue(Letter='\\varphi', Value=Vv),
            )


class Rymkevich748(variant.VariantTask):
    def __call__(self, U=None, Q=None):
        answer = u'''
            ${Q.Letter} = {C.Letter}{U.Letter} \\implies
            {C.Letter} = \\frac{{{Q.Letter}}}{{{U.Letter}}} = \\frac{{{Q:Answer}}}{{{U:Answer}}} = {C:Answer} = {C:ShortAnswer}.
            \\text{{ Заряды обкладок: ${Q.Letter}$ и $-{Q.Letter}$}}$
        '''.format(
            C=LetterValue(Letter='C', Value=1. * Q.Value / U.Value, units=Units(basic=u'\\units{пФ}', standard=u'\\units{Ф}', power=-12)),
            U=U,
            Q=Q,
        )
        return problems.task.Task(u'''
            Определите ёмкость конденсатора, если при его зарядке до напряжения
            ${U:Task}$ он приобретает заряд ${Q:Task}$.
            Чему при этом равны заряды обкладок конденсатора (сделайте рисунок)?
        '''.format(U=U, Q=Q),
        answer=answer,
        )

    def All(self):
        for Ul, Uv, ql, qv in itertools.product(['U', 'V'], [2, 3, 5, 6, 12, 15, 20], ['Q', 'q'], [4, 6, 15, 18, 24, 25]):
            yield self.__call__(
                U=LetterValue(Letter=Ul, Value=Uv, units=Units(basic=u'\\units{кВ}', standard=u'\\units{В}', power=3)),
                Q=LetterValue(Letter=ql, Value=qv, units=Units(basic=u'\\units{нКл}', standard=u'\\units{Кл}', power=-9)),
            )


class Rymkevich750(variant.VariantTask):
    def __call__(self, U=None, Q=None, C=None):
        resultQ = C.Value * U.Value
        if resultQ >= Q.Value:
            sign = '\\ge'
            result = u'удастся'
        else:
            sign = '\\less'
            result = u'не удастся'
        answer = u'''
            ${Q.Letter}' = {C.Letter}{U.Letter} = {C:Answer}\\cdot{U:Answer} = {Q:Answer} = {Q:ShortAnswer}
            \\implies {Q.Letter}' {sign} {Q.Letter} \\implies \\text{{{result}}}$
        '''.format(
            Q=LetterValue(Letter=Q.Letter, Value=resultQ, units=Units(basic=u'\\units{нКл}', standard=u'\\units{Кл}', power=-9)),
            U=U,
            C=C,
            sign=sign,
            result=result,
        )

        return problems.task.Task(u'''
            На конденсаторе указано: ${C:Task}$, ${U:Task}$.
            Удастся ли его использовать для накопления заряда ${Q:Task}$?
        '''.format(U=U, Q=Q, C=C),
        answer=answer,
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
        value = fractions.Fraction(numerator=b, denominator=a)
        if value == 1:
            sign = '='
            result = u'не изменится'
        else:
            if value > 1:
                sign = '>'
                result = u'увеличится'
            elif value < 1:
                sign = '<'
                result = u'уменьшится'
                value = 1 / value
            result += u' в $\\frac{value.numerator}{value.denominator}$ раз'.format(value=value)
        answer = u'''
            $\\frac{{C'}}{{C}}
                = \\frac{{\\eps_0\\eps \\frac S{a}}}{{\\frac d{b}}} \\Big/ \\frac{{\\eps_0\\eps S}}{{d}}
                = \\frac{{ {b} }}{{ {a} }} {sign} 1 \\implies \\text{{{result}}}
            $
        '''.format(a=a, b=b, sign=sign, result=result)
        return problems.task.Task(u'''
            Как и во сколько раз изменится ёмкость плоского конденсатора при уменьшении площади пластин в {a} раз
            и уменьшении расстояния между ними в {b} раз?
        '''.format(a=a, b=b),
        answer=answer,
        )

    def All(self):
        for a, b in itertools.product([2, 3, 4, 5, 6, 7, 8], [2, 3, 4, 5, 6, 7, 8]):
            yield self.__call__(a=a, b=b)


class Rymkevich762(variant.VariantTask):
    def __call__(self, C=None, Q=None):
        answer = u'''
            ${W:Letter}
                = \\frac{{{Q:Letter}^2}}{{2{C:Letter}}}
                =   \\frac{{
                        \\sqr{{{Q:Answer}}}
                    }}{{
                        2\\cdot{C:Answer}
                    }}
                = {W:Answer} = {W:ShortAnswer}
            $
        '''.format(
            C=C,
            Q=Q,
            W=LetterValue(Letter='W', Value=1. * Q.Value ** 2 / 2 / C.Value, units=Units(basic=u'\\units{мкДж}', standard=u'\\units{Дж}', power=-6)),
        )

        return problems.task.Task(u'''
            Электрическая ёмкость конденсатора равна ${C:Task}$,
            при этом ему сообщён заряд ${Q:Task}$. Какова энергия заряженного конденсатора?
        '''.format(C=C, Q=Q),
        answer=answer,
        )

    def All(self):
        for Ql, Qv, Cv in itertools.product(['Q', 'q'], [300, 500, 800, 900], [200, 400, 600, 750]):
            yield self.__call__(
                Q=LetterValue(Letter=Ql, Value=Qv, units=Units(basic=u'\\units{нКл}', standard=u'\\units{Кл}', power=-9)),
                C=LetterValue(Letter='C', Value=Cv, units=Units(basic=u'\\units{пФ}', standard=u'\\units{Ф}', power=-12)),
            )


class Cond1(variant.VariantTask):
    def __call__(self, C=None, U=None):
        answer = u'''
            $Q_1
                = Q_2
                = C{U:Letter}
                = \\frac{{{U:Letter}}}{{\\frac1{{C_1}} + \\frac1{{C_2}}}}
                = \\frac{{C_1C_2{U:Letter}}}{{C_1 + C_2}}
                = \\frac{{
                    {C[0]:Answer} \\cdot {C[1]:Answer} \\cdot {U:Answer}
                }}{{
                    {C[0]:Answer} + {C[1]:Answer}
                }}
                = {Q:Answer}
                = {Q:ShortAnswer}
            $
        '''.format(
            C=C,
            U=U,
            Q=LetterValue(Letter='Q', Value=1. * C[0].Value * C[1].Value * U.Value / (C[0].Value + C[1].Value), units=Units(basic=u'\\units{нКл}', standard=u'\\units{Кл}', power=-9))
        )
        return problems.task.Task(u'''
            Два конденсатора ёмкостей ${C[0]:Task}$ и ${C[1]:Task}$ последовательно подключают
            к источнику напряжения ${U:Task}$ (см. рис.). Определите заряды каждого из конденсаторов.
        '''.format(C=C, U=U),
        answer=answer,
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


class Rezistor1(variant.VariantTask):
    def __call__(self, R=None, I=None, U=None):
        assert R and ((I is None) != (U is None))
        if I:
            U = LetterValue(Letter='U', Value=I.Value * R.Value, units=Units(basic=u'\\units{В}', standard=u'\\units{В}', power=0))
            P = LetterValue(Letter='P', Value=I.Value ** 2 * R.Value, units=Units(basic=u'\\units{Вт}', standard=u'\\units{Вт}', power=0))
            text = u'''
                Через резистор сопротивлением ${R:Task}$ протекает электрический ток ${I:Task}$.
                Определите, чему равны напряжение на резисторе и мощность, выделяющаяся на нём.
            '''.format(R=R, I=I)
            answer = u'''
                \\begin{{align*}}
                {U:Letter} &= {I:Letter}{R:Letter} = {I:Answer} \\cdot {R:Answer} = {U:Answer}, \\\\
                {P:Letter} &= {I:Letter}^2{R:Letter} = \\sqr{I:Answer:s} \\cdot {R:Answer} = {P:Answer}
                \\end{{align*}}
            '''
        elif U:
            I = LetterValue(Letter='\\mathcal{I}', Value=1. * U.Value / R.Value, units=Units(basic=u'\\units{А}', standard=u'\\units{А}', power=0))
            P = LetterValue(Letter='P', Value=1. * U.Value ** 2 / R.Value, units=Units(basic=u'\\units{Вт}', standard=u'\\units{Вт}', power=0))
            text = u'''
                На резистор сопротивлением ${R:Task}$ подали напряжение ${U:Task}$.
                Определите ток, который потечёт через резистор, и мощность, выделяющуюся на нём.
            '''.format(R=R, U=U)
            answer = u'''
                \\begin{{align*}}
                {I:Letter} &= \\frac{U:Letter:s}{R:Letter:s} = \\frac{U:Answer:s}{R:Answer:s} = {I:Answer}, \\\\
                {P:Letter} &= \\frac{{ {U:Letter}^2 }}{R:Letter:s} = \\frac{{ \\sqr{U:Answer:s} }}{R:Answer:s} = {P:Answer}
                \\end{{align*}}
            '''
        return problems.task.Task(text, answer=answer.format(I=I, U=U, R=R, P=P))

    def All(self):
        for rLetter, rValue in itertools.product(['r', 'R'], [5, 12, 18, 30]):
            R = LetterValue(Letter=rLetter, Value=rValue, units=Units(basic=u'\\units{Ом}', standard=u'\\units{Ом}', power=0))
            for iValue in [2, 3, 4, 5, 6, 8, 10, 15]:
                yield self.__call__(
                    I=LetterValue(Letter='\\mathcal{I}', Value=iValue, units=Units(basic=u'\\units{А}', standard=u'\\units{А}', power=0)),
                    R=R,
                )
            for uLetter, uValue in itertools.product(['U', 'V'], [120, 150, 180, 240]):
                yield self.__call__(
                    U=LetterValue(Letter=uLetter, Value=uValue, units=Units(basic=u'\\units{В}', standard=u'\\units{В}', power=0)),
                    R=R,
                )


class Rezistor2(variant.VariantTask):
    def __call__(self, r=None, R=None, E=None, t=None):
        I1 = LetterValue(Letter='\\mathcal{I}_1', Value=1. * E.Value / R.Value, units=Units(standard=u'\\units{А}'))
        I2 = LetterValue(Letter='\\mathcal{I}_2', Value=1. * E.Value / (R.Value + r.Value), units=Units(standard=u'\\units{А}'))
        Q1 = LetterValue(Letter='Q_1', Value=1. * I1.Value ** 2 * R.Value * t.Value, units=Units(standard=u'\\units{Дж}'))
        Q2 = LetterValue(Letter='Q_2', Value=1. * I2.Value ** 2 * R.Value * t.Value, units=Units(standard=u'\\units{Дж}'))
        A1 = LetterValue(Letter='A_1', Value=1. * I1.Value * E.Value * t.Value, units=Units(standard=u'\\units{Дж}'))
        A2 = LetterValue(Letter='A_2', Value=1. * I2.Value * E.Value * t.Value, units=Units(standard=u'\\units{Дж}'))
        # eta1 = LetterValue(Letter='\\eta_1', Value=1. * 15 /Q1.Value, units=Units(standard=u''))
        # print А2.Value
        # eta1 = LetterValue(Letter='\\eta_1', Value=, units=Units(standard=u''))
        # print A2.Value
        # print A2
        # # print int(А2.Value)
        eta1 = LetterValue(Letter='\\eta_1', Value=1. * Q1.Value / A1.Value, units=Units(standard=u''))
        eta2 = LetterValue(Letter='\\eta_2', Value=1. * Q2.Value / A2.Value, units=Units(standard=u''))
        answer = u'''
            \\begin{{align*}}
            {I1:Letter}
                            &= \\frac{E:Letter:s}{R:Letter:s}
                            = \\frac{E:Answer:s}{R:Answer:s}
                            = {I1:Answer}, \\\\
            {I2:Letter}
                            &= \\frac{E:Letter:s}{{ {R:Letter} + {r:Letter} }}
                            = \\frac{E:Answer:s}{{ {R:Answer} + {r:Answer} }}
                            = {I2:Answer}, \\\\
            {Q1:Letter}
                            &= {I1:Letter}^2{R:Letter}{t:Letter}
                            = \\cbr{{ \\frac{E:Letter:s}{R:Letter:s} }}^2 {R:Letter} {t:Letter}
                            = \\cbr{{ \\frac{E:Answer:s}{R:Answer:s} }}^2 \\cdot {R:Answer} \\cdot {t:Answer}
                            = {Q1:Answer}, \\\\
            {Q2:Letter}
                            &= {I2:Letter}^2{R:Letter}{t:Letter}
                            = \\cbr{{\\frac{E:Letter:s}{{ {R:Letter} + {r:Letter} }} }}^2 {R:Letter} {t:Letter}
                            = \\cbr{{\\frac{E:Answer:s}{{ {R:Answer} + {r:Answer} }} }}^2 \\cdot {R:Answer} \\cdot {t:Answer}
                            = {Q2:Answer}, \\\\
            {A1:Letter}
                            &= {I1:Letter}{t:Letter}{E:Letter}
                            = \\frac{E:Letter:s}{{ {R:Letter} }} {t:Letter} {E:Letter}
                            = \\frac{{ {E:Letter}^2 {t:Letter} }}{{ {R:Letter} }}
                            = \\frac{{ \\sqr{E:Answer:s} \\cdot {t:Answer} }}{R:Answer:s}
                            = {A1:Answer}, \\text{{положительна}}, \\\\
            {A2:Letter}
                            &= {I2:Letter}{t:Letter}{E:Letter}
                            = \\frac{E:Letter:s}{{ {R:Letter} + {r:Letter} }} {t:Letter} {E:Letter}
                            = \\frac{{ {E:Letter}^2 {t:Letter} }}{{ {R:Letter} + {r:Letter} }}
                            = \\frac{{ \\sqr{E:Answer:s} \\cdot {t:Answer} }}{{ {R:Answer} + {r:Answer} }}
                            = {A2:Answer}, \\text{{положительна}}, \\\\
            {eta1:Letter}
                            &= \\frac{Q1:Letter:s}{A1:Letter:s}
                            = \\ldots
                            = \\frac{R:Letter:s}{R:Letter:s}
                            = 1, \\\\
            {eta2:Letter}
                            &= \\frac{Q2:Letter:s}{A2:Letter:s}
                            = \\ldots
                            = \\frac{R:Letter:s}{{ {R:Letter} + {r:Letter} }}
                            = {eta2:Value}
            \\end{{align*}}
        '''.format(I1=I1, I2=I2, Q1=Q1, Q2=Q2, A1=A1, A2=A2, eta1=eta1, eta2=eta2, E=E, r=r, R=R, t=t)
        text = u'''
            Замкнутая электрическая цепь состоит из ЭДС ${E:Task}$ и сопротивлением ${r:Letter}$
            и резистора ${R:Task}$. Определите ток, протекающий в цепи. Какая тепловая энергия выделится на резисторе за время
            ${t:Task}$? Какая работа будет совершена ЭДС за это время? Каков знак этой работы? Чему равен КПД цепи? Вычислите значения для 2 случаев:
            ${r:Letter}=0$ и ${r:Task}$.
        '''.format(E=E, r=r, R=R, t=t)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for rValue, RValue, EValue, tValue in itertools.product([1, 2, 3, 4], [10, 15, 24, 30], [10, 20, 30, 60], [2, 5, 10]):
            yield self.__call__(
                E=LetterValue(Letter='\\mathcal{E}', Value=EValue, units=Units(standard=u'\\units{В}')),
                R=LetterValue(Letter='R', Value=RValue, units=Units(standard=u'\\units{Ом}')),
                r=LetterValue(Letter='r', Value=rValue, units=Units(standard=u'\\units{Ом}')),
                t=LetterValue(Letter='\\tau', Value=rValue, units=Units(standard=u'\\units{с}')),
            )


class Rezistor3(variant.VariantTask):
    def __call__(self, R=None):
        r = LetterValue(Letter='r', Value=(1. * R[0].Value * R[1].Value) ** 0.5, units=Units(standard=u'\\units{Ом}'))
        eta1 = LetterValue(Letter='\\eta_1', Value=1. * R[0].Value / (R[0].Value + r.Value), units=Units(standard=u''))
        eta2 = LetterValue(Letter='\\eta_2', Value=1. * R[1].Value / (R[1].Value + r.Value), units=Units(standard=u''))
        answer = u'''
            \\begin{{align*}}
            P_1 &= \\sqr{{ \\frac{E:Letter:s}{{ {R[0]:Letter} + {r:Letter} }} }} {R[0]:Letter},
            P_2  = \\sqr{{ \\frac{E:Letter:s}{{ {R[1]:Letter} + {r:Letter} }} }} {R[1]:Letter},
            P_1 = P_2 \\implies \\\\
            &\\implies {R[0]:Letter} \\sqr{{ {R[1]:Letter} + {r:Letter} }} = {R[1]:Letter} \\sqr{{ {R[0]:Letter} + {r:Letter} }} \\implies \\\\
            &\\implies {R[0]:Letter} {R[1]:Letter}^2 + 2 {R[0]:Letter} {R[1]:Letter} {r:Letter} + {R[0]:Letter} {r:Letter}^2 =
                        {R[1]:Letter} {R[0]:Letter}^2 + 2 {R[1]:Letter} {R[0]:Letter} {r:Letter} + {R[1]:Letter} {r:Letter}^2  \\implies \\\\
            &\\implies {r:Letter}^2 ({R[1]:Letter} - {R[0]:Letter}) = {R[1]:Letter}^2 {R[1]:Letter} - {R[0]:Letter}^2 {R[1]:Letter} \\implies \\\\
            &\\implies {r:Letter}
                = \\sqrt{{ {R[0]:Letter} {R[1]:Letter} \\frac{{ {R[1]:Letter} - {R[0]:Letter} }}{{ {R[1]:Letter} - {R[0]:Letter} }} }}
                = \\sqrt{{ {R[0]:Letter} {R[1]:Letter} }}
                = \\sqrt{{ {R[0]:Answer} \\cdot {R[1]:Answer} }}
                = {r:Answer}. \\\\
             {eta1:Letter}
                &= \\frac{R[0]:Letter:s}{{ {R[0]:Letter} + {r:Letter} }}
                = \\frac{{ \\sqrt{R[0]:Letter:s} }}{{ \\sqrt{R[0]:Letter:s} + \\sqrt{R[1]:Letter:s} }}
                = {eta1:Value}, \\\\
             {eta2:Letter}
                &= \\frac{R[1]:Letter:s}{{ {R[1]:Letter} + {r:Letter} }}
                = \\frac{{ \\sqrt{R[1]:Letter:s} }}{{ \\sqrt{R[1]:Letter:s} + \\sqrt{R[0]:Letter:s} }}
                = {eta2:Value}
            \\end{{align*}}
        '''.format(R=R, r=r, eta1=eta1, eta2=eta2, E=LetterValue(Letter='\\mathcal{E}', Value=0, units=None))
        text = u'''
            Лампочки, сопротивления которых ${R[0]:Task}$ и ${R[1]:Task}$, поочерёдно подключённные к некоторому источнику тока,
            потребляют одинаковую мощность. Найти внутреннее сопротивление источника и КПД цепи в каждом случае.
        '''.format(R=R)
        return problems.task.Task(text, answer=answer)

    def All(self):
        for RValues in [
            (0.25, 16),
            (0.25, 64),
            (0.25, 4),
            (0.5, 18),
            (0.5, 2),
            (0.5, 4.5),
            (1, 4),
            (1, 9),
            (1, 49),
            (3, 12),
            (3, 48),
            (4, 36),
            (4, 100),
            (5, 45),
            (5, 80),
            (6, 24),
            (6, 54),
        ]:
            yield self.__call__(
                R=[
                    LetterValue(Letter='R_1', Value=RValues[0], units=Units(basic=u'\\units{Ом}', standard=u'\\units{Ом}', power=0)),
                    LetterValue(Letter='R_2', Value=RValues[1], units=Units(basic=u'\\units{Ом}', standard=u'\\units{Ом}', power=0)),
                ]
            )


class Rezistor4(variant.VariantTask):
    def __call__(self, R=None, r=None, E=None):
        text = u'''
            Определите ток, протекающий через резистор ${R:Task}$ и разность потенциалов на нём (см. рис. на доске),
            если ${r[0]:Task}$, ${r[1]:Task}$, ${E[0]:Task}$, ${E[1]:Task}$
        '''.format(R=R, r=r, E=E)
        return problems.task.Task(text)

    def All(self):
        for RValue, r1Value, r2Value, E1Value, E2Value in itertools.product(
            [10, 12, 15, 18, 20],
            [1, 2, 3],
            [1, 2, 3],
            [20, 30, 40, 60],
            [20, 30, 40, 60],
        ):
            if r1Value != r2Value and E1Value != E2Value:
                yield self.__call__(
                    R = LetterValue(Letter='R', Value=RValue, units=Units(basic=u'\\units{Ом}', standard=u'\\units{Ом}', power=0)),
                    r=[
                        LetterValue(Letter='r_1', Value=r1Value, units=Units(basic=u'\\units{Ом}', standard=u'\\units{Ом}', power=0)),
                        LetterValue(Letter='r_2', Value=r2Value, units=Units(basic=u'\\units{Ом}', standard=u'\\units{Ом}', power=0)),
                    ],
                    E=[
                        LetterValue(Letter='\\mathcal{E}_1', Value=E1Value, units=Units(basic=u'\\units{В}', standard=u'\\units{В}', power=0)),
                        LetterValue(Letter='\\mathcal{E}_2', Value=E2Value, units=Units(basic=u'\\units{В}', standard=u'\\units{В}', power=0)),
                    ],
                )

