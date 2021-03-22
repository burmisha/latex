import generators.variant as variant
from generators.value import Consts

@variant.solution_space(40)
@variant.text('''
    Молекулы газа в некотором сосуде движутся со средней скоростью {v:Value|e}.
    Определите, какое расстояние в среднем проходит одна из таких молекул за {t:Value|e}.
''')
@variant.answer_short('s = v t = {v:Value} * {t:Value} = {s:Value}.')
@variant.arg(v=['%d м / с' % v for v in [150, 200, 250, 300, 500]])
@variant.arg(t=['%d час' % v for v in [2, 3, 4, 5]] + ['%d сут' % v for v in [2, 3, 4, 5]])
class Basic01(variant.VariantTask):
    def GetUpdate(self, v=None, t=None, **kws):
        if 'час' in f'{t:Value}':
            mult = 3600
        elif 'сут' in f'{t:Value}':
            mult = 3600 * 24
        return dict(
            s='{} м'.format(v.Value * t.Value * mult),
        )

@variant.solution_space(0)
@variant.text('''
    Напротив каждой физической величины укажите её обозначение и единицы измерения в СИ:
    \\begin{{enumerate}}
        \\item {first},
        \\item {second},
        \\item {third}.
    \\end{{enumerate}}
''')
@variant.arg(first=['масса', 'объём'])
@variant.arg(second=['плотность', 'количество вещества'])
@variant.arg(third=['молярная масса', 'количество молекул'])
class Basic02(variant.VariantTask):
    pass


@variant.solution_space(60)
@variant.text('''
    Ответьте на вопросы и запишите формулы:
    \\begin{{enumerate}}
        \\item {what},
        \\item {formula}.
    \\end{{enumerate}}
''')
@variant.arg(what=[
    'сформилируйте, что такое броуновское движение',
    'запишите 3 основных положения МКТ',
])
@variant.arg(formula=[
    'cвязь количества вещества, числа частиц и числа Авогадро',
    'cвязь количества вещества, массы тела и молярной массы',
])
class Basic03(variant.VariantTask):
    pass


@variant.solution_space(30)
@variant.text('''
    Определите молярную массу веществ (не табличное значение, а вычислением по таблице Менделеева):
    \\begin{{enumerate}}
        \\item {first},
        \\item {second},
        \\item {third}.
    \\end{{enumerate}}
''')
@variant.arg(first=['гелий', 'неон'])
@variant.arg(second=['азот', 'кислород'])
@variant.arg(third=['углекислый газ', 'вода', 'озон'])
class Basic04(variant.VariantTask):
    pass


@variant.text('''
    Укажите, верны ли утверждения («да» или «нет» слева от каждого утверждения):
    \\begin{{enumerate}}
        \\item В твёрдом состоянии вещества связи между молекулами наиболее сильны (в сравнении с жидким и газообразным состояниями).
        \\item Любая частица (например, картошечка в супе) находится в броуновском движении, однако наблюдать его технически возможно только для малых частиц.
        \\item Сжимаемость газов объясняется проникновением атомов молекул друг в друга и уменьшением межатомного расстояния внутри молекул.
        \\item Броуновское движение частиц пыльцы в жидкости — следствие взаимодействия этих частиц пыльцы между собой.
        \\item Если в двух телах одинаковое число молекул, то их массы с большой точностью будут равны.
        \\item Если в двух телах одинаковое число протонов и нейтронов (между телами), то и массы тел с большой точностью окажутся равны.
        \\item При определении размеров молекул мы зачастую пренебрегаем их формой, не различая радиус и диаметр, а то и вовсе считая их форму кубической.
        \\item Диффузия вызвана тепловым движением молекул и может наблюдаться в твердых, жидких и газообразных веществах.
    \\end{{enumerate}}
''')
@variant.no_args
@variant.solution_space(0)
@variant.answer_short('''
    \\text{ да, да, нет, нет, нет, да, да, да }
''')
class Basic05(variant.VariantTask):
    pass


