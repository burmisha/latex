import generators.variant as variant
from generators.helpers import letter_variants, Fraction

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
@variant.answer_align([
])
class Task01(variant.VariantTask):
    pass


@variant.text('''
    Тело совершает гармонические колебания с периодом {T:V:e}. 
    За какое время тело смещается от положения {position} до смещения в половину амплитуды?
''')
@variant.solution_space(80)
@variant.arg(T=('T = {} c', [4, 5, 6]))
@variant.arg(position=['крайнего отклонения', 'равновесия'])
@variant.answer_align([
])
class Task02(variant.VariantTask):
    pass


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
class Task03(variant.VariantTask):
    pass


@variant.text('''
    Частота колебаний {what} равна {nu:V:e}. Определите периоды колебаний
    \\begin{itemize}
        \\item {what1} энергии груза,
        \\item {what2} груза,
        \\item {what3} груза.
    \\end{itemize}
''')
@variant.solution_space(80)
@variant.arg(nu=('\\nu = {} Гц', [8, 10, 12, 15]) )
@variant.arg(what=['пружинного маятника', 'математического маятника'])
@variant.arg(what1=['потенциальной', 'кинетической'])
@variant.arg(what2=['скорости', 'ускорения'])
@variant.arg(what3=['модуля скорости', 'модуля ускорения'])
class Task04(variant.VariantTask):
    pass


@variant.text('''
    Тело колеблется по гармоническому закону с амплитудой {A:V:e}.
    Какой {which} путь тело может пройти за {how} периода?
''')
@variant.solution_space(80)
@variant.arg(A=('A = {} см', [4, 6, 12]))
@variant.arg(which=['минимальный', 'максимальный'])
@variant.arg(how=['половину', 'четверть', 'одну шестую долю'])
@variant.answer_align([
])
class Task05(variant.VariantTask):
    pass


@variant.text('''
    Период колебаний математического маятника равен {T:V:e},
    а их амплитуда — {A:V:e}. Определите {what}.
''')
@variant.solution_space(80)
@variant.arg(A=('A = {} см', [10, 15, 20]))
@variant.arg(T=('T = {} с', [2, 3, 4, 5]))
@variant.arg(what=['максимальную скорость маятника', 'амплитуду колебаний скорости маятника'])
@variant.answer_align([
])
class Task06(variant.VariantTask):
    pass


@variant.text('''
    Определите период колебаний груза массой $m$, подвешенного к пружине жёсткостью $k$. 
    Ускорение свободного падения $g$. 
''')
@variant.solution_space(120)
@variant.no_args
class Task07(variant.VariantTask):
    pass


@variant.text('''
    Куб со стороной $a$ и плотности $\\rho$ плавает в жидкости плотностью $\\rho_0$.
    Определите частоту колебаний куба, считая, что 4 грани куба всегда вертикальны.
''')
@variant.solution_space(120)
@variant.no_args
class Task08(variant.VariantTask):
    pass


@variant.text('''
    Математический маятник с нитью длиной {l:V:e} подвешен к потолку в лифте.
    За {t:V:e} маятник совершил {N:V:e} колебаний.
    Определите модуль и направление ускорения лифта. Куда движется лифт?
''')
@variant.solution_space(80)
@variant.arg(l=('\\ell = {} см', [35, 40, 45]))
@variant.arg(t=('t = {} с', [11, 12, 13]))
@variant.arg(N=('N = {}', [7, 9, 11, 13]))
class Task09(variant.VariantTask):
    pass


@variant.text('''
    Масса груза в пружинном маятнике равна {M:V:e}, при этом период его колебаний равен {T:V:e}. 
    Груз {what} на {m:V:e} г. Определите новый период колебаний маятника.
''')
@variant.solution_space(80)
@variant.arg(T=('T = {} с', [11.2, 1.3, 1.4, 1.5]))
@variant.arg(m=('m = {} г', [50, 100, 150]))
@variant.arg(M=('M = {} г', [400, 500, 600]))
@variant.arg(what=['утяжеляют', 'облегчают'])
class Task10(variant.VariantTask):
    pass


@variant.text('''
    При какой длине нити математического маятника период колебаний груза массой {m:V:e} 
    окажется равен периоду колебаний этого же груза в пружинном маятнике с пружиной жесткостью {k:V:e}?
''')
@variant.solution_space(80)
@variant.arg(m=('m = {} г', [200, 300, 400]))
@variant.arg(k=('k = {} Н/м', [40, 50, 60]))
class Task11(variant.VariantTask):
    pass


@variant.text('''
    Груз подвесили к пружине, при этом удлинение пружины составило {dx:V:e}.
    Определите частоту колебаний пружинного маятника, собранного из этой пружины и этого груза.
''')
@variant.solution_space(80)
@variant.arg(dx=('\\ell = {} мм', [30, 45, 60]))
class Task12(variant.VariantTask):
    pass


@variant.text('''
    Определите период колебаний системы (см. рис. на доске), 
    для случая $n = {n}$. Длина маятника $\\ell$, ускорение свободного падения $g$. 
''')
@variant.solution_space(80)
@variant.arg(n__frac=[('2', 12), ('\\sqrt{2}', 8), ('\\frac{\\sqrt{2}}3', 6)])
@variant.answer_short('''
    T = 2\\pi\\sqrt{\\frac\\ell g}, \\qquad
    T\' = 2 * \\frac T 4 + 2 * \\frac T{{frac}} = {r1:LaTeX}T = {r2:LaTeX}\\pi\\sqrt{\\frac\\ell g}
''')
class Task13(variant.VariantTask):
    def GetUpdate(self, n=None, frac=None):
        r1 = Fraction() / 2 + Fraction() * 2 / frac
        r2 = r1 * 2
        return dict(
            r1=r1,
            r2=r2,
        )
