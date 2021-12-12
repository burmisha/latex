import generators.variant as variant
import math

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
@variant.answer_short('''
    d\\sin \\varphi_k = k\\lambda
    \\implies \\lambda = \\frac{d \\sin \\varphi_k}k
    = \\frac{{d:V} * \\sin {phi}\\degrees}{{k}} \\approx {lmbd:V}
''')
class Vishnyakova_3_6_15(variant.VariantTask):
    def GetUpdate(self, *, which=None, d=None, phi=None):
        k = {
            'второго': 2,
            'третьего': 3,
            'четвёртого': 4,
        }[which]
        return dict(
            lmbd=(d * math.sin(math.pi * int(phi) / 180) / k).IncPrecision(2).As('нм'),
            k=k,
        )


@variant.text('''
    Свет с длиной волны {lmbd:V:e} падает нормально на дифракционную решётку с периодом, равным {d:V:e}.
    Под каким углом наблюдается дифракционный максимум первого порядка?
''')
@variant.solution_space(150)
@variant.arg(lmbd='\\lambda = 0.4/0.5/0.6/0.7 мкм')
@variant.arg(d='d = 1/2/3 мкм')
@variant.answer_short('''
    d\\sin \\varphi_k = k\\lambda
    \\implies \\sin \\varphi_k = \\frac{k\\lambda}{ d }
    = \\frac{{k} * {lmbd:V}}{d:V:s} \\approx {sin:V} \\implies \\varphi_k \\approx {phi:.1f}\\degrees
''')
class Vishnyakova_3_6_16(variant.VariantTask):
    def GetUpdate(self, *, lmbd=None, d=None):
        k = 1
        sin = lmbd * k / d
        phi = math.asin(sin.SI_Value) / math.pi * 180
        return dict(
            k=k,
            sin=sin,
            phi=phi,
        )


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
@variant.answer_short('''
    d\\sin \\varphi_k = k\\lambda
    \\implies d = \\frac{k\\lambda}{\\sin \\varphi_k}.
    \\qquad N = \\frac{ l }{d} = \\frac{ l \\sin \\varphi_k}{k\\lambda}
    = \\frac{{l:V} * \\sin {phi}\\degrees}{{k} * {lmbd:V}} \\approx {N:V}
''')
class Vishnyakova_3_6_17(variant.VariantTask):
    def GetUpdate(self, *, which=None, color=None, lmbd=None, phi=None, l=None):
        k = {
            'второго': 2,
            'третьего': 3,
            'четвёртого': 4,
        }[which]
        return dict(
            N=(l * math.sin(math.pi * int(phi) / 180) / k / lmbd).IncPrecision(2),
            k=k,
        )


@variant.text('''
    Каков наибольший порядок спектра, который можно наблюдать при дифракции света
    с длиной волны $\\lambda$, на дифракционной решётке с периодом $d = {n}\\lambda$?
    Под каким углом наблюдается последний максимум?
''')
@variant.solution_space(80)
@variant.arg(n='2.2/2.5/2.7/3.3/3.5/3.9/4.1/4.5/4.6')
@variant.answer_short('''
    d\\sin \\varphi_k = k\\lambda
    \\implies k = \\frac{d\\sin \\varphi_k}{\\lambda} \\le \\frac{d * 1}{\\lambda} = {n}
    \\implies k_{\\max} = {k_max}
    \\implies \\alpha_{{k_max}} \\approx {alpha}\\degrees
''')
class Vishnyakova_3_6_18(variant.VariantTask):
    def GetUpdate(self, *, n=None):
        k = float(n.strip())
        k_max = int(k)
        alpha = math.asin(k_max / k) / math.pi * 180
        return dict(
            k_max=k_max,
            alpha=alpha,
        )
