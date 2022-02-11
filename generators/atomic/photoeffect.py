import generators.variant as variant

from generators.helpers import letter_variants, Fraction, Consts



@variant.text('''
    Свет с энергией кванта {E:V:e} вырывает из металлической пластинки электроны,
    имеющие максимальную кинетическую энергию {K:V:e}.
    Найдите работу выхода (в эВ) электрона из этого металла.
''')
@variant.solution_space(80)
@variant.arg(A='3.5/3.8/4.1 эВ')
@variant.arg(K='1.5/1.7/1.8 эВ')
@variant.answer_align([
])
class Chernoutsan_13_66(variant.VariantTask):
    def GetUpdate(self, *, A=None):
        return dict(
            B=1,
        )


@variant.text('''
    Какой максимальной кинетической энергией (в эВ) обладают электроны,
    вырванные из металла при действии на него ультрафиолетового излучения с длиной волны 0,33 мкм,
    если работа выхода электрона 2,8101? Дж? Постоянная Планка {Consts:h:Task}, заряд электрона {Consts:e:Task}.
''')
@variant.solution_space(80)
@variant.arg(A=('A = {} a', [1]))
@variant.answer_align([
])
class Chernoutsan_13_67(variant.VariantTask):
    def GetUpdate(self, *, A=None):
        return dict(
            B=1,
        )


@variant.text('''
    Чему равно задерживающее напряжение для фотоэлектронов, вырываемых с поверхности металла светом
    с энергией фотонов 7,8:10°° Дж, если работа выхода из этого металла 3-10? Дж? Заряд электрона {Consts:e:Task}.
''')
@variant.solution_space(80)
@variant.arg(A=('A = {} a', [1]))
@variant.answer_align([
])
class Chernoutsan_13_68(variant.VariantTask):
    def GetUpdate(self, *, A=None):
        return dict(
            B=1,
        )


@variant.text('''
    Красная граница фотоэффекта для некоторого металла соответствует длине волны 6,6:107 м.
    Чему равно напряжение, полностью задерживающее фотоэлектроны, вырываемые из этого металла излучением
    с длиной волны 18-105 см? Постоянная Планка {Consts:h:Task}, заряд электрона {Consts:e:Task}.
''')
@variant.solution_space(80)
@variant.arg(A=('A = {} a', [1]))
@variant.answer_align([
])
class Chernoutsan_13_69(variant.VariantTask):
    def GetUpdate(self, *, A=None):
        return dict(
            B=1,
        )


@variant.text('''
    Определите длину волны (в нм) света, которым освещается поверхность металла,
    если фотоэлектроны имеют максимальную кинетическую энергию 6-10-20 Дж,
    а работа выхода электронов из этого металла 6-107! Дж. Постоянная Планка {Consts:h:Task}.
''')
@variant.solution_space(80)
@variant.arg(A=('A = {} a', [1]))
@variant.answer_align([
])
class Chernoutsan_13_70(variant.VariantTask):
    def GetUpdate(self, *, A=None):
        return dict(
            B=1,
        )


@variant.text('''
    Работа выхода электронов из некоторого металла 3,375 эВ. Найдите скорость электронов (в км/с),
    вылетающих с поверхности металла при освещении его светом с длиной волны 2-10`7 м.
    Масса электрона 9-10 кг. Постоянная Планка {Consts:h:Task}, заряд электрона {Consts:e:Task}.
''')
@variant.solution_space(80)
@variant.arg(A=('A = {} a', [1]))
@variant.answer_align([
])
class Chernoutsan_13_71(variant.VariantTask):
    def GetUpdate(self, *, A=None):
        return dict(
            B=1,
        )


@variant.text('''
    Работа выхода электронов из некоторого металла 5,2-1 07° Дж.
    На металл падают фотоны с импульсом .
    Во сколько раз максимальный импульс электронов, вылетающих с поверхности металла при фотоэффекте,
    больше импульса падающих фотонов? Масса электрона {Consts:m_e:Task}.
''')
@variant.solution_space(80)
@variant.arg(p='p = 2.4/2.7/3.0 10**-27 кг м / с')
@variant.answer_align([
])
class Chernoutsan_13_72(variant.VariantTask):
    def GetUpdate(self, *, A=None):
        return dict(
            B=1,
        )
