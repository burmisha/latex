import generators.variant as variant
from generators.helpers import letter_variants, Fraction, Consts
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
    Схематично изобразите колебательный контур.
    Запишите формулу для периода колебаний в колебательном контуре и ...
    \\begin{itemize}
        \\item подпишите все физические величины,
        \\item укажите их единицы измерения,
        \\item выразите из формулы периода {q1},
        \\item выразите из формулы периода {q2}.
    \\end{itemize}
''')
@variant.solution_space(80)
@variant.arg(q1=['частоту', 'циклическую частоту'])
@variant.arg(q2=['ёмкость конденсатора', 'индуктивность катушки'])
@variant.answer_short('''
    T = 2\\pi\\sqrt{LC},
    \\nu = \\frac 1{2\\pi\\sqrt{LC}},
    \\omega = \\frac 1{\\sqrt{LC}},
    L = \\frac 1C \\sqr{\\frac T{2\\pi}},
    C = \\frac 1L \\sqr{\\frac T{2\\pi}}.
''')
class Task01(variant.VariantTask):
    pass


@variant.text('''
    Оказалось, что наибольший заряд конденсатора в колебательном контуре равен {q:V:e},
    а максимальный ток — {I:V:e}. Определите частоту колебаний.
''')
@variant.solution_space(80)
@variant.arg(I=('\\eli_{{\\max}} = {} мА', [120, 150, 180, 240, 270]))
@variant.arg(q=('q_{{\\max}} = {} мкКл', [40, 60, 80]))
@variant.answer_short('''
    {I:L} = {q:L}\\omega \\implies \\nu = \\frac{\\omega}{2\\pi} = \\frac{I:L:s}{2\\pi q} \\approx {nu:V}.
''')
class Task02(variant.VariantTask):
    def GetUpdate(self, *, q=None, I=None):
        nu = I / 2 / math.pi / q
        return dict(
            nu=f'\\nu = {nu.SI_Value:.1f} Гц',
        )


@variant.text('''
    В колебательном контура сила тока изменяется 
    по закону $\\eli={I.SI_Value:.2f}\\{func}({omega}t)$ (в СИ).
    Индуктивность катушки при этом равна {L:V:e}. Определите:
    \\begin{itemize}
        \\item период колебаний,
        \\item ёмкость конденсатора,
        \\item максимальный заряд конденсатора.
    \\end{itemize}
''')
@variant.solution_space(80)
@variant.arg(omega=[12, 15, 18])
@variant.arg(I=('\\eli = {} A', [0.05, 0.25, 0.30]))
@variant.arg(L=('L = {} мГн', [50, 60, 70, 80]))
@variant.arg(func=['sin', 'cos'])
@variant.answer_align([
    '\\omega &= {omega}\\funits{рад}{c},',
    'T &= \\frac{2\\pi}\\omega \\approx {T:V},',
    'C &= \\frac 1{\\omega^2 L} \\approx {C:V},',
    '{q:L} &= \\frac{\\eli_{\\max}}\\omega  \\approx {q:V}.',
])
class Task03(variant.VariantTask):
    def GetUpdate(self, *, omega=None, I=None, func=None, L=None):
        T = 2 * math.pi / omega
        C = 1 / omega ** 2 / L.SI_Value
        q = I.SI_Value / omega
        return dict(
            T=f'T = {T * 1000:.1f} мc',
            C=f'C = {C * 1000:.1f} мФ',
            q=f'q_{{\\max}} = {q * 1000:.1f} мКл',
        )


@variant.text('''
    Электрический колебательный контур состоит
    из катушки индуктивностью $L$ и конденсатора ёмкостью $C$. 
    {how} {what1} подключают ещё {what2} ${frac:LaTeX}{what3}$.
    Как изменится период свободных колебаний в контуре?
