import generators.variant as variant

from generators.helpers import letter_variants, Fraction, Consts

import math


@variant.text('''
    Луч падает из воздуха/вакуума на стекло с показателем преломления {n}. 
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
@variant.solution_space(80)
@variant.arg(n='1.35/1.45/1.55/1.65')
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
