import generators.variant as variant
from generators.helpers import letter_variants, Fraction, Consts, Decimal
import math

@variant.text('''
''')
@variant.solution_space(80)
@variant.arg(A=('A = {} a', [1]))
@variant.answer_align([
])
class Template(variant.VariantTask):
    pass


@variant.text('''
    Тело колеблется по гармоническому закону,
    амплитуда этих колебаний {A:V:e}, период {T:V:e}.
    Чему равно смещение тела относительно положения равновесия через {t:V:e}
    после прохождения положения {what}?
''')
@variant.solution_space(80)
@variant.arg(A=('A = {} см', [10, 12, 14, 16, 18, 20]))
@variant.arg(T=('T = {} c', [2, 4, 6]))
@variant.arg(t=('t = {} c', [20, 21, 22, 23, 24, 25, 26]))
@variant.arg(what=['равновесия', 'максимального отклонения'])
@variant.answer_short(
    'x = A \\{f} \\omega t '
    '= A \\{f} \\cbr{ \\frac {2\\pi}T t } '
    '= A \\{f} \\cbr{ 2\\pi \\frac tT } '
    '= {A:V} * \\{f} \\cbr{ 2\\pi * \\frac {t:V:s}{T:V:s}}'
    '\\approx {x:V}.'
)
class Task01(variant.VariantTask):
    def GetUpdate(self, *, A=None, T=None, t=None, what=None):
        phi = 2 * math.pi * float(t.SI_Value / T.SI_Value)
        if what == 'максимального отклонения':
            multiplier = math.cos(phi)
            f = 'cos'
        elif what == 'равновесия':
            multiplier = math.sin(phi)
            f = 'sin'
        else:
            raise RuntimeError()

        x = A * multiplier
        if abs(x.SI_Value) <= 1e-6:
            value = 0
        else:
            value = f'{x.SI_Value * 100:.1f}'
        return dict(
            x=f'{value} см',
            f=f,
        )


@variant.text('''
    Тело совершает гармонические колебания с периодом {T:V:e}. 
    За какое время тело смещается от положения {position} до смещения в половину амплитуды?
''')
@variant.solution_space(120)
@variant.arg(T=('T = {} c', [4, 5, 6]))
@variant.arg(position=['наибольшего отклонения', 'равновесия'])
@variant.answer_short('t = \\frac T{{denom}} \\approx {t:V}.')
class Task02(variant.VariantTask):
    def GetUpdate(self, *, T=None, position=None):
        if position == 'наибольшего отклонения':
            denom = 6
        elif position == 'равновесия':
            denom = 12
        else:
            raise RuntimeError()

        return dict(
            denom=denom,
            t=f'{T.SI_Value / denom:.1f} c',
        )


@variant.text('''
    Запишите формулу для периода колебаний {which} и ...
    \\begin{itemize}
        \\item укажите названия всех физических величин в формуле, 
        \\item выразите из неё {what1} 
        \\item выразите из неё {what2}.
    \\end{itemize}
''')
@variant.solution_space(80)
@variant.arg(which__what2=[
    ('математического маятника', 'длину маятника'),
    ('математического маятника', 'ускорение свободного падения'),
    ('пружинного маятника', 'массу груза'),
    ('пружинного маятника', 'жёсткость пружины'),
])
@variant.arg(what1=['частоту колебаний', 'циклическую частоту колебаний'])
@variant.answer_align([
    'T &= 2\\pi \\sqrt{\\frac lg} '
        '\\implies \\nu = \\frac 1T = \\frac 1{2\\pi}\\sqrt{\\frac gl}, '
        '\\omega = 2\\pi\\nu = \\sqrt{\\frac gl}, '
        'l = g\\sqr{\\frac T{2\\pi}}, '
        'g = l\\sqr{\\frac {2\\pi}T}',
    'T &= 2\\pi \\sqrt{\\frac mk} '
        '\\implies \\nu = \\frac 1T = \\frac 1{2\\pi}\\sqrt{\\frac km}, '
        '\\omega = 2\\pi\\nu = \\sqrt{\\frac km}, '
        'm = k\\sqr{\\frac T{2\\pi}}, '
        'k = m\\sqr{\\frac {2\\pi}T}',
])
class Task03(variant.VariantTask):
    pass


