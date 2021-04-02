import generators.variant as variant
from generators.helpers import Consts




@variant.solution_space(150)
@variant.text('''
    Какая доля (от начального количества) радиоактивных ядер {what} через время,
    равное {when} периодам полураспада? Ответ выразить в процентах.
''')
@variant.answer_align([
    '''N &= N_0 * 2^{ - \\frac t{ T_{ 1/2 } } } \\implies
    \\frac N{ N_0 } = 2^{ - \\frac t{ T_{ 1/2 } } }
    = 2^{ -{t} } \\approx {N_value:.2f} \\approx {N_percent:.0f}\\%''',
    '''N_\\text{ расп. } &= N_0 - N = N_0 - N_0 * 2^{ - \\frac t{ T_{ 1/2 } } }
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
class BK_53_01(variant.VariantTask):  # Вишнякова - Базовый курс 5.3 - задача 01
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
    '''N &= N_0 * 2^{ - \\frac t{ T_{ 1/2 } } }
    = 2^{ - \\frac {t:Value|s}{T:Value|s} }
    \\approx {share} \\approx {percent}\\%''',
])
@variant.arg(t=['t = %s суток' % t for t in ['91.2', '136.8', '182.4']])
@variant.arg(T=['T = 45.6 суток'])
class BK_53_02(variant.VariantTask):  # Вишнякова - Базовый курс 5.3 - задача 02
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
        N &= N_0 * 2^{ - \\frac t{ T_{ 1/2 } } }
        \\implies \\frac N{ N_0 } = 2^{ - \\frac t{ T_{ 1/2 } } }
        \\implies \\frac 1{ {num} } = 2^{ - \\frac {t:Value|s}{ T_{ 1/2 } } }
        \\implies {log_num} = \\frac {t:Value|s}{ T_{ 1/2 } }
        \\implies T_{ 1/2 } = \\frac {t:Value|s}{log_num} \\approx {T:Value}.
    ''',
    '''
        \\delta &= \\frac{ N(t) }{ N_0 } - \\frac{ N(2t) }{ N_0 }
        = 2^{ - \\frac t{ T_{ 1/2 } } } - 2^{ - \\frac { 2t }{ T_{ 1/2 } } }
        = 2^{ - \\frac t{ T_{ 1/2 } } }\\cbr{ 1 - 2^{ - \\frac { t }{ T_{ 1/2 } } } }
        = \\frac 1{ {num} } * \\cbr{ 1 - \\frac 1{ {num} } } \\approx {res:.3f}''',
])
@variant.arg(how__num__log_num=[
    ('четверть', 4, 2),
    ('одна восьмая', 8, 3),
    ('половина', 2, 1),
    ('одна шестнадцатая', 16, 4),
])
@variant.arg(t=['%d суток' % t for t in [2, 3, 4, 5]])
class BK_53_03(variant.VariantTask):  # Вишнякова - Базовый курс 5.3 - задача 03
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
        = \\frac{ {eV} * 10^6 * {Consts.eV:Value} }{Consts.c:Value|sqr|s}
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
class BK_53_12(variant.VariantTask):  # Вишнякова - Базовый курс 5.3 - задача 12
    def GetUpdate(self, E=None, **kws):
        dm = E.Mult(Consts.e, precisionInc=1).Div(Consts.c).Div(Consts.c, units='кг')
        aem = dm.Div(Consts.aem, units='а.е.м.')
        return dict(
            eV=E.Value,
            dm=dm,
            aem=aem,
        )
