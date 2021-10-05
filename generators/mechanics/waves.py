import math

import generators.variant as variant


@variant.text('''
    Укажите, верны ли утверждения:
    \\begin{itemize}
        \\item механические волны переносят вещество,
        \\item механические волны переносят энергию,
        \\item источником механических волны служат колеблющиеся тела,
        \\item продольные волны могут распространяться только в твёрдых телах,
        \\item в твёрдых телах могут распространяться поперечные волны,
        \\item скорость распространения волны равна произведению её длины на её частоту,
        \\item звуковая волна~--- поперечная волна,
        \\item волна на поверхности озера~--- поперечная волна (или же поверхностная).
    \\end{itemize}
    (4 из 8~--- это «–»)
''')
@variant.answer('нет, да, да, нет, да, да, нет, да''')
@variant.no_args
@variant.solution_space(20)
class Waves00(variant.VariantTask):
    pass


@variant.text('''
    Частота собственных малых колебаний пружинного маятника равна {nu:Task:e}.
    Чему станет равен период колебаний, если массу пружинного маятника увеличить в ${alpha}$ раз?
''')
@variant.answer_short('''
    T'  = 2\\pi\\sqrt{\\frac {m'}k}
        = 2\\pi\\sqrt{\\frac {\\alpha m}k}
        = \\sqrt{\\alpha} * 2\\pi\\sqrt{\\frac mk}
        = \\sqrt{\\alpha} * T
        = T\\sqrt{\\alpha}
        = \\frac 1\\nu * \\sqrt{\\alpha}
        = \\frac{\\sqrt{\\alpha}}{\\nu}
        = \\frac{\\sqrt{{alpha}}}{nu:V:s}
        = {T1:V}
''')
@variant.arg(nu=('\\nu = {} Гц', [2, 4, 5, 8]))
@variant.arg(alpha=[4, 16, 25])
class Waves01(variant.VariantTask):
    def GetUpdate(self, alpha=None, nu=None):
        T1 = alpha ** 0.5 / nu.Value
        return dict(
            T1=f'T\' = {T1:.2f} с',
        )


@variant.text('''
    Тело массой {m:Task:e} совершает гармонические колебания.
    При этом амплитуда колебаний его скорости равна {v:Task:e}.
    Определите запас полной механической энергии колебательной системы
    и амплитуду колебаний потенциальной энергии.
''')
@variant.answer_align([
    '''
        E_{\\text{полная механическая}} &= E_{\\text{max кинетическая}}
        = \\frac{m v_{\\max}^2}2 = \\frac{{m:V} * {v:V|sqr}}2 = {E:V},''',
    'A_{E_{\\text{потенциальная}}} &= \\frac{E_{\\text{полная механическая}}}2 = {E2:V}.'
])
@variant.arg(mLetter=['m', 'M'])
@variant.arg(mValue=[100, 200, 250, 400])
@variant.arg(v=('v = {} м / с', [1, 2, 4, 5]))
class Waves02(variant.VariantTask):
    def GetUpdate(self, mLetter=None, mValue=None, v=None):
        return dict(
            m='%s = %d г' % (mLetter, mValue),
            E='E_1 = %.3f Дж' % (0.001 * mValue * (v.Value ** 2) / 2),
            E2='E_2 = %.3f Дж' % (0.001 * mValue * (v.Value ** 2) / 2 / 2)
        )


@variant.text('''
    Определите расстояние между {first} и {second} гребнями волн,
    если длина волны равна {lmbd:V:e}. Сколько между ними ещё уместилось гребней?
''')
@variant.answer_short('''
    l = (n_2 - n_1) * \\lambda = \\cbr{{n2} - {n1}} * {lmbd:V} = {l:V},
    \\quad n = n_2 - n_1 - 1 = {n2} - {n1} - 1 = {n}
''')
@variant.arg(first__n1=[
    ('первым', 1),
    ('вторым', 2),
    ('третьим', 3),
])
@variant.arg(second__n2=[
    ('шестым', 6),
    ('седьмым', 7),
    ('восьмым', 8),
    ('девятым', 9),
    ('десятым', 10),
])
@variant.arg(lmbd=('\\lambda = {} м', [3, 4, 5, 6]))
class Waves03(variant.VariantTask):
    def GetUpdate(self, first=None, n1=None, second=None, n2=None, lmbd=None):
        return dict(
            l='l = %d м' % ((n2 - n1) * lmbd.Value),
            n=n2 - n1 - 1,
        )


@variant.text('''
    Определите скорость звука в среде, если источник звука,
    колеблющийся с периодом {T:V:e}, возбуждает волны длиной
    {lmbd:V:e}.
''')
@variant.answer_short('\\lambda = vT \\implies v = \\frac{\\lambda}T = \\frac{lmbd:V:s}{T:V:s} = {v:V:s}')
@variant.arg(lmbd=('\\lambda = {} м', [1.2, 1.5, 2.1, 2.4]))
@variant.arg(T=('T = {} мc', [2, 3, 4, 5, 6]))
class Waves04(variant.VariantTask):
    def GetUpdate(self, lmbd=None, T=None):
        return dict(
            v='v = %.1f м / c' % (1000. * lmbd.Value / T.Value),
        )


