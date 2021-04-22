import math
import itertools

import generators.variant as variant
from generators.helpers import UnitValue, Consts


@variant.text('''
    Сколько фотонов испускает за {minutes} минут лазер,
    если мощность его излучения {power:Value:e}?
    Длина волны излучения {length:Value:e}. {h:Task:e}.
''')
@variant.answer_short('''
    N = \\frac{ Pt\\lambda }{ hc }
       = \\frac{
            {power:Value} * {minutes} * 60 \\units{ с } * {length:Value}
         }{
            {h:V} * {c:V}
        }
       \\approx {approx} * 10^{ {answerPower} }\\units{ фотонов }
''')
@variant.arg(minutes=[5, 10, 20, 30, 40, 60, 120])
@variant.arg(power=('P = {} мВт', [15, 40, 75, 200]))
@variant.arg(length=('\\lambda = {} нм', [500, 600, 750]))
class Fotons(variant.VariantTask):
    def GetUpdate(self, power=None, minutes=None, length=None, **kws):
        answer = 1. * power.Value * minutes * length.Value / 6.626 * 2 / (10 ** 5)
        return dict(
            answerValue=answer,
            answerPower=15 + 5,
            approx='%.2f' % float(answer),
            h=Consts.h,
            c=Consts.c,
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
    \\begin{{enumerate}}
        \\item {q1:V:e},
        \\item {q2:V:e},
        \\item {q3:V:e},
        \\item {q4:V:e}.
    \\end{{enumerate}}
''')
@variant.arg(q1__a1=[('450 нм', 'синий'), ('580 нм', 'жёлтый '), ('660 нм', 'красный')])
@variant.arg(q2__a2=[('470 нм', 'синий'), ('390 нм', 'фиолетовый'), ('595 нм', 'оранжевый ')])
@variant.arg(q3__a3=[('530 нм', 'зелёный'), ('720 нм', 'красный'), ('610 нм', 'оранжевый')])
@variant.arg(q4__a4=[('580 нм', 'зелёный'), ('490 нм', 'голубой'), ('420 нм', 'фиолетовый')])
class ColorNameFromLambda(variant.VariantTask):
    pass


@variant.solution_space(80)
@variant.text('''
    Определите {what} колебаний вектора напряженности {of} 
    в электромагнитной волне в вакууме, длина который составляет {lmbd:V:e}. 
''')
@variant.arg(what=['период', 'частоту'])
@variant.arg(of=['электрического поля', 'индукции магнитного поля'])
@variant.arg(lmbd=['%d %s' % (l, s) for l in [2, 3, 5] for s in ['м', 'см']])
class T_Nu_from_lambda(variant.VariantTask):
    pass


@variant.solution_space(80)
@variant.text('''
    Определите энергию фотона излучения частотой {nu:V:e}. 
    Ответ получите в джоулях и в электронвольтах.
''')
@variant.arg(nu=('{} 10^16 Гц', [4, 5, 6, 7, 8, 9]))
class E_from_nu(variant.VariantTask):
    pass


@variant.solution_space(80)
@variant.text('''
    Определите энергию {of} с длиной волны {lmbd:V:e}. Ответ выразите в {in_what}.
    Способен ли человеческий глаз увидеть один такой квант? А импульс таких квантов?'
''')
@variant.arg(lmbd=('{} нм', [150, 200, 400, 500, 600, 700, 850, 900]))
@variant.arg(of=['кванта света', 'фотона'])
@variant.arg(in_what=['джоулях', 'электронвольтах'])
class E_from_lambda(variant.VariantTask):
    pass


@variant.solution_space(40)
@variant.text('''
    Из формулы Планка выразите (нужен вывод, не только ответ)...
    \\begin{{enumerate}}
        \\item длину соответствующей электромагнитной волны,
        \\item {second}.
    \\end{{enumerate}}
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
    N(t) = N_0 * 2^{ -\\frac t{ \\tau_\\frac12 }  }
    \\implies \\log_2\\frac N{ N_0 } = - \\frac t{ \\tau_\\frac 12 }
    \\implies \\tau_\\frac 12 = - \\frac t { \\log_2\\frac N{ N_0 } }
                              =   \\frac t { \\log_2\\frac { N_0 }N }
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
            T='%.1f ч' % (time / math.log(total / (total - delta), 2)),
        )


@variant.text('''
    Определите длину волны лучей, фотоны которых имеют энергию
    равную кинетической энергии электрона, ускоренного напряжением {V:Value|e}.
''')
@variant.arg(V=['%d В' % v for v in [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]])
class Quantum1119(variant.VariantTask):  # 1119 Рымкевич
    pass


@variant.text('''
    Лучше всего нейтронное излучение ослабляет вода: в 4 раза лучше бетона и в 3 раза лучше свинца.
    Толщина слоя половинного ослабления $\\gamma$-излучения для воды равна {d1:Value|e}.
    Во сколько раз ослабит нейтронное излучение слой воды толщиной {d:Task|e}?
''')
@variant.arg(d1=['3 см'])
@variant.arg(d=['%s = %d см' % (l, v) for l, v in itertools.product(['l', 'h', 'd'], [15, 30, 60, 120])])
class Quantum1120(variant.VariantTask):  # 1120 Рымкевич
    pass
