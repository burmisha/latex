import generators.variant as variant

from generators.helpers import letter_variants, Fraction, Consts

import math


@variant.text('''
    Луч падает из {what} на стекло с показателем преломления {n}.
    Сделайте рисунок (без рисунка и отмеченных углов задача не проверяется) и определите:
    \\begin{itemize}
        \\item угол отражения,
        \\item угол преломления,
        \\item угол между падающим и отраженным лучом,
        \\item угол между падающим и преломленным лучом,
        \\item угол отклонения луча при преломлении,
    \\end{itemize}
    если {which} равен ${alpha_base}\\degrees$.
''')
@variant.solution_space(100)
@variant.arg(n='1.35/1.45/1.55/1.65')
# @variant.arg(what='воздуха/вакуума')  # TODO: enable
@variant.arg(which=['угол падения', 'между падающим лучом и границей раздела сред'])
@variant.arg(alpha_base=[22, 28, 35, 40, 50, 55, 65])
@variant.answer_align([
    '\\alpha &= {alpha}\\degrees,',
    '1 * \\sin \\alpha &= n \\sin \\beta \\implies \\beta = \\arcsin\\cbr{ \\frac{\\sin \\alpha}{ n } } \\approx {beta:.2f}\\degrees,',
    '\\varphi_1 &= \\alpha \\approx {phi1}\\degrees,',
    '\\varphi_2 &= \\beta \\approx {phi2:.2f}\\degrees,',
    '\\varphi_3 &= 2\\alpha = {phi3}\\degrees,',
    '\\varphi_4 &= 180\\degrees - \\alpha + \\beta \\approx {phi4:.2f}\\degrees,',
    '\\varphi_5 &= \\alpha - \\beta \\approx {phi5:.2f}\\degrees.',
])
class Refraction01(variant.VariantTask):
    def GetUpdate(self, *, n=None, which=None, alpha_base=None):
        alpha = {
            'угол падения': alpha_base,
            'между падающим лучом и границей раздела сред': 90 - alpha_base,
        }[which]
        beta = math.asin(math.sin(alpha_base / 180 * math.pi) / float(n)) / math.pi * 180
        return dict(
            alpha=alpha,
            beta=beta,
            phi1=alpha,
            phi2=beta,
            phi3=2 * alpha,
            phi4=180 - alpha + beta,
            phi5=alpha - beta,
        )


@variant.text('''
    На плоскопараллельную стеклянную пластинку под углом ${angle}\\degrees$
    падают два параллельных луча света, расстояние между которыми {d:V:e}.
    Определите расстояние между точками, в которых эти лучи выходят из пластинки.
''')
@variant.solution_space(80)
@variant.arg(d='d = 3/4/5/6/7/8 см')
@variant.arg(angle=[35, 40, 50, 55])
@variant.answer_short('\\ell = \\frac{d:L:s}{\\cos \\alpha} \\approx {l:V}')
class Chernoutsan_13_12(variant.VariantTask):
    def GetUpdate(self, *, angle=None, d=None):
        cos = math.cos(angle / 180 * math.pi)
        return dict(
            l=(d / cos).IncPrecision(2).As('мм'),
        )


@variant.text('''
    Солнце составляет с горизонтом угол, синус которого {sin}.
    Шест высотой {H:V:e} вбит в дно водоема глубиной {h:V:e}.
    Найдите длину тени от этого шеста на дне водоема, если показатель преломления воды {n}.
''')
@variant.solution_space(80)
@variant.arg(sin='0.5/0.6/0.7/0.8')
@variant.arg(H='120/130/140/150/160/170/180 см')
@variant.arg(h='70/80/90 см')
@variant.arg(n=['1.33'])
@variant.answer_short('''
    n \\sin \\beta = 1 * \\cos \\alpha \\implies \\beta \\approx {beta:.1f}\\degrees,
    L = (H - h)\\ctg \\alpha + h \\tg \\beta \\approx {L:V}.
''')
class Chernoutsan_13_13(variant.VariantTask):
    def GetUpdate(self, *, sin=None, H=None, h=None, n=None):
        sin_a = float(sin)
        cos_a = (1 - sin_a ** 2) ** 0.5
        l1 = float(H.SI_Value - h.SI_Value) * cos_a / sin_a

        sin_b = cos_a / float(n)
        cos_b = (1 - sin_b ** 2) ** 0.5
        l2 = float(h.SI_Value) * sin_b / cos_b

        L = l1 + l2

        return dict(
            beta=math.asin(sin_b) / math.pi * 180,
            L=f'{L * 100:.1f} см',
        )


