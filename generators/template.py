import generators.variant as variant

from generators.helpers import letter_variants, Fraction, Consts

import math


@variant.text('''
''')
@variant.solution_space(80)
@variant.arg(A=('A = {} a', [1]))
@variant.answer_align([
])
class Template(variant.VariantTask):
    pass
