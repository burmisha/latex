import itertools

import generators.variant as variant
from generators.helpers import Consts, letter_variants, n_times, UnitValue, Fraction

import math


@variant.solution_space(0)
@variant.text('''
    Установите каждой букве в соответствие ровно одну цифру и запишите ответ (только цифры, без других символов).

    {lv.Questions}.

    {lv.Options}.
''')
@variant.answer_test('{lv.Answer}')
@variant.arg(lv=letter_variants(
    {
        '$\\Phi$': '$L\\eli$',
        '$\\Delta \\eli$': '$\\eli_2 - \\eli_1$',
        '$\\Delta \\Phi$': '$\\Phi_2 - \\Phi_1$',
    },
    ['$\\frac{L}{\\eli}$', '$\\frac{\\eli}{L}$', '$\\eli_1 - \\eli_2$', '$\\Phi_1 - \\Phi_2$'],
    answers_count=3,
    mocks_count=3,
))
@variant.answer_short('{lv.Answer}')
class Definitions01(variant.VariantTask):
    pass


@variant.solution_space(0)
@variant.text('''
    Установите каждой букве в соответствие ровно одну цифру и запишите ответ (только цифры, без других символов).

    {lv.Questions}.

    {lv.Options}.
''')
@variant.answer_test('{lv.Answer}')
@variant.arg(lv=letter_variants(
    {
        'индукция магнитного поля': '$\\vec B$',
        'поток магнитной индукции': '$\\Phi$',
        'индуктивность': '$L$',
        'электрический ток': '$\\eli$',
        'электрический заряд': '$q$',
    },
    ['$R$', '$g$', '$\\phi$'],
    answers_count=3,
    mocks_count=2,
))
@variant.answer_short('{lv.Answer}')
class Definitions02(variant.VariantTask):
    pass


@variant.solution_space(0)
@variant.text('''
    Установите каждой букве в соответствие ровно одну цифру и запишите ответ (только цифры, без других символов).

    {lv.Questions}.

    {lv.Options}.
''')
@variant.answer_test('{lv.Answer}')
@variant.arg(lv=letter_variants(
    {
        'индукция магнитного поля': 'Тл',
        'поток магнитной индукции': 'Вб',
        'индуктивность': 'Гн',
        'время': 'с',
    },
    ['м', 'Кл', 'А'],
    answers_count=3,
    mocks_count=2,
))
@variant.answer_short('{lv.Answer}')
class Definitions03(variant.VariantTask):
    pass


@variant.text('''
	В катушке, индуктивность которой равна {L:V:e}, сила тока равномерно уменьшается
	с {I1:V:e} до {I2:V:e} за {t:V:e}. Определите ЭДС самоиндукции, ответ выразите в мВ и округлите до целых.
''')
@variant.arg(I1=('\\eli_1 = {} А', [7, 8, 9]))
@variant.arg(I2=('\\eli_2 = {} А', [1, 2, 3, 4]))
@variant.arg(L=('L = {} мГн', [4, 5, 6, 7]))
@variant.arg(t=('\\Delta t = {} c', [0.2, 0.3, 0.4, 0.5]))
@variant.answer_test('{E_answer}')
@variant.answer_short('''
    {E:Letter}
    = {L:L}\\frac{\\abs{\\Delta \\eli}}{{t:L}}
    = {L:L}\\frac{\\abs{{I2:L} - {I1:L}}}{{t:L}}
    = {L:V} * \\frac{\\abs{{I2:V} - {I1:V}}}{{t:V}}
    \\approx {E:V} \\to {E_answer}
''')
@variant.solution_space(60)
class Find_E_easy(variant.VariantTask):
    def GetUpdate(self, I1=None, I2=None, t=None, L=None):
        E = abs(I1.Value - I2.Value) / t.Value * L.Value
        E_answer = int(E + 0.5)

        assert E_answer >= 10, [E_answer]
        return dict(
            E=f'\\ele = {E:.3f} мВ',
            E_answer=E_answer,
        )


