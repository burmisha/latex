import generators.variant as variant
from generators.helpers import Consts, Elements
import itertools
import math


@variant.lv_variant_task(
    {
        '$\\alpha$-излучение': 'обладает положительным зарядом',
        '$\\beta$-излучение': 'обладает отрицательным электрическим зарядом',
        '$\\gamma$-излучение': 'не несёт электрического заряда',
    },
    [],
    answers_count=3,
    mocks_count=0,
)
class Definitions01(variant.VariantTask):
    pass


@variant.lv_variant_task(
    {
        '$\\alpha$-излучение': 'ядра атомов гелия',
        '$\\beta$-излучение': 'электроны',
        '$\\gamma$-излучение': 'электромагнитное излучение',
    },
    [],
    answers_count=3,
    mocks_count=0,
)
class Definitions02(variant.VariantTask):
    pass


@variant.lv_variant_task(
    {
        'атом Резерфорда': 'планетарная модель атома',
        'атом Томсона': '«пудинг с изюмом»',
    },
    [],
    answers_count=2,
    mocks_count=0,
)
class Definitions03(variant.VariantTask):
    pass


@variant.lv_variant_task(
    {
        'размер атома': '$10^{-8}\\units{см}$',
        'размер ядра атома': '$10^{-13}\\units{см}$',
    },
    ['$10^{-15}\\units{см}$', '$10^{-10}\\units{см }$'],
    answers_count=2,
    mocks_count=1,
)
class Definitions04(variant.VariantTask):
    pass


@variant.lv_variant_task(
    {
        'массовое число водорода \\ce{^{1}_{1}H}': 1,
        'массовое число углерода \\ce{^{12}_{6}C}': 12,
        'массовое число кислорода \\ce{^{16}_{8}O}': 16,
        'массовое число азота \\ce{^{14}_{7}N}': 14,
        'зарядовое число водорода \\ce{^{1}_{1}H}': 0,
        'зарядовое число углерода \\ce{^{12}_{6}C}': 6,
        'зарядовое число кислорода \\ce{^{16}_{8}O}': 8,
        'зарядовое число азота \\ce{^{14}_{7}N}': 7,
    },
    [4, 10, 11, 9, 5],
    answers_count=2,
    mocks_count=2,
)
class Definitions05(variant.VariantTask):
    pass


@variant.lv_variant_task(
    {
        'массовое число $\\alpha$-частицы': 4,
        'массовое число $\\beta$-частицы': 0,
        # 'массовое число $\\gamma$-частицы': 0,
        'зарядовое число $\\alpha$-частицы': 2,
        'зарядовое число $\\beta$-частицы': -1,
        # 'зарядовое число $\\gamma$-частицы': 0,
    },
    [1, -2],
    answers_count=3,
    mocks_count=2,
)
class Definitions06(variant.VariantTask):
    pass


@variant.text('''
    На какой {which} угол (в градусах) отконялись $\\alpha$-частицы
    в опытах Резерфорда по их рассеянию на тонкой золотой фольге?
''')
@variant.arg(which__a=[('минимальный', 0), ('максимальный', 180)])
@variant.answer_test('{a}')
@variant.solution_space(40)
@variant.answer_short('{a}\\degrees')
class Definitions07(variant.VariantTask):
    pass



@variant.solution_space(150)
@variant.text('''
    Определите неизвестный продукт X ядерной реакции ${reaction}$.
''')
@variant.answer_short('{X}')
@variant.arg(reaction__X=[
    ('\\ce{^{10}_{5}B} + \\alpha \\to \\ce{^{14}_{7}N} + X', ''),
])
class Vishnyakova_5_3_6(variant.VariantTask):
    pass


