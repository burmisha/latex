import itertools

import generators.variant as variant
from generators.helpers import Consts, letter_variants, n_times, UnitValue, Fraction

import math


@variant.solution_space(10)
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


@variant.solution_space(10)
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
    ['$R$', '$g$', '$\\varphi$', '$\\ele$'],
    answers_count=3,
    mocks_count=2,
))
@variant.answer_short('{lv.Answer}')
class Definitions02(variant.VariantTask):
    pass


@variant.solution_space(10)
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
        'длина проводника': 'м',
        'время': 'с',
    },
    ['м / с', 'Кл', 'А', 'Вт'],
    answers_count=2,
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


@variant.text('''
    Плоская прямоугольная рамка со сторонами {a:V:e} и {b:V:e} находится в однородном вертикальном магнитном поле
    с индукцией {B:V:e}. Сопротивление рамки {R:V:e}. Вектор магнитной индукции {how} плоскости рамки.
    Рамку повернули на ${angle}\\degrees$ вокруг одной из её горизонтальных сторон. Какой заряд протёк по рамке?
    Ответ выразите в микрокулонах и округлите до целого.
''')
@variant.solution_space(120)
@variant.arg(how=['параллелен', 'перпендикулярен'])
@variant.arg(angle=[30, 60])
@variant.arg(a=('a = {} см', [20, 30, 40]))
@variant.arg(b=('b = {} см', [25, 50, 60]))
@variant.arg(R=('R = {} Ом', [8, 12, 15]))
@variant.arg(B=('B = {} мТл', [120, 150, 200, 300]))
@variant.answer_align([
    '\\ele_i &= - \\frac{\\Delta \\Phi_i}{\\Delta t}, \\eli_i = \\frac{\\ele_i}{R:L:s}, \\Delta q_i = \\eli_i\\Delta t'
        '\\implies \\Delta q_i = \\frac{\\ele_i}{R:L:s} * \\Delta t '
        '= - \\frac 1{R:L:s} \\frac{\\Delta \\Phi_i}{\\Delta t} * \\Delta t'
        '= - \\frac{\\Delta \\Phi_i}{R:L:s} \\implies',

    '\\implies \\Delta q &= q_2 - q_1 = \\sum_i \\Delta q_i '
        '= \\sum_i \\cbr{ - \\frac{\\Delta \\Phi_i}{R:L:s}} '
        '= -\\frac 1{R:L:s} \\sum_i \\Delta \\Phi_i = -\\frac{\\Phi_2 - \\Phi_1}{R:L:s}.',

    'q &= \\abs{\\Delta q} = \\frac {\\abs{\\Phi_2 - \\Phi_1}}{R:L:s}'
        '= \\frac {\\abs{BS \\cos \\varphi_2 - BS \\cos \\varphi_1}}{R:L:s}'
        '= \\frac {B S}{R:L:s}\\abs{\\cos \\varphi_2 - \\cos \\varphi_1}'
        '= \\frac {B a b}{R:L:s}\\abs{\\cos \\varphi_2 - \\cos \\varphi_1},',

    '\\varphi_1 &= {phi1}\\degrees, \\varphi_2 = {phi2}\\degrees,',

    'q&= \\frac {{B:V} * {a:V} * {b:V}}{R:V:s}\\abs{\\cos {phi2}\\degrees - \\cos {phi1}\\degrees} \\approx {q:V} \\to {q_answer}.',
])
class q_from_B_a_b_r(variant.VariantTask):  # Вишнякова 3.4.7
    def GetUpdate(self, B=None, how=None, angle=None, a=None, b=None, R=None):
        if 'перп' in how:
            phi1 = 0
            phi2 = angle
        else:
            phi1 = 90
            phi2 = 90 - angle

        q_value = (
            B.Value * a.Value * b.Value * abs(math.cos(phi2 * math.pi / 180) - math.cos(phi1 * math.pi / 180)) / R.Value
            * 10 ** (B.Power + a.Power + b.Power - R.Power)
        ) * 10 ** 6
        q_answer = int(q_value + 0.5)
        assert q_answer >= 10
        return dict(
            phi1=phi1,
            phi2=phi2,
            q='q = %.2f мкКл' % q_value,
            q_answer=q_answer,
        )


