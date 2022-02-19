import generators.variant as variant

from generators.helpers import Fraction, Consts, UnitValue

import math

@variant.text('''
    Вертикально стоящий шест высотой {h:V:e}, освещённый солнцем,
    отбрасывает на горизонтальную поверхность земли тень длиной {l:V:e}.
    Известно, что длина тени от телеграфного столба на {DL:V:e} больше. Определить высоту столба.
''')
@variant.solution_space(80)
@variant.arg(h='h = 1.2/1.5/1.8 м')
@variant.arg(l='\\ell = 1/2/3/4 м')
@variant.arg(DL='\\Delta L = 5/6/7/8/9 м')
@variant.answer_short('\\cfrac{ H }{ h } = \\cfrac{l + \\Delta l}{ l } \\implies H = h \\cbr{1 + \\cfrac{\\Delta l}{ l }} \\approx {H:V}')
class Vishnyakova_3_6_1(variant.VariantTask):
    def GetUpdate(self, *, h=None, l=None, DL=None):
        h = UnitValue('1.1 м')
        return dict(
            H=(h * ((DL / l).SI_Value + 1)).IncPrecision(1),
        )


@variant.text('''
    Определите {what} полутени на экране диска размером {D:Task:e} от протяжённого источника, также обладающего формой диска размером {d:Task:e} (см. рис. на доске, вид сбоку).
    Расстояние от источника до диска равно {l:Task:e}, а расстояние от диска до экрана — {L:Task:e}.
''')
@variant.solution_space(80)
@variant.arg(what='диаметр/радиус')
@variant.arg(d='d = 2/3/4 см')
@variant.arg(D='D = 2/2.5/3/3.5/4 см')
@variant.arg(l='l = 12/15/18 см')
@variant.arg(L='L = 10/20/30 см')
@variant.answer_short('\\cfrac{\\frac d2 + \\frac D2}l = \\cfrac{\\frac d2 + r}{l + L} \\implies r = \\cfrac{Dl + dL + DL}{2l} = \\cfrac D2 + \\cfrac{ L }{ l } * \\cfrac{d+D}2 \\approx {r:V} \\implies 2r \\approx {r2:V}')
@variant.is_one_arg
class Shadow01(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        r_value = ((a.D * a.l).SI_Value + (a.d * a.L).SI_Value + (a.D * a.L).SI_Value) / 2 / a.l.SI_Value
        r = f'{r_value * 100:.1f} см'
        return dict(
            r=r,
            r2=f'{r_value * 100 * 2:.1f} см',
        )


@variant.text('''
    Высота солнца над горизонтом составляет ${phi}\\degrees$. Посреди ровного бетонного поля стоит одинокий цилиндрический столб высотой {H:V:e} и радиусом {R:V:e}.
    Определите площадь полной тени от этого столба на бетоне. Угловой размер Солнца принять равным $30'$ и считать малым углом.
''')
@variant.solution_space(80)
@variant.arg(phi='35/40/50/55')
@variant.arg(H='3/5/7 м')
@variant.arg(R='2/4/8/10 см')
@variant.answer_short('\\text{{figure}} \\implies {S:Task}')
class Shadow02(variant.VariantTask):
    def GetUpdate(self, *, phi=None, H=None, R=None):
        sin = math.sin(int(phi) / 180 * math.pi)
        cos = math.cos(int(phi) / 180 * math.pi)
        R_Value = float(R.SI_Value)
        H_Value = float(H.SI_Value)
        alpha = 0.5 / 180 * math.pi
        if 2 * float(R_Value / H_Value) * sin < alpha:
            figure = 'треугольник'
            S = R_Value ** 2 * cos / alpha * 2
        else:
            figure = 'трапеция'
            S = (2 * R_Value + H_Value * alpha / 2 / sin) * H_Value * cos / sin
        return dict(
            figure=figure,
            S=f'S = {S:.2f} м^2',
        )