@variant.text('''
    Частота колебаний {what} равна {nu:V:e}. Определите периоды колебаний
    \\begin{itemize}
        \\item {what1},
        \\item {what2} груза,
        \\item {what3} груза.
    \\end{itemize}
''')
@variant.solution_space(80)
@variant.arg(nu=('\\nu = {} Гц', [8, 10, 12, 15]) )
@variant.arg(what=['пружинного маятника', 'математического маятника'])
@variant.arg(what1=['потенциальной энергии системы', 'кинетической энергии системы'])
@variant.arg(what2=['скорости', 'ускорения'])
@variant.arg(what3=['модуля скорости', 'модуля ускорения'])
@variant.answer_short('T = \\frac 1\\nu \\approx {T:V}, T_1 = \\frac T2 \\approx {T2:V}, T_2 = T \\approx {T:V}, T_3 = \\frac T2 \\approx {T2:V}.')
class Task04(variant.VariantTask):
    def GetUpdate(self, *, nu=None, what=None, what1=None, what2=None, what3=None):
        T = nu / nu / nu
        return dict(
            T=f'{T.SI_Value * 1000:.1f} мc',
            T2=f'{T.SI_Value / 2 * 1000:.1f} мc',
        )


@variant.text('''
    Тело колеблется по гармоническому закону с амплитудой {A:V:e}.
    Какой {which} путь тело может пройти за {how} периода?
''')
@variant.solution_space(80)
@variant.arg(A=('A = {} см', [4, 6, 12]))
@variant.arg(which=['минимальный', 'максимальный'])
@variant.arg(how=['половину', 'четверть', 'одну шестую долю'])
@variant.answer_short('{answer} \\approx {s:V}.')
class Task05(variant.VariantTask):
    def GetUpdate(self, *, A=None, which=None, how=None):
        if how == 'половину':
            answer = '2A'
            s = A * 2
        elif how == 'четверть' and which == 'минимальный':
            answer = '2 * A \\cbr{1 - \\frac 1{\\sqrt 2}} = A\\cbr{2 - \\sqrt{2}}'
            s = A * 2 * (1 - 0.5 ** 0.5)
        elif how == 'четверть' and which == 'максимальный':
            answer = '2 * A \\frac{1}{\\sqrt 2} = A\\sqrt{2}'
            s = A * 2 * 0.5 ** 0.5
        elif how == 'одну шестую долю' and which == 'минимальный':
            answer = '2 * A \\frac{1}{12} = \\frac{A:L:s}3'
            s = A * 2 / 12
        elif how == 'одну шестую долю' and which == 'максимальный':
            answer = '2 * A \\frac{1}{2} = A'
            s = A
        else:
            raise RuntimeError()
        return dict(
            answer=answer,
            s=f'{s.SI_Value * 100:.1f} см',
        )
    

@variant.text('''
    Период колебаний математического маятника равен {T:V:e},
    а их амплитуда — {A:V:e}. Определите {what}.
''')
@variant.solution_space(100)
@variant.arg(A=('A = {} см', [10, 15, 20]))
@variant.arg(T=('T = {} с', [2, 3, 4, 5]))
@variant.arg(what=['максимальную скорость маятника', 'амплитуду колебаний скорости маятника'])
@variant.answer_short('''
    T = \\frac{2\\pi}{\\omega}
    \\implies \\omega = \\frac{2\\pi}{T:L:s}
    \\implies v_{\\max} = \\omega A = \\frac{2\\pi}{T:L:s}A
    \\approx {v:V}.
''')
class Task06(variant.VariantTask):
    def GetUpdate(self, *, A=None, T=None, what=None):
        v = A / T * 2 * math.pi
        return dict(
            v=f'{v.SI_Value * 100:.1f} см / с'
        )


