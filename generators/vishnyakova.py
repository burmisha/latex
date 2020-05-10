# -*- coding: utf-8 -*-

import variant
from value import UnitValue

import logging
log = logging.getLogger(__name__)


@variant.solution_space(150)
@variant.text(u'''
    {what} движется со скоростью $0{{,}}{percent}\,c$, где $c$~--- скорость света в вакууме.
    Каково при этом отношение {energy} к его энергии покоя $E_0$?
''')
@variant.answer(u'''\\begin{{align*}}
    E &= \\frac{{E_0}}{{\\sqrt{{1 - \\frac{{v^2}}{{c^2}}}}}}
        \\implies \\frac{{E}}{{E_0}}
            = \\frac 1{{\\sqrt{{1 - \\frac{{v^2}}{{c^2}}}}}}
            = \\frac 1{{\\sqrt{{1 - \\sqr{{0{{,}}{percent}}}}}}}
            \\approx {E:.3f}
    \\\\
    E_{{\\text{{кин}}}} &= E - E_0
        \\implies \\frac{{E_{{\\text{{кин}}}}}}{{E_0}}
            = \\frac{{E}}{{E_0}} - 1
            = \\frac 1{{\\sqrt{{1 - \\frac{{v^2}}{{c^2}}}}}} - 1
            = \\frac 1{{\\sqrt{{1 - \\sqr{{0{{,}}{percent}}}}}}} - 1
            \\approx {E_kin:.3f}
\\end{{align*}}''')
@variant.args(
    what=[u'Протон', u'Позитрон'],
    energy=[u'полной энергии частицы $E$', u'кинетической энергии частицы $E_{\\text{кин}}$'],
    percent=['9', '8', '7', '6'],
)
class BK_4_01(variant.VariantTask):
    def GetUpdate(self, energy=None, percent=None, **kws):
        share = float('0.' + percent)
        return {
            'E':  1. / ((1. - share ** 2) ** 0.5),
            'E_kin': 1. / ((1. - share ** 2) ** 0.5) - 1,
        }


@variant.solution_space(150)
@variant.text(u'''
    {what} движется со скоростью $0{{,}}{percent}\,c$, где $c$~--- скорость света в вакууме.
    Определите его {x} (в ответе приведите формулу и укажите численное значение).
''')
@variant.answer(u'''\\begin{{align*}}
    E &= \\frac{{ mc^2 }}{{ \\sqrt{{ 1 - \\frac{{v^2}}{{c^2}} }} }}
        \\approx \\frac{{
            {m:Value|cdot} {Consts.c:Value|sqr}
        }}{{
            \\sqrt{{1 - 0{{,}}{percent}^2}}
        }} \\approx {E:Value},
    \\\\
    E_{{\\text{{кин}}}} &= \\frac{{mc^2}}{{\\sqrt{{1 - \\frac{{v^2}}{{c^2}}}}}} - mc^2
        = mc^2 \\cbr{{
            \\frac 1{{
                \\sqrt{{1 - \\frac{{v^2}}{{c^2}} }}
            }} - 1
        }}
        \\approx
        \\\\
        &\\approx \\cbr{{
            {m:Value|cdot} {Consts.c:Value|sqr}
        }} \\cdot \\cbr{{
            \\frac 1{{ \\sqrt{{ 1 - 0{{,}}{percent}^2 }} }} - 1
        }}
        \\approx {E_kin:Value},
    \\\\
    p &= \\frac{{
            mv
        }}{{
            \\sqrt{{1 - \\frac{{v^2}}{{c^2}} }}
        }}
        \\approx \\frac{{
            {m:Value|cdot} 0{{,}}{percent} {Consts.c:Value}
        }}{{
            1 - 0{{,}}{percent}^2
        }}
        \\approx {p:Value}.
\\end{{align*}}''')
@variant.args(
    what=[u'Протон', u'Электрон'],
    x=[u'полную энергию', u'кинетическую энергию', u'импульс'],
    percent=['85', '75', '65'],
)
class BK_4_03(variant.VariantTask):
    def GetUpdate(self, what=None, percent=None, Consts=None, **kws):
        m = {
            u'Протон': UnitValue(u'm = 1.67 10^-27 кг'),
            u'Электрон': UnitValue(u'm = 9.1 10^-31 кг'),
        }[what]
        share = float('0.' + percent)
        return {
            'E': u'{value:.2f} 10^{power} Дж'.format(
                value=m.Value * Consts.c.Value ** 2 / ((1. - share ** 2) ** 0.5),
                power=m.Power + 2 * Consts.c.Power,
            ),
            'E_kin': u'{value:.2f} 10^{power} Дж'.format(
                value=m.Value * Consts.c.Value ** 2 * (1. / ((1. - share ** 2) ** 0.5) - 1),
                power=m.Power + 2 * Consts.c.Power,
            ),
            'p': u'{value:.2f} 10^{power} кг м / с'.format(
                value=m.Value * Consts.c.Value / ((1. - share ** 2) ** 0.5),
                power=m.Power + Consts.c.Power,
            ),
            'm': m,
        }



@variant.solution_space(150)
@variant.text(u'''
    При какой скорости движения (в {what}) релятивистское сокращение длины движущегося тела
    составит {percent}\\%?
''')
@variant.answer(u'''\\begin{{align*}}
    l_0 &= \\frac{{l}}{{\\sqrt{{1 - \\frac {{v^2}}{{c^2}}}}}}
    \\implies 1 - \\frac {{v^2}}{{c^2}} = \\sqr{{\\frac l{{l_0}}}}
    \\implies \\frac v c = \\sqrt{{1 - \\sqr{{\\frac l{{l_0}}}}}} \\implies \\\\
    \\implies v &= c\\sqrt{{1 - \\sqr{{\\frac l{{l_0}}}}}}
    = {Consts.c:Value} \\cdot \\sqrt{{1 - \\sqr{{\\frac {{l_0 - 0{{,}}{percent}l_0}} {{l_0}} }} }}
    = {Consts.c:Value} \\cdot \\sqrt{{1 - \\sqr{{1 - 0{{,}}{percent} }} }} \\approx \\\\
    &\\approx {answerShare:.3f}c
    \\approx {speed:Value}
    \\approx {kmch:Value}.
\\end{{align*}}''')
@variant.args(
    what=[u'км/ч', u'м/с', u'долях скорости света'],
    percent=['50', '30', '10'],
)
class BK_4_06(variant.VariantTask):
    def GetUpdate(self, percent=None, Consts=None, **kws):
        share = float('0.' + percent)
        answerShare = (1. - (1. - share) ** 2) ** 0.5
        return {
            'answerShare': answerShare,
            'speed': u'%.3f 10^8 м / с' % (answerShare * Consts.c.Value),
            'kmch': u'%.3f 10^8 км / ч' % (3.6 * answerShare * Consts.c.Value),
        }


@variant.solution_space(150)
@variant.text(u'''
    При переходе электрона в атоме с одной стационарной орбиты на другую
    излучается фотон с энергией ${E:Value}$.
    Какова длина волны этой линии спектра?
    Постоянная Планка ${Consts.h:Task}$, скорость света ${Consts.c:Task}$.
''')
@variant.answer(u'''$
    E = h\\nu = h \\frac c\\lambda
    \\implies \\lambda = \\frac{{hc}}{{E}}
        = \\frac{{
            {Consts.h:Value|s|cdot}{Consts.c:Value|s}
        }}{E:Value|s}
        = {lmbd:Value}.
$''')
@variant.args(
    E=[u'E = %s 10^{-19} Дж' % E for E in [u'4.04', u'5.05', u'2.02', u'7.07', u'1.01', u'0.55']],
)
class BK_52_01(variant.VariantTask):
    def GetUpdate(self, E=None, Consts=None, **kws):
        return {
            'lmbd': u'{value:.2f} 10^{power} м'.format(
                value=Consts.h.Value * Consts.c.Value / E.Value,
                power=Consts.h.Power + Consts.c.Power - E.Power,
            ),
        }


@variant.solution_space(150)
@variant.text(u'''
    Излучение какой длины волны поглотил атом водорода, если полная энергия в атоме увеличилась на ${E:Value}$?
    Постоянная Планка ${Consts.h:Task}$, скорость света ${Consts.c:Task}$.
''')
@variant.answer(u'''$
    E = h\\nu = h \\frac c\\lambda
    \\implies \\lambda = \\frac{{hc}}{{E}}
        = \\frac{{
            {Consts.h:Value|s|cdot}{Consts.c:Value|s}
        }}{E:Value|s}
        = {lmbd:Value}.
$''')
@variant.args(
    E=[u'E = %d 10^{-19} Дж' % E for E in [2, 3, 4, 6]],
)
class BK_52_02(variant.VariantTask):
    def GetUpdate(self, E=None, Consts=None, **kws):
        return {
            'lmbd': u'{value:.2f} 10^{power} м'.format(
                value=Consts.h.Value * Consts.c.Value / E.Value,
                power=Consts.h.Power + Consts.c.Power - E.Power,
            ),
        }