@variant.solution_space(40)
@variant.text('Какое количество вещества содержит тело, состоящее из {N:Value:e} молекул?')
@variant.arg(N=[
    '3 10^22', '3 10^23', '3 10^24', '3 10^25',
    '9 10^22', '9 10^23', '9 10^24', '9 10^25',
    '12 10^22', '12 10^23', '12 10^24', '12 10^25',
])
@variant.answer_short('\\nu = \\frac{ N }{Consts.N_A:L|s} = \\frac{N:V|s}{Consts.N_A:V|s} = {nu:V}.')
class CountNu(variant.VariantTask):
    def GetUpdate(self, N=None, **kws):
        return dict(
            nu=N.Div(Consts.N_A, units='моль'),
        )


@variant.solution_space(40)
@variant.text('Какова масса {nu:Value:e} ({formula}) {what}? Молярная масса {what} {mu:Value:e}.')
@variant.arg(nu=['\\nu = %d моль' % nu for nu in [2, 4, 5, 10, 15, 20, 25, 50]])
@variant.arg(what__mu__formula=[
    ('метана', '\\mu = 16 г / моль', '\\ce{CH4}'),
    ('этана', '\\mu = 30 г / моль', '\\ce{C2H6}'),
    ('пропана', '\\mu = 44 г / моль', '\\ce{C3H8}'),
    ('бутана', '\\mu = 58 г / моль', '\\ce{C4H10}'),
    ('пентана', '\\mu = 72 г / моль', '\\ce{C5H12}'),
    ('гексана', '\\mu = 86 г / моль', '\\ce{C6H14}'),
    ('гептана', '\\mu = 100 г / моль', '\\ce{C7H16}'),
    ('октана', '\\mu = 114 г / моль', '\\ce{C8H18}'),
    ('нонана', '\\mu = 128 г / моль', '\\ce{C9H20}'),
    ('декана', '\\mu = 142 г / моль', '\\ce{C10H22}'),
])
@variant.answer_short('m = \\mu\\nu = {mu:Value} * {nu:Value} = {m:Value}.')
class CountMass(variant.VariantTask):
    def GetUpdate(self, nu=None, mu=None, **kws):
        return dict(
            m='{} г'.format(nu.Value * mu.Value),
        )


@variant.solution_space(40)
@variant.text('Сколько молекул содержится в {m:Value:e} {what}? Молярная масса {what} ({formula}) {mu:Value:e}.')
@variant.arg(m=['m = %d г' % nu for nu in [20, 50, 200, 500]])
@variant.arg(what__mu__formula=[
    ('метана', '\\mu = 16 г / моль', '\\ce{CH4}'),
    ('этана', '\\mu = 30 г / моль', '\\ce{C2H6}'),
    ('пропана', '\\mu = 44 г / моль', '\\ce{C3H8}'),
    ('бутана', '\\mu = 58 г / моль', '\\ce{C4H10}'),
    ('пентана', '\\mu = 72 г / моль', '\\ce{C5H12}'),
    ('гексана', '\\mu = 86 г / моль', '\\ce{C6H14}'),
    ('гептана', '\\mu = 100 г / моль', '\\ce{C7H16}'),
    ('октана', '\\mu = 114 г / моль', '\\ce{C8H18}'),
    ('нонана', '\\mu = 128 г / моль', '\\ce{C9H20}'),
    ('декана', '\\mu = 142 г / моль', '\\ce{C10H22}'),
])
@variant.answer_short('N = {Consts.N_A:L}\\nu = {Consts.N_A:L}\\frac{m:L|s}{mu:L|s} = {Consts.N_A:Value} * \\frac{m:V|s}{mu:V|s} = {N:V}.')
class CountParticles(variant.VariantTask):
    def GetUpdate(self, m=None, mu=None, **kws):
        return dict(
            N=m.Div(mu).Mult(Consts.N_A),
        )


