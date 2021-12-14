import generators.variant as variant
from generators.helpers import Consts, n_times
import math


@variant.text('''
    Определить абсолютный показатель преломления прозрачной среды,
    в которой распространяется свет с длиной волны {lmbd:V:e} и частотой {nu:V:e}.
    Скорость света в вакууме {c:V:e}.
''')
@variant.solution_space(80)
@variant.arg(lmbd='\\lambda = 0.450/0.500/0.550/0.600/0.650 мкм')
@variant.arg(n='n = 1.3/1.4/1.5/1.6/1.7')
@variant.answer_short('''
    n = \\frac{c:L:s}{v}
    = \\frac{c:L:s}{\\frac \\lambda T}
    = \\frac{c:L:s}{\\lambda \\nu}
    = \\frac{c:V:s}{{lmbd:V} * {nu:V:s}}
    \\approx{answer_n:V}
''')
class Vishnyakova_3_6_2(variant.VariantTask):
    def GetUpdate(self, *, lmbd=None, n=None):
        c = Consts.c
        nu = (c / lmbd / n).IncPrecision(1).As('ТГц').SetLetter('\\nu')
        return dict(
            nu=nu,
            c=c,
            answer_n=(c / lmbd / nu),
        )


# @variant.text('''
#     Ha рисунке показан ход луча света, проходящего из среды с показателем преломления п,
#     через плоскопараллельную пластинку с показателем пре ломления п›
#     в среду с показателем преломления п.
#     Определить соотношения между показателями преломления сред, используя символы >, < или =.
# ''')
# @variant.solution_space(180)
# @variant.arg(a='a = 1 м')
# class Vishnyakova_3_6_3(variant.VariantTask):
#     pass


@variant.text('''
    На дне водоема глубиной {h:V:e} лежит зеркало.
    Луч света, пройдя через воду, отражается от зеркала и выходит из воды.
    Найти расстояние между точкой входа луча в воду и точкой выхода луча из воды,
    если показатель преломления воды {n:V:e}, а угол падения луча ${alpha}\\degrees$.
''')
@variant.solution_space(120)
@variant.arg(h='h = 2/3/4 м')
@variant.arg(n=['n = 1.33'])
@variant.arg(alpha=[25, 30, 35])
@variant.answer_align([
    '\\ctg \\beta &= \\frac{h:L:s}{d:L:s} \\implies d = \\frac{h:L:s}{\\ctg \\beta}',
    '\\frac 1{\\sin^2 \\beta} &= \\ctg^2 \\beta + 1 \\implies \\ctg \\beta = \\sqrt{\\frac 1{\\sin^2 \\beta} - 1}',
    '\\sin\\alpha &= n\\sin \\beta \\implies \\sin \\beta = \\frac{\\sin\\alpha}{n:L:s}',
    'd &= \\frac{h:L:s}{\\sqrt{\\frac 1{\\sin^2 \\beta} - 1}} '
    '= \\frac{h:L:s}{\\sqrt{\\sqr{\\frac{n:L:s}{\\sin\\alpha}} - 1}}',
    '2d &= \\frac{2{h:L:s}}{\\sqrt{\\sqr{\\frac{n:L:s}{\\sin\\alpha}} - 1}} \\approx {d2:V}',
])
class Vishnyakova_3_6_4(variant.VariantTask):
    def GetUpdate(self, *, h=None, n=None, alpha=None):
        sin = math.sin(float(alpha) / 180 * math.pi)
        d_value = float(h.SI_Value) * 2 * ((float(n.SI_Value) / sin) ** 2 - 1) ** -0.5
        return dict(
            d2=f'2d = {d_value * 100:.1f} см',
        )


