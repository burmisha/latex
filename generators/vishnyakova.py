# -*- coding: utf-8 -*-

import generators.variant as variant

import logging
log = logging.getLogger(__name__)


@variant.solution_space(150)
@variant.text('''
    {what} движется со скоростью $0.{percent}\,c$, где $c$~--- скорость света в вакууме.
    Каково при этом отношение {energy} к его энергии покоя $E_0$?
''')
@variant.answer_align([
    '''E &= \\frac{ E_0 }{ \\sqrt{ 1 - \\frac{ v^2 }{ c^2 } } }
        \\implies \\frac{ E }{ E_0 }
            = \\frac 1{ \\sqrt{ 1 - \\frac{ v^2 }{ c^2 } } }
            = \\frac 1{ \\sqrt{ 1 - \\sqr{ 0.{percent} } } }
            \\approx {E:.3f},
    ''',
    '''
    E_{ \\text{ кин } } &= E - E_0
        \\implies \\frac{ E_{ \\text{ кин } } }{ E_0 }
            = \\frac{ E }{ E_0 } - 1
            = \\frac 1{ \\sqrt{ 1 - \\frac{ v^2 }{ c^2 } } } - 1
            = \\frac 1{ \\sqrt{ 1 - \\sqr{ 0.{percent} } } } - 1
            \\approx {E_kin:.3f}.
    ''',
])
@variant.arg(what=['Протон', 'Позитрон'])
@variant.arg(energy=['полной энергии частицы $E$', 'кинетической энергии частицы $E_{ \\text{ кин } }$'])
@variant.arg(percent=['9', '8', '7', '6'])
class BK_4_01(variant.VariantTask):
    def GetUpdate(self, energy=None, percent=None, **kws):
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
    '''E &= \\frac{ mc^2 }{  \\sqrt{ 1 - \\frac{ v^2 }{ c^2 } } }
        \\approx \\frac{ {m:Value|cdot} {Consts.c:Value|sqr} }{ \\sqrt{ 1 - 0.{percent}^2 } }
        \\approx {E:Value},
    ''',
    '''
    E_{ \\text{ кин } } &= \\frac{ mc^2 }{ \\sqrt{ 1 - \\frac{ v^2 }{ c^2 } } } - mc^2
        = mc^2 \\cbr{ \\frac 1{ \\sqrt{ 1 - \\frac{ v^2 }{ c^2 } } } - 1 } \\approx''',
    '''
        &\\approx \\cbr{ {m:Value|cdot} {Consts.c:Value|sqr} }
        \\cdot \\cbr{ \\frac 1{ \\sqrt{ 1 - 0.{percent}^2 } } - 1 }
        \\approx {E_kin:Value},
    ''',
    '''
    p &= \\frac{ mv }{ \\sqrt{ 1 - \\frac{ v^2 }{ c^2 } } }
        \\approx \\frac{ {m:Value|cdot} 0.{percent} \\cdot {Consts.c:Value} }{ \\sqrt{ 1 - 0.{percent}^2 } }
        \\approx {p:Value}.
    '''
])
@variant.arg(what=['Протон', 'Электрон'])
@variant.arg(x=['полную энергию', 'кинетическую энергию', 'импульс'])
@variant.arg(percent=['85', '75', '65'])
class BK_4_03(variant.VariantTask):
    def GetUpdate(self, what=None, percent=None, Consts=None, **kws):
        m = {
            'Протон': Consts.m_p,
            'Электрон': Consts.m_e,
        }[what]
        share = float('0.' + percent)
        return dict(
            E='{value:.1f} 10^{power} Дж'.format(
                value=m.Value * Consts.c.Value ** 2 / ((1. - share ** 2) ** 0.5),
                power=m.Power + 2 * Consts.c.Power,
            ),
            E_kin='{value:.1f} 10^{power} Дж'.format(
                value=m.Value * Consts.c.Value ** 2 * (1. / ((1. - share ** 2) ** 0.5) - 1),
                power=m.Power + 2 * Consts.c.Power,
            ),
            p='{value:.1f} 10^{power} кг м / с'.format(
                value=m.Value * share * Consts.c.Value / ((1. - share ** 2) ** 0.5),
                power=m.Power + Consts.c.Power,
            ),
            m=m,
        )


