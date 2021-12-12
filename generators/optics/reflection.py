import generators.variant as variant

from generators.helpers import letter_variants, Fraction, Consts

import math

    # \\begin{tikzpicture}[use optics]
    #     \\node[lens] at (0,0) {};
    #     \\node[mirror] at (1cm,0) {};
    # \\end{tikzpicture}


@variant.text('''
    Постройте изображения $A'B'$ и $C'D'$ стрелок $AB$ и $CD$ в зеркале.


    \\begin{tikzpicture}[rotate={rotate}, circuit ee IEC, thick]
        \\node [contact]  (contact1) at (-1.5, 0) {};
        \\draw  (0, 0) to [resistor={info=$R_1$}] ++(left:1.5);
        \\draw  (0, 0) -- ++(up:1.5) to [resistor={near start, info=$R_2$}, resistor={near end, info=$R_3$}] ++(right:3);
        \\draw  (0, 0) to [resistor={info=$R_4$}] ++(right:3) -- ++(up:1.5);
        {appendix}
    \\end{tikzpicture}
''')
@variant.solution_space(80)
@variant.arg(A=('A = {} a', [1]))
@variant.answer_align([
])
class Reflection01(variant.VariantTask):
    pass