@variant.text('''
    Прямолинейный проводник длиной $\\ell$ перемещают в однородном магнитном поле с индукцией $B$.
    Проводник, вектор его скорости и вектор индукции поля взаимно перпендикулярны.
    Определите зависимость ускорения от времени, если разность потенциалов на концах проводника
    изменяется по закону $\\Delta \\varphi = kt^{n}$.
''')
@variant.solution_space(80)
@variant.arg(n=[2, 3, 4])
@variant.answer_short('''
    \\Delta \\varphi = Bv\\ell = kt^{n} \\implies v = \\frac{kt^{n}}{B\\ell} \\implies a(t) = \\frac{v(t)}{t} = \\frac{kt^{n_1}}{B\\ell}
''')
class a_from_n(variant.VariantTask):  # Вишнякова 3.4.11
    def GetUpdate(self, n=None):
        if n == 2:
            n_1 = '{}'
        else:
            n_1 = n - 1
        return dict(
            n_1=n_1,
        )


@variant.text('''
    При изменении силы тока в проводнике по закону $\\eli = {a} {sign} {b}t$ (в системе СИ),
    в нём возникает ЭДС самоиндукции {E:V:e}. Чему равна индуктивность проводника?
    Ответ выразите в миллигенри и округлите до целого.
''')
@variant.solution_space(80)
@variant.arg(a=[2, 3, 4, 5, 6, 7])
@variant.arg(b=[0.4, 0.5, 0.8, 1.5])
@variant.arg(sign=['-', '+'])
@variant.arg(E=('\\ele = {} мВ', [150, 200, 300, 400]))
@variant.answer_short('''
    {E:L} = L\\frac{\\abs{\\Delta \\eli}}{\\Delta t} = L * \\abs{ {sign} {b} } \\text{(в СИ)}
    \\implies L = \\frac{E:L:s}{ {b} } = \\frac{E:V:s}{ {b} } \\approx {L:V:s}
''')
class L_from_b(variant.VariantTask):  # Вишнякова 3.4.14
    def GetUpdate(self, a=None, b=None, sign=None, E=None):
        L = E.Value / b
        L_answer = int(L + 0.5)
        return dict(
            L=f'L = {L:.1f} мГн',
            L_answer=L_answer,
        )


@variant.text('''
    Резистор сопротивлением {R:Task:e} и катушка индуктивностью {L:Task:e} (и пренебрежимо малым сопротивлением)
    подключены параллельно к источнику тока с ЭДС {E:Task:e} и внутренним сопротивлением {r:Task:e} (см. рис. на доске).
    Какое количество теплоты выделится в цепи после размыкания ключа $K$?
''')
@variant.solution_space(150)
@variant.arg(E=('\\ele = {} В', [5, 6, 8, 12]))
@variant.arg(R=('R = {} Ом', [3, 4, 5]))
@variant.arg(r=('r = {} Ом', [1, 2]))
@variant.arg(L=('L = {} Гн', [0.2, 0.4, 0.5]))
@variant.answer_align([
    '&\\text{закон Ома для полной цепи}: \\eli = \\frac{E:L:s}{r + R_\\text{внешнее}} = \\frac{E:L:s}{r + \\frac{R * 0}{R + 0}} = \\frac{E:L:s}{r:L:s},',
    'Q &= W_m = \\frac{L\\eli^2}2 = \\frac{L\\sqr{\\frac{E:L:s}{r:L:s}}}2 = '
    '\\frac L2\\frac{{E:L}^2}{{r:L}^2} = '
    '\\frac{L:V:s}2 * \\sqr{\\frac{E:V:s}{r:V:s}} \\approx {Q:V}.'
])
class W_kirchgof(variant.VariantTask):  # Вишнякова 3.4 УК
    def GetUpdate(self, E=None, R=None, r=None, L=None):
        Q = L.Value / 2 * (E.Value / r.Value) ** 2
        return dict(
            Q=f'Q = {Q:.2f} Дж',
        )