@variant.solution_space(40)
@variant.text('''
    Переведите температуры из шкалы Цельсия в шкалу Кельвина (или обратно).
    \\begin{{enumerate}}
        \\item ${T1:Value} = $
        \\item ${T2:Value} = $
        \\item ${T3:Value} = $
    \\end{{enumerate}}
''')
@variant.arg(T1=['%d \\celsius' % v for v in [50, 100, 200, 250, 300]])
@variant.arg(T2=['%d К' % v for v in [50, 100, 200, 250, 300]])
@variant.arg(T3=['%d \\celsius' % v for v in [27, 77, 127]] + ['%d К' % v for v in [127, 227, 327]])
class Celsuis(variant.VariantTask):
    pass


@variant.text('''
    Укажите, верны ли утверждения («да» или «нет» слева от каждого утверждения):
    \\begin{{enumerate}}
        \\item Увеличение температуры на 3 градуса цельсия всегда соответствует увеличению на 3 градуса кельвина.
        \\item Температуру тела всегда можно понизить на 30 кельвин (пусть при этом и может произойти фазовый переход).
        % \\item Температуру тела всегда можно повысить на 30 кельвин (пусть при этом и может произойти фазовый переход).
        \\item Температуру тела всегда можно понизить на 30 градусов Цельсия (пусть при этом и может произойти фазовый переход).
        % \\item Температуру тела всегда можно повысить на 30 градусов Цельсия (пусть при этом и может произойти фазовый переход).

        \\item У шкалы температур Кельвина есть минимальное значение (пусть и недостижимое): 0 кельвин, а у шкалы Цельсия такого значения нет вовсе и возможны температуры меньше 0 градусов цельсия.
        \\item Если бы стекло, из которого изготовлен термометр, расширялось при нагревании сильнее жидкости внутри, то мы бы наблюдали, как столбик жидкости укорачивается при нагревании.
        \\item Давление газа на окружающий его сосуд вызвано ударами молекул газа о его стенки: при этом изменяется импульс молекул, а значит кто-то (стенка) действовала с некоторой силой, а тогда по 3 закону Ньютона и газ действовал на стенку.
        \\item В модели идеального газа невозможен теплообмен: например, если смешать две порции кислорода и азота разной температуры, то их молекулы не будут сталкиваться и обмениваться энергиями. Диффузия при этом произойдет.
        \\item Основное уравнение МКТ идеального газа применимо к газам сколь угодно малой плотности.

        \\item Основное уравнение МКТ способно описать даже плазму: состояние вещества, при котором молекулы от ударов друг об друга начинают расщепляется на ионы и электроны.
        \\item Основное уравнение МКТ ИГ может быть получено теоретически из модели идеального газа, однако в нем присутствуют микропараметры, поэтому оно не допускает непосредственной экспериментальной проверки.

        \\item Все процессы: изохорный, изобарный, изотермный по умолчанию предполагают, что количество вещества в них не изменяется.
        \\item При горении, например, водорода в кислороде (2H2+O2-2H2O), не изменяется, ни масса вещества участвующего в реакции, ни его количество. Также при этом не изменяется и количество протонов, нейтронов и электронов.
        \\item Каждый набор макропараметров идеального газа (P, V и T) задаёт точку в трехмерном пространстве. При их изменении образуется линия в этом пространстве. Строя графики изопроцессов в координатах PV, VT, PT мы строим проекцию этой линии на одну из плоскостей.
    \\end{{enumerate}}
''')
@variant.no_args
@variant.solution_space(0)
class Basic06(variant.VariantTask):
    pass


@variant.solution_space(0)
@variant.text('''
    Выразите:
    \\begin{{enumerate}}
        \\item {formula1},
        \\item {formula2},
        \\item {formula3}.
    \\end{{enumerate}}
''')
@variant.arg(formula1=[
    'плотность тела через его массу и объём',
    'массу тела через его плотность и объём',
    'объём тела через его массу и плотность',
])
@variant.arg(formula2=[
    'количество вещества через массу и молярную массу',
    'количество вещества через число частиц и число Авогадро',
])
@variant.arg(formula3=[
    'концентрацию молекул через их число и объём',
    'основное уравнение МКТ идеального газа через концентрацию и среднюю кинетическую энергию поступательного движения его молекул'
])
class Basic07(variant.VariantTask):
    pass


