import itertools

import generators.variant as variant
from generators.helpers import Consts, Decimal

@variant.text('''
    Для частицы, движущейся с релятивистской скоростью,
    выразите ${x}$ и ${y}$ через $c$, ${a}$ и ${b}$,
    где $E_\\text{кин}$~--- кинетическая энергия частицы,
    а $E_0$, $p$ и $v$~--- её энергия покоя импульс и скорость.
''')
@variant.arg(x__y__a__b=itertools.permutations([
    'E_\\text{кин}',
    'E_0',
    'p',
    'v',
], 4))
@variant.solution_space(200)
@variant.arg(E_kin=['E_\\text{кин} = 1 Дж'])
@variant.arg(E_0=['E_0 = 1 Дж'])
@variant.arg(gamma_denom=['\\sqrt{1 - \\frac{v^2}{c^2}} = 1'])
@variant.answer_align([
    '{E_kin:L}, {E_0:L}:\\quad'
        '&E = {E_kin:L} + {E_0:L} = \\frac{E_0:L:s}{gamma_denom:L:s} \\implies {gamma_denom:L} = \\frac{E_0:L:s}{{E_0:L:s} + {E_kin:L:s}} \\implies v = c\\sqrt{1 - \\sqr{\\frac{E_0:L:s}{{E_0:L:s} + {E_kin:L:s}}}}',
        '&p = \\frac{mv}{gamma_denom:L:s} = \\frac{E_0:L:s}{c^2} * \\sqrt{1 - \\sqr{\\frac{E_0:L:s}{{E_0:L:s} + {E_kin:L:s}}}} * \\frac{{E_kin:L:s} + {E_0:L:s}}{E_0:L:s} = \\frac{E_0:L:s}{c^2} * \\sqrt{\\sqr{\\frac{{E_kin:L:s} + {E_0:L:s}}{E_0:L:s}} - 1}.',

    '{E_kin:L}, p:\\quad'
        '&{E_kin:L} = E - E_0 = mc^2\\cbr{\\frac 1{gamma_denom:L:s} - 1}, p = \\frac{mv}{gamma_denom:L:s} \\implies \\frac{E_kin:L:s}{p} = \\frac{\\frac 1{gamma_denom:L:s} - 1}{gamma_denom:L:s} \\implies v = \\ldots',
        '&E_0 = E - {E_kin:L} = \\frac{E_0:L:s}{gamma_denom:L:s} - {E_kin:L} \\implies E_0 = \\frac{E_kin:L:s}{\\frac 1{gamma_denom:L:s} - 1} = \\ldots',

    '{E_kin:L}, v:\\quad'
        '&{E_kin:L} = E - E_0 = mc^2\\cbr{\\frac 1{gamma_denom:L:s} - 1} \\implies m = \\frac{E_kin:L:s}{c^2\\cbr{\\frac 1{gamma_denom:L:s} - 1}}',
        '&E_0 = mc^2 = \\frac{E_kin:L:s}{\\frac 1{gamma_denom:L:s} - 1}',
        # 'p^2 c^2 + m^2 c^4 &= \\sqr{E_0 + {E_kin:L}} \\implies p = \\frac 1c \\sqrt{\\sqr{E_0 + {E_kin:L}} - m^2 c^4} = \\ldots',
        '&p = \\frac{mv}{gamma_denom:L:s} = \\frac{E_kin:L:s}{c^2\\cbr{\\frac 1{gamma_denom:L:s} - 1}} * \\frac{v}{gamma_denom:L:s} = \\frac{{E_kin:L:s} v}{c^2\\cbr{1 - {gamma_denom:L:s}}}',

    'E_0, p:\\quad'
        '&E_0 = mc^2, \\quad p = \\frac{mv}{gamma_denom:L:s} \\implies \\frac{E_0:L:s}{p} = \\frac{c^2}v{gamma_denom:L:s} = c\\sqrt{\\frac{c^2}{v^2} - 1}',
        '&\\sqr{\\frac{E_0:L:s}{pc}} = \\frac{c^2}{v^2} - 1 \\implies \\frac{v^2}{c^2} = \\frac 1{1 + \\frac{E_0^2}{p^2c^2}} \\implies v = \\frac c{\\sqrt{1 + \\frac{E_0^2}{p^2c^2}}}',
        '&{E_kin:L:s} = E - E_0 = \\sqrt{E_0^2 + p^2c^2} - E_0',

    'E_0, v:\\quad'
        '&E_0 = mc^2 \\implies m = \\frac{E_0:L:s}{c^2} \\qquad p = \\frac{mv}{gamma_denom:L:s} = \\frac{E_0:L:s}{c^2} * \\frac{v}{gamma_denom:L:s}',
        '&{E_kin:L}= mc^2\\cbr{\\frac 1{gamma_denom:L:s} - 1} = \\frac{E_0:L:s}{c^2}\\cbr{\\frac 1{gamma_denom:L:s} - 1}',

    'p, v:\\quad'
        '&p = \\frac{mv}{gamma_denom:L:s} \\implies m = \\frac p v {gamma_denom:L:s} \\implies E_0 = mc^2 =\\frac {pc^2} v {gamma_denom:L:s}',
        '&{E_kin:L} = mc^2\\cbr{\\frac 1{gamma_denom:L:s} - 1} = \\frac p v {gamma_denom:L:s}\\cbr{\\frac 1{gamma_denom:L:s} - 1} = \\frac p v \\cbr{1 - {gamma_denom:L:s}}',
])
class Equations(variant.VariantTask):
    pass


@variant.solution_space(150)
@variant.text('''
    {what} движется со скоростью $0.{percent}\,c$, где $c$~--- скорость света в вакууме.
    Каково при этом отношение {energy} к его энергии покоя $E_0$?
''')
@variant.answer_align([
    '''E &= \\frac{E_0}{\\sqrt{1 - \\frac{v^2}{c^2}}}
        \\implies \\frac E{E_0}
            = \\frac 1{\\sqrt{1 - \\frac{v^2}{c^2}}}
            = \\frac 1{\\sqrt{1 - \\sqr{0.{percent}}}}
            \\approx {E:.3f},
    ''',
    '''
    E_{\\text{кин}} &= E - E_0
        \\implies \\frac{E_{\\text{кин}}}{E_0}
            = \\frac E{E_0} - 1
            = \\frac 1{\\sqrt{1 - \\frac{v^2}{c^2}}} - 1
            = \\frac 1{\\sqrt{1 - \\sqr{0.{percent}}}} - 1
            \\approx {E_kin:.3f}.''',
])
@variant.arg(what='Протон/Позитрон')
@variant.arg(energy='полной энергии частицы $E$/кинетической энергии частицы $E_\\text{кин.}$')
@variant.arg(percent=['9', '8', '7', '6'])
class E_ratio_from_v_ratio(variant.VariantTask):  # Вишнякова - Базовый курс 4 - задача 1
    def GetUpdate(self, what=None, energy=None, percent=None):
        share = float('0.' + percent)
        return dict(
            E=1. / ((1. - share ** 2) ** 0.5),
            E_kin=1. / ((1. - share ** 2) ** 0.5) - 1,
        )


@variant.solution_space(150)
@variant.text('''
    {what} движется со скоростью $0.{percent}\,c$, где $c$~--- скорость света в вакууме.
    Определите его {x} (в ответе приведите формулу и укажите численное значение).
''')
@variant.answer_align([
    '''{E:L} &= \\frac{mc^2}{\\sqrt{1 - \\frac{v^2}{c^2}}}
        \\approx \\frac{{m:Value} * {Consts.c:Value|sqr}}{\\sqrt{1 - 0.{percent}^2}}
        \\approx {E:Value},
    ''',
    '''
    {E_kin:L} &= \\frac{mc^2}{\\sqrt{1 - \\frac{v^2}{c^2}}} - mc^2
        = mc^2 \\cbr{\\frac 1{\\sqrt{1 - \\frac{v^2}{c^2}}} - 1} \\approx''',
    '''
        &\\approx \\cbr{{m:Value} * {Consts.c:Value|sqr}}
        * \\cbr{\\frac 1{\\sqrt{1 - 0.{percent}^2}} - 1}
        \\approx {E_kin:Value},
    ''',
    '''
    {p:L} &= \\frac{mv}{\\sqrt{1 - \\frac{v^2}{c^2}}}
        \\approx \\frac{{m:Value} * 0.{percent} * {Consts.c:Value}}{\\sqrt{1 - 0.{percent}^2}}
        \\approx {p:Value}.'''
])
@variant.arg(what='Протон/Электрон')
@variant.arg(x='полную энергию/кинетическую энергию/импульс')
@variant.arg(percent=['85', '75', '65'])
class E_P_from_v_ratio(variant.VariantTask):  # Вишнякова - Базовый курс 4._ - задача 3
    def GetUpdate(self, what=None, x=None, percent=None):
        m = {
            'Протон': Consts.m_p,
            'Электрон': Consts.m_e,
        }[what]
        share = float('0.' + percent)
        gamma = Decimal(1 / ((1 - share ** 2) ** 0.5))

        c = Consts.c

        E = m * c * c * gamma
        E_kin = m * c * c * (gamma - 1)
        p = m * c * Decimal(share) * gamma

        power = -12
        power_p = -21
        mul = 10 ** (-power)
        mul_p = 10 ** (-power_p)

        return dict(
            E=f'E = {E.SI_Value * mul:.3f} 10^{power} Дж',
            E_kin=f'E_{{\\text{{кин}}}} = {E_kin.SI_Value * mul:.3f} 10^{power} Дж',
            p=f'p = {p.SI_Value * mul_p:.3f} 10^{power_p} кг м / с',
            m=m,
        )


@variant.solution_space(150)
@variant.text('''
    При какой скорости движения (в {what}) релятивистское сокращение длины движущегося тела
    составит {percent}\\%?
''')
@variant.answer_align([
    '''l_0 &= \\frac l{\\sqrt{1 - \\frac{v^2}{c^2}}}
    \\implies 1 - \\frac{v^2}{c^2} = \\sqr{\\frac l{l_0}}
    \\implies \\frac v c = \\sqrt{1 - \\sqr{\\frac l{l_0}}} \\implies
    ''',
    '''
    \\implies v &= c\\sqrt{1 - \\sqr{\\frac l{l_0}}}
    = {Consts.c:Value} * \\sqrt{1 - \\sqr{\\frac {l_0 - 0.{percent}l_0}{l_0}}}
    = {Consts.c:Value} * \\sqrt{1 - \\sqr{1 - 0.{percent}}} \\approx ''',
    '''
    &\\approx {answerShare:.3f}c
    \\approx {speed:Value}
    \\approx {kmch:Value}.''',
])
@variant.arg(what=['км/ч', 'м/с', 'долях скорости света'])
@variant.arg(percent=['50', '30', '10'])
class beta_from_l_reduction(variant.VariantTask):  # Вишнякова - Базовый курс 4._ - задача 6
    def GetUpdate(self, what=None, percent=None):
        share = float('0.' + percent)
        answerShare = Decimal((1. - (1. - share) ** 2) ** 0.5)
        return dict(
            answerShare=answerShare,
            speed='%.3f 10^8 м / с' % (answerShare * Consts.c.Value),
            kmch='%.3f 10^8 км / ч' % (Decimal('3.6') * answerShare * Consts.c.Value),
        )
