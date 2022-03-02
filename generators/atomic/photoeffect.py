import generators.variant as variant

from generators.helpers import Fraction, Consts


@variant.text('''
    Переведите в джоули:
    \\begin{itemize}
        \\item {E0:V:e},
        \\item {E1:V:e},
        \\item {E2:V:e},
        \\item {E3:V:e},
        \\item {E4:V:e},
        \\item {E5:V:e},
    \\end{itemize}
''')
@variant.solution_space(40)
@variant.arg(E0=['1 эВ'])
@variant.arg(E1='1.3/2.1/3.2/4.3 эВ')
@variant.arg(E2='1.4/13.5/4.6/5.7 МэВ')
@variant.arg(E3='1.5/5.1/6.2/7.3 кэВ')
@variant.arg(E4='1.6/7.2/8.3/9.4 10^{-3} эВ')
@variant.arg(E5='1.7/3.3/5.4 10^7 эВ')
@variant.answer_align([
    '{E1:V} &\\approx {E1_eV:V}',
    '{E2:V} &\\approx {E2_eV:V}',
    '{E3:V} &\\approx {E3_eV:V}',
    '{E4:V} &\\approx {E4_eV:V}',
    '{E5:V} &\\approx {E5_eV:V}',
])
@variant.is_one_arg
class Energy_from_eV(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            E0_eV=(a.E0 * 1).IncPrecision(1).As('Дж'),
            E1_eV=(a.E1 * 1).IncPrecision(1).As('Дж'),
            E2_eV=(a.E2 * 1).IncPrecision(1).As('Дж'),
            E3_eV=(a.E3 * 1).IncPrecision(1).As('Дж'),
            E4_eV=(a.E4 * 1).IncPrecision(1).As('Дж'),
            E5_eV=(a.E5 * 1).IncPrecision(1).As('Дж'),
        )


@variant.text('''
    Переведите в электронвольты:
    \\begin{itemize}
        \\item {E0:V:e},
        \\item {E1:V:e},
        \\item {E2:V:e},
        \\item {E3:V:e},
        \\item {E4:V:e},
        \\item {E5:V:e},
    \\end{itemize}
''')
@variant.solution_space(40)
@variant.arg(E0=['1 Дж'])
@variant.arg(E1='1.3/2.1/3.2/4.3 Дж')
@variant.arg(E2='1.4/13.5/4.6/5.7 мкДж')
@variant.arg(E3='1.5/5.1/6.2/7.3 кДж')
@variant.arg(E4='1.6/7.2/8.3/9.4 10^{-17} Дж')
@variant.arg(E5='1.7/3.3/5.4 10^{-21} Дж')
@variant.answer_align([
    '{E1:V} &\\approx {E1_eV:V}',
    '{E2:V} &\\approx {E2_eV:V}',
    '{E3:V} &\\approx {E3_eV:V}',
    '{E4:V} &\\approx {E4_eV:V}',
    '{E5:V} &\\approx {E5_eV:V}',
])
@variant.is_one_arg
class Energy_to_eV(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            E0_eV=(a.E0 * 1).IncPrecision(1).As('эВ'),
            E1_eV=(a.E1 * 1).IncPrecision(1).As('эВ'),
            E2_eV=(a.E2 * 1).IncPrecision(1).As('эВ'),
            E3_eV=(a.E3 * 1).IncPrecision(1).As('эВ'),
            E4_eV=(a.E4 * 1).IncPrecision(1).As('эВ'),
            E5_eV=(a.E5 * 1).IncPrecision(1).As('эВ'),
        )


@variant.text('''
    Свет с энергией кванта {E:V:e} вырывает из металлической пластинки электроны,
    имеющие максимальную кинетическую энергию {K:V:e}.
    Найдите работу выхода (в эВ) электрона из этого металла.
''')
@variant.solution_space(80)
@variant.arg(E='3.5/3.8/4.1 эВ')
@variant.arg(K='1.5/1.7/1.8 эВ')
@variant.answer_short('A = E - K \\approx {A:V}')
@variant.is_one_arg
class Chernoutsan_13_66(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            A=(a.E - a.K).IncPrecision(1).As('эВ'),
        )


