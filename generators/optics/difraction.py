import generators.variant as variant


@variant.text('''
    На стеклянную пластинку ({n1:Task:e}) нанесена прозрачная пленка ({n2:Task:e}).
    На плёнку нормально к поверхности падает монохроматический свет с длиной волны {lmbd:Task:e}.
    Какова должна быть минимальная толщина пленки, если в результате интерференции свет имеет {text} интенсивность?
''')
@variant.solution_space(180)
@variant.arg(n1=['\\hat n = 1.%d' % n1 for n1 in [5, 6]])
@variant.arg(n2=['n = 1.%d' % n2 for n2 in [2, 4, 7, 8]])
@variant.arg(lmbd=['\\lambda = %d нм' % lmbd for lmbd in [400, 500, 600]])
@variant.arg(text=['наибольшую', 'наименьшую'])
class Belolipetsky_5_196(variant.VariantTask):
    pass


@variant.text('''
    Разность фаз двух интерферирующих световых волн равна ${n:V}\\pi$,
    а разность хода между ними равна {l:V:e}. Определить длину волны.
''')
@variant.solution_space(100)
@variant.arg(n='n = 3/5/7/9')
@variant.arg(l='\\ell= 7.5/9.5/10.5/12.5/15.5 10^{-7} м')
class Vishnyakova_3_6_12(variant.VariantTask):
    pass


# @variant.text('''
#     Расстояние между соседними темными интерференционными полосами на экране Ах.
#     Два когерентных источника света лежат в плоскости, параллельной экрану, на расстоянии Г, от него.
#     Длина световой волны ^. Каково расстояние между источниками света?
# ''')
# @variant.solution_space(100)
# class Vishnyakova_3_6_13(variant.VariantTask):
#     pass


@variant.text('''
    Расстояние между двумя точечными когерентными источниками света $S_1$ u $S_2$ равно {d:V:e}.
    Источники расположены в плоскости, параллельной экрану, на расстоянии {a:V:e} от него.
    На экране в точках, лежащих на перпендикулярах, опущенных из источников света $S_1$ и $S_2$,
    находятся два ближайших минимума (тёмные полосы).
    Определите длину световой волны. Ответ дать в нанометрах.
''')
@variant.solution_space(100)
@variant.arg(d='d = 1.5/2/2.5 мм')
@variant.arg(a='a = 7/8/9 м')
class Vishnyakova_3_6_14(variant.VariantTask):
    pass


@variant.text('''
    На дифракционную решетку, имеющую период {d:V:e}, нормально падает монохроматическая световая волна.
    Под углом ${phi}\\degrees$ наблюдается дифракционный максимум второго порядка.
    Какова длина волны падающего света?
''')
@variant.solution_space(100)
@variant.arg(d='d = 2/3/4 10^{-4} см')
@variant.arg(phi='20/25/30/35/40')
class Vishnyakova_3_6_15(variant.VariantTask):
    pass


@variant.text('''
    Свет с длиной волны {lmbd:V:e} падает нормально на дифракционную решетку с периодом, равным {d:V:e}.
    Под каким углом наблюдается дифракционный максимум первого порядка?
''')
@variant.solution_space(100)
@variant.arg(lmbd='\\lambda = 0.4/0.5/0.6/0.7 мкм')
@variant.arg(d='d = 1/2/3 мкм')
class Vishnyakova_3_6_16(variant.VariantTask):
    pass


@variant.text('''
    При нормальном падении белого света на дифракционную решетку {color} линия ({lmbd:V:e})
    в спектре второго порядка видна под углом дифракции ${phi}\\degrees$.
    Определить число штрихов на {l:V:e} длины этой решетки.
''')
@variant.solution_space(100)
@variant.arg(color__lmbd=[
    ('зелёная', '\\lambda = 500 нм'),
])
@variant.arg(phi=[20, 25, 53])
@variant.arg(l=['1 мм', '1 см'])
class Vishnyakova_3_6_17(variant.VariantTask):
    pass


@variant.text('''
    Каков наибольший порядок спектра, который можно наблюдать при дифракции света
    с длиной волны $\\lambda$, на дифракционной решетке с периодом $d = {n}\\lambda$?
''')
@variant.solution_space(100)
@variant.arg(n='2.5/3.5/4.5')
class Vishnyakova_3_6_18(variant.VariantTask):
    pass
