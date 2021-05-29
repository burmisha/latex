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
@variant.answer_short('\\nu = \\frac 1T = \\frac 1{T:Value:s} = {nu:Value}')
@variant.arg(T=['T = %d мс' % T for T in [2, 4, 5, 10, 20, 40, 50]])
class Nu02(variant.VariantTask):
    def GetUpdate(self, T=None, **kws):
        return dict(
            nu='''\\nu = %d Гц''' % (1000 / T.Value),
        )


@variant.text('''
    Определите период колебаний, если их частота составляет {nu:Task:e}.
    Сколько колебаний произойдёт за {t:Task:e}?
''')
@variant.answer_align([
    'T &= \\frac 1\\nu = \\frac 1{nu:Value:s} = {T:Value},',
    'N &= \\nu t = {nu:Value|cdot}{t:Value} = {N:Value}.',
])
@variant.arg(nu=['\\nu = %d кГц' % nu for nu in [2, 4, 5, 10, 20, 40, 50]])
@variant.arg(t=['t = %d мин' % t for t in [1, 2, 3, 5, 10]])
class Nu03(variant.VariantTask):
    def GetUpdate(self, nu=None, t=None, **kws):
        return dict(
            T='T = %.3f мc' % (1. / nu.Value),
            N='N = %d колебаний' % (nu.Value * 1000 * t.Value * 60),
        )


@variant.text('''
    Амплитуда колебаний точки составляет {A:Task:e}, а частота~--- {nu:Task:e}.
    Определите, какой путь преодолеет эта точка за {t:Task:e}.
''')
@variant.answer_short('''
    s
        = 4A * N = 4A * \\frac tT = 4A * t\\nu
        = 4 * {A:Value} * {t:Value} * {nu:Value}
        = {s:Value}
''')
@variant.arg(A=['A = %d см' % A for A in [2, 3, 5, 10, 15]])
@variant.arg(nu=['\\nu = %d Гц' % nu for nu in [2, 5, 6, 10, 20]])
@variant.arg(t=['t = %d с' % t for t in [10, 40, 80]])
class Nu04(variant.VariantTask):
    def GetUpdate(self, A=None, nu=None, t=None, **kws):
        return dict(
            s='s = %.1f м' % (4. * A.Value / 100 * t.Value * nu.Value),
        )


@variant.text('''
    Изобразите график гармонических колебаний, амплитуда которых составляла бы
    {A:Task:e}, а период {T:Task:e}.
''')
@variant.arg(A=['A = %d см' % A for A in [1, 2, 3, 5, 6, 15, 30, 40, 75]])
@variant.arg(T=['T = %d с' % T for T in [2, 4, 6, 8, 10]])
class Nu05(variant.VariantTask):
    pass