@variant.solution_space(150)
@variant.text(u'''
    Сделайте схематичный рисунок энергетических уровней атома водорода
    и отметьте на нём первый (основной) уровень и последующие.
    Сколько различных длин волн может испустить атом водорода,
    находящийся в {n}-м возбуждённом состоянии?
    Отметьте все соответствующие переходы на рисунке и укажите,
    при каком переходе (среди отмеченных) {what} излучённого фотона {minmax}.
''')
@variant.answer(u'''$N = {N}$, {answer}''')
@variant.args(
    n=[3, 4, 5],
    what=[u'энергия', u'частота', u'длина волны'],
    minmax=[u'минимальна', u'максимальна'],
)
class BK_52_07(variant.VariantTask):
    def GetUpdate(self, n=None, what=None, minmax=None, **kws):
        whatSign = {
            u'энергия': 1,
            u'частота': 1,
            u'длина волны': -1,
        }[what]
        minmaxSign = {
            u'минимальна': -1,
            u'максимальна': 1,
        }[minmax]
        answer = u'самая длинная линия' if whatSign == minmaxSign else u'самая короткая линия'
        return {
            'N': n * (n - 1) / 2,
            'answer': answer,
        }


@variant.solution_space(150)
@variant.text(u'''
    Какая доля (от начального количества) радиоактивных ядер {what} через время,
    равное {when} периодам полураспада? Ответ выразить в процентах.
''')
@variant.answer_align([
    u'''N &= N_0 \\cdot 2^{ - \\frac t{ T_{ 1/2 } } } \\implies 
    \\frac N{ N_0 } = 2^{ - \\frac t{ T_{ 1/2 } } }
    = 2^{ -{t} } \\approx {N_value:.2f} \\approx {N_percent:.0f}\\%''',
    u'''N_\\text{{ост.}} &= N_0 - N = N_0 - N_0 \\cdot 2^{ - \\frac t{ T_{ 1/2 } } } 
    = N_0\\cbr{ 1 - 2^{ - \\frac t{ T_{ 1/2 } } } } \\implies 
    \\frac { N_\\text{ ост. } }{ N_0 } = 1 - 2^{ - \\frac t{ T_{ 1/2 } } }
    = 1 - 2^{ -{t} } \\approx {N_left_value:.2f} \\approx {N_left_percent:.0f}\\%''',
])
@variant.args(
    what=[u'распадётся', u'останется'],
    when=[u'двум', u'трём', u'четырём'],
)
class BK_53_01(variant.VariantTask):
    def GetUpdate(self, what=None, when=None, **kws):
        t = {
            u'двум': 2,
            u'трём': 3,
            u'четырём': 4,
        }[when]
        share = 2. ** (-t)
        left = 1. - share
        return dict(
            t=t,
            N_value=share,
            N_percent=share * 100,
            N_left_value=left,
            N_left_percent=left * 100,
        )


@variant.solution_space(150)
@variant.text(u'''
    Сколько процентов ядер радиоактивного железа \ce{{^{{59}}Fe}}
    останется через ${t:Value}$, если период его полураспада составляет ${T:Value}$?
''')
@variant.answer_align([
    u'''N_\\text{{ост.}} &= N_0 - N = N_0 - N_0 \\cdot 2^{ - \\frac t{ T_{ 1/2 } } } 
    = N_0\\cbr{ 1 - 2^{ - \\frac t{ T_{ 1/2 } } } } \\implies''',
    u'''
    \\implies 
    \\frac { N_\\text{ ост. } }{ N_0 } &= 1 - 2^{ - \\frac t{ T_{ 1/2 } } }
     = 1 - 2^{ - \\frac {t:Value|s}{T:Value|s} }
    \\approx {share} \\approx {percent}\\%''',
])
@variant.args(
    t=[u't = %s суток' % t for t in [u'91.2', u'136.8', u'182.4']],
    T=[u'T = 45.6 суток'],
)
class BK_53_02(variant.VariantTask):
    def GetUpdate(self, t=None, T=None, **kws):
        share = 1. - 2. ** (-t.Value / T.Value)
        return dict(
            share=share,
            percent=share * 100,
        )


