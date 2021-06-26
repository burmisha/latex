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
@variant.answer('''нет, да, да, нет, да, да, нет, да''')
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
        = \\frac{\\sqrt{{alpha}}}{nu:Value:s}
        = {T1:Value}
''')
@variant.arg(nu=['\\nu = %s Гц' % nu for nu in ['2', '4', '5', '8']])
@variant.arg(alpha=['4', '16', '25'])
class Waves01(variant.VariantTask):
    def GetUpdate(self, alpha=None, nu=None, **kws):
        return dict(
            T1='T\' = %.2f с' % (math.sqrt(int(alpha)) / int(nu.Value)),
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
        = \\frac{m v_{\\max}^2}2 = \\frac{{m:Value} * {v:Value|sqr}}2 = {E:Value},''',
    'A_{E_{\\text{потенциальная}}} &= \\frac{E_{\\text{полная механическая}}}2 = {E2:Value}.'
])
@variant.arg(mLetter=['m', 'M'])
@variant.arg(mValue=[100, 200, 250, 400])
@variant.arg(v=['v = %d м / с' % v for v in [1, 2, 4, 5]])
class Waves02(variant.VariantTask):
    def GetUpdate(self, mLetter=None, mValue=None, v=None, **kws):
        return dict(
            m='%s = %d г' % (mLetter, mValue),
            E='E_1 = %.3f Дж' % (0.001 * mValue * (v.Value ** 2) / 2),
            E2='E_2 = %.3f Дж' % (0.001 * mValue * (v.Value ** 2) / 2 / 2)
        )


@variant.text('''
    Определите расстояние между {first} и {second} гребнями волн,
    если длина волны равна {lmbd:Value:e}. Сколько между ними ещё уместилось гребней?
''')
@variant.answer_short('''
    l = (n_2 - n_1) * \\lambda = \\cbr{{n2} - {n1}} * {lmbd:Value} = {l:Value},
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
@variant.arg(lmbd=['\\lambda = %d м' % lmbd for lmbd in [3, 4, 5, 6]])
class Waves03(variant.VariantTask):
    def GetUpdate(self, n1=None, n2=None, lmbd=None, **kws):
        return dict(
            l='l = %d м' % ((n2 - n1) * lmbd.Value),
            n=n2 - n1 - 1,
        )


@variant.text('''
    Определите скорость звука в среде, если источник звука,
    колеблющийся с периодом {T:Value:e}, возбуждает волны длиной
    {lmbd:Value:e}.
''')
@variant.answer_short('\\lambda = vT \\implies v = \\frac{\\lambda}T = \\frac{lmbd:Value:s}{T:Value:s} = {v:Value:s}')
@variant.arg(lmbd=['\\lambda = %.1f м' % lmbd for lmbd in [1.2, 1.5, 2.1, 2.4]])
@variant.arg(T=['T = %d мc' % T for T in [2, 3, 4, 5, 6]])
class Waves04(variant.VariantTask):
    def GetUpdate(self, lmbd=None, T=None, **kws):
        return dict(
            v='v = %.1f м / c' % (1000. * lmbd.Value / T.Value),
        )


@variant.text('''
    Мимо неподвижного наблюдателя прошло {N:Value:e} гребней волн за {t:Value:e},
    начиная с первого. Каковы длина, период и частота волны,
    если скорость распространения волн {v:Value:e}?
''')
@variant.answer_align([
    u"\\lambda &= \\frac L{N-1} = \\frac {vt}{N-1} = \\frac {{v:Value} * {t:Value}}{{N:Value} - 1} = {lmbd:Value}, ",
    u"T &= \\frac {\\lambda}{v:L} = \\frac {vt}{\\cbr{N-1}v} = \\frac t{N-1} =  \\frac {t:Value:s}{{N:Value} - 1} = {T:Value}, ",
    u"\\nu &= \\frac 1T = \\frac {N-1}t = \\frac {{N:Value} - 1}{t:Value:s} = {nu:Value}. ",
    u"&\\text{Если же считать гребни целиком, т.е. не вычитать единицу:} ",
    u"\\lambda' &= \\frac L{N:L:s} = \\frac {vt}{N:L:s} = \\frac {{v:Value} * {t:Value}}{N:Value:s} = {lmbd_1:Value}, ",
    u"T' &= \\frac {\\lambda'}{v:L} = \\frac {vt}{Nv} = \\frac tN =  \\frac {t:Value:s}{N:Value:s} = {T_1:Value}, ",
    u"\\nu' &= \\frac 1{T'} = \\frac {N:L:s}t = \\frac {N:Value:s}{t:Value:s} = {nu_1:Value}. ",
])
@variant.arg(N=['N = %d' % N for N in [4, 5, 6]])
@variant.arg(t=['t = %d c' % t for t in [5, 6, 8, 10]])
@variant.arg(v=['v = %d м / с' % v for v in [1, 2, 3, 4, 5]])
class Waves05(variant.VariantTask):
    def GetUpdate(self, N=None, t=None, v=None, **kws):
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
    \\lambda_1
        = v T_1 = v * \\frac 1{\\nu_1} = \\frac {v:L}{\\nu_1}
        = \\frac{v:Value:s}{nu_1:Value:s} = {l_1:Value},
    \\quad
    \\lambda_2
        = c T_2 = c * \\frac 1{\\nu_2} = \\frac c{\\nu_2}
        = \\frac{c:Value:s}{nu_2:Value:s} = {l_2:Value},
    \\quad n = \\frac{\\lambda_2}{\\lambda_1} \\approx {n:Value}
''')
@variant.arg(nu_1=['\\nu_1 = %s Гц' % nu_1 for nu_1 in [150, 200, 300, 500]])
@variant.arg(nu_2=['\\nu_2 = %s МГц' % nu_2 for nu_2 in [200, 500, 800]])
class Ch1238(variant.VariantTask):
    def GetUpdate(self, nu_1=None, nu_2=None, **kws):
        return dict(
            v='v = 320 м / с',
            c='c = 300 Мм / с',
            l_1='l_1 = %.2f м' % (320. / nu_1.Value),
            l_2='l_2 = %.2f м' % (300. / nu_2.Value),
            n='n = %.2f' % ((300. / nu_2.Value) / (320. / nu_1.Value)),
        )


@variant.text('''
    Чему равна длина волны, если две точки среды, находящиеся на расстоянии {l:Task:e},
    совершают колебания с разностью фаз ${delta}$?
''')
@variant.answer_short('''
    \\frac l\\lambda = \\frac \\varphi{2\\pi} + k (k\\in\\mathbb{N:L:s})
    \\implies \\lambda = \\frac l{\\frac \\varphi{2\\pi} + k} = \\frac {2\\pi l}{\\varphi + 2\\pi k},
    \\quad \\lambda_0 = \\frac {2\\pi l}{\\varphi} = {lmbd:Value}
''')
@variant.arg(delta__frac=[
    ('\\frac{\\pi}{8}', 1. / 16),
    ('\\frac{2\\pi}{5}', 1. / 5),
    ('\\frac{3\\pi}{8}', 3. / 16),
    ('\\frac{\\pi}{2}', 1. / 4),
    ('\\frac{3\\pi}{4}', 3. / 8),
])
@variant.arg(l=['l = %d см' % l for l in [20, 25, 40, 50, 75]])
class Ch1240(variant.VariantTask):
    def GetUpdate(self, l=None, frac=None, **kws):
        return dict(
            lmbd='\\lambda = %.2f см' % (1. * l.Value / frac),
        )