@variant.text('''
	В катушке, индуктивность которой равна {L:V:e}, течёт электрический ток силой {I:V:e}.
	Число витков в катушке: {n}. Определите магнитный поток, пронизывающий 1 виток катушки.
	Ответ выразите в милливеберах и округлите до целых.
''')
@variant.arg(I=('\\eli = {} А', [5, 6, 7]))
@variant.arg(L=('L = {} мГн', [50, 60, 70, 80, 90]))
@variant.arg(n=[20, 30, 40])
@variant.answer_test('{Phi1_answer}')
@variant.answer_short('''
    {Phi1:L}
    = \\frac{\\Phi}{N}
    = \\frac{{L:L}{I:L}}{N}
    = \\frac{{L:V} * {I:V}}{{n}}
    \\approx {Phi1:V}
    \\to {Phi1_answer}
''')
@variant.solution_space(60)
class Find_Phi_1(variant.VariantTask):
    def GetUpdate(self, I=None, L=None, n=None):
        Phi1 = L.Value * I.Value / n
        Phi1_answer = int(Phi1 + 0.5)

        assert Phi1_answer >= 5, [Phi1, Phi1_answer]
        return dict(
            Phi1=f'\\Phi_\\text{{1 виток}} = {Phi1:.3f} мВб',
            Phi1_answer=Phi1_answer,
        )


@variant.text('Определите энергию магнитного поля в катушке индуктивностью {L:V:e}, если {what} равен {value:V:e}.')
@variant.solution_space(60)
@variant.arg(L=('L = {} мГн', [200, 300, 400, 600]))
@variant.arg(what__value=[
        ('её собственный магнитный поток', v) for v in ['3 Вб', '4 Вб', '5 Вб', '6 Вб', '7 Вб', '8 Вб']
    ]+ [
        ('протекающий через неё ток', v) for v in ['3 А', '4 А', '5 А', '6 А', '7 А', '8 А']
    ]
)
@variant.answer_short('{answer_short}.')
class W_from_L_or_Phi(variant.VariantTask):
    def GetUpdate(self, what=None, value=None, L=None):
        if 'поток' in what:
            W_value = value.Value ** 2 / 2 / L.Value * 10 ** (0 - L.Power)
            W = UnitValue(f'W = {W_value:.2f} Дж')
            answer_short = f'W = \\frac{{\\Phi^2}}{{2L}} = \\frac{{\\sqr{{{value:V}}}}}{{2 \\cdot {L:V}}} \\approx {W:V}'
        else:
            W_value = value.Value ** 2 * L.Value / 2 * 10 ** L.Power
            W = UnitValue(f'W = {W_value:.2f} Дж')
            answer_short = f'W = \\frac{{L\\eli^2}}2 = \\frac{{{L:V} \\cdot \\sqr{{{value:V}}}}}2 \\approx {W:V}'

        return dict(answer_short=answer_short)


@variant.text('''
    В одной катушке индуктивностью {L:V:e} протекает электрический ток силой {I:V:e}.
    А в другой — с индуктивностью в {n_text} {what} — ток в {m_text} сильнее.
    Определите энергию магнитного поля первой катушки, индуктивность второй катушки
    и отношение энергий магнитного поля в двух этих катушках.
''')
@variant.arg(L=('L_1 = {} мГн', list(range(123, 800, 11))))
@variant.arg(I=('\\eli_1 = {} мА', list(range(450, 900, 23))))
@variant.arg(n__n_text=n_times(2, 3, 4, 5, 6, 7, 8))
@variant.arg(m__m_text=n_times(3, 4, 5, 6))
@variant.arg(what=['больше', 'меньше'])
@variant.answer_short('''
    L_2 = {l:LaTeX}L_1 = {L2:V}, \\quad
    {W1:L} = \\frac{{L:L}{I:L}^2}2 = \\frac{{L:V} * {I:V|sqr}}2 \\approx {W1:V}, \\quad
    \\frac{W_2}{W_1} = \\frac{\\frac{L_2\\eli_2^2}2}{\\frac{L_1\\eli_1^2}2} = {W2_W1:LaTeX}.
''')
@variant.solution_space(90)
class L_W_ratio(variant.VariantTask):
    def GetUpdate(self, L=None, I=None, n=None, n_text=None, m=None, m_text=None, what=None):
        if what == 'больше':
            l = Fraction() * n
            L2 = L.Value * n
        else:
            l = Fraction() / n
            L2 = L.Value / n
        W1 = L.Value * I.Value ** 2 / 2 * 10 ** (L.Power + 2 * I.Power)
        W2_W1 = l * m ** 2
        return dict(
            l=l,
            L2=f'L_2 = {L2:.2f} мГн',
            W1=f'W_1 = {W1:.3f} Дж',
            W2_W1=W2_W1,
        )


