import itertools

import generators.variant as variant
from generators.helpers import Consts

import logging
log = logging.getLogger(__name__)


@variant.text('''
    Узкий пучок протонов, нейтронов и электронов влетает в однородное магнитное поле перпендикулярно его линиям (см. рис). 
    Определите отношение скоростей/кинетических энергий/импульсов частиц {first} и {second}, по их трекам.
''')
@variant.solution_space(120)
@variant.arg(first=[1, 2, 3])
@variant.arg(first=[5, 6, 7, 8])
class Force16(variant.VariantTask):
    pass


@variant.text('''
    Частица массой $m$ и зарядом q влетает со скоростью $v$ в однородное магнитное поле индукцией $B$ перпендикулярно его линиям. 
    Определите, за какое время вектор скорости частицы повернётся на ${angle}\\degrees$ (впервые, если таких моментов будет несколько).
''')
@variant.solution_space(120)
@variant.arg(angle=[30, 45, 60, 90, 120, 135, 160, 180])
class Force17(variant.VariantTask):
    pass


@variant.text('''
    {particle} прошедший через ускоряющую разность потенциалов оказывается в магнитном поле индукцией {B:V:e} 
    и движется по окружности диаметром {d:Value}. Сделайте рисунок, определите значение разности потенциалов 
    и укажите, в какой области потенциал больше, а где меньше.
''')
@variant.solution_space(120)
@variant.arg(particle=['Электрон', 'Позитрон', 'Протон'])
@variant.arg(B=('B = {} мТл', [20, 40, 50]))
@variant.arg(d=('d = {} мм', [4, 6, 8]))
class Force18(variant.VariantTask):
    pass