@variant.solution_space(80)
@variant.text('''
    В какое ядро превращается исходное в результате ядерного распада?
    Запишите уравнение реакции и явно укажите число протонов и нейтронов в получившемся ядре.
    \\begin{itemize}
        \\item {element1:RuName}, ${fall1}$-распад,
        \\item {element2:RuName}, ${fall2}$-распад,
        \\item {element3:RuName}, ${fall3}$-распад,
        \\item {element4:RuName}, ${fall4}$-распад.
    \\end{itemize}
''')
@variant.answer_align([
    '{reaction1}: \\qquad \\text{{r1:RuName}}: {r1:protons}\,p^+, {r1:neutrons}\,n^0,',
    '{reaction2}: \\qquad \\text{{r2:RuName}}: {r2:protons}\,p^+, {r2:neutrons}\,n^0,',
    '{reaction3}: \\qquad \\text{{r3:RuName}}: {r3:protons}\,p^+, {r3:neutrons}\,n^0,',
    '{reaction4}: \\qquad \\text{{r4:RuName}}: {r4:protons}\,p^+, {r4:neutrons}\,n^0.',
])
@variant.arg(element1__fall1=[
    (Elements.get_by_z_a(90, 234), '\\beta^-'),            # Белолипецкий 6.86
    (Elements.get_by_ru_a('торий', 234), '\\beta'),        # Марон 9 840
    (Elements.get_by_ru_a('протактиний', 234), '\\beta'),  # Марон 9 840
    (Elements.get_by_z_a(15, 30), '\\beta^+'),             # Белолипецкий 6.89
    (Elements.get_by_z_a(6, 14), '\\beta^-'),              # Марон 9 832
])
@variant.arg(element2__fall2=[
    (Elements.get_by_z_a(88, 226), '\\alpha'),             # Белолипецкий 6.87
    (Elements.get_by_z_a(84, 210), '\\alpha'),             # Белолипецкий 6.88
    (Elements.get_by_ru_a('уран', 238), '\\alpha'),        # Марон 9 840
    (Elements.get_by_ru_a('уран', 234), '\\alpha'),        # Марон 9 840
    (Elements.get_by_ru_a('торий', 230), '\\alpha'),       # Марон 9 840
    (Elements.get_by_ru_a('радий', 226), '\\alpha'),       # Марон 9 840
    (Elements.get_by_ru_a('радон', 222), '\\alpha'),       # Марон 9 840
])
@variant.arg(element3__fall3=[
    (Elements.get_by_ru_a('полоний', 218), '\\alpha'),     # Марон 9 840
    (Elements.get_by_ru_a('свинец', 214), '\\alpha'),      # Марон 9 840
    (Elements.get_by_ru_a('висмут', 214), '\\beta'),       # Марон 9 840
    (Elements.get_by_ru_a('полоний', 214), '\\alpha'),     # Марон 9 840
    (Elements.get_by_ru_a('свинец', 210), '\\beta'),       # Марон 9 840
    (Elements.get_by_ru_a('висмут', 210), '\\beta'),       # Марон 9 840
    (Elements.get_by_ru_a('полоний', 210), '\\beta'),      # Марон 9 840
    (Elements.get_by_ru_a('свинец', 206), '\\alpha'),      # Марон 9 840
])
@variant.arg(element4__fall4=[
    (Elements.get_by_ru_a('плутоний', 239), '\\alpha'),    # Марон 9 ДМ СР 2-2
    (Elements.get_by_ru_a('свинец', 209), '\\beta'),       # Марон 9 ДМ СР 10-2
])
@variant.is_one_arg
class WriteRadioFall(variant.VariantTask):  
    def GetUpdateOneArg(self, a):
        return dict(
            r1=a.element1.fall(a.fall1),
            reaction1=a.element1.get_reaction(a.fall1),
            r2=a.element2.fall(a.fall2),
            reaction2=a.element2.get_reaction(a.fall2),
            r3=a.element3.fall(a.fall3),
            reaction3=a.element3.get_reaction(a.fall3),
            r4=a.element4.fall(a.fall4),
            reaction4=a.element4.get_reaction(a.fall4),
        )


@variant.solution_space(150)
@variant.text('''
    Какая доля (от начального количества) радиоактивных ядер {what} через время,
    равное {when} периодам полураспада? Ответ выразить в процентах.
''')
@variant.answer_align([
    '''N &= N_0 * 2^{- \\frac t{T_{1/2}}} \\implies
    \\frac N{N_0} = 2^{- \\frac t{T_{1/2}}}
    = 2^{-{t}} \\approx {N_value:.2f} \\approx {N_percent:.0f}\\%''',
    '''N_\\text{расп.} &= N_0 - N = N_0 - N_0 * 2^{-\\frac t{T_{1/2}}}
    = N_0\\cbr{1 - 2^{-\\frac t{T_{1/2}}}} \\implies
    \\frac{N_\\text{расп.}}{N_0} = 1 - 2^{-\\frac t{T_{1/2}}}
    = 1 - 2^{-{t}} \\approx {N_left_value:.2f} \\approx {N_left_percent:.0f}\\%''',
])
@variant.arg(what=['распадётся', 'останется'])
@variant.arg(when__t=[
    ('двум', 2),
    ('трём', 3),
    ('четырём', 4),
])
class Vishnyakova_5_3_1(variant.VariantTask):
    def GetUpdate(self, what=None, when=None, t=None):
        share = 2. ** (-t)
        left = 1. - share
        return dict(
            t=t,
            N_value=share,
            N_percent=share * 100,
            N_left_value=left,
            N_left_percent=left * 100,
        )


@variant.text('''
    Каков период полураспада радиоактивного изотопа,
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
    Лучше всего нейтронное излучение ослабляет вода: в 4 раза лучше бетона и в 3 раза лучше свинца.
    Толщина слоя половинного ослабления $\\gamma$-излучения для воды равна {d1:V|e}.
    Во сколько раз ослабит нейтронное излучение слой воды толщиной {d:Task|e}?
''')
@variant.arg(d1=['3 см'])
@variant.arg(d=['%s = %d см' % (l, v) for l, v in itertools.product(['l', 'h', 'd'], [15, 30, 60, 120])])
class Quantum1120(variant.VariantTask):  # 1120 Рымкевич
    pass