@variant.text('''
    Мимо неподвижного наблюдателя прошло {N:V:e} гребней волн за {t:V:e},
    начиная с первого. Каковы длина, период и частота волны,
    если скорость распространения волн {v:V:e}?
''')
@variant.answer_align([
    u"\\lambda &= \\frac L{N-1} = \\frac {vt}{N-1} = \\frac {{v:V} * {t:V}}{{N:V} - 1} = {lmbd:V}, ",
    u"T &= \\frac {\\lambda}{v:L} = \\frac {vt}{\\cbr{N-1}v} = \\frac t{N-1} =  \\frac {t:V:s}{{N:V} - 1} = {T:V}, ",
    u"\\nu &= \\frac 1T = \\frac {N-1}t = \\frac {{N:V} - 1}{t:V:s} = {nu:V}. ",
    u"&\\text{Если же считать гребни целиком, т.е. не вычитать единицу:} ",
    u"\\lambda' &= \\frac L{N:L:s} = \\frac {vt}{N:L:s} = \\frac {{v:V} * {t:V}}{N:V:s} = {lmbd_1:V}, ",
    u"T' &= \\frac {\\lambda'}{v:L} = \\frac {vt}{Nv} = \\frac tN =  \\frac {t:V:s}{N:V:s} = {T_1:V}, ",
    u"\\nu' &= \\frac 1{T'} = \\frac {N:L:s}t = \\frac {N:V:s}{t:V:s} = {nu_1:V}. ",
])
@variant.arg(N=('N = {}', [4, 5, 6]))
@variant.arg(t=('t = {} c', [5, 6, 8, 10]))
@variant.arg(v=('v = {} м / с', [1, 2, 3, 4, 5]))
class Waves05(variant.VariantTask):
    def GetUpdate(self, N=None, t=None, v=None):
        return dict(
            lmbd='\\lambda = %.2f м' % (1. * v.Value * t.Value / (N.Value - 1)),
            T='T = %.2f с' % (1. * t.Value / (N.Value - 1)),
            nu='\\nu = %.2f Гц' % (1. * (N.Value - 1) / t.Value),
            lmbd_1='\\lambda = %.2f м' % (1. * v.Value * t.Value / N.Value),
            T_1='T = %.2f с' % (1. * t.Value / N.Value),
            nu_1='\\nu = %.2f Гц' % (1. * N.Value / t.Value),
        )


@variant.text('''
    Сравните длины звуковой волны частотой {nu_1:Task:e} и радиоволны частотой {nu_2:Task:e}.
    Какая больше, во сколько раз? Скорость звука примите равной {v:Task:e}.
''')
@variant.answer_short('''
    {l1:L} = {v:L} T_1 = {v:L} * \\frac 1{nu_1:L:s} = \\frac {v:L}{nu_1:L:s} = \\frac{v:V:s}{nu_1:V:s} = {l1:V},
    \\quad
    {l2:L} = {c:L} T_2 = {c:L} * \\frac 1{nu_2:L:s} = \\frac {c:L}{nu_2:L:s} = \\frac{c:V:s}{nu_2:V:s} = {l2:V},
    \\quad 
    n = \\frac{l2:L:s}{l1:L:s} \\approx {n:V}.
''')
@variant.arg(nu_1=('\\nu_1 = {} Гц', [150, 200, 300, 500]))
@variant.arg(nu_2=('\\nu_2 = {} МГц', [200, 500, 800]))
class Ch1238(variant.VariantTask):
    def GetUpdate(self, nu_1=None, nu_2=None):
        return dict(
            v='v = 320 м / с',
            c='c = 300 Мм / с',
            l1='\\lambda_1 = %.2f м' % (320. / nu_1.Value),
            l2='\\lambda_2 = %.2f м' % (300. / nu_2.Value),
            n='n = %.2f' % ((300. / nu_2.Value) / (320. / nu_1.Value)),
        )


@variant.text('''
    Чему равна длина волны, если две точки среды, находящиеся на расстоянии {l:Task:e},
    совершают колебания с разностью фаз ${delta}$?
''')
@variant.answer_short('''
    \\frac l\\lambda = \\frac \\varphi{2\\pi} + k (k\\in\\mathbb{N:L:s})
    \\implies \\lambda = \\frac l{\\frac \\varphi{2\\pi} + k} = \\frac {2\\pi l}{\\varphi + 2\\pi k},
    \\quad \\lambda_0 = \\frac {2\\pi l}{\\varphi} = {lmbd:V}
''')
@variant.arg(delta__frac=[
    ('\\frac{\\pi}{8}', 1. / 16),
    ('\\frac{2\\pi}{5}', 1. / 5),
    ('\\frac{3\\pi}{8}', 3. / 16),
    ('\\frac{\\pi}{2}', 1. / 4),
    ('\\frac{3\\pi}{4}', 3. / 8),
])
@variant.arg(l=('l = {} см', [20, 25, 40, 50, 75]))
class Ch1240(variant.VariantTask):
    def GetUpdate(self, delta=None, frac=None, l=None):
        return dict(
            lmbd='\\lambda = %.2f см' % (1. * l.Value / frac),
        )
