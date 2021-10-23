import math
import itertools

import generators.variant as variant
from generators.helpers import UnitValue, Consts


@variant.text('''
    Сколько фотонов испускает за {minutes} минут лазер,
    если мощность его излучения {power:V:e}?
    Длина волны излучения {length:V:e}. {h:Task:e}.
''')
@variant.answer_short('''
    N
        = \\frac{E_{\\text{общая}}}{E_{\\text{одного фотона}}}
        = \\frac{Pt}{h\\nu} = \\frac{Pt}{h \\frac c\\lambda}
        = \\frac{Pt\\lambda}{hc}
        = \\frac{
            {power:V} * {minutes} * 60 \\units{с} * {length:V}
        }{
            {h:V} * {c:V}
        }
        \\approx {approx} * 10^{{answerPower}}\\units{фотонов}
''')
@variant.arg(minutes=[5, 10, 20, 30, 40, 60, 120])
@variant.arg(power=('P = {} мВт', [15, 40, 75, 200]))
@variant.arg(length=('\\lambda = {} нм', [500, 600, 750]))
class Fotons(variant.VariantTask):
    def GetUpdate(self, power=None, minutes=None, length=None):
        h = Consts.h
        c = Consts.c
        mul = 10 ** 20
        answer = power * 60 * minutes * length / h / c / mul
        return dict(
            answerValue=answer,
            answerPower=20,
            approx=f'{answer.SI_Value:.2f}',
            h=h,
            c=c,
        )


# Сколько радиостанций сможет работать без помех в диапазоне {}-{} м, если для каждой необходима полоса частот {}?

# Сигнал радиолокатора отразился от самолёта и вернулся обратно через {}. Чему равно расстояние от локатора для самолёта?



# Длина волны рентгеновского излучения больше длины волны видимого излучения.
# Частота волны инфракрасного излучения больше частоты волны гамма-излучения.
# Скорость распространения инфракрасного излучения составляет 200000 км/с
# Скорость любого электромагнитного излучения в вакууме составляет ровно 299792458 м/с. Там целое число в дробной части (после запятой) исключительно нули.
# Ультрафиолетовое излучение невидимо для человеческого глаза, однако при высокой интенсивности может нанести вред здоровью.
# Чем больше длина волны, тем ниже способность этой волны огибать препятствия.
# Чем выше частота волны, тем больше информации в единицу времени она способна передать, что актуально для средств связи.

@variant.solution_space(80)
@variant.text('''
    Определите название цвета по длине волны в вакууме
    и частоту колебаний электромагнитного поля в ней:
    \\begin{enumerate}
        \\item {q1:V:e},
        \\item {q2:V:e},
        \\item {q3:V:e},
        \\item {q4:V:e}.
    \\end{enumerate}
''')
@variant.answer_tex('''
    \\begin{enumerate}
        \\item ${q1:V} \\to$ {a1}, $\\nu_1 = \\frac c{\\lambda_1} \\approx {nu1:V}$,
        \\item ${q2:V} \\to$ {a2}, $\\nu_2 = \\frac c{\\lambda_2} \\approx {nu2:V}$,
        \\item ${q3:V} \\to$ {a3}, $\\nu_3 = \\frac c{\\lambda_3} \\approx {nu3:V}$,
        \\item ${q4:V} \\to$ {a4}, $\\nu_4 = \\frac c{\\lambda_4} \\approx {nu4:V}$.
    \\end{enumerate}

    $\\nu = \\frac 1 T = \\frac c{\\lambda} = \\frac {Consts.c_4:V:s}{l * {mkm:V}} \\approx \\frac{nu_0:V:s}l$,
    где $l$~--- численное значение длины волны в мкм.
''')
@variant.arg(q1__a1=[('450 нм', 'синий'), ('580 нм', 'жёлтый '), ('660 нм', 'красный')])
@variant.arg(q2__a2=[('470 нм', 'синий'), ('390 нм', 'фиолетовый'), ('595 нм', 'оранжевый')])
@variant.arg(q3__a3=[('530 нм', 'зелёный'), ('720 нм', 'красный'), ('610 нм', 'оранжевый')])
@variant.arg(q4__a4=[('580 нм', 'зелёный'), ('490 нм', 'голубой'), ('420 нм', 'фиолетовый')])
class ColorNameFromLambda(variant.VariantTask):
    def GetUpdate(self, q1=None, a1=None, q2=None, a2=None, q3=None, a3=None, q4=None, a4=None):
        mkm = UnitValue('1 мкм')
        return dict(
            mkm=mkm,
            nu_0=Consts.c_4.Div(mkm, units='Гц', precisionInc=3),
            nu1=Consts.c.Div(q1, units='Гц'),
            nu2=Consts.c.Div(q2, units='Гц'),
            nu3=Consts.c.Div(q3, units='Гц'),
            nu4=Consts.c.Div(q4, units='Гц'),
        )


