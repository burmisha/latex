import generators.variant as variant

from generators.helpers import letter_variants, Fraction, Consts, n_times

import math


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
@variant.arg(I='\\eli_{\\max} = 120/150/180/240/270 мА')
@variant.arg(q='q_{\\max} = 40/60/80 мкКл')
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
@variant.arg(I='\\eli = 0.05/0.25/0.30 A')
@variant.arg(L='L = 50/60/70/80 мГн')
@variant.arg(func=['sin', 'cos'])
@variant.answer_align([
    '\\omega &= {omega}\\funits{рад}{c}, \\qquad \\eli_{\\max} = {I:V},',
    'T &= \\frac{2\\pi}\\omega \\approx {T:V},',
    'C &= \\frac 1{\\omega^2 L} \\approx {C:V},',
    '{q:L} &= \\frac{\\eli_{\\max}}\\omega  \\approx {q:V}.',
])
class Task03(variant.VariantTask):
    def GetUpdate(self, *, omega=None, I=None, func=None, L=None):
        T = 2 * math.pi / omega
        C = 1 / float(omega ** 2) / float(L.SI_Value)
        q = float(I.SI_Value) / omega
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
    Электрический колебательный контур состоит
    из катушки индуктивностью $L$ и конденсатора ёмкостью $C$.
    {how} {what1} подключают ещё {what2} ${frac:LaTeX}{what3}$.
    Как изменится частота свободных колебаний в контуре?
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
    \\implies \\frac{\\nu'}{\\nu} = \\frac{T}{T'} = \\frac1{\\sqrt{ {l:LaTeX} * {c:LaTeX} }} \\approx {ans}.
''')
class Task04_2(variant.VariantTask):
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

        ans = 1 / float(l * c) ** 0.5

        if ans > 1:
            answer = f'увеличится в ${ans:.2f}$ раз'
        elif ans < 1:
            answer = f'уменьшится в ${1 / ans:.2f}$ раз'
        elif ans == 1:
            answer = f'не изменится'

        return dict(
            frac=frac,
            l=l,
            c=c,
            ans=f'{ans:.3f}',
            answer=answer,
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
        nu_posl = 1 / (float(1 / nu1.SI_Value ** 2 + 1 / nu2.SI_Value ** 2) ** 0.5)
        nu_par = float(nu1.SI_Value ** 2  + nu2.SI_Value ** 2) ** 0.5
        return dict(
            nu_posl=f'{nu_posl:.2f} Гц',
            nu_par=f'{nu_par:.2f} Гц',
        )


@variant.text('''
    В $LC$-контуре ёмкость конденсатора {C:V:e}, а максимальное напряжение на нём {Um:V:e}.
    Определите энергию магнитного поля катушки в момент времени, когда напряжение на конденсаторе оказалось равным {U:V:e}.
''')
@variant.solution_space(100)
@variant.arg(C=('C = {} мкФ', [2, 4, 6, 8]))
@variant.arg(Um=('U_m = {} В', [7, 9, 12]))
@variant.arg(U=('U = {} В', [1, 3, 5]))
@variant.answer_align([
    'W &= \\frac{LI^2}2 + \\frac{CU^2}2 = \\frac{CU_m^2}2 \\implies W_L = \\frac{CU_m^2}2 - \\frac{CU^2}2 = \\frac C2(U_m^2 - U^2) =',
    '&= \\frac {C:V:s}2 \\cbr{{Um:V|sqr} - {U:V|sqr}} \\approx {Wl:V}.'
])
class Task06(variant.VariantTask):  # Вишнякова 3.5.11
    def GetUpdate(self, *, C=None, Um=None, U=None):
        Wl = C.SI_Value / 2 * (Um.SI_Value ** 2 - U.SI_Value ** 2)
        return dict(
            Wl=f'W_L = {Wl * 1000000:.1f} мкДж',
        )


@variant.text('''
    Конденсатор ёмкостью {C:V:e} зарядили до напряжения {U:V:e} и подключили к катушке индуктивностью {L:V:e}.
    Определите максимальную энергию {what} и период колебаний в $LC$-контуре.
''')
@variant.solution_space(100)
@variant.arg(what=['магнитного поля катушки', 'электрического поля конденсатора'])
@variant.arg(C=('C = {} мкФ', [2, 4, 6, 8]))
@variant.arg(U=('U = {} В', [5, 8, 10]))
@variant.arg(L=('L = {} мГн', [20, 25, 30, 40]))
@variant.answer_align([
    'W &= \\frac{CU^2}2 = \\frac{{C:V} * {U:V|sqr}}2 \\approx {W:V},',
    'T &= 2\\pi\\sqrt{LC}= 2\\pi\\sqrt{{L:V} * {C:V}} \\approx {T:V}',
])
class Task07(variant.VariantTask):
    def GetUpdate(self, *, C=None, U=None, L=None, what=None):
        T = 2 * math.pi * float(L.SI_Value * C.SI_Value) ** 0.5
        return dict(
            W=(C * U * U / 2).SetLetter('W').As('мкДж'),
            T=f'T = {T * 1000:.2f} мс.',
        )


class Relation:
    def __init__(self):
        self._value = Fraction(1)

    def More(self, what, value):
        if 'велич' in what:
            self._value *= nl
        elif 'меньш' in what:
            self._value /= value
        else:
            raise RuntimeError(f'Invalid {what!r}')

    def Inv(self, what, *args):
        if what in args:
            self._value = 1 / self._value


@variant.text('''
    Во сколько раз (и как) изменится {what} свободных незатухающих колебаний в контуре,
    если его индуктивность {what_l} в {nl_times}, а ёмкость {what_c} в {nc_times}?
