import generators.variant as variant

from generators.helpers import letter_variants, Fraction, Consts

import math


@variant.text('''
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Template(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )
