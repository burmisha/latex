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
        assert (self.Basic == self.Standard) == (self.Power == 0)


class LetterValue(object):
    def __init__(self, Letter=None, Value=None, units=None):
        self.Letter = Letter
        self.Value = Value
        self.Units = units

    def __format__(self, format):
        if isinstance(self.Value, int):
            fmt = '{:d}'
        else:
            fmt = '{:.2f}'
        if self.Value < 0:
            fmt = '(%s)' % fmt
        value = fmt.format(self.Value).replace('.', '{,}')
        if format == 'Task':
            return u'{self.Letter}={self.Value}{self.Units.Basic}'.format(self=self)
        elif format == 'Letter':
            return u'{self.Letter}'.format(self=self)
        elif format == 'Value':
            return u'{self.Value}'.format(self=self)
        elif format == 'ShortAnswer':
            return u'{value}{self.Units.Basic}'.format(self=self, value=value)
        elif format == 'Answer':
            if self.Units.Power != 0:
                return u'{value} \\cdot 10^{{{self.Units.Power}}} {self.Units.Standard}'.format(self=self, value=value)
            else:
                return u'{value} {self.Units.Standard}'.format(self=self, value=value)
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
                = \\frac ba {sign} 1 \\implies \\text{{{result}}}
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
            text = u'''
                Через резистор сопротивлением ${R:Task}$ протекает электрический ток ${I:Task}$.
                Определите, чему равны напряжение на резисторе и мощность, выделяющаяся на нём.
            '''.format(R=R, I=I)
        elif U:
            text = u'''
                На резистор сопротивлением ${R:Task}$ подали напряжение ${U:Task}$.
                Определите ток, который потечёт через резистор, и мощность, выделяющуюся на нём.
            '''.format(R=R, U=U)
        return problems.task.Task(text)

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
        text = u'''
            Замкнутая электрическая цепь состоит из ЭДС ${E:Task}$ и сопротивлением ${r:Letter}$
            и резистора ${R:Task}$. Определите ток, протекающий в цепи. Какая тепловая энергия выделится на резисторе за время
            ${t:Task}$? Какая работа будет совершена ЭДС за это время? Каков знак этой работы? Чему равен КПД цепи? Вычислите значения для 2 случаев:
            ${r:Letter}=0$ и ${r:Task}$.
        '''.format(E=E, r=r, R=R, t=t)
        return problems.task.Task(text)

    def All(self):
        for rValue, RValue, EValue, tValue in itertools.product([1, 2, 3, 4], [10, 15, 24, 30], [10, 20, 30, 60], [2, 5, 10]):
            yield self.__call__(
                E=LetterValue(Letter='\\mathcal{E}', Value=EValue, units=Units(basic=u'\\units{В}', standard=u'\\units{В}', power=0)),
                R=LetterValue(Letter='R', Value=RValue, units=Units(basic=u'\\units{Ом}', standard=u'\\units{Ом}', power=0)),
                r=LetterValue(Letter='r', Value=rValue, units=Units(basic=u'\\units{Ом}', standard=u'\\units{Ом}', power=0)),
                t=LetterValue(Letter='\\tau', Value=rValue, units=Units(basic=u'\\units{с}', standard=u'\\units{с}', power=0)),
            )


class Rezistor3(variant.VariantTask):
    def __call__(self, R=None):
        text = u'''
            Лампочки, сопротивления которых ${R[0]:Task}$ и ${R[1]:Task}$, поочерёдно подключённные к некоторому источнику тока,
            потребляют одинаковую мощность. Найти внутреннее сопротивление источника и КПД цепи в каждом случае.
        '''.format(R=R)
        return problems.task.Task(text)

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