@variant.solution_space(150)
@variant.text('''
    При какой скорости движения (в {what}) релятивистское сокращение длины движущегося тела
    составит {percent}\\%?
''')
@variant.answer_align([
    '''l_0 &= \\frac{ l }{ \\sqrt{ 1 - \\frac { v^2 }{ c^2 } } }
    \\implies 1 - \\frac{ v^2 }{ c^2 } = \\sqr{ \\frac l{ l_0 } }
    \\implies \\frac v c = \\sqrt{ 1 - \\sqr{ \\frac l{ l_0 } } } \\implies
    ''',
    '''
    \\implies v &= c\\sqrt{ 1 - \\sqr{ \\frac l{ l_0 } } }
    = {Consts.c:Value} \\cdot \\sqrt{ 1 - \\sqr{ \\frac { l_0 - 0.{percent}l_0 }{ l_0 } } }
    = {Consts.c:Value} \\cdot \\sqrt{ 1 - \\sqr{ 1 - 0.{percent} } } \\approx ''',
    '''
    &\\approx {answerShare:.3f}c
    \\approx {speed:Value}
    \\approx {kmch:Value}.''',
])
@variant.arg(what=['км/ч', 'м/с', 'долях скорости света'])
@variant.arg(percent=['50', '30', '10'])
class BK_4_06(variant.VariantTask):
    def GetUpdate(self, percent=None, Consts=None, **kws):
        share = float('0.' + percent)
        answerShare = (1. - (1. - share) ** 2) ** 0.5
        return dict(
            answerShare=answerShare,
            speed='%.3f 10^8 м / с' % (answerShare * Consts.c.Value),
            kmch='%.3f 10^8 км / ч' % (3.6 * answerShare * Consts.c.Value),
        )


@variant.solution_space(150)
@variant.text('''
    При переходе электрона в атоме с одной стационарной орбиты на другую
    излучается фотон с энергией ${E:Value}$.
    Какова длина волны этой линии спектра?
    Постоянная Планка ${Consts.h:Task}$, скорость света ${Consts.c:Task}$.
''')
@variant.answer_short('''
    E = h\\nu = h \\frac c\\lambda
    \\implies \\lambda = \\frac{ hc }{ E }
        = \\frac{ {Consts.h:Value|cdot}{Consts.c:Value|s} }{E:Value|s}
        = {lmbd:Value}.
''')
@variant.arg(E=['E = %s 10^{-19} Дж' % E for E in ['4.04', '5.05', '2.02', '7.07', '1.01', '0.55']])
class BK_52_01(variant.VariantTask):
    def GetUpdate(self, E=None, Consts=None, **kws):
        return dict(
            lmbd='{value:.2f} 10^{power} м'.format(
                value=Consts.h.Value * Consts.c.Value / E.Value,
                power=Consts.h.Power + Consts.c.Power - E.Power,
            ),
        )


@variant.solution_space(150)
@variant.text('''
    Излучение какой длины волны поглотил атом водорода, если полная энергия в атоме увеличилась на ${E:Value}$?
    Постоянная Планка ${Consts.h:Task}$, скорость света ${Consts.c:Task}$.
''')
@variant.answer_short('''
    E = h\\nu = h \\frac c\\lambda
    \\implies \\lambda = \\frac{ hc }{ E }
        = \\frac{ {Consts.h:Value|cdot}{Consts.c:Value|s} }{E:Value|s}
        = {lmbd:Value}.
''')
@variant.arg(E=['E = %d 10^{-19} Дж' % E for E in [2, 3, 4, 6]])
class BK_52_02(variant.VariantTask):
    def GetUpdate(self, E=None, Consts=None, **kws):
        return dict(
            lmbd='{value:.2f} 10^{power} м'.format(
                value=Consts.h.Value * Consts.c.Value / E.Value,
                power=Consts.h.Power + Consts.c.Power - E.Power,
            ),
        )


