import itertools

import generators.variant as variant


@variant.text('''
    Для частицы, движущейся с релятивистской скоростью, 
    выразите ${x}$ и ${y}$ через $m$, ${a}$ и ${b}$, где
    $E_\\text{ кин }$~--- кинетическая энергия частицы,
    $E_0$~--- её энергия покоя,
    а $p, v, m$~--- её импульс, скорость и масса.
''')
@variant.arg(x__y__a__b=itertools.permutations([
    'E_\\text{кин}',
    'E_0',
    'p',
    'v',
], 4))
@variant.solution_space(200)
class Equations(variant.VariantTask):
    pass