@variant.text('''
    Определите индуктивность катушки, если при пропускании тока силой {I:V:e}
    в ней возникает магнитное поле индукцией {B:V:e}.
    Катушка представляет собой цилиндр радиусом {R:V:e} и высотой {h:V:e}.
    Число витков в катушке {n}.
''')
@variant.solution_space(90)
@variant.arg(B=('B = {} Тл', [2, 5, 8]))
@variant.arg(I=('\\eli = {} А', [1.5, 2.5, 3]))
@variant.arg(R=('R = {} см', [3, 4, 5]))
@variant.arg(h=('h = {} мм', [6, 7, 8]))
@variant.arg(n=[200, 400, 500])
@variant.answer_short('''
    \\Phi = L\\eli,
    \\Phi = BSN,
    S=\\pi R^2
    \\implies L = \\frac{\\pi B R^2 N}{\\eli} = \\frac{\\pi * {B:V} * {R:V|sqr} * {n}}{I:V:s}
    \\approx {L:V}.
''')
class L_from_BIRn(variant.VariantTask):
    def GetUpdate(self, B=None, I=None, R=None, h=None, n=None):
        L = math.pi * B.Value * R.Value ** 2 * n / I.Value * 10 ** (B.Power + 2 * R.Power - I.Power)
        return dict(
            L=f'L = {L:.2f} Гн'
        )


@variant.text('''
    Тонкий прямой стержень длиной {l:V:e} вращается в горизонтальной плоскости
    вокруг одного из своих концов. Период обращения стержня {T:V:e}.
    Однородное магнитное поле индукцией {B:V:e} направлено вертикально.
    Чему равна разность потенциалов на концах стержня? Ответ выразите в милливольтах.
''')
@variant.solution_space(120)
@variant.arg(l=('l = {} см', [20, 25, 30, 40, 50]))
@variant.arg(B=('B = {} мТл', [150, 200, 300, 400]))
@variant.arg(T=('T = {} c', [2, 3, 4, 5]))
@variant.answer_short('''
    {E:L}
        = \\frac{\\Delta \\Phi}{\\Delta t}
        = \\frac{B\\Delta S}{\\Delta t}
        = \\frac{B \\frac 12 l^2 \\Delta \\alpha}{\\Delta t}
        = \\frac{B l^2 \\omega}2, \\quad
    \\omega = \\frac{2 \\pi}T \\implies
    \\ele_i = \\frac{\\pi B l^2}T \\approx {E:V}.
''')
class E_rotation(variant.VariantTask):
    def GetUpdate(self, l=None, B=None, T=None):
        E = math.pi * B.Value * l.Value ** 2 / T.Value * 10 ** (B.Power + 2 * l.Power - T.Power) * 1000
        return dict(
            E=f'\\ele_i = {E:.1f} мВ'
        )


@variant.text('''
    Проводник лежит на горизонтальных рельсах,
    замкнутых резистором сопротивлением {R:V:e} (см. рис. на доске). Расстояние между рельсами {l:V:e}.
    Конструкция помещена в вертикальное однородное магнитное поле индукцией {B:V:e}.
    Какую силу необходимо прикладывать к проводнику, чтобы двигать его вдоль рельс с постоянной скоростью {v:V:e}?
    Трением пренебречь, сопротивления рельс и проводника малы по сравнению с сопротивлением резистора.
    Ответ выразите в миллиньютонах.
''')
@variant.solution_space(120)
@variant.arg(l=('l = {} см', [50, 60, 70, 80]))
@variant.arg(R=('R = {} Ом', [2, 3, 4]))
@variant.arg(B=('B = {} мТл', [150, 200, 300, 400]))
@variant.arg(v=('v = {} м / c', [2, 3, 4, 5]))
@variant.answer_short('''
    {F:L}
        = F_A
        = \\eli B l
        = \\frac{\\ele}R * B l
        = \\frac{B v l}R * B l
        = \\frac{B^2 v l^2}R
        = \\frac{{B:V|sqr} * {v:V} * {l:V|sqr}}{R:V:s}
        \\approx {F:V}.
''')

class F_speed(variant.VariantTask):
    def GetUpdate(self, l=None, R=None, B=None, v=None):
        F = B.Value ** 2 * l.Value ** 2 * v.Value / R.Value * 10 ** (2 * B.Power + 2 * l.Power + v.Power - R.Power) * 1000
        return dict(
            F=f'F = {F:.2f} мН'
        )