@variant.text('''
    Определите период колебаний груза массой $m$, подвешенного к пружине жёсткостью $k$. 
    Ускорение свободного падения $g$. 
''')
@variant.solution_space(150)
@variant.no_args
@variant.answer_align([
    '-kx_0 + mg = 0,',
    'F &= -k(x_0 + \\Delta x),',
    'ma &= -k(x_0 + \\Delta x) + mg,',
    'ma &= -kx_0 -k \\Delta x + mg = -mg -k \\Delta x + mg = -k \\Delta x,',
    'a &+ \\frac k m x = 0,',
    '\\omega^2 &= \\frac k m \\implies T = \\frac{2\\pi}\\omega = 2\\pi\\sqrt{\\frac m k}.',
])
class Task07(variant.VariantTask):
    pass


@variant.text('''
    Куб со стороной $a$ и плотности $\\rho$ плавает в жидкости плотностью $\\rho_0$.
    Определите частоту колебаний куба, считая, что 4 грани куба всегда вертикальны.
''')
@variant.solution_space(150)
@variant.no_args
@variant.answer_align([
    '\\Delta F &= -\\rho_0 g a^2 \\Delta x,'
    '\\Delta F = m\\ddot x, m = \\rho a^3'
    '\\implies \\rho a^3 \\ddot x = -\\rho_0 g a^2 \\Delta x \\implies',
    '\\implies \\ddot x &= -\\frac{\\rho_0}{\\rho} \\frac g a \\Delta x'
    '\\implies \\omega^2 = \\frac{\\rho_0}{\\rho} * \\frac g a'
    '\\implies T = \\frac{2 \\pi}{\\omega} = 2 \\pi\\sqrt{\\frac{\\rho}{\\rho_0} * \\frac a g}.'
])
class Task08(variant.VariantTask):
    pass


@variant.text('''
    Математический маятник с нитью длиной {l:V:e} подвешен к потолку в лифте.
    За {t:V:e} маятник совершил {N:V:e} колебаний.
    Определите модуль и направление ускорения лифта. Куда движется лифт?
''')
@variant.solution_space(120)
@variant.arg(l=('\\ell = {} см', [37, 40, 43]))
@variant.arg(t=('t = {} с', [20, 25, 30]))
@variant.arg(a_raw=[-2, -1.5, -0.5, 0.5, 1.5, 2.5])
@variant.answer_short('''
    T = 2\\pi\\sqrt{\\frac\\ell {a + g}}, T = \\frac {t:L:s}{N:L:s}
    \\implies a + g = \\ell * \\frac{4 \\pi ^ 2}{T^2},
    a = \\ell * \\frac{4 \\pi ^ 2}{T^2} - g = \\ell * \\frac{4 \\pi ^ 2 {N:L}^2}{t^2} - g \\approx {a:V},
    \\text{{ans}}.
''')
class Task09(variant.VariantTask):
    def GetUpdate(self, *, l=None, t=None, a_raw=None):
        g = 10
        TT = 2 * math.pi * (float(l.SI_Value) / (g + a_raw)) ** 0.5
        N = int(float(t.SI_Value) / TT + 0.5)
        assert 12 <= N <= 50, N
        a = (math.pi ** 2) * 4 * (N ** 2) / (float(t.SI_Value) ** 2) * float(l.SI_Value) - g
        assert -4 <= a <= 4
        return dict(
            N=f'N = {N}',
            a=f'a = {a:.2f} м / c^2',
            ans='вниз' if a > 0 else 'вверх',
        )