@variant.text('''
    Луч света падает на плоское зеркало под углом, синус которого {sin}.
    На сколько миллиметров сместится отраженный луч,
    если на зеркало положить прозрачную пластину толщиной {d:V:e} с показателем преломления {n:V:e}?
''')
@variant.solution_space(80)
@variant.arg(sin='0.65/0.75/0.85')
@variant.arg(d='d = 11/12/13/14/15/16/17/18/19 мм')
@variant.arg(n='n = 1.3/1.35/1.4/1.45/1.5/1.55/1.6')
@variant.answer_short('1 * \\sin \\alpha = n * \\sin \\beta \\implies \\beta \\approx {beta:.1f}, L = 2 d \\tg \\alpha - 2 d \\tg \\beta \\approx {L:V}')
class Chernoutsan_13_14(variant.VariantTask):
    def GetUpdate(self, *, sin=None, d=None, n=None):
        cos = (1 - float(sin) ** 2) ** 0.5
        sin_b = float(sin) / float(n.SI_Value)
        cos_b = (1 - float(sin_b) ** 2) ** 0.5
        return dict(
            beta=math.asin(sin_b) / math.pi * 180,
            L=(2 * d * (float(sin) / cos - sin_b / cos_b)).IncPrecision(1).As('мм'),
        )


@variant.text('''
    В некотором прозрачном веществе свет распространяется со скоростью,
    {how} меньшей скорости света в вакууме. Чему будет равен предельный угол
    внутреннего отражения для поверхности раздела этого вещества с {what}?
''')
@variant.solution_space(80)
@variant.arg(how__N1=[('вдвое', 2), ('втрое', 3), ('вчетверо', 4)])
@variant.arg(what__N2=[('воздухом', 1), ('водой', 1.33)])
@variant.answer_short('n_1 = \\frac c v = {N1}, n_1 \\sin \\varphi_\\text{п.в.о.} = n_2 \\sin \\frac \\pi 2 \\implies \\varphi_\\text{п.в.о.} \\approx {phi:.1f}\\degrees.')
class Chernoutsan_13_15(variant.VariantTask):
    def GetUpdate(self, *, how=None, N1=None, what=None, N2=None):
        return dict(
            phi=math.asin(N2 / N1) / math.pi * 180,
        )


# 13.16. Широкий непрозрачный сосуд доверху наполнен жидкостью с показателем преломления 1,25. Поверхность жидкости закрыли тонкой непрозрачной пластиной, в которой имеется отверстие радиусом 2 см. Определите диаметр (в см) светлого пятна на дне сосуда, если он освещается рассеянным светом облачного неба, идущим со всех направлений. Толщина слоя жидкости 6 см.
# 13.17. В стекле с показателем преломления 1,5 имеется сферическая полость радиусом 9 см, заполненная водой с показателем преломления 4/3. На полость падают параллельные лучи света. Определите радиус (в см) светового пучка, который проникает в полость.
# 13.18. При переходе луча света из первой среды во вторую угол преломления 45°, а при переходе из первой среды в третью угол преломления 30° (при том же угле падения). Найдите предельный угол (в градусах) полного внутреннего отражения для луча, идущего из третьей среды во вторую.
# 13.19. Угол падения луча света из воздуха на слой воды толщиной 40 см равен углу полного внутреннего отражения для воды. Вычислите смещение (в см) луча в результате прохождения этого слоя воды. Показатель преломления воды 4/3.
# 13.20. Между точечным источником света и наблюдателем поместили стеклянную пластину толщиной 24 мм. На сколько миллиметров сместится видимое положение источника? Показатель преломления стекла 1,5. Пластина перпендикулярна линии наблюдения, углы считать малыми, т. е. {24 = зто.
# 13.21. Пловец, нырнувший с открытыми глазами, рассматривает из под воды светящийся предмет, находящийся над его головой на высоте 75 см над поверхностью воды. Какова будет видимая`высота (в см) предмета над поверхностью воды? Показатель преломления воды 4/3. Углы считать малыми, т. е. {20 = зто.
# 13.22. На дне сосуда с водой лежит плоское зеркало. Толщина слоя воды 16 см. На расстоянии 20 см от поверхности воды находится точечный источник света. На каком расстоянии (в см) от зеркала находится его изображение, образуемое лучами, вышедшими обратно из воды? Показатель преломления воды 4/3. Углы считать малыми, т. е. 120 = зто.
# 13.23. Аквариум из тонкого стекла имеет форму шара радиусом 3 м. Аквариум заполнили водой и запустили туда маленькую рыбку. В какой-то момент рыбка оказалась между глазами наблюдателя и центром шара, на расстоянии | мот центра. На сколько сантиметров кажущееся положение рыбки будет ближе реального? Показатель преломления воды 4/3. ›