@variant.solution_space(150)
@variant.text('''
    Сколько процентов ядер радиоактивного железа $\\ce{^{59}Fe}$
    останется через ${t:Value}$, если период его полураспада составляет ${T:Value}$?
''')
@variant.answer_align([
    '''N &= N_0 * 2^{-\\frac t{T_{1/2}}}
    = 2^{-\\frac{t:Value|s}{T:Value|s}}
    \\approx {share:.4f} = {percent:.2f}\\%''',
])
@variant.arg(t=['t = %s суток' % t for t in ['91.2', '136.8', '182.4']])
@variant.arg(T=['T = 45.6 суток'])
class Vishnyakova_5_3_2(variant.VariantTask):  # Вишнякова - Базовый курс 5.3 - задача 02
    def GetUpdate(self, t=None, T=None):
        share = 2 ** float(- (t / T).SI_Value)
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
        N &= N_0 * 2^{-\\frac t{T_{1/2}}}
        \\implies \\frac N{N_0} = 2^{-\\frac t{T_{1/2}}}
        \\implies \\frac 1{{num}} = 2^{-\\frac {t:Value|s}{T_{1/2}}}
        \\implies {log_num} = \\frac {t:Value|s}{T_{1/2}}
        \\implies T_{1/2} = \\frac {t:Value|s}{log_num} \\approx {T:Value}.
    ''',
    '''
        \\delta &= \\frac{N(t)}{N_0} - \\frac{N(2t)}{N_0}
        = 2^{-\\frac t{T_{1/2}}} - 2^{-\\frac {2t}{T_{1/2}}}
        = 2^{-\\frac t{T_{1/2}}}\\cbr{1 - 2^{-\\frac t{T_{1/2}}}}
        = \\frac 1{{num}} * \\cbr{1-\\frac 1{{num}}} \\approx {res:.3f}''',
])
@variant.arg(how__num__log_num=[
    ('четверть', 4, 2),
    ('одна восьмая', 8, 3),
    ('половина', 2, 1),
    ('одна шестнадцатая', 16, 4),
])
@variant.arg(t=['%d суток' % t for t in [2, 3, 4, 5]])
class Vishnyakova_5_3_3(variant.VariantTask):
    def GetUpdate(self, how=None, t=None, num=None, log_num=None):
        return dict(
            T=(t / log_num).IncPrecision(1).As('суток'),
            res=1. / num * (1 - 1 / num),
        )


@variant.solution_space(100)
@variant.text('''
    Энергия связи ядра {element} равна ${E:Value}$.
    Найти дефект массы этого ядра. Ответ выразите в а.е.м. и кг.
    Скорость света {Consts.c_4:Task|e}, элементарный заряд {Consts.e:Task|e}.
''')
@variant.answer_align([
    'E_\\text{св.} &= \\Delta m c^2 \\implies',
    '''\\implies
        \\Delta m &= \\frac {E_\\text{св.}}{c^2} = \\frac{E:Value|s}{c:V|sqr|s}
        = \\frac{{eV} * 10^6 * {Consts.eV:Value}}{c:V|sqr|s}
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
class Vishnyakova_5_3_12(variant.VariantTask):
    def GetUpdate(self, element=None, E=None):
        c = Consts.c_4
        dm = E / c / c
        return dict(
            eV=E.Value,
            dm=dm,
            aem=dm.As('а.е.м.'),
            c=c,
        )


@variant.solution_space(150)
@variant.text('''
    Определите деффект массы (в а.е.м.) и энергию связи (в МэВ) ядра атома {element:LaTeX},
    если его масса составляет {m_aem:Value|e}.
    Считать {Consts.m_p_aem:Task|e}, {Consts.m_n_aem:Task|e}.
''')
@variant.answer_align([
    '{dm:L} &= (A - Z){Consts.m_n_aem:L} + Z{Consts.m_p_aem:L} - m = {element.n} * {Consts.m_n_aem:V} + {element.p} * {Consts.m_p_aem:V} - {m_aem:V} \\approx {dm:V}',
    '{dE:L} &= {dm:L} c^2 \\approx {dm.Value:.4f} * {Consts.one_aem_eV:V} \\approx {dE:V}',
])
@variant.arg(element__m_aem=[
    # https://ru.wikipedia.org/wiki/%D0%A1%D0%B2%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F_%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0_%D0%B8%D0%B7%D0%BE%D1%82%D0%BE%D0%BF%D0%BE%D0%B2
    (Elements.get_by_z_a(1, 2), 'm = 2.0141 а.е.м.'),
    (Elements.get_by_z_a(1, 3), 'm = 3.01605 а.е.м.'),
    (Elements.get_by_z_a(2, 3), 'm = 3.01603 а.е.м.'),
    (Elements.get_by_z_a(2, 4), 'm = 4.0026 а.е.м.'),
    (Elements.get_by_z_a(2, 6), 'm = 6.0189 а.е.м.'),
    (Elements.get_by_z_a(2, 8), 'm = 8.0225 а.е.м.'),
])
class Delta_m_from_m(variant.VariantTask):
    def GetUpdate(self, element, m_aem):
        dm = element.n * Consts.m_n_aem.Value + element.p * Consts.m_p_aem.Value - m_aem.Value
        dE = dm * Consts.one_aem_eV.Value
        return dict(
            dm='\\Delta m = %.5f а.е.м.' % dm,
            dE='E_\\text{св.} = %.2f МэВ' % dE,
        )