@variant.text('''
    Масса груза в пружинном маятнике равна {M:V:e}, при этом период его колебаний равен {T:V:e}. 
    Груз {what} на {m:V:e}. Определите новый период колебаний маятника.
''')
@variant.solution_space(120)
@variant.arg(T=('T = {} с', [1.2, 1.3, 1.4, 1.5]))
@variant.arg(m=('m = {} г', [50, 100, 150]))
@variant.arg(M=('M = {} г', [400, 500, 600]))
@variant.arg(what=['утяжеляют', 'облегчают'])
@variant.answer_short('''
    T' 
        = 2\\pi\\sqrt{\\frac{M {sign} m}{k}}
        = 2\\pi\\sqrt{\\frac{M:L:s}{k} * \\frac{M {sign} m}{M:L:s}}
        = T\\sqrt{\\frac{M {sign} m}{M:L:s}} =  T\\sqrt{1 {sign} \\frac{m:L:s}{M:L:s}} \\approx {T2:V}.
''')
class Task10(variant.VariantTask):
    def GetUpdate(self, *, T=None, m=None, M=None, what=None):
        if what == 'утяжеляют':
            sign = '+'
            m2 = M.SI_Value + m.SI_Value
        elif what == 'облегчают':
            sign = '-'
            m2 = M.SI_Value - m.SI_Value
        else:
            raise RuntimeError()
        T2 = T * float(m2 / M.SI_Value) ** 0.5
        return dict(
            T2=f'{T2.SI_Value:.2f} с',
            sign=sign,
        )


@variant.text('''
    При какой длине нити математического маятника период колебаний груза массой {m:V:e} 
    окажется равен периоду колебаний этого же груза в пружинном маятнике с пружиной жёсткостью {k:V:e}?
''')
@variant.solution_space(120)
@variant.arg(m=('m = {} г', [200, 300, 400]))
@variant.arg(k=('k = {} Н/м', [40, 50, 60]))
@variant.answer_short('''
    2\\pi \\sqrt{\\frac \\ell g} = 2\\pi \\sqrt{\\frac m k}
    \\implies \\frac \\ell g = \\frac m k
    \\implies \\ell = g \\frac m k \\approx {l:V}.
''')
class Task11(variant.VariantTask):
    def GetUpdate(self, *, m=None, k=None):
        g = Consts.g_ten
        l = g * m / k
        return dict(
            l=f'\\ell = {l.SI_Value * 100:.1f} см',
        )


@variant.text('''
    Груз подвесили к пружине, при этом удлинение пружины составило {dx:V:e}.
    Определите частоту колебаний пружинного маятника, собранного из этой пружины и этого груза.
''')
@variant.solution_space(120)
@variant.arg(dx=('\\ell = {} мм', [30, 45, 60]))
@variant.answer_short('''
    mg -k\\Delta x = 0 \\implies \\frac m k = \\frac{\\Delta x} g
    \\implies T = 2\\pi \\sqrt{\\frac m k } = 2\\pi \\sqrt{\\frac{\\Delta x} g } \\approx {T:V:e},
    \\nu = \\frac 1T \\approx {nu:V:e}.
''')
class Task12(variant.VariantTask):
    def GetUpdate(self, *, dx=None):
        g = Consts.g_ten
        T = 2 * math.pi * float(dx.SI_Value / g.SI_Value) ** 0.5
        nu = 1 / T
        return dict(
            T=f'T = {T:.2f} с',
            nu=f'\\nu = {nu:.2f} Гц',

        )


@variant.text('''
    Определите период колебаний системы: математический маятник ограничен с одной стороны стенкой (см. рис. на доске).
    Удары маятника о стенку абсолютно упругие, $n = {n}$. Длина маятника $\\ell$, ускорение свободного падения $g$. 
''')
@variant.solution_space(120)
@variant.arg(n__frac=[('2', 12), ('\\sqrt{2}', 8), ('\\frac{2}{\\sqrt{3}}', 6)])
@variant.answer_short('''
    T = 2\\pi\\sqrt{\\frac\\ell g}, \\qquad
    T\' = 2 * \\frac T 4 + 2 * \\frac T{{frac}} = {r1:LaTeX}T = {r2:LaTeX}\\pi\\sqrt{\\frac\\ell g}
''')
class Task13(variant.VariantTask):
    def GetUpdate(self, *, n=None, frac=None):
        r1 = Fraction(1) / 2 + Fraction(1) * 2 / frac
        r2 = r1 * 2
        return dict(
            r1=r1,
            r2=r2,
        )