@variant.text('''
    Какой максимальной кинетической энергией (в эВ) обладают электроны,
    вырванные из металла при действии на него ультрафиолетового излучения с длиной волны {lmbd:V:e},
    если работа выхода электрона {A:V:e}? Постоянная Планка {Consts.h:Task:e}, заряд электрона {Consts.e:Task:e}.
''')
@variant.solution_space(80)
@variant.arg(A='A = 2.8/3.2/3.4 10^{-19} Дж')
@variant.arg(lmbd='\\lambda = 0.25/0.33/0.40 мкм')
@variant.answer_short('K = \\frac{hc}{lmbd:L:s} - A \\approx {K:V}')
@variant.is_one_arg
class Chernoutsan_13_67(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        K = Consts.c * Consts.h / a.lmbd - a.A
        assert K.SI_Value > 0
        return dict(
            K=K.IncPrecision(1).As('эВ'),
        )


@variant.text('''
    Чему равно задерживающее напряжение для фотоэлектронов, вырываемых с поверхности металла светом
    с энергией фотонов {E:V:e}, если работа выхода из этого металла {A:V:e}? Заряд электрона {Consts.e:Task:e}.
''')
@variant.solution_space(80)
@variant.arg(E='E = 6.3/7.8/8.5/9.2 10^{-19} Дж')
@variant.arg(A='A = 3/4/5 10^{-19} Дж')
@variant.answer_short('eU = K = E - A \\implies U = \\frac{E - A}{ e } \\approx {U:V}')
@variant.is_one_arg
class Chernoutsan_13_68(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        U = (a.E - a.A) / Consts.e
        assert U.SI_Value > 0
        return dict(
            U=U,
        )


@variant.text('''
    Красная граница фотоэффекта для некоторого металла соответствует длине волны {lmbd0:V:e}.
    Чему равно напряжение, полностью задерживающее фотоэлектроны, вырываемые из этого металла излучением
    с длиной волны {lmbd:V:e}? Постоянная Планка {Consts.h:Task:e}, заряд электрона {Consts.e:Task:e}.
''')
@variant.solution_space(80)
@variant.arg(lmbd0='\\lambda_0 = 5.3/5.7/6.2/6.6 10^{-7} м')
@variant.arg(lmbd='\\lambda = 1.7/2.2/2.6/3.2 10^{-5} см')
@variant.answer_short('eU = K = E - A = \\frac{hc}{lmbd:L:s} - A, \\qquad 0 = \\frac{hc}{lmbd0:L:s} - A \\implies U = \\frac{ \\frac{hc}{lmbd:L:s} - \\frac{hc}{lmbd0:L:s} }{ e } = \\frac{hc}{ e }\\cbr{ \\frac 1{lmbd:L:s} - \\frac 1{lmbd0:L:s}}  \\approx {U:V}')
@variant.is_one_arg
class Chernoutsan_13_69(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        U1 = Consts.h * Consts.c / Consts.e / a.lmbd
        U2 = Consts.h * Consts.c / Consts.e / a.lmbd0
        U = U1 - U2
        assert U.SI_Value > 0
        return dict(
            U=U,
        )


@variant.text('''
    Определите длину волны (в нм) света, которым освещается поверхность металла,
    если фотоэлектроны имеют максимальную кинетическую энергию 6-10-20 Дж,
    а работа выхода электронов из этого металла 6-107! Дж. Постоянная Планка {Consts.h:Task:e}.
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2 a')
@variant.answer_short('K = \\frac{hc}{lmbd:L:s} - A \\approx {K:V}')
@variant.is_one_arg
class Chernoutsan_13_70(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=1,
        )


@variant.text('''
    Работа выхода электронов из некоторого металла 3,375 эВ. Найдите скорость электронов (в км/с),
    вылетающих с поверхности металла при освещении его светом с длиной волны 2-10`7 м.
    Масса электрона 9-10 кг. Постоянная Планка {Consts.h:Task:e}, заряд электрона {Consts.e:Task:e}.
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2 a')
@variant.answer_short('K = \\frac{hc}{lmbd:L:s} - A \\approx {K:V}')
@variant.is_one_arg
class Chernoutsan_13_71(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=1,
        )


@variant.text('''
    Работа выхода электронов из некоторого металла 5,2-1 07° Дж.
    На металл падают фотоны с импульсом .
    Во сколько раз максимальный импульс электронов, вылетающих с поверхности металла при фотоэффекте,
    больше импульса падающих фотонов? Масса электрона {Consts.m_e:Task}.
''')
@variant.solution_space(80)
@variant.arg(p='p = 2.4/2.7/3.0 10**-27 кг м / с')
@variant.answer_short('K = \\frac{hc}{lmbd:L:s} - A \\approx {K:V}')
@variant.is_one_arg
class Chernoutsan_13_72(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=1,
        )


@variant.text('''
    Электрон вылетает из металлической пластинки с кинетической энергией 1,8 эВ.
    Какова длина волны света, вызывающего фотоэффект, если работа выхода электрона
    из металла равна 1,3 эВ? 1эВ = 1,6:10°° Дж, постоянная Планка {Const.h:Task:e},
    модуль заряда электрона {Const.e:Task:e}, скорость света {Const.c:Task:e}.
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Vishnyakova_5_1_1(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    Кинетическая энергия фотоэлектрона составляет 25% от работы выхода.
    Во сколько раз энергия фотона, вырвавшего электрон, больше работы выхода?
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Vishnyakova_5_1_2(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    Найти потенциал, до которого может зарядиться металлическая пластина,
    работа выхода электронов из которой 1,6 эВ, при длительном освещении
    потоком фотонов с энергией 4 эВ. 1эВ = 1.6.1079 Дж, модуль заряда электрона {Const.e:Task:e}.
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Vishnyakova_5_1_3(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    Наибольшая длина волны излучения, способного вызвать фотоэффект у платины,
    равна 0,234 мкм. Какова наибольшая кинетическая энергия вырываемых электронов
    при облучении платины излучением с частотой 1,5`10'° Гц?
    Постоянная Планка {Const.h:Task:e}. Скорость света {Const.c:Task:e}.
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Vishnyakova_5_1_4(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    При облучении некоторого металла светом частотой 2,2-10'° Гц
    фототок прекращается при задерживающей разности потенциалов 6,6 В.
    Определить красную границу фотоэффекта для этого металла.
    Постоянная Планка {Const.h:Task:e}, модуль заряда электрона {Const.e:Task:e},
    скорость света {Const.с:Task:e}.
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Vishnyakova_5_1_5(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    Красная граница фотоэффекта для некоторого металла соответствует длине волны 275 нм.
    Определите задерживающую разность потенциалов для фотоэлектронов,
    вырываемых с поверхности этого металла при освещении его светом с частотой 4,6-10'° Гц.
    Постоянная Планка {Const.h:Task:e}, модуль заряда электрона {Const.e:Task:e}, скорость света {Const.c:Task:e}.
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Vishnyakova_5_1_6(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    На фотокатод, для которого красная граница фотоэффекта равна 240 нм,
    приложено запирающее напряжение 1 В, при котором фототок прекратился.
    Какова частота падающего на фотокатод света? Постоянная Планка {Const.h:Task:e},
    модуль заряда электрона {Const.e:Task:e}, скорость света {Const.c:Task:e}.
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Vishnyakova_5_1_7(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    При облучении некоторого металла светом с частотой 9.10“ Гц
    фототок прекращается при задерживающей разности потенциалов 1,8 В.
    Найти задерживающую разность потенциалов для излучения с частотой Ш: 105 Гц.
    Постоянная Планка {Const.h:Task:e}, модуль заряда электрона {Const.e:Task:e}.
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Vishnyakova_5_1_8(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )
