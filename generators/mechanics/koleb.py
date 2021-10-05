import generators.variant as variant


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


@variant.solution_space(60)
@variant.text('Определите частоту колебаний, если их период составляет {T:Task:e}.')
@variant.answer_short('\\nu = \\frac 1T = \\frac 1{T:V:s} = {nu:V}')
@variant.arg(T=('T = {} мс', [2, 4, 5, 10, 20, 40, 50]))
class Nu02(variant.VariantTask):
    def GetUpdate(self, T=None):
        nu = int(1000 / T.Value)
        return dict(
            nu=f'\\nu = {nu} Гц',
        )


@variant.text('''
    Определите период колебаний, если их частота составляет {nu:Task:e}.
    Ответ выразите в миллисекундах. Сколько колебаний произойдёт за {t:Task:e}?
''')
@variant.answer_align([
    'T &= \\frac 1\\nu = \\frac 1{nu:V:s} = {T:V},',
    'N &= \\nu t = {nu:V|cdot}{t:V} = {N:V}.',
])
@variant.arg(nu=('\\nu = {} кГц', [2, 4, 5, 10, 20, 40, 50]))
@variant.arg(t=('t = {} мин', [1, 2, 3, 5, 10]))
class Nu03(variant.VariantTask):
    def GetUpdate(self, nu=None, t=None):
        T = nu / nu / nu  # TODO: 1 / nu
        N = nu * t * 60
        return dict(
            T=f'T = {T.SI_Value * 1000:.3f} мc',
            N=f'N = {N.SI_Value:.0f} колебаний',
        )


@variant.text('''
    Амплитуда колебаний точки составляет {A:Task:e}, а частота~--- {nu:Task:e}.
    Определите, какой путь преодолеет эта точка за {t:Task:e}.
''')
@variant.answer_short('s = 4A * N = 4A * \\frac tT = 4A * t\\nu = 4 * {A:V} * {t:V} * {nu:V} = {s:V}')
@variant.arg(A=('A = {} см', [2, 3, 5, 10, 15]))
@variant.arg(nu=('\\nu = {} Гц', [2, 5, 6, 10, 20]))
@variant.arg(t=('t = {} с', [10, 40, 80]))
class Nu04(variant.VariantTask):
    def GetUpdate(self, A=None, nu=None, t=None):
        s = 4 * A * t * nu
        return dict(s=f's = {s.SI_Value:.1f} м')


@variant.text('''
    Изобразите график гармонических колебаний, амплитуда которых составляла бы
    {A:Task:e}, а период {T:Task:e}.
''')
@variant.arg(A=('A = {} см', [1, 2, 3, 5, 6, 15, 30, 40, 75]))
@variant.arg(T=('T = {} с', [2, 4, 6, 8, 10]))
class Nu05(variant.VariantTask):
    pass