@variant.solution_space(80)
@variant.text('''
    Определите {what} колебаний вектора напряженности {of}
    в электромагнитной волне в вакууме, длина который составляет {lmbd:V:e}.
''')
@variant.answer_align([
    '\\lambda &= c T \\implies T = \\frac{\\lambda}c = \\frac{lmbd:V:s}{Consts.c:V:s} = {T:V},',
    '\\lambda &= c T = c * \\frac 1\\nu \\implies \\nu = \\frac c{\\lambda} = \\frac{Consts.c:V:s}{lmbd:V:s} = {nu:V}.',
])
@variant.arg(what=['период', 'частоту'])
@variant.arg(of=['электрического поля', 'индукции магнитного поля'])
@variant.arg(lmbd=['%d %s' % (l, s) for l in [2, 3, 5] for s in ['м', 'см']])
class T_Nu_from_lambda(variant.VariantTask):
    def GetUpdate(self, what=None, of=None, lmbd=None):
        return dict(
            T=lmbd.Div(Consts.c, units='с'),
            nu=Consts.c.Div(lmbd, units='Гц'),
        )


@variant.solution_space(80)
@variant.text('''
    Определите энергию фотона излучения частотой {nu:V:e}.
    Ответ получите в джоулях и в электронвольтах.
''')
@variant.answer_short('E = h \\nu = {Consts.h:V} * {nu:V} \\approx {E:V} \\approx {E_eV:V}')
@variant.arg(nu=('{} 10^16 Гц', [4, 5, 6, 7, 8, 9]))
class E_from_nu(variant.VariantTask):
    def GetUpdate(self, nu=None):
        E = Consts.h.Mult(nu, units='Дж', precisionInc=1)
        E_eV = E.Div(Consts.e, units='эВ')
        return dict(
            E=E,
            E_eV=E_eV,
        )


@variant.solution_space(80)
@variant.text('''
    Определите энергию {of} с длиной волны {lmbd:V:e}. Ответ выразите в {in_what}.
    Способен ли человеческий глаз увидеть один такой квант? А импульс таких квантов?'
''')
@variant.answer_short('E = h\\nu = \\frac{hc}{\\lambda} = \\frac{{Consts.h:V} * {Consts.c:V}}{lmbd:V:s} \\approx {E:V} \\approx {E_eV:V}')
@variant.arg(lmbd=('{} нм', [150, 200, 400, 500, 600, 700, 850, 900]))
@variant.arg(of=['кванта света', 'фотона'])
@variant.arg(in_what=['джоулях', 'электронвольтах'])
class E_from_lambda(variant.VariantTask):
    def GetUpdate(self, lmbd=None, of=None, in_what=None):
        E = Consts.h.Mult(Consts.c, units='Дж').Div(lmbd, units='Дж')
        E_eV = E.Div(Consts.e, units='эВ')
        return dict(
            E=E,
            E_eV=E_eV,
        )


@variant.solution_space(40)
@variant.text('''
    Из формулы Планка выразите (нужен вывод, не только ответ)...
    \\begin{enumerate}
        \\item длину соответствующей электромагнитной волны,
        \\item {second}.
    \\end{enumerate}
''')
@variant.arg(second=[
    'период колебаний индукции магнитного поля в соответствующей электромагнитной волне',
    'период колебаний электрического поля в соответствующей электромагнитной волне',
])
class Deduce01(variant.VariantTask):
    pass


@variant.text('''
    Какой период полураспада радиоактивного изотопа,
    если за {time} ч в среднем распадается {delta} атомов из {total}?
''')
@variant.answer_short('''
    N(t) = N_0 * 2^{-\\frac t{\\tau_{\\frac12}}}
    \\implies \\log_2\\frac N{N_0} = - \\frac t{\\tau_\\frac 12}
    \\implies \\tau_\\frac 12 = - \\frac t{\\log_2\\frac N{N_0}}
                              =   \\frac t{\\log_2\\frac{N_0}N}
    = \\frac{
        {time} \\units{ч}
    }
    {
        \\log_2\\frac{{total}}{{total} - {delta}}
    }
    \\approx {T:V}.
''')
@variant.arg(time__delta__total=[
    (12, 7500, 8000),
    (24, 75000, 80000),
    (6, 3500, 4000),
    (8, 37500, 40000),
    (8, 300, 400),
])
class RadioFall2(variant.VariantTask):
    def GetUpdate(self, time=None, total=None, delta=None):
        return dict(
            T='%.1f ч' % (time / math.log(total / (total - delta), 2)),
        )


@variant.text('''
    Определите длину волны лучей, фотоны которых имеют энергию
    равную кинетической энергии электрона, ускоренного напряжением {V:V|e}.
''')
@variant.arg(V=['%d В' % v for v in [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]])
class Quantum1119(variant.VariantTask):  # 1119 Рымкевич
    pass


@variant.text('''
    Лучше всего нейтронное излучение ослабляет вода: в 4 раза лучше бетона и в 3 раза лучше свинца.
    Толщина слоя половинного ослабления $\\gamma$-излучения для воды равна {d1:V|e}.
    Во сколько раз ослабит нейтронное излучение слой воды толщиной {d:Task|e}?
''')
@variant.arg(d1=['3 см'])
@variant.arg(d=['%s = %d см' % (l, v) for l, v in itertools.product(['l', 'h', 'd'], [15, 30, 60, 120])])
class Quantum1120(variant.VariantTask):  # 1120 Рымкевич
    pass