@variant.text('''
    2 маленьких шарика скреплены лёгкой пружиной жёсткостью $k$, масса каждого шарика $m$.
    Пружина недеформирована, система летит со скоростью $v$ к стенке, 
    расстояние от ближайшего шарика до стены $\\ell$ (см. рис. на доске). 
    Все удары упругие, трением пренебречь, $\\frac{mv^2}{kd^2} < \\frac 12,$ где $d$ — длина пружины.
    Через какое время шарики вновь окажутся в том же положении?
''')
@variant.solution_space(150)
@variant.no_args
@variant.answer_align([
    'F &= -k * 2x = ma \\implies a + \\frac {2k}m x = 0 \\implies \\omega^2 = \\frac {2k}m \\implies T =\\frac{2\\pi}\\omega = 2\\pi\\sqrt{\\frac m{2k}},',
    '\\frac{mv^2}2 &< \\frac{2k\\sqr{\\frac d2}}2 \\implies \\text{шарики между собой не ударятся},',
    'T &= 2 * \\frac \\ell v + \\frac 12 * 2 \\pi\\sqrt{\\frac m{2k}}.',
])
class Task14(variant.VariantTask):
    pass


@variant.text('''
    Определите период колебаний жидкости в тонкой $U$-образной трубке постоянного сечения,
    если длина столбика жидкости равна {l:V:e} (см. рис. на доске).
    Вязкостью, силами трения и сопротивления, капиллярными эффектами и притяжением {what}, пренебречь.
''')
@variant.solution_space(100)
@variant.arg(l=('\\ell = {} см', [45, 55, 65, 75, 85]))
@variant.arg(what=['Юпитера', 'Сатурна', 'Марса', 'Венеры'])
@variant.answer_short('''
    \\Delta F = -m \\frac {2x}\\ell g = ma
    \\implies a + \\frac{2g}\\ell x = 0
    \\implies \\omega^2 = \\frac{2g}\\ell 
    \\implies T = \\frac{2\\pi}\\omega = 2\\pi\\sqrt{\\frac\\ell{2g}}
    \\approx {T:V:e}.
''')
class Task15(variant.VariantTask):
    def GetUpdate(self, *, l=None, what=None):
        T = math.pi * 2 * float(l.SI_Value / 2 / Consts.g_ten.SI_Value) ** 0.5
        return dict(
            T=f'{T:.3f} c',
        )


@variant.text('''
    Определите период колебаний и массу груза в пружинном маятнике,
    если максимальная скорость груза равна {v:V:e},
    жёсткость пружины {k:V:e}, а амплитуда колебаний {A:V:e}.
''')
@variant.solution_space(80)
@variant.arg(A=('A = {} см', [10, 12, 15, 20]))
@variant.arg(v=('v = {} м / с', [2, 3, 4, 5]))
@variant.arg(k=('k = {} Н / м', [180, 240, 300]))
@variant.answer_align([
    '\\frac{mv^2}2 &= \\frac{kA^2}2 \\implies m = k\\sqr{\\frac{A:L:s}{v:L:s}} \\approx {m:V},',
    'T &= \\frac{2\\pi}\\omega = 2\\pi\\sqrt{\\frac mk} = 2\\pi\\frac{A:L:s}{v:L:s} \\approx {T:V}.',
])
class Task16(variant.VariantTask):
    def GetUpdate(self, *, A=None, v=None, k=None):
        m = k * A * A / v / v
        T = A / v * math.pi * 2
        return dict(
            m=f'm = {m.SI_Value * 1000 + Decimal(0.5):.0f} г',
            T=f'T = {T.SI_Value:.3f} c',
        )