@variant.solution_space(0)
@variant.text('''
    Напротив каждой физической величины укажите её обозначение и единицы измерения в СИ:
    \\begin{{enumerate}}
        \\item {fv_1},
        \\item {fv_2},
        \\item {fv_3}.
    \\end{{enumerate}}
''')
@variant.arg(fv_1=[
    'температура в Кельвинах',
    'температура в Цельсиях',
])
@variant.arg(fv_2=['объем', 'плотность', 'масса', 'молярная масса', 'количество вещества', 'число частиц', 'число Авогадро'])
@variant.arg(fv_3=[
    'постоянная Больцмана',
    'число Авогадро',
    # 'универсальная газовая Постоянная',
])
class Basic08(variant.VariantTask):
    pass


@variant.solution_space(0)
@variant.text('''
    Запишите, как бы вы обозначили...
    \\begin{{enumerate}}
        \\item {fv_1},
        \\item {fv_2},
        \\item {fv_3},
        \\item {fv_4}.
    \\end{{enumerate}}
''')
@variant.arg(fv_1=[
    'увеличение давления в сосуде с газом',
    'два объема газа: до и после его расширения'
])
@variant.arg(fv_2=[
    'число частиц: до и после утечки газа из баллона',
    'количество вещества: до и после утечки газа из баллона',
])
@variant.arg(fv_3=[
    'массы газа: до и после утечки газа из баллона',
    'концентрацию молекул газа в сосуде после сжатия и нагрева',
])
@variant.arg(fv_4=[
    'температуры газа: до и после нагрева в 3 раза',
    'объемы газа: до и после сжатия в 4 раза',
    'давления газа: до и после его увеличения в 5 раз',
])
class Basic09(variant.VariantTask):
    pass


@variant.solution_space(0)
@variant.text('''
    Запишите, какие физические величины соответствуют следующим единицам измерения (указать название и обозначение),
    \\begin{{enumerate}}
        \\item {fv_1},
        \\item {fv_2},
        \\item {fv_3},
        \\item {fv_4},
        \\item {fv_5}.
    \\end{{enumerate}}
''')
@variant.arg(fv_1=[
    'кельвин',
    'градус Цельсия',
])
@variant.arg(fv_2=['мПа', 'МПа'])
@variant.arg(fv_3=['эВ', 'мкДж', 'мДж'])
@variant.arg(fv_4=[
    '$\\frac{ \\text{ кг } }{ \\text{ м }^3 }$',
    '$\\frac{ \\text{ г } }{ \\text{ л } }$',
    '$\\frac{ 1 }{ \\text{ м }^3 }$',
    '$\\frac{ 1 }{ \\text{ л } }$',
    '$\\text{ м }^3$',
    '$\\text{ л }$',
])
@variant.arg(fv_5=[
    '$\\units{ г }$',
    '$\\units{ моль }$',
    '$\\funits{ г }{ моль }$',
    '$\\funits{ кг }{ моль }$',
])
class Basic10(variant.VariantTask):
    pass


@variant.text('''
    Выразите одну величину через остальные, используя при необходимости постоянную Больцмана, число Авогадро или универсальную газовую постоянную:
    \\begin{{enumerate}}
        \\item {fv_1},
        \\item {fv_2},
        \\item {fv_3},
        \\item {fv_4},
    \\end{{enumerate}}
''')
@variant.arg(fv_1=[
    'температуру газа через его давление, объем, число частиц',
    'концентрацию молекул через давление и температуру',
])
@variant.arg(fv_2=[
    'массу молекулы через молярную массу вещества',
    'плотность газа через концентрацию молекул и массу молекулы',
    'плотность газа через его молярную массу и концентрацию молекул',
])
@variant.arg(fv_3=[
    'число молекул через температуру, давление и объём',
    'среднюю кинетическую энергию поступательного движения молекул через температуру',
])
@variant.arg(fv_4=[
    'среднеквадратичную скорость поступательного движения молекул через температуру и массу молекулы',
    'среднеквадратичную скорость молекул через средний квадрат скорости',
    'средний квадрат скорости молекул через скорости отдельных молекул',
    'средний квадрат проекции скорости молекул на ось $Ox$ через средний квадрат скорости молекул',
])
class Basic11(variant.VariantTask):
    pass