@variant.solution_space(150)
@variant.text(u'''
    За ${t:Value}$ от начального количества ядер радиоизотопа осталась {how}.
    Каков период полураспада этого изотопа (ответ приведите в сутках)?
    Какая ещё доля (также от начального количества) распадётся, если подождать ещё столько же?
''')
@variant.answer_align([
    u'''
        N &= N_0 \\cdot 2^{ - \\frac t{ T_{ 1/2 } } } 
        \\implies \\frac N{ N_0 } = 2^{ - \\frac t{ T_{ 1/2 } } } 
        \\implies \\frac 1{num} = 2^{ - \\frac {t:Value|s}{ T_{ 1/2 } } } 
        \\implies {log_num} = \\frac {t:Value|s}{ T_{ 1/2 } }
        \\implies T_{ 1/2 } = \\frac {t:Value|s}{log_num} \\approx {T:Value}.
    ''',
    u'''
        \\delta &= \\frac{ N(t) }{ N_0 } - \\frac{ N(2t) }{ N_0 }
        = 2^{ - \\frac t{ T_{ 1/2 } } } - 2^{ - \\frac { 2t }{ T_{ 1/2 } } } 
        = 2^{ - \\frac t{ T_{ 1/2 } } }\\cbr{ 1 - 2^{ - \\frac { t }{ T_{ 1/2 } } } }
        = \\frac 1{num}\\cdot \\cbr{ 1 - \\frac 1{num} } \\approx {res:.3f}
    '''
])
@variant.args(
    how=[u'четверть', u'одна восьмая', u'половина', u'одна шестнадцатая'],
    t=[u'%d суток' % t for t in [2, 3, 4, 5]],
)
class BK_53_03(variant.VariantTask):
    def GetUpdate(self, how=None, t=None, **kws):
        num, log_num = {
            u'четверть': (4, 2),
            u'одна восьмая': (8, 3),
            u'половина': (2, 1),
            u'одна шестнадцатая': (16, 4),
        }[how]
        return dict(
            num=num,
            log_num=log_num,
            T=u'%.2f суток' % (t.Value / log_num),
            res=1. / num * (1 - 1./num),
        )


@variant.solution_space(150)
@variant.text(u'''
    Энергия связи ядра {element} равна ${E:Value}$.
    Найти дефект массы этого ядра. Ответ выразите в а.е.м. и кг. Скорость света ${Consts.c:Task}$.
''')
@variant.args({
    # https://www.calc.ru/Energiya-Svyazi-Nekotorykh-Yader.html
    ('element', 'E'): [
        (u'дейтерия \\ce{^{2}_{1}H} (D)', u'E = 2.22 МэВ'),
        (u'трития \\ce{^{3}_{1}H} (T)', u'E = 8.48 МэВ'),
        (u'гелия \\ce{^{3}_{2}He}', u'E = 7.72 МэВ'),
        (u'гелия \\ce{^{3}_{2}He}', u'E = 28.29 МэВ'),
        (u'лития \\ce{^{6}_{3}Li}', u'E = 31.99 МэВ'),
        (u'лития \\ce{^{7}_{3}Li}', u'E = 39.2 МэВ'),
        (u'бериллия \\ce{^{9}_{4}Be}', u'E = 58.2 МэВ'),
        (u'бора \\ce{^{10}_{5}B}', u'E = 64.7 МэВ'),
        (u'бора \\ce{^{11}_{5}B}', u'E = 76.2 МэВ'),
        (u'углерода \\ce{^{12}_{6}C}', u'E = 92.2 МэВ'),
        (u'углерода \\ce{^{13}_{6}C}', u'E = 97.1 МэВ'),
        (u'азота \\ce{^{14}_{7}N}', u'E = 104.7 МэВ'),
        (u'азота \\ce{^{14}_{7}N}', u'E = 115.5 МэВ'),
        (u'кислорода \\ce{^{16}_{8}O}', u'E = 127.6 МэВ'),
        (u'кислорода \\ce{^{17}_{8}O}', u'E = 131.8 МэВ'),
        (u'кислорода \\ce{^{18}_{8}O}', u'E = 139.8 МэВ'),
    ],
})
class BK_53_12(variant.VariantTask):
    pass