''')
@variant.solution_space(100)
@variant.arg(what=['частота', 'период', 'циклическая частота'])
@variant.arg(what_l=['уменьшить', 'увеличить'])
@variant.arg(what_c=['уменьшить', 'увеличить'])
@variant.arg(nl__nl_times=n_times(2, 3, 4, 5, 6))
@variant.arg(nc__nc_times=n_times(3, 4, 5, 6, 7))
@variant.answer_short('\\text{{answer}}')
class Task08(variant.VariantTask):
    def GetUpdate(self, *, what=None, what_l=None, what_c=None, nl=None, nl_times=None, nc=None, nc_times=None):
        n = Fraction(1)
        if what_l == 'увеличить':
            n *= nl
        elif what_l == 'уменьшить':
            n /= nl
        else:
            raise RuntimeError(f'Invalid {what_l}')
        if what_c == 'увеличить':
            n *= nc
        elif what_c == 'уменьшить':
            n /= nc
        else:
            raise RuntimeError(f'Invalid {what_c}')

        if what == 'частота':
            n = 1 / n
        elif what == 'период':
            pass
        elif what == 'циклическая частота':
            n = 1 / n
        else:
            raise RuntimeError(f'Invalid {what}')

        n_value = float(n) ** 0.5

        if n > 1:
            answer = f'увеличится в ${n_value:.2f}$ раз'
        elif n < 1:
            answer = f'уменьшится в ${1 / n_value:.2f}$ раз'
        elif n == 1:
            answer = f'не изменится'

        return dict(
            answer=answer,
        )



@variant.text('''
    В схеме (см. рис. на доске) при разомкнутом ключе $K$ конденсатор ёмкостью {C:Task:e} заряжен до напряжения {U0:Task:e}.
    ЭДС батареи {E:Task:e}, индуктивность катушки {L:Task:e}. Определите
    \\begin{itemize}
        \\item чему равен установившийся ток в цепи после замыкания ключа?
        \\item чему равен максимальный ток в цепи после замыкания ключа?
    \\end{itemize}
    Внутренним сопротивлением батареи и омическим сопротивлением катушки пренебречь, $D$ — идеальный диод.
''')
@variant.solution_space(100)
@variant.arg(C=('C = {} мкФ', [10]))
@variant.arg(U0=('U_0 = {} В', [10]))
@variant.arg(L=('L = {} В', [0.1]))
@variant.arg(E=('\\ele = {} В', [15]))
class Task09(variant.VariantTask):  # 3.120 Чешев
    pass


@variant.text('''
    Во сколько раз уменьшится частота собственных колебаний контура,
    если его индуктивность увеличить в 10 раз, а емкость уменьшить в 2,5 раза?
''')
@variant.solution_space(100)
class Chernoutsan_12_43(variant.VariantTask):
    pass


@variant.text('''
    Колебательный контур с конденсатором емкостью 1 мкФ настроен на частоту 400 Гц.
    Если подключить к нему параллельно второй конденсатор, то частота колебаний в контуре становится равной 200 Гц.
    Определите емкость (в мкФ) второго конденсатора.
''')
@variant.solution_space(100)
class Chernoutsan_12_44(variant.VariantTask):
    pass



@variant.text('''
    В колебательном контуре к конденсатору параллельно присоединили другой конденсатор,
    втрое большей емкости, после чего частота колебаний контура уменьшилась на 300 Гц.
    Найдите первоначальную частоту колебаний контура.
''')
@variant.solution_space(100)
class Chernoutsan_12_45(variant.VariantTask):
    pass


@variant.text('''
    Колебательный контур состоит из катушки и конденсатора.
    Во сколько раз увеличится частота собственных колебаний в контуре,
    если в контур последовательно включить второй конденсатор,
    емкость которого в 3 раза меньше емкости первого?
''')
@variant.solution_space(100)
class Chernoutsan_12_46(variant.VariantTask):
    pass


@variant.text('''
    Максимальная разность потенциалов на конденсаторе в колебательном контуре 100 В.
    Какой будет максимальная сила тока, если конденсатор имеет емкость 36 мкФ,
    а катушка обладает индуктивностью 0,01 Гн?
''')
@variant.solution_space(100)
class Chernoutsan_12_47(variant.VariantTask):
    pass


@variant.text('''
    К конденсатору, заряд которого 250 пКл, подключили катушку индуктивности.
    Определите максимальную силу тока (в мА)‚ протекающего через катушку,
    если циклическая частота свободных колебаний в контуре 8- 107 рад/с.
''')
@variant.solution_space(100)
class Chernoutsan_12_48(variant.VariantTask):
    pass


@variant.text('''
    Заряженный конденсатор емкостью 4 мкФ подключили к катушке с индуктивностью 90 мГн.
    Через какое минимальное время (в мкс) от момента подключения заряд конденсатора уменьшится в 2'раза? л = 3,14.
''')
@variant.solution_space(100)
class Chernoutsan_12_49(variant.VariantTask):
    pass