@variant.solution_space(0)
@variant.text('''
    Из уравнения состояния идеального газа выведите или выразите...
    \\begin{{enumerate}}
        \\item {first},
        \\item {second},
        \\item {third}.
    \\end{{enumerate}}
''')
@variant.arg(first=[
    'объём',
    'давление',
])
@variant.arg(second=[
    'молярную массу',
    'температуру',
])
@variant.arg(third=[
    'плотность газа',
    'концентрацию молекул газа',
])
class Basic12(variant.VariantTask):
    pass


@variant.solution_space(40)
@variant.text('{task}')
@variant.arg(task=[
    'Почему плазму (одно из агрегатных состояний вещества, при котором часть молекул распадаются на ионы и электроны) нельзя считать идеальным газом?',
    'В межзвездном пространстве встречаются молекулы (до нескольких десятков на $\\text{{м}}^3$). Почему такой газ нельзя считать идеальным?',
])
class Basic13(variant.VariantTask):
    pass


@variant.solution_space(100)
@variant.text('''
    Изобразите в координатах $PV$/$VT$/$PT$ графики {what} в {N} раза (все 3 графика).
    Не забудьте указать оси и масштаб, начальную и конечную точки, направление движения на графике.
''')
@variant.arg(what=[
    'изохорического нагрева',
    'изохорического охлаждения',
    'изобарического сжатия',
    'изобарического расширения',
    'изотермического повышения давления',
    'изотермического понижения давления',
])
@variant.arg(N=[2, 3, 4])
class GraphPV_1(variant.VariantTask):
    pass


@variant.solution_space(160)
@variant.text('''
    Изобразите в координатах $PV$, соблюдая масштаб, процесс 1234,
    в котором 12 — {first} {first_what} в {first_n} раза,
    23 — изотермическое {second_what} в {second_n} раза,
    34 — {third} {third_what} в {third_n} раза.
''')
@variant.arg(first=['изобарическое', 'изохорическое'])
@variant.arg(first_what=['нагревание', 'охлаждение'])
@variant.arg(first_n=[2, 3])
@variant.arg(second_what=['расширение', 'сжатие'])
@variant.arg(second_n=[2, 3])
@variant.arg(third=['изобарическое', 'изохорическое'])
@variant.arg(third_what=['нагревание', 'охлаждение'])
@variant.arg(third_n=[2, 3])
class GraphPV_2(variant.VariantTask):
    pass


@variant.solution_space(120)
@variant.text('''
    Небольшую цилиндрическую пробирку с воздухом погружают на некоторую глубину в глубокое пресное озеро,
    после чего воздух занимает в ней лишь {ratio} часть от общего объема.
    Определите глубину, на которую погрузили пробирку.
    Температуру считать постоянной {T:Task:e}, давлением паров воды пренебречь,
    атмосферное давление принять равным {Consts.p_atm:Task:e}.
''')
@variant.arg(ratio__n=[
    ('третью', 3),
    ('четвертую', 4),
    ('пятую', 5),
    ('шестую', 6),
])
@variant.arg(T=[f'T = {t+5+273} К' for t in range(15)])
@variant.answer_align([
    'T\\text{ — const } &\\implies P_1V_1 = \\nu RT = P_2V_2.',
    'V_2 = \\frac 1{n} V_1 &\\implies P_1V_1 = P_2 * \\frac 1{n}V_1 \\implies P_2 = {n}P_1 = {n}{Consts.p_atm:L}.',
    'P_2 = {Consts.p_atm:L} + {Consts.water.rho:L} {Consts.g_ten:L} h \\implies '
    'h = \\frac{ P_2 - {Consts.p_atm:L} }{ {Consts.water.rho:L} {Consts.g_ten:L} }'
    ' &= \\frac{ {n}{Consts.p_atm:L} - {Consts.p_atm:L} }{ {Consts.water.rho:L} {Consts.g_ten:L} }'
    ' = \\frac{ {n_1} * {Consts.p_atm:L} }{ {Consts.water.rho:L} {Consts.g_ten:L} } = ',
    ' &= \\frac{ {n_1} * {Consts.p_atm:V} }{ {Consts.water.rho:V} *  {Consts.g_ten:V} } \\approx {h:V}.'
])
class ZFTSH_10_2_9_kv(variant.VariantTask):
    def GetUpdate(self, ratio=None, n=None, T=None, **kws):
        return dict(
            n_1=n - 1,
            h='%d м' % ((n - 1) * Consts.p_atm.Value * 1000 / Consts.water.rho.Value / Consts.g_ten.Value),
        )


@variant.solution_space(120)
@variant.text('''
    В замкнутом сосуде объёмом {V:Value:e} находится {gas.Name} ($\\mu = {gas.mu:V}$) под давлением ${p}\\units{ атм }$.
    Определите массу газа в сосуде и выразите её в граммах, приняв температуру газа равной ${t}\\celsius$.
''')
@variant.arg(gas=[
    Consts.gas_air,
    Consts.gas_n2,
    Consts.gas_o2,
    Consts.gas_co2,
    Consts.gas_ne,
    Consts.gas_ar,
])
@variant.arg(V=[f'{V} л' for V in [2, 3, 4, 5]])
@variant.arg(p=[2.5, 3, 3.5, 4, 4.5, 5])
@variant.arg(t=[7, 17, 27, 37, 47])
@variant.answer_short('''
    PV = \\frac m\\mu RT \\implies m = \\frac{ PV \\mu }{ RT } =
    \\frac{ {P:V} * {V:V} *  {gas.mu:V} }{ {Consts.R:V} *  \\cbr{ {t} + 273 }\\units{{К}} }
    \\approx {m:V}.
''')

class ZFTSH_10_2_2_kv(variant.VariantTask):
    def GetUpdate(self, gas=None, V=None, p=None, t=None, **kws):
        return dict(
            P='%.1f атм' % p,
            m='%.2f г' % (p * Consts.p_atm.Value * 1000 * V.Value * gas.mu.Value / 1000 / Consts.R.Value / (t + 273)),
        )


@variant.solution_space(120)
@variant.text('''
    Идеальный газ в экспериментальной установке подвергут политропному процессу $PV^n\\text{ — const }$
    с показателем политропы $n={n}$. В одном из экспериментов объём газа {what} в ${how}$ раза.
    Как при этом изменилась температура газа (выросла или уменьшилась, на сколько или во сколько раз)?
''')
@variant.arg(what=['увеличился', 'уменьшился'])
@variant.arg(n=[0.4, 0.7, 1.2, 1.5, 1.8])
@variant.arg(how=[2, 3, 4])
@variant.answer_align([
    'P_1V_1^n &= P_2V_2^n, P_1V_1 = \\nu R T_1, P_2V_2 = \\nu R T_2 \\implies'
    '\\frac{ \\nu R T_1 }{ V_1 } V_1^n = \\frac{ \\nu R T_2 }{ V_2 } V_2^n \\implies',
    '\\implies T_1V_1^{ n-1 } &= T_2V_2^{ n - 1 } \\implies'
    '\\frac{ T_2 }{ T_1 } = \\cbr{ \\frac{ V_1 }{ V_2 } }^{ n-1 } \\approx {ans}'
])
class Polytrope(variant.VariantTask):
    def GetUpdate(self, what=None, n=None, how=None, **kws):
        ans = how ** (n - 1)
        if what == 'увеличился':
            ans = 1 / ans
        return dict(
            ans='%.3f' % ans,
        )