@variant.solution_space(150)
@variant.text('''
    Сделайте схематичный рисунок энергетических уровней атома водорода
    и отметьте на нём первый (основной) уровень и последующие.
    Сколько различных длин волн может испустить атом водорода,
    находящийся в {n}-м возбуждённом состоянии?
    Отметьте все соответствующие переходы на рисунке и укажите,
    при каком переходе (среди отмеченных) {what} излучённого фотона {minmax}.
''')
@variant.answer_short('N = {N}, \\text{ {answer} }')
@variant.arg(n=[3, 4, 5])
@variant.arg(what__what_sign=[
    ('энергия', 1),
    ('частота', 1),
    ('длина волны', -1),
])
@variant.arg(minmax__minmax_sign=[
    ('минимальна', -1),
    ('максимальна', 1),
])
class BK_52_07(variant.VariantTask):
    def GetUpdate(self, n=None, what=None, minmax=None, what_sign=None, minmax_sign=None, **kws):
        answer = {
            1: 'самая длинная линия',
            -1: 'самая короткая линия',
        }[what_sign * minmax_sign]
        return dict(
            N=n * (n - 1) / 2,
            answer=answer,
        )


@variant.solution_space(150)
@variant.text('''
    Какая доля (от начального количества) радиоактивных ядер {what} через время,
    равное {when} периодам полураспада? Ответ выразить в процентах.
''')
@variant.answer_align([
    '''N &= N_0 \\cdot 2^{ - \\frac t{ T_{ 1/2 } } } \\implies
    \\frac N{ N_0 } = 2^{ - \\frac t{ T_{ 1/2 } } }
    = 2^{ -{t} } \\approx {N_value:.2f} \\approx {N_percent:.0f}\\%''',
    '''N_\\text{ расп. } &= N_0 - N = N_0 - N_0 \\cdot 2^{ - \\frac t{ T_{ 1/2 } } }
    = N_0\\cbr{ 1 - 2^{ - \\frac t{ T_{ 1/2 } } } } \\implies
    \\frac { N_\\text{ расп. } }{ N_0 } = 1 - 2^{ - \\frac t{ T_{ 1/2 } } }
    = 1 - 2^{ -{t} } \\approx {N_left_value:.2f} \\approx {N_left_percent:.0f}\\%''',
])
@variant.arg(what=['распадётся', 'останется'])
@variant.arg(when__t=[
    ('двум', 2),
    ('трём', 3),
    ('четырём', 4),
])
class BK_53_01(variant.VariantTask):
    def GetUpdate(self, what=None, when=None, t=None, **kws):
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
@variant.text('''
    Сколько процентов ядер радиоактивного железа \ce{{^{{59}}Fe}}
    останется через ${t:Value}$, если период его полураспада составляет ${T:Value}$?
''')
@variant.answer_align([
    '''N &= N_0 \\cdot 2^{ - \\frac t{ T_{ 1/2 } } }
    = 2^{ - \\frac {t:Value|s}{T:Value|s} }
    \\approx {share} \\approx {percent}\\%''',
])
@variant.arg(t=['t = %s суток' % t for t in ['91.2', '136.8', '182.4']])
@variant.arg(T=['T = 45.6 суток'])
class BK_53_02(variant.VariantTask):
    def GetUpdate(self, t=None, T=None, **kws):
        share = 2. ** (-t.Value / T.Value)
        return dict(
            share=share,
            percent=share * 100,
        )