@variant.text('''
    Луч света падает на {how} расположенную стеклянную пластинку толщиной {d:V:e}.
    Пройдя через пластину, он выходит из неё в точке, смещённой по {how2} от точки падения на расстояние {h:V:e}.
    Показатель преломления стекла {n:V:e}. Найти синус угла падения.
''')
@variant.solution_space(120)
@variant.arg(how__how2=[('горизонтально', 'горизонтали'), ('вертикально', 'вертикали')])
@variant.arg(d='d = 1.2/1.3/1.4/1.5/1.6 см')
@variant.arg(h='h = 4/5/6 мм')
@variant.arg(n='n = 1.4/1.5/1.6')
@variant.answer_align([
    '\\ctg \\beta &= \\frac{h:L:s}{d:L:s} \\implies',
    '\\implies \\frac 1{\\sin^2 \\beta} &= \\ctg^2 \\beta + 1 = \\sqr{\\frac{h:L:s}{d:L:s}} + 1 \\implies',
    '\\implies \\sin\\alpha &= n\\sin \\beta = n\\sqrt {\\frac 1{\\sqr{\\frac{h:L:s}{d:L:s}} + 1}} \\approx {sin:.2f}',
])
class Vishnyakova_3_6_5(variant.VariantTask):
    def GetUpdate(self, *, how=None, how2=None, d=None, h=None, n=None):
        ctg_b = float((d / h).SI_Value)
        sin_b = 1 / (ctg_b ** 2 + 1) ** 0.5
        sin_a = float(n.SI_Value) * sin_b
        assert 0.1 <= sin_a <= 0.9, [sin_a, sin_b, h, d]
        return dict(
            sin=sin_a,
        )


@variant.text('''
    Найти оптическую силу собирающей линзы, если действительное изображение предмета,
    помещённого в {a:V:e} от линзы, получается на расстоянии {b:V:e} от неё.
''')
@variant.solution_space(180)
@variant.arg(a='a = 15/35/35/55 см')
@variant.arg(b='b = 20/30/40 см')
class Vishnyakova_3_6_6(variant.VariantTask):
    pass


@variant.text('''
    Найти увеличение изображения, если изображение предмета, находящегося
    на расстоянии {a:V:e} от линзы, получается на расстоянии {b:V:e} от неё.
''')
@variant.solution_space(180)
@variant.arg(a='a = 15/20/25 см')
@variant.arg(b='b = 12/18/30 см')
class Vishnyakova_3_6_7(variant.VariantTask):
    pass


@variant.text('''
    Расстояние от предмета до линзы {a:V:e}, а от линзы до мнимого изображения {b:V:e}.
    Чему равно фокусное расстояние линзы?
''')
@variant.solution_space(180)
@variant.arg(a='a = 8/10/12 см')
@variant.arg(b='b = 20/25/30 см')
class Vishnyakova_3_6_8(variant.VariantTask):
    pass


@variant.text('''
    Две тонкие линзы с фокусными расстояниями {f_1:V:e} и {f_2:V:e} сложены вместе.
    Чему равно фокусное расстояние такой оптической системы?
''')
@variant.solution_space(180)
@variant.arg(f_1='f_1 = 12/18/25 см')
@variant.arg(f_2='f_2 = 20/30 см')
class Vishnyakova_3_6_9(variant.VariantTask):
    pass


@variant.text('''
    Линейные размеры прямого изображения предмета, полученного в собирающей линзе,
    в {n_word} больше линейных размеров предмета.
    Зная, что предмет находится на {l:V:e} ближе к линзе,
    чем его изображение, найти оптическую силу линзы.
''')
@variant.solution_space(180)
@variant.arg(l='l = 20/25/30/35/40 см')
@variant.arg(n__n_word=n_times(2, 3, 4))
class Vishnyakova_3_6_10(variant.VariantTask):
    pass


@variant.text('''
    Оптическая сила объектива фотоаппарата равна {D:V:e}.
    При фотографировании чертежа с расстояния {a:V:e} площадь изображения
    чертежа на фотопластинке оказалась равной {S:V:e}.
    Какова площадь самого чертежа? Ответ выразите в квадратных сантиметрах.
''')
@variant.solution_space(180)
@variant.arg(D='D = 3/4/5/6 дптр')
@variant.arg(a='a = 0.8/0.9/1.1/1.2 м')
@variant.arg(S='S = 4/9/16 см^2')
class Vishnyakova_3_6_11(variant.VariantTask):
    pass
