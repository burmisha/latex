import generators.variant as variant
from generators.helpers import Consts


@variant.text('''
    Установка для наблюдения интерференции состоит
    из двух когерентных источников света и экрана.
    Расстояние между источниками {l:Task:e},
    а от каждого источника до экрана — {L:Task:e}.
    Сделайте рисунок и укажите положение нулевого максимума освещенности,
    а также определите расстояние между первым {text} и нулевым максимумом.
    Длина волны падающего света составляет {lmbd:Task:e}.
''')
@variant.arg(l=['l = %d мкм' % l for l in [400, 500, 600]])
@variant.arg(L=['L = %d м' % L for L in [2, 4, 5, 6]])
@variant.arg(lmbd=['\\lambda = %d нм' % lmbd for lmbd in [400, 500, 600]])
@variant.arg(text=['максимумом', 'минимумом'])
@variant.solution_space(180)
class Vishnyakova_example_11(variant.VariantTask):
    # d_1^2=L^2 + (h - l/2)^2
    # Вычитаем, приближаем
    # h=lambda L/l = 3,6 мм.
    pass


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
