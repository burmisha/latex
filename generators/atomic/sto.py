import itertools

import generators.variant as variant
from generators.helpers import Consts, Decimal, n_times

@variant.text('''
    Для частицы, движущейся с релятивистской скоростью,
    выразите ${x}$ и ${y}$ через $c$, ${a}$ и ${b}$,
    где $E_\\text{кин}$~--- кинетическая энергия частицы,
    а $E_0$, $p$ и $v$~--- её энергия покоя, импульс и скорость.
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


@variant.solution_space(120)
@variant.text('''
    Запишите
    \\begin{itemize}
        \\item постулаты специальной теории относительности,
        \\item пример релятивистского эффекта, обнаружимый при скоростях гораздо меньше скорости света.
    \\end{itemize}
''')
@variant.no_args
class Theory01(variant.VariantTask):
    pass


@variant.solution_space(150)
@variant.text('''
    Запишите формулу для ...
    \\begin{itemize}
        \\item {q1},
        \\item {q2},
        \\item {q3},
        \\item {q4},
        \\item связь между релятивистским импульсом и релятивистской энергией. 
    \\end{itemize}
    Обязательно подпишите все физические величины. 
''')
@variant.arg(q1=['релятивистского замедления времени', 'релятивистского сжатия'])
@variant.arg(q2=['классической полной механической энергии тела', 'классического импульса'])
@variant.arg(q3=['релятивистской энергии тела', 'релятивистского импульса тела'])
@variant.arg(q4=['релятивистской кинетической энергии', 'энергии покоя тела'])
class Theory02(variant.VariantTask):
    pass



@variant.solution_space(80)
@variant.text('''
    {what} движется со скоростью $0{,}{percent}\,c$, где $c$~--- скорость света в вакууме.
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
    {E_kin_L:L:s} &= E - E_0
        \\implies \\frac{E_kin_L:L:s}{E_0}
            = \\frac E{E_0} - 1
            = \\frac 1{\\sqrt{1 - \\frac{v^2}{c^2}}} - 1
            = \\frac 1{\\sqrt{1 - \\sqr{0.{percent}}}} - 1
            \\approx {E_kin:.3f}.''',
])
@variant.arg(what='Протон/Позитрон/Электрон')
@variant.arg(energy='полной энергии частицы $E$/кинетической энергии частицы $E_\\text{кин.}$')
@variant.arg(percent=['9', '8', '7', '6'])
class E_ratio_from_v_ratio(variant.VariantTask):  # Вишнякова - Базовый курс 4 - задача 1, Vishnyakova_4_1
    def GetUpdate(self, what=None, energy=None, percent=None):
        share = float('0.' + percent)
        E_share = 1. / ((1. - share ** 2) ** 0.5)
        return dict(
            E=E_share,
            E_kin=E_share - 1,
            E_kin_L='E_{\\text{кин}} = 1',
        )


@variant.text('''
    Полная энергия релятивистской частицы в {n_word} больше её энергии покоя.
    Найти скорость этой частицы: в долях $c$ и численное значение. Скорость света в вакууме {Consts.c:Task:e}.
''')
@variant.solution_space(80)
@variant.arg(n__n_word=n_times(3, 4, 5, 6))
@variant.answer_align([
    'E &= \\frac{E_0}{\\sqrt{1 - \\frac{v^2}{c^2}}}'
    '\\implies \\sqrt{1 - \\frac{v^2}{c^2}} = \\frac{E_0}{E}'
    '\\implies \\frac{v^2}{c^2} = 1 - \\sqr{\\frac{E_0}{E}}'
    '\\implies v = c \\sqrt{1 - \\sqr{\\frac{E_0}{E}}} \\approx {share:.3f}c \\approx {v:V}.',
])
@variant.is_one_arg
class Vishnyakova_4_2(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        share = (1 - (1 / a.n) ** 2) ** 0.5
        v = Consts.c * share
        return dict(
            share=share,
            v=v,
        )


@variant.text('''
    Кинетическая энергия релятивистской частицы в {n_word} больше её энергии покоя.
    Найти скорость этой частицы. Скорость света в вакууме {Consts.c:Task:e}.
''')
@variant.solution_space(80)
@variant.arg(n__n_word=n_times(3, 4, 5, 6))
@variant.answer_align([
    'E &= E_0 + {E_kin:L}',
    'E &= \\frac{E_0}{\\sqrt{1 - \\frac{v^2}{c^2}}}'
    '\\implies \\sqrt{1 - \\frac{v^2}{c^2}} = \\frac{E_0}{E}'
    '\\implies \\frac{v^2}{c^2} = 1 - \\sqr{\\frac{E_0}{E}} \\implies',
    '\\implies &v = c \\sqrt{1 - \\sqr{\\frac{E_0}{E}}} = c \\sqrt{1 - \\sqr{\\frac{E_0}{E_0 + {E_kin:L} }}} '
    '= c \\sqrt{1 - \\frac 1 {\\sqr{ 1 + \\frac{E_kin:L:s}{E_0} }} }'
    '\\approx {share:.3f}c \\approx {v:V}.',
])
@variant.is_one_arg
class Vishnyakova_4_2_kin(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        share = (1 - 1 / (1 + a.n) ** 2) ** 0.5
        v = Consts.c * share
        return dict(
            share=share,
            v=v,
            E_kin='E_{\\text{кин}} = 1',
        )



@variant.solution_space(100)
@variant.text('''
    {what} движется со скоростью $0{,}{percent}\,c$, где $c$~--- скорость света в вакууме.
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
class E_P_from_v_ratio(variant.VariantTask):  # Вишнякова - Базовый курс 4._ - задача 3, Vishnyakova_4_3
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
        p = m * c * share * gamma

        return dict(
            E=E.SetLetter('E').IncPrecision(1),
            E_kin=E_kin.SetLetter('E_{\\text{кин}}').IncPrecision(1),
            p=p.SetLetter('p').IncPrecision(1),
            m=m,
        )


@variant.text('''
    Кинетическая энергия частицы космических лучей в {n_word} превышает её энергию покоя.
    Определить отношение скорости частицы к скорости света.
''')
@variant.solution_space(80)
@variant.arg(n__n_word=n_times(3, 4, 5, 6))
@variant.answer_align([
    'E &= E_0 + {E_kin:L}',
    'E &= \\frac{E_0}{\\sqrt{1 - \\frac{v^2}{c^2}}}'
    '\\implies \\sqrt{1 - \\frac{v^2}{c^2}} = \\frac{E_0}{E}'
    '\\implies \\frac{v^2}{c^2} = 1 - \\sqr{\\frac{E_0}{E}} \\implies',
    '\\implies \\frac vc &= \\sqrt{1 - \\sqr{\\frac{E_0}{E}}} = \\sqrt{1 - \\sqr{\\frac{E_0}{E_0 + {E_kin:L} }}} '
    '\\approx {share:.3f}.',
])
@variant.is_one_arg
class Vishnyakova_4_4(variant.VariantTask):  # see Vishnyakova_4_2_kin
   def GetUpdateOneArg(self, a):
        share = (1 - 1 / (1 + a.n) ** 2) ** 0.5
        return dict(
            share=share,
            E_kin='E_{\\text{кин}} = 1',
        )


@variant.text('''
    Некоторая частица, пройдя ускоряющую разность потенциалов, приобрела импульс {p:V:e}.
    Скорость частицы стала равной {v:V:e}. Найти массу частицы.
''')
@variant.solution_space(80)
@variant.arg(p='3/3.5/3.8/4.2 10**{-19} кг м /с')
@variant.arg(v='1.5/1.8/2.0/2.4 10**8 м/с')
@variant.answer_short(
    'p = \\frac{ mv }{\\sqrt{1 - \\frac{v^2}{c^2} }}'
    '\\implies m = \\frac pv \\sqrt{1 - \\frac{v^2}{c^2}}'
    '= \\frac {p:V:s}{v:V:s} \\sqrt{1 - \\sqr{\\frac{v:V:s}{Consts.c:V:s}} } \\approx {m:V}.'
)
@variant.is_one_arg
class Vishnyakova_4_5(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        r = (a.v / Consts.c).SI_Value
        m = a.p / a.v * float(1 - r ** 2) ** 0.5
        return dict(
            m=m.IncPrecision(1),
        )



@variant.solution_space(80)
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
    = {c:V} * \\sqrt{1 - \\sqr{\\frac {l_0 - 0.{percent}l_0}{l_0}}}
    = {c:V} * \\sqrt{1 - \\sqr{1 - 0.{percent}}} \\approx ''',
    '''
    &\\approx {answerShare:.3f}c
    \\approx {speed:V}
    \\approx {kmch:V}.''',
])
@variant.arg(what=['км/ч', 'м/с', 'долях скорости света'])
@variant.arg(percent=['50', '30', '10'])
class beta_from_l_reduction(variant.VariantTask):  # Вишнякова - Базовый курс 4._ - задача 6, Vishnyakova_4_6
    def GetUpdate(self, what=None, percent=None):
        c = Consts.c
        share = float('0.' + percent)
        answerShare = Decimal((1. - (1. - share) ** 2) ** 0.5)
        speed = c * answerShare
        return dict(
            answerShare=answerShare,
            c=c,
            speed=speed,
            kmch=speed.As('км / ч'),
        )


@variant.text('''
    Стержень движется в продольном направлении с постоянной скоростью относительно инерциальной системы отсчёта.
    При каком значении скорости (в долях скорости света) длина стержня в этой системе отсчёта
    будет в {n} раза меньше его собственной длины?
''')
@variant.solution_space(80)
@variant.arg(n='1.25/1.5/1.67/2.5/3/4')
@variant.answer_short(
    'l_0 = \\frac l{\\sqrt{1 - \\frac{v^2}{c^2}}}'
    '\\implies \\sqrt{1 - \\frac{v^2}{c^2}} = \\frac{ l }{ l_0 }'
    '\\implies \\frac v c = \\sqrt{1 - \\sqr{\\frac{ l }{ l_0 }}} \\approx {r:.3f}.'
)
@variant.is_one_arg
class Vishnyakova_4_7(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            r = (1 - (1 / float(a.n)) ** 2) ** 0.5,
        )


@variant.text('''
    Какую скорость должно иметь движущееся тело, чтобы его продольные размеры уменьшились в {n_word}?
    Скорость света {Consts.c:Task:e}.
''')
@variant.solution_space(80)
@variant.arg(n__n_word=n_times(2, 3, 4, 5, 6))
@variant.answer_short(
    'l_0 = \\frac l{\\sqrt{1 - \\frac{v^2}{c^2}}}'
    '\\implies \\sqrt{1 - \\frac{v^2}{c^2}} = \\frac{ l }{ l_0 }'
    '\\implies v = c\\sqrt{1 - \\sqr{\\frac{ l }{ l_0 }}} \\approx {v:V}.'
)
@variant.is_one_arg
class Vishnyakova_4_8(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        r = (1 - (1 / float(a.n)) ** 2) ** 0.5
        return dict(
            v=Consts.c * r,
        )


@variant.text('''
    Время жизни мюона, измеренное наблюдателем, относительно которого мюон покоился, равно $\\tau_0$
    Какое расстояние пролетит мюон в системе отсчёта, относительно которой он движется со скоростью $v$,
    сравнимой со скоростью света в вакууме $c$?
''')
@variant.solution_space(80)
@variant.no_args
@variant.answer_short('\\ell = v\\tau = v \\frac{\\tau_0}{\\sqrt{1 - \\frac{v^2}{c^2}}}')
class Vishnyakova_4_9(variant.VariantTask):
    pass


@variant.text('''
    Если $c$ — скорость света в вакууме, то с какой скоростью должна двигаться нестабильная частица относительно наблюдателя,
    чтобы её время жизни было в {n_word} больше, чем у такой же, но покоящейся относительно наблюдателя частицы?
''')
@variant.solution_space(80)
@variant.arg(n__n_word=n_times(3, 4, 5, 6, 7, 8, 9, 10))
@variant.answer_short(
    '\\tau = \\frac{\\tau_0}{\\sqrt{1 - \\frac{v^2}{c^2}}}'
    '\\implies \\sqrt{1 - \\frac{v^2}{c^2}} = \\frac{\\tau_0}{\\tau}'
    '\\implies v = c\\sqrt{1 - \\sqr{\\frac{\\tau_0}{\\tau}} } \\approx {v:V}.'
)
@variant.is_one_arg
class Vishnyakova_4_10(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        r = (1 - (1 / float(a.n)) ** 2) ** 0.5
        return dict(
            v=Consts.c * r,
        )


@variant.text('''
    Время жизни нестабильной частицы, входящего в состав космических лучей, измеренное земным наблюдателем,
    относительно которого частица двигалась со скоростью, составляющей {percent}\\% скорости света в вакууме, оказалось равным {t:V:e}.
    Каково время жизни частицы, покоящейся относительно наблюдателя?
''')
@variant.solution_space(80)
@variant.arg(percent=['85', '75', '65'])
@variant.arg(t='3.7/4.8/5.3/6.4/7.1 мкс')
@variant.answer_short(
    't = \\frac{t_0}{\\sqrt{1 - \\frac{v^2}{c^2}}}'
    '\\implies t_0 = t\\sqrt{1 - \\frac{v^2}{c^2}} \\approx {t0:V}.'
)
@variant.is_one_arg
class Vishnyakova_4_11(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        r = float(a.percent) / 100
        return dict(
            t0=a.t * (1 - r ** 2) ** 0.5,
        )


@variant.text('''
    Частица увеличила в ускорителе свою скорость с $0{,}{percent1}c$ до $0{,}{percent2}c$.
    Во сколько раз выросла её кинетическая энергия?
''')
@variant.solution_space(120)
@variant.arg(percent1=['01', '02', '03', '04', '05'])
@variant.arg(percent2=['50', '60', '70', '80', '90'])
@variant.answer_align([
    'E_{\\text{кин.}} &= E - E_0 = \\frac{mc^2}{\\sqrt{1 - \\frac{v^2}{c^2}}} - mc^2 = '
    'mc^2\\cbr{ \\frac1{\\sqrt{1 - \\frac{v^2}{c^2} }} - 1}.',
    '\\frac{E_{\\text{кин. 2}}}{E_{\\text{кин. 1}}} &= \\frac{\\frac1{\\sqrt{1 - \\frac{v_2^2}{c^2} }} - 1}{\\frac1{\\sqrt{1 - \\frac{v_1^2}{c^2} }} - 1}'
    '\\approx {r:.2f}'
])
@variant.is_one_arg
class Gelfgat_9_18(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        r1 = float(a.percent1) / 100
        r2 = float(a.percent2) / 100
        return dict(
            r=(1 / (1 - r2 ** 2) ** 0.5 - 1) / (1 / (1 - r1 ** 2) ** 0.5 - 1),
        )


# 9.1.@2 На ракете, скорость которой относительно Земли равна 0,9, 9.2. 
# 9.3. 9.4. 
# 9.5. 
# 9.6. 
# 9.7. 
# 9.8. 
# 9.9. 
# включен прожектор. Какова скорость распространения света относительно Земли, если луч прожектора направлен:
#      а) в направлении движения ракеты;
#      ,) в противоположную сторону?
# С ракеты, скорость которой относительно Земли равна 0,9с, выпустили вперед и назад снаряды со скоростью 0,5с относительно ракеты. Какова скорость снарядов относительно Земли?
# Какова энергия покоя | глюбого вещества?
# Найдите полную энергию космического аппарата с массой покоя 10 т, движущегося со скоростью 0,9. 
# Wolpe Ven ce dk) al
# Две частицы удаляются от наблюдателя со скоростями 0,7с в противоположные стороны. Какова скорость частиц друг относительно друга?
# Полная энергия тела в 1,5 раза превышает энергию покоя этого тела. Во сколько раз кинетическая энергия тела отличается от энергии покоя?
# При какой скорости движения кинетическая энергия тела в 3 раза превышает энергию покоя?
# Найдите кинетическую энергию космического аппарата с массой покоя 10 т, движущегося со скоростью 0,9с. 
# На сколько изменяется масса покоя 10 кг воды при охлаждении
# от 100 °С до 0 °С?
# 9.10. На сколько изменяется масса покоя 1 кг льда при плавлении?
# 9.11. На сколько изменяется масса покоя пружины с жесткостью 5 кН/м при сжатии на 10 см?

# 9.12. В результате ядерной реакции масса покоя вещества уменьшается на 0,1%. Какая энергия выделяется в результате использования 1 гядерного топлива?

# 9.13”. Ракета движется относительно Земли со скоростью 0,6с. Какова длина находящегося в ракете метрового стержня в системе отсчета, связанной с Землей, если стержень расположен:
#      а) параллельно курсу ракеты;
#      6) перпендикулярно курсу ракеты?

# 9.14. При какой скорости движения длина стержня «сокращается» втрое?
# 9.15. Какое время пройдет на Земле, если в ракете, движущейся относительно Земли со скоростью 0,999с, пройдет 1 год?
# 9.16. Какое среднее расстояние проходят от рождения до распада частицы, среднее время жизни которых (в «собственной» системе отсчета) 3 мкс, движущиеся со скоростью 0,86?
# 9.17. Выразите кинетическую энергию релятивистской частицы через ее массу покоя и импульс. 
# 9.18. Частица движется со скоростью 0,04с. Во сколько раз увеличится ее кинетическая энергия, если скорость движения увеличится:
#     а) в 2 раза;
#     ,) в 20 раз?
# 9.19. При какой скорости движения кинетическая энергия протона равна:
#      а) энергии покоя протона;
#      б) энергии покоя электрона?
# 9.20. Найдите импульс протона, у которого кинетическая энергия вдвое больше энергии покоя. 
# 9.21. Какую скорость приобретает электрон, пройдя ускоряющую разность потенциалов И = 500 кВ? Какую скорость приобретает протон, пройдя такую же ускоряющую разность потенциалов?
# 9.22. Кинетическая энергия движущегося электрона равна кинетической энергии автомобиля массой |т при скорости 72 км/ч. На сколько скорость электрона меньше скорости света в вакууме?
# 9.23. Солнечная постоянная (плотность потока излучения Солнца вблизи верхней границы атмосферы Земли) равна 1,36 кВт/м2. На какую величину ежесекундно уменьшается масса Солнца вследствие излучения?

