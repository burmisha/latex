import itertools

import generators.variant as variant
from generators.helpers import Consts

import logging
log = logging.getLogger(__name__)


@variant.text('''
    Проводник массой {m:V:e} и длиной {l:V:e} подвешен на двух нитях горизонтально в однородном горизонтальном магнитном поле индукцией {B:V:e} (см. рис).
    По проводнику протекает электрический ток силой {I:V:e}. Определите, во сколько раз увеличится натяжение нитей, если увеличить {what} в {n} раза.
''')
@variant.solution_space(120)
@variant.arg(m=('m = {} г', [20, 40, 50]))
@variant.arg(l=('l = {} см', [30, 60, 80]))
@variant.arg(I=('\\eli = {} А', [2, 3, 5]))
@variant.arg(B=('B = {} мТл', [20, 40, 50]))
@variant.arg(what=['силу тока', 'индукцию магнитного поля'])
@variant.arg(N=[2, 3, 4])
class Force19(variant.VariantTask):
    pass
