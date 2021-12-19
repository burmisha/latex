import generators.variant as variant
from generators.helpers import Consts, n_times
import math


@variant.text('''
    Определить абсолютный показатель преломления прозрачной среды,
    в которой распространяется свет с длиной волны {lmbd:V:e} и частотой {nu:V:e}.
    Скорость света в вакууме {c:V:e}.
''')
@variant.solution_space(80)
@variant.arg(lmbd='\\lambda = 0.450/0.500/0.550/0.600/0.650 мкм')
@variant.arg(n='n = 1.3/1.4/1.5/1.6/1.7')
@variant.answer_short('''
    n = \\frac{c:L:s}{v}
    = \\frac{c:L:s}{\\frac \\lambda T}
    = \\frac{c:L:s}{\\lambda \\nu}
    = \\frac{c:V:s}{{lmbd:V} * {nu:V:s}}
    \\approx{answer_n:V}
''')
class Vishnyakova_3_6_2(variant.VariantTask):
    def GetUpdate(self, *, lmbd=None, n=None):
        c = Consts.c
        nu = (c / lmbd / n).IncPrecision(1).As('ТГц').SetLetter('\\nu')
        return dict(
            nu=nu,
            c=c,
            answer_n=(c / lmbd / nu),
        )