''')
@variant.solution_space(100)
@variant.arg(how=['Параллельно', 'Последовательно'])
@variant.arg(what1__what2__what3=[
    ('катушке', 'одну катушку индуктивностью', 'L'),
    ('конденсатору', 'один конденсатор ёмкостью', 'C'),
])
@variant.arg(nom__denom=[(1, 2), (1, 3), (2, 1), (3, 1)])
@variant.answer_short('''
    T = 2\\pi\\sqrt{LC}, \\quad
    T' = 2\\pi\\sqrt{L'C'}
        = T \\sqrt{\\frac{L'}L * \\frac{C'}C}
        = T \\sqrt{ {l:LaTeX} * {c:LaTeX} }
    \\implies \\frac{T'}T = \\sqrt{ {l:LaTeX} * {c:LaTeX} } \\approx {ans}.
''')
class Task04(variant.VariantTask):
    def GetUpdate(self, *, how=None, what1=None, what2=None, what3=None, nom=None, denom=None):
        frac = Fraction(1) * nom / denom
        l = Fraction(1)
        c = Fraction(1)
        if how == 'Параллельно':
            if what1 == 'катушке':
                l = (frac * 1) / (frac + 1)
            elif what1 == 'конденсатору':
                c = frac + 1
            else:
                raise RuntimeError()
        elif how == 'Последовательно':
            if what1 == 'катушке':
                l = frac + 1
            elif what1 == 'конденсатору':
                c = (frac * 1) / (frac + 1)
            else:
                raise RuntimeError()                
        else:
            raise RuntimeError()

        ans = float(l * c) ** 0.5

        return dict(
            frac=frac,
            l=l,
            c=c,
            ans=f'{ans:.3f}'
        )


@variant.text('''
    В колебательном контуре частота собственных колебаний {nu1:V:e}.
    После замены катушки индуктивности на другую катушку частота стала равной {nu2:V:e}.
    А какой станет частота, если в контур установить обе эти катушки {how}?
''')
@variant.solution_space(100)
@variant.arg(how=['параллельно', 'последовательно'])
@variant.arg(nu1=('\\nu_1 = {} Гц', [40, 60, 80]))
@variant.arg(nu2=('\\nu_2 = {} Гц', [30, 50, 70, 90]))
@variant.answer_align([
    'T &= 2\\pi\\sqrt{LC} \\implies \\nu = \\frac 1T = \\frac 1{2\\pi\\sqrt{LC}} \\implies L = \\frac1 {4\\pi^2 \\nu^2 C},',
    'L_1 &= \\frac1 {4\\pi^2 \\nu_1^2 C}, L_2 = \\frac1 {4\\pi^2 \\nu_1^2 C},',
    '''\\nu_\\text{послед.} 
        &= \\frac 1{2\\pi\\sqrt{(L_1 + L_2)C}}
        = \\frac 1{2\\pi\\sqrt{\\cbr{\\frac1 {4\\pi^2 \\nu_1^2 C} + \\frac1 {4\\pi^2 \\nu_2^2 C}}C}}
        = \\frac 1{\\sqrt{\\cbr{\\frac1 {\\nu_1^2 C} + \\frac1 {\\nu_2^2 C}}C}} = ''',
    ''' &= \\frac 1{\\sqrt{\\frac1 {\\nu_1^2} + \\frac1 {\\nu_2^2}}}
        = \\frac 1{\\sqrt{ \\frac1 {nu1:V|sqr|s} + \\frac1 {nu2:V|sqr|s}}} 
        \\approx {nu_posl:V},''',
    '''\\nu_\\text{паралл.} 
        &= \\frac 1{2\\pi\\sqrt{\\frac 1{\\frac 1{L_1} + \\frac 1{L_2}}C}}
        = \\frac 1{2\\pi\\sqrt{\\frac 1{\\frac 1{\\frac1 {4\\pi^2 \\nu_1^2 C}} + \\frac 1{\\frac1 {4\\pi^2 \\nu_2^2 C}}}C}} 
        = \\frac 1{2\\pi\\sqrt{\\frac 1{4\\pi^2 \\nu_1^2 C + 4\\pi^2 \\nu_2^2 C}C}} =''',
    ''' &= \\frac 1{\\sqrt{\\frac 1{\\nu_1^2 + \\nu_2^2}}} 
        = \\sqrt{\\nu_1^2 + \\nu_2^2} = \\sqrt{{nu1:V|sqr} + {nu2:V|sqr}} \\approx {nu_par:V}.'''
])
class Task05(variant.VariantTask):  # 3800 14.8
    def GetUpdate(self, *, how=None, nu1=None, nu2=None):
        nu_posl = 1 / ((1 / nu1.SI_Value ** 2 + 1 / nu2.SI_Value ** 2) ** 0.5)
        nu_par = (nu1.SI_Value ** 2  + nu2.SI_Value ** 2) ** 0.5
        return dict(
            nu_posl=f'{nu_posl:.2f} Гц',
            nu_par=f'{nu_par:.2f} Гц',
        )
