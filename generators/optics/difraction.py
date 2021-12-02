import generators.variant as variant

# @variant.text('''
#     Расстояние между соседними темными интерференционными полосами на экране Ах.
#     Два когерентных источника света лежат в плоскости, параллельной экрану, на расстоянии Г, от него.
#     Длина световой волны ^. Каково расстояние между источниками света?
# ''')
# @variant.solution_space(100)
# class Vishnyakova_3_6_13(variant.VariantTask):
#     pass


@variant.text('''
    На дифракционную решётку, имеющую период {d:V:e}, нормально падает монохроматическая световая волна.
    Под углом ${phi}\\degrees$ наблюдается дифракционный максимум {which} порядка.
    Какова длина волны падающего света?
''')
@variant.solution_space(150)
@variant.arg(which='второго/третьего/четвёртого')
@variant.arg(d='d = 2/3/4 10^{-4} см')
@variant.arg(phi='20/25/30/35/40')
class Vishnyakova_3_6_15(variant.VariantTask):
    pass


@variant.text('''
    Свет с длиной волны {lmbd:V:e} падает нормально на дифракционную решётку с периодом, равным {d:V:e}.
    Под каким углом наблюдается дифракционный максимум первого порядка?
''')
@variant.solution_space(150)
@variant.arg(lmbd='\\lambda = 0.4/0.5/0.6/0.7 мкм')
@variant.arg(d='d = 1/2/3 мкм')
class Vishnyakova_3_6_16(variant.VariantTask):
    pass


@variant.text('''
    При нормальном падении белого света на дифракционную решётку {color} линия ({lmbd:V:e})
    в спектре {which} порядка видна под углом дифракции ${phi}\\degrees$.
    Определить число штрихов на {l:V:e} длины этой решётки.
''')
@variant.solution_space(150)
@variant.arg(which='второго/третьего/четвёртого')
@variant.arg(color__lmbd=[
    ('зелёная', '\\lambda = 520 нм'),
    ('зелёная', '\\lambda = 550 нм'),
    ('синяя', '\\lambda = 450 нм'),
    ('синяя', '\\lambda = 480 нм'),
    ('жёлтая', '\\lambda = 570 нм'),
    ('жёлтая', '\\lambda = 580 нм'),
    ('оранжевая', '\\lambda = 600 нм'),
    ('красная', '\\lambda = 720 нм'),
    ('красная', '\\lambda = 680 нм'),
])
@variant.arg(phi=[5, 12, 18, 25])
@variant.arg(l=['1 мм', '1 см'])
class Vishnyakova_3_6_17(variant.VariantTask):
    pass


@variant.text('''
    Каков наибольший порядок спектра, который можно наблюдать при дифракции света
    с длиной волны $\\lambda$, на дифракционной решётке с периодом $d = {n}\\lambda$?
''')
@variant.solution_space(150)
@variant.arg(n='2.2/2.5/2.7/3.3/3.5/3.9/4.1/4.5/4.6')
class Vishnyakova_3_6_18(variant.VariantTask):
    pass
