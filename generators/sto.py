# -*- coding: utf-8 -*-

import variant

import itertools

import logging
log = logging.getLogger(__name__)


@variant.text(u'''
    Для частицы, движущейся с релятивистской скоростью, 
    выразите ${x}$ и ${y}$ через $m$, ${a}$ и ${b}$, где
    $E_\\text{ кин }$~--- кинетическая энергия частицы,
    $E_0$~--- её энергия покоя,
    а $p, v, m$~--- её импульс, скорость и масса.
''')
@variant.args(
    x__y__a__b=itertools.permutations([
        u'E_\\text{кин}',
        u'E_0',
        u'p',
        u'v',
    ], 4),
)
@variant.solution_space(200)
class Equations(variant.VariantTask):
    pass
