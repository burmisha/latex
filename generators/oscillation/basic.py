import generators.variant as variant
from generators.helpers import Decimal


@variant.lv_variant_task(
    {
        'период колебаний': '$T$',
        'частота колебаний': '$\\nu$',
        'циклическая частота': '$\\omega$',
        'число колебаний': '$N$',
        'время колебаний': '$t$',
    },
    ['$\\frac{2\\pi}{\\nu}$', '$\\frac{\\nu}{2\\pi}$', '$tN$'],
    answers_count=3,
    mocks_count=2,
)
class Definitions01(variant.VariantTask):
    pass


@variant.lv_variant_task(
    {
        'период колебаний': 'c',
        'частота колебаний': 'Гц',
        'циклическая частота': 'рад / с',
    },
    ['м / с', 'Гн'],
    answers_count=2,
    mocks_count=2,
)
class Definitions02(variant.VariantTask):
    pass


@variant.solution_space(135)
@variant.text('''
    \\begin{itemize}
        \\item Запишите линейное однородное дифференциальное уравнение второго порядка,
            описывающее свободные незатухающие колебания гармонического осциллятора,
        \\item запишите общее решение этого уравнения,
        \\item подпишите в выписанном решении фазу и амплитуду колебаний,
        \\item запишите выражение для скорости,
        \\item запишите выражение для ускорения.
    \\end{itemize}
''')
@variant.answer_align([
    '&\\ddot x + \\omega^2 x = 0 \\Longleftrightarrow a_x + \\omega^2 x = 0,',
    '&x = A \\cos(\\omega t + \\varphi_0) \\text{ или же } x = A \\sin(\\omega t + \\varphi_0) \\text{ или же } x = a \\cos(\\omega t) + b \\sin(\\omega t),',
    '&A \\text{\, или \,} \\sqrt{a^2 + b^2} \\text{ --- это амплитуда}, \\omega t + \\varphi_0\\text{ --- это фаза},',
    '&v = \\dot x = -\\omega A \\sin(\\omega t + \\varphi_0),',
    '&a = \\dot v = \\ddot x = -\\omega^2 A \\cos(\\omega t + \\varphi_0) = -\\omega^2 x,',
])
@variant.no_args
class Definitions03(variant.VariantTask):
    pass


@variant.text('''
    Дайте определения:
    \\begin{itemize}
        \\item {koleb},
        \\item {free},
        \\item {const},
        \\item {what}.
    \\end{itemize}
''')
@variant.arg(koleb=['гармонические колебания', 'механические колебания'])
@variant.arg(free=['свободные колебания', 'вынужденные колебания'])
@variant.arg(const=['незатухающие колебания', 'затухающие колебания'])
@variant.arg(what=['амплитуда колебаний', 'период колебаний'])
class Nu01(variant.VariantTask):
    pass


@variant.solution_space(40)
@variant.text('Определите частоту колебаний, если их период составляет {T:Task:e}.')
@variant.answer_short('\\nu = \\frac 1T = \\frac 1{T:V:s} = {nu:V}')
@variant.arg(T='T = 2/4/5/10/20/40/50 мс')
class Nu02(variant.VariantTask):
    def GetUpdate(self, T=None):
        nu = T / T / T  # TODO: 1 / T
        return dict(
            nu=f'\\nu = {nu.SI_Value:.0f} Гц',
        )


@variant.solution_space(60)
@variant.text('''
    Координата материальной точки зависит от времени по закону ${axis} = {A} * {func} ({n}\\pi t)$ (в СИ).
    Чему равен путь, пройденный точкой за {t:V:e}?
''')
@variant.answer_short('\\omega = {n}\\pi \\implies \\nu = \\frac{n}2\,\\units{Гц}, N = \\nu t = {N}, s = 4AN = 4 * {A} * {N} = {s} \\text{(м)}')
@variant.arg(t='t = 2/3/4 мин')
@variant.arg(n=[3, 4, 5, 6])
@variant.arg(axis=['x', 'y', 'z'])
@variant.arg(func=['\\sin', '\\cos'])
@variant.arg(A=['0.02', '0.05', '0.15', '0.25'])
class S_from_func(variant.VariantTask):
    def GetUpdate(self, t=None, n=None, axis=None, A=None, func=None):
        N = n * t.SI_Value / 2
        s = Decimal(A) * 4 * N
        return dict(
            N=N,
            s=str(s),
        )


@variant.text('''
    Определите период колебаний, если их частота составляет {nu:Task:e}.
    Сколько колебаний произойдёт за {t:Task:e}?
''')
@variant.answer_align([
    'T &= \\frac 1\\nu = \\frac 1{nu:V:s} = {T:V},',
    'N &= \\nu t = {nu:V|cdot}{t:V} = {N:V}.',
])
@variant.arg(nu='\\nu = 2/4/5/10/20/40/50 кГц')
@variant.arg(t='t = 1/2/3/5/10 мин')
@variant.solution_space(40)
class Nu03(variant.VariantTask):
    def GetUpdate(self, nu=None, t=None):
        T = nu / nu / nu  # TODO: 1 / nu
        N = nu * t
        return dict(
            T=f'T = {T.SI_Value * 1000:.3f} мc',
            N=f'N = {N.SI_Value:.0f} колебаний',
        )


@variant.text('''
    Амплитуда колебаний точки составляет {A:Task:e}, а частота~--- {nu:Task:e}.
    Определите, какой путь преодолеет эта точка за {t:Task:e}.
''')
@variant.answer_short('s = 4A * N = 4A * \\frac tT = 4A * t\\nu = 4 * {A:V} * {t:V} * {nu:V} = {s:V}')
@variant.arg(A='A = 2/3/5/10/15 см')
@variant.arg(nu='\\nu = 2/5/6/10/20 Гц')
@variant.arg(t='t = 10/40/80 с')
class Nu04(variant.VariantTask):
    def GetUpdate(self, A=None, nu=None, t=None):
        s = 4 * A * t * nu
        return dict(s=f's = {s.SI_Value:.1f} м')


@variant.solution_space(80)
@variant.text('''
    Изобразите график гармонических колебаний,
    амплитуда которых составляла бы {A:Task:e}, а период {T:Task:e}.
''')
@variant.arg(A=('A = {} см', [1, 2, 3, 5, 6, 15, 30, 40, 75]))
@variant.arg(T=('T = {} с', [2, 4, 6, 8, 10]))
class Nu05(variant.VariantTask):
    pass
