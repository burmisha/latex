import generators.variant as variant
from generators.helpers import Consts, n_times
import math


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
