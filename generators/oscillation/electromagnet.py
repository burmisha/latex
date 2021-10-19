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
@variant.arg(q2=['выразите емкость конденсатора', 'индуктивность катушки.'])
@variant.answer_align([
    'T &= 2\\pi\\sqrt{LC}',
    '\\nu &= \\frac 1{2\\pi\\sqrt{LC}},',
    '\\omega &= \\frac 1{\\sqrt{LC}},',
    'L &= \\frac 1C \\sqr{\\frac T{2\\pi}},',
    'C &= \\frac 1L \\sqr{\\frac T{2\\pi}}.',
])
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
    {I:L} = {q:L}\\omega \\implies \\nu = \\frac{\\omega}{2\\pi} = \\frac{I:L:s}{2\\pi q} \\approx {nu:V}
''')
class Task02(variant.VariantTask):
    def GetUpdate(self, *, q=None, I=None):
        nu = I / 2 / math.pi / q
        return dict(
            nu=f'\\nu = {nu.SI_Value / 1000:.3f} кГц',
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
    '\\omega &= {omega}\\units{c}^-1,',
    'T &= \\frac{2\\pi}\\omega \\approx {T:V},',
    'C &= \\frac 1{\\omega^2 L} \\approx {C:V},',
    'q &= \\frac{\\eli_{\\max}}\\omega  \\approx {q:V}.',
])
class Task03(variant.VariantTask):
    def GetUpdate(self, *, omega=None, I=None, func=None, L=None):
        T = 2 * math.pi / omega
        C = 1 / omega ** 2 / L.SI_Value
        q = I.SI_Value / omega
        return dict(
            T=f'T = {T * 1000:.1f} мc',
            C=f'C = {C * 1000:.1f} мФ',
            q=f'q = {q * 1000:.1f} мКл',
        )


@variant.text('''
    Электрический колебательный контур состоит
    из катушки индуктивностью $L$ и конденсатора ёмкостью $C$. 
    {how} {what1} подключают ещё {what2} ${frac:LaTeX}{what3}$.
    Как изменится период сводобных колебаний в контуре?
''')
@variant.solution_space(100)
@variant.arg(how=['параллельно', 'последовательно'])
@variant.arg(what1__what2__what3=[
    ('катушке', 'одну катушку индуктивностью', 'L'),
    ('конденсатору', 'один конденсатор емкостью', 'L'),
])
@variant.arg(nom__denom=[(1, 2), (1, 3), (2, 1), (3, 1)])
@variant.answer_align([
    'T &= 2\\pi\\sqrt{LC}',
    "T\' &= 2\\pi\\sqrt{L\'C\'}"
    "= T \\sqrt{\\frac{L'}L * \\frac{C'}C} "
    "= T \\sqrt{ {l:LaTeX} * {c:LaTeX} }",
    '\\frac{T\'}T = \\sqrt{ {l:LaTeX} * {c:LaTeX} } \\approx {ans}',
])
class Task04(variant.VariantTask):
    def GetUpdate(self, *, how=None, what1=None, what2=None, what3=None, nom=None, denom=None):
        frac = Fraction() * nom / denom
        l = Fraction()
        c = Fraction()
        if how == 'параллельно':
            if what1 == 'катушке':
                l = (frac * 1) / (frac + 1)
            elif what1 == 'конденсатору':
                c = frac + 1
            else:
                raise RuntimeError()
        elif how == 'последовательно':
            if what1 == 'катушке':
                l = frac + 1
            elif what1 == 'конденсатору':
                c = (frac * 1) / (frac + 1)
            else:
                raise RuntimeError()                
        else:
            raise RuntimeError()

        ans = float(l * c) ** 2

        return dict(
            frac=frac,
            l=l,
            c=c,
            ans=f'{ans:.3f}'
        )