@variant.text('''
    По параллельным рельсам, расположенным под углом ${angle}\\degrees$ к горизонтали,
    соскальзывает проводник массой {m:V:e}: без трения и с постоянной скоростью {v:V:e}.
    Рельсы замнуты резистором сопротивлением {R:V:e}, расстояние между рельсами {l:V:e}.
    Вся система находитится в однородном вертикальном магнитном поле (см. рис. на доске).
    Определите индукцию магнитного поля и ток, протекающий в проводнике.
    Сопротивлением проводника, рельс и соединительных проводов пренебречь, ускорение свободного падения принять равным {g:Task:e}.
''')
@variant.solution_space(150)
@variant.arg(m=('m = {} г', [50, 100, 150, 200]))
@variant.arg(R=('R = {} Ом', [5, 8, 12]))
@variant.arg(v=('v = {} м/с', [12, 15]))
@variant.arg(l=('\\ell = {} см', [20, 40, 60]))
@variant.arg(angle=[10, 15, 20, 25])
@variant.answer_align([
    '\\ele &= {B:L}_\\bot v {l:L}, {B:L}_\\bot = {B:L}\\cos \\alpha, {I:L} = \\frac{\\ele}R,',
    'F_A &= {I:L} {B:L} {l:L} = \\frac{\\ele}R {B:L} {l:L},',

    'F_A \\cos \\alpha &= mg \\sin \\alpha '
        '\\implies \\frac{\\ele}R {B:L} \\ell \\cos \\alpha = mg \\sin \\alpha',

        '&\\frac{{B:L} \\cos \\alpha * v {l:L}}R {B:L} {l:L} \\cos \\alpha = mg \\sin \\alpha' 
        '\\implies \\frac{{B:L}^2 \\cos^2 \\alpha  * v {l:L}^2}R = mg \\sin \\alpha,',

    '{B:L} &= '
        '\\sqrt{\\frac{mg R \\sin \\alpha}{v {l:L}^2 \\cos^2 \\alpha}} '
        '= \\sqrt{\\frac{{m:V} * {g:V} * {R:V} * \\sin {angle}\\degrees}{{v:V} * {l:V|sqr} * \\cos^2 {angle}\\degrees}}'
        '\\approx {B:V},',

    '{I:L} &= \\frac{\\ele}R'
        '= \\frac{B_\\bot v {l:L}}R '
        '= \\frac {v {l:L} \\cos \\alpha}R \\sqrt{\\frac{mg R \\sin \\alpha}{v {l:L}^2 \\cos^2 \\alpha}}'
        '=\\sqrt{\\frac{mg v \\sin \\alpha}{R:L:s}}'
        '=\\sqrt{\\frac{{m:V} * {g:V} * {v:V} * \\sin {angle}\\degrees}{R:V:s}} '
        '\\approx {I:V}.',
])
class B_angle_hard(variant.VariantTask):  # Вишнякова 3.4 УК
    def GetUpdate(self, m=None, R=None, v=None, l=None, angle=None):
        a_radian = angle * math.pi / 180
        g = Consts.g_ten
        BB = 1. * m.Value * g.Value * R.Value * math.sin(a_radian) / math.cos(a_radian) ** 2 / v.Value / l.Value ** 2 * 10 ** (
            m.Power + g.Power + R.Power - v.Power - 2 * l.Power
        )
        B = BB ** 0.5
        II = 1. * m.Value * g.Value * v.Value * math.sin(a_radian) / R.Value * 10 ** (
            m.Power + g.Power + v.Power - R.Power
        )
        I = II ** 0.5
        return dict(
            g=g,
            B=f'B = {B:.2f} Тл',
            I=f'\\eli = {I:.2f} А',
        )