@variant.text('''
    Определите период малых колебаний маятника (см. рис. на доске),
    если {l:Task:e}, а {h:Task:e}.
''')
@variant.solution_space(80)
@variant.arg(l=('\\ell = {} м', [0.6, 0.75, 0.9]))
@variant.arg(h=('h = {} см', [20, 25, 35]))
@variant.answer_short('''
    T = 2 * \\cfrac{T_1}4 + 2 * \\cfrac{T_2}4 = \\cfrac{T_1 + T_2}2 
    = \\cfrac{2\\pi\\sqrt{\\frac {l:L:s}{g}} + 2\\pi\\sqrt{\\frac {h:L:s}{g} } }2
    = \\pi\\cbr{\\sqrt{\\frac {l:L:s}{g}} + \\sqrt{\\frac {h:L:s}{g} } }
    \\approx {T:V}.
''')
class Task17(variant.VariantTask):
    def GetUpdate(self, *, l=None, h=None):
        g = Consts.g_ten
        T = math.pi * (
            float(l.SI_Value / g.SI_Value) ** 0.5
            + float(h.SI_Value / g.SI_Value) ** 0.5
        )
        return dict(
            T=f'T = {T:.3f} c',
        )


@variant.text('''
    Доска массой $m$ и длиной $\\ell$ скользит по гладкой горизонтальной плоскости со скоростью $v$,
    а после въезжает на шероховатую поверхность с коэффициентом трения $\\mu$ (см. рис. на доске).
    Определите, за какое время доска остановится (от начала въезжания) и на какое расстояние въедет.
    Ускорение свободного падения $g$, $v^2 < \\mu g \\ell.$
''')
@variant.solution_space(150)
@variant.no_args
@variant.answer_align([
    'F_\\text{трения} &= -\\mu m \\frac x\\ell g = ma '
    '\\implies a + \\mu \\frac g\\ell x = 0 '
    '\\implies \\omega^2 = \\frac {\\mu g}\\ell,',
    'T &= \\frac{2\\pi}{\\omega} = 2\\pi \\sqrt{\\frac \\ell{\\mu g}}'
    '\\implies t = \\frac T4 = \\frac\\pi2 \\sqrt{\\frac \\ell{\\mu g}},',
    'A &= \\frac v\\omega = v \\sqrt{\\frac \\ell{\\mu g}} \\quad (\\text{отметим, что $A < \\sqrt{\\mu g \\ell} * \\sqrt{\\frac \\ell{\\mu g}} = \\ell$}).'
])
class Task18(variant.VariantTask):
    pass


@variant.text('''
    Тело совершает гармонические колебания с периодом $T$ и амплитудой $A$. 
    Определите, какую долю периода тело находится на расстоянии {which} ${x_frac}A$ от положения равновесия.
''')
@variant.solution_space(80)
@variant.arg(which=['более', 'менее'])
@variant.arg(nom__denom=[(1, 2), (1, 3), (2, 3)])
@variant.answer_short('t = {share:LaTeX}T \\implies \\frac tT = {share:LaTeX}')
class Task19(variant.VariantTask):
    def GetUpdate(self, *, which=None, nom=None, denom=None):
        share = Fraction(1) * nom / denom
        if which == 'более':
            share = share * (-1) + 1

        if (nom, denom) == (1, 2):
            x_frac = '\\frac{\\sqrt 2}2'
        elif (nom, denom) == (1, 3):
            x_frac = '\\frac 12'
        elif (nom, denom) == (2, 3):
            x_frac = '\\frac{\\sqrt 3}2'
        else:
            raise RuntimeError()

        return dict(
            x_frac=x_frac,
            share=share,
        )