@variant.solution_space(150)
@variant.text('''
    За ${t:Value}$ от начального количества ядер радиоизотопа осталась {how}.
    Каков период полураспада этого изотопа (ответ приведите в сутках)?
    Какая ещё доля (также от начального количества) распадётся, если подождать ещё столько же?
''')
@variant.answer_align([
    '''
        N &= N_0 \\cdot 2^{ - \\frac t{ T_{ 1/2 } } }
        \\implies \\frac N{ N_0 } = 2^{ - \\frac t{ T_{ 1/2 } } }
        \\implies \\frac 1{ {num} } = 2^{ - \\frac {t:Value|s}{ T_{ 1/2 } } }
        \\implies {log_num} = \\frac {t:Value|s}{ T_{ 1/2 } }
        \\implies T_{ 1/2 } = \\frac {t:Value|s}{log_num} \\approx {T:Value}.
    ''',
    '''
        \\delta &= \\frac{ N(t) }{ N_0 } - \\frac{ N(2t) }{ N_0 }
        = 2^{ - \\frac t{ T_{ 1/2 } } } - 2^{ - \\frac { 2t }{ T_{ 1/2 } } }
        = 2^{ - \\frac t{ T_{ 1/2 } } }\\cbr{ 1 - 2^{ - \\frac { t }{ T_{ 1/2 } } } }
        = \\frac 1{ {num} }\\cdot \\cbr{ 1 - \\frac 1{ {num} } } \\approx {res:.3f}
    ''',
])
@variant.arg(how__num__log_num=[
    ('четверть', 4, 2),
    ('одна восьмая', 8, 3),
    ('половина', 2, 1),
    ('одна шестнадцатая', 16, 4),
])
@variant.arg(t=['%d суток' % t for t in [2, 3, 4, 5]])
class BK_53_03(variant.VariantTask):
    def GetUpdate(self, how=None, t=None, num=None, log_num=None, **kws):
        return dict(
            T='%.1f суток' % (1. * t.Value / log_num),
            res=1. / num * (1 - 1./num),
        )


@variant.solution_space(150)
@variant.text('''
    Энергия связи ядра {element} равна ${E:Value}$.
    Найти дефект массы этого ядра. Ответ выразите в а.е.м. и кг. Скорость света ${Consts.c:Task}$.
''')
@variant.answer_align([
    'E_\\text{ св. } &= \\Delta m c^2 \\implies',
    '''\\implies
        \\Delta m &= \\frac { E_\\text{ св. } }{ c^2 } = \\frac{E:Value|s}{Consts.c:Value|sqr|s}
        = \\frac{ {eV} \\cdot 10^6 \\cdot {Consts.eV:Value} }{Consts.c:Value|sqr|s}
        \\approx {dm:Value} \\approx {aem:Value}''',
])
@variant.arg(element__E=[  # https://www.calc.ru/Energiya-Svyazi-Nekotorykh-Yader.html
    ('дейтерия \\ce{^{2}_{1}H} (D)', 'E = 2.22 МэВ'),
    ('трития \\ce{^{3}_{1}H} (T)', 'E = 8.48 МэВ'),
    ('гелия \\ce{^{3}_{2}He}', 'E = 7.72 МэВ'),
    ('гелия \\ce{^{3}_{2}He}', 'E = 28.29 МэВ'),
    ('лития \\ce{^{6}_{3}Li}', 'E = 31.99 МэВ'),
    ('лития \\ce{^{7}_{3}Li}', 'E = 39.2 МэВ'),
    ('бериллия \\ce{^{9}_{4}Be}', 'E = 58.2 МэВ'),
    ('бора \\ce{^{10}_{5}B}', 'E = 64.7 МэВ'),
    ('бора \\ce{^{11}_{5}B}', 'E = 76.2 МэВ'),
    ('углерода \\ce{^{12}_{6}C}', 'E = 92.2 МэВ'),
    ('углерода \\ce{^{13}_{6}C}', 'E = 97.1 МэВ'),
    ('азота \\ce{^{14}_{7}N}', 'E = 104.7 МэВ'),
    ('азота \\ce{^{14}_{7}N}', 'E = 115.5 МэВ'),
    ('кислорода \\ce{^{16}_{8}O}', 'E = 127.6 МэВ'),
    ('кислорода \\ce{^{17}_{8}O}', 'E = 131.8 МэВ'),
    ('кислорода \\ce{^{18}_{8}O}', 'E = 139.8 МэВ'),
])
class BK_53_12(variant.VariantTask):
    def GetUpdate(self, E=None, Consts=None, **kws):
        dm = E.Other(Consts.e, action='mult', precisionInc=1).Other(Consts.c, action='div').Other(Consts.c, action='div', units='кг')
        aem = dm.Other(Consts.aem, action='div', units='а.е.м.')
        return dict(
            eV=E.Value,
            dm=dm,
            aem=aem,
        )
