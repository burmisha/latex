import generators.variant as variant
from generators.helpers import Consts, Decimal


@variant.text('''
    Шарики массами {m1:Value:e} и {m2:Value:e}
    движутся параллельно друг другу в одном направлении
    со скоростями {v1:Value:e} и {v2:Value:e} соответственно.
    Сделайте рисунок и укажите направления скоростей и импульсов.
    Определите импульс каждого из шариков, а также их суммарный импульс.
''')
@variant.text_test('''
    Шарики массами {m1:Value:e} и {m2:Value:e} движутся параллельно друг другу в одном направлении
    со скоростями {v1:Value:e} и {v2:Value:e} соответственно. Определите общий импульс шариков.
''')
@variant.answer_align([
    '{p1:Letter} &= {m1:Letter}{v1:Letter} = {m1:Value} * {v1:Value} = {p1:Value},',
    '{p2:Letter} &= {m2:Letter}{v2:Letter} = {m2:Value} * {v2:Value} = {p2:Value},',
    '{p:Letter} &= {p1:Letter} + {p2:Letter} = {m1:Letter}{v1:Letter} + {m2:Letter}{v2:Letter} = {p:Value}.',
])
@variant.answer_test('{p:TestAnswer}')
@variant.arg(m1__m2=[('m_1 = %d кг' % m1, 'm_2 = %d кг' % m2) for m1 in [1, 2, 3, 4] for m2 in [1, 2, 3, 4] if m1 != m2])
@variant.arg(v1=['v_1 = %d м / с' % v1 for v1 in [2, 4, 5, 10]])
@variant.arg(v2=['v_2 = %d м / с' % v2 for v2 in[3, 6, 8]])
class Ch_3_1(variant.VariantTask):
    def GetUpdate(self, m1=None, m2=None, v1=None, v2=None):
        return dict(
            p1=(m1 * v1).SetLetter('p_1'),
            p2=(m2 * v2).SetLetter('p_2'),
            p='p = %d кг м / с' % (m1.Value * v1.Value + m2.Value * v2.Value),
        )


@variant.text('''
    Два шарика, масса каждого из которых составляет {m:Value:e},
    движутся навстречу друг другу.
    Скорость одного из них {v1:Value:e}, а другого~--- {v2:Value:e}.
    Сделайте рисунок, укажите направления скоростей и импульсов.
    Определите импульс каждого из шариков, а также их суммарный импульс.
''')
@variant.text_test('''
    Два шарика, масса каждого из которых составляет {m:Value:e}, движутся навстречу друг другу.
    Скорость одного из них {v1:Value:e}, а другого~--- {v2:Value:e}. Определите общий импульс шариков.
''')
@variant.answer_align([
    '{p1:L} &= {m:L}{v1:L} = {m:Value} * {v1:Value} = {p1:Value},',
    '{p2:L} &= {m:L}{v2:L} = {m:Value} * {v2:Value} = {p2:Value},',
    '{p:L} &= \\abs{{p1:L} - {p2:L}} = \\abs{{m:L}({v1:L} - {v2:L})}= {p:Value}.',
])
@variant.answer_test('{p:TestAnswer}')
@variant.arg(m=['m = %d кг' % m for m in [2, 5, 10]])
@variant.arg(v1=['v_1 = %d м / с' % v1 for v1 in [1, 2, 5, 10]])
@variant.arg(v2=['v_2 = %d м / с' % v2 for v2 in [3, 6, 8]])
class Ch_3_2(variant.VariantTask):
    def GetUpdate(self, m=None, v1=None, v2=None):
        return dict(
            p1=(m * v1).SetLetter('p_1'),
            p2=(m * v2).SetLetter('p_2'),
            p='p = %d кг м / с' % abs(m.Value * v1.Value - m.Value * v2.Value),
        )


@variant.text('''
    Два одинаковых шарика массами по {m:Value:e}
    движутся во взаимно перпендикулярных направлениях.
    Скорости шариков составляют {v1:Value:e} и {v2:Value:e}.
    Сделайте рисунок, укажите направления скоростей и импульсов.
    Определите импульс каждого из шариков и полный импульс системы.
''')
@variant.text_test('''
    Два одинаковых шарика массами по {m:Value:e} движутся во взаимно перпендикулярных направлениях.
    Скорости шариков составляют {v1:Value:e} и {v2:Value:e}. Определите полный импульс системы.
''')
@variant.answer_align([
    '{p1:L} &= {m:L}{v1:L} = {m:Value} * {v1:Value} = {p1:Value},',
    '{p2:L} &= {m:L}{v2:L} = {m:Value} * {v2:Value} = {p2:Value},',
    '{p:L} &= \\sqrt{{p1:L}^2 + {p2:L}^2} = {m:L}\\sqrt{{v1:L}^2 + {v2:L}^2} = {p:Value}.',
])
@variant.answer_test('{p:TestAnswer}')
@variant.arg(v1__v2__v=[(
    'v_1 = %d м / с' % v1,
    'v_2 = %d м / с' % v2,
    'v = %d м / с' % v3,
) for v1, v2, v3 in [
    (3, 4, 5),
    (5, 12, 13),
    (7, 24, 25),
]])
@variant.arg(m=['m = %d кг' % m for m in [2, 5, 10]])
class Ch_3_3(variant.VariantTask):
    def GetUpdate(self, m=None, v1=None, v2=None, v=None):
        return dict(
            p1=(m * v1).SetLetter('p_1'),
            p2=(m * v2).SetLetter('p_2'),
            p='p = %d кг м / с' % (m.Value * v.Value),
        )


@variant.text('''
    Шарик массой {m:Value:e} свободно упал на горизонтальную площадку, имея в момент падения скорость {v:Value:e}.
    Считая удар абсолютно {which}, определите изменение импульса шарика. В ответе укажите модуль полученной величины.
''')
@variant.answer_align([
    '{delta_p:L} &= {mult} * {m:L}{v:L} = {mult} * {m:Value} * {v:Value} = {delta_p:Value}.',
])
@variant.answer_test('{delta_p:TestAnswer}')
@variant.arg(which__mult=[('упругим', 2), ('неупругим', 1)])
@variant.arg(m=['m = %d кг' % m for m in [1, 2, 4]])
@variant.arg(v=['v = %d м / с' % v for v in [10, 15, 20, 25]])
class Ch_3_6(variant.VariantTask):
    def GetUpdate(self, m=None, v=None, which=None, mult=None):
        return dict(
            delta_p=(m * v * mult).SetLetter('\\Delta p')
        )


@variant.text('''
    Паровоз массой {M:Task:e}, скорость которого равна {v:Task:e},
    сталкивается с {count} неподвижными вагонами массой {m:Task:e} каждый и сцепляется с ними.
    Запишите (формулами, не числами) импульсы каждого из тел до и после сцепки и после,
    а также определите скорость их совместного движения.
''')
@variant.answer_align([
    '\\text{ЗСИ: } &M * v + {n} * \\cbr{m * 0} =  M * u + {n} * \\cbr{m * u} \\implies',
    '&\\implies u = v * \\frac M{M + nm} = {v:Value} *  \\frac{M:Value|s}{{M:Value} + {n} * {m:Value}} \\approx {u:Value}.',
])
@variant.arg(M=['M = %d т' % M for M in [120, 150, 210]])
@variant.arg(m=['m = %d т' % m for m in [30, 40, 50]])
@variant.arg(v=['v = %.2f м / с' % v for v in [0.2, 0.4, 0.6]])
@variant.arg(count__n=[('двумя', 2), ('тремя', 3), ('четыремя', 4)])
class Ch_3_24(variant.VariantTask):
    def GetUpdate(self, m=None, M=None, v=None, count=None, n=None):
        return dict(
            u='u = %.2f м / с' % (v.Value * M.Value / (M.Value + n * m.Value)),
        )


@variant.text('''
    Два тела двигаются навстречу друг другу. Скорость каждого из них составляет {v1:Value:e}.
    После соударения тела слиплись и продолжили движение уже со скоростью {v2:Value:e}.
    Определите отношение масс тел (большей к меньшей).
''')
# @variant.arg(v=['v = %f м / с' % v for v in [3, 4, 5, 6]])
# @variant.arg(u=['u = %.1f м / с' % u for u in [1.0, 1.5, 2.0]])
@variant.answer_align([
    '&\\text{ЗСИ в проекции на ось, соединяющую центры тел: } m_1 v_1 - m_2 v_1 = (m_1 + m_2) v_2 \\implies',
    '''&\\implies \\frac{m_1}{m_2} v_1 - v_1 = \\cbr{\\frac{m_1}{m_2} + 1} v_2 \\implies
    \\frac{m_1}{m_2} (v_1 - v_2) = v_2 + v_1 \\implies \\frac{m_1}{m_2} = \\frac{v_2 + v_1}{v_1 - v_2} = {answer}''',
])
@variant.answer_test('{answer}')
@variant.arg(v1__v2=[(
    'v_1 = %d м / с' % v1,
    'v_2 = %d м / с' % v2,
) for v1, v2 in [
    (2, 1),
    (3, 1),
    (6, 3),
    (4, 3),
    (5, 4),
    (6, 4),
    (5, 3),
    (7, 5),
    (9, 7),
    (11, 9),
]])
class Ch_3_26(variant.VariantTask):
    def GetUpdate(self, v1=None, v2=None):
        assert (v1.Value + v2.Value) % (v1.Value - v2.Value) == 0
        return dict(
            answer=int((v1.Value + v2.Value) / (v1.Value - v2.Value)),
        )


@variant.text('''
    Шар движется с некоторой скоростью и абсолютно неупруго соударяется с телом, масса которого в {N} раз больше.
    Определите во сколько раз уменьшилась скорость шара после столкновения.
''')
@variant.answer_align([
    '&\\text{ЗСИ в проекции на ось, соединяющую центры тел: } ',
    '&mv + {N}m * 0 = (m + {N}m) v\' \\implies',
    '&v\' = v\\frac m{{N}m + m} = \\frac v{{N} + 1} \\implies \\frac v{v\'} = {answer}',
])
@variant.answer_test('{answer}')
@variant.arg(N=list(range(5, 15)))
class Vishnyakova_1_4_6(variant.VariantTask):
    def GetUpdate(self, N=None):
        return dict(
            answer=N + 1,
        )


@variant.text('''
    Для того, чтобы разогать тело из состояния покоя до скорости $v$ с постоянным ускорением,
    требуется совершить работу {A1:Value:e}. Какую работу нужно совершить, чтобы увеличить скорость этого тела от $v$ до ${n}v$?
''')
@variant.answer_align([
    '&\\text{Изменение кинетической энергии равно работе внешних сил: }',
    '&A_1 = \\frac{mv^2}2 - \\frac{m * 0^2}2 = \\frac{mv^2}2, A_2 = \\frac{m\\sqr{{n}v }}2 - \\frac{mv^2}2 \\implies ',
    '&\\implies A_2 = \\frac{mv^2}2 \\cbr{{n}^2 - 1} = A_1 * \\cbr{{n}^2 - 1} = {A2:Value}.'
])
@variant.answer_test('{A2:TestAnswer}')
@variant.arg(A1=['A = %d Дж' % A for A in [10, 20, 40, 100, 200]])
@variant.arg(n=[2, 3, 4, 5])
class Vishnyakova_1_4_12(variant.VariantTask):
    def GetUpdate(self, A1=None, n=None):
        return dict(
            A2='A\' = %d Дж' % (A1.Value * (n ** 2 - 1)),
        )


@variant.solution_space(60)
@variant.text('''
    Определите работу силы, которая обеспечит {what} тела массой {m:Value:e} на высоту {h:Value:e} с постоянным ускорением {a:Value:e}.
    % Примите {Consts.g_ten:Task:e}.
''')
@variant.answer_align([
    '&\\text{Для подъёма: } A = Fh = (mg + ma) h = m(g+a)h,',
    '&\\text{Для спуска: } A = -Fh = -(mg - ma) h = -m(g-a)h,',
    '&\\text{В результате получаем: } {A:Task}.',
])
@variant.answer_test('{A:TestAnswer}')
@variant.arg(what__mult=[('подъём', +1), ('спуск', -1)])
@variant.arg(a=['a = %d м / с^2' % a for a in [2, 3, 4, 6]])
@variant.arg(m=['m = %d кг' % m for m in [2, 3, 5]])
@variant.arg(h=['h = %d м' % h for h in [2, 5, 10]])
class Ch_4_2(variant.VariantTask):
    def GetUpdate(self, what=None, mult=None, m=None, h=None, a=None):
        return dict(
            A='A = %d Дж' % (mult * m.Value * h.Value * (Consts.g_ten.Value + mult * a.Value))
        )


@variant.text('''
    Тело массой {m:Value} бросили с обрыва {how} с начальной скоростью {v0:Value:e}.
    Через некоторое время скорость тела составила {v:Value:e}.
    Пренебрегая сопротивлением воздуха и считая падение тела свободным, определите работу силы тяжести в течение наблюдаемого промежутка времени.
''')
@variant.answer_align([
    '&\\text{Изменение кинетической энергии равно работе внешних сил: }',
    '&\\Delta E_k = E_k\' - E_k = A_\\text{тяж} \\implies A_\\text{тяж} = \\frac{mv\'^2}2 - \\frac{mv_0^2}2 = {A:Value}.'
])
@variant.answer_test('{A:TestAnswer}')
@variant.arg(how=['вертикально вверх', 'горизонтально', 'под углом $45\\degrees$ к горизонту', 'под углом $30\\degrees$ к горизонту'])
@variant.arg(m=['m = %d кг' % m for m in [1, 2, 3]])
@variant.arg(v0=['v_0 = %d м / с' % v for v in [2, 4, 6]])
@variant.arg(v=['v = %d м / с' % v for v in [8, 10, 12]])
class Ch_4_29(variant.VariantTask):
    def GetUpdate(self, how=None, m=None, v=None, v0=None):
        return dict(
            A='%d Дж' % (m.Value * (v.Value ** 2 - v0.Value ** 2) / 2)
        )


@variant.text('''
    Тонкий однородный {what} длиной {l:Value:e} и массой {m:Value:e} лежит на горизонтальной поверхности.
    \\begin{itemize}
        \\item Какую минимальную силу надо приложить к одному из его концов, чтобы оторвать его от этой поверхности?
        \\item Какую минимальную работу надо совершить, чтобы поставить его на землю в вертикальное положение?
    \\end{itemize}
    % Примите {Consts.g_ten:Task:e}.
''')
@variant.answer_short('F = \\frac{mg}2 \\approx {F:V}, A = mg\\frac l2 = {A:V}')
@variant.answer_test('{A:TestAnswer}')
@variant.arg(what=['лом', 'шест', 'кусок арматуры'])
@variant.arg(m=['m = %d кг' % m for m in [10, 20, 30]])
@variant.arg(l=['l = %d м' % l for l in [1, 2, 3]])
class Ch_4_45(variant.VariantTask):
    def GetUpdate(self, what=None, m=None, l=None):
        return dict(
            F=(m * Consts.g_ten).SetLetter('F'),
            A=(m * l * Consts.g_ten / 2).SetLetter('A'),
        )


@variant.solution_space(100)
@variant.text('''
    Тело бросили вертикально вверх со скоростью {v:Value:e}.
    На какой высоте кинетическая энергия тела составит {how} от потенциальной?
''')
@variant.arg(how__n=[('половину', 2), ('треть', 3)])
@variant.arg(v=('v_0 = {} м / с', [10, 14, 20]))
@variant.answer_align([
    '0 + \\frac{mv_0^2}2 = E_p + E_k, E_k = \\frac 1{n} E_p \\implies',
    '\\implies \\frac{mv_0^2}2 = E_p + \\frac 1{n} E_p = E_p\\cbr{1 + \\frac 1{n}} = mgh\\cbr{1 + \\frac 1{n}} \\implies',
    '\\implies h = \\frac{\\frac{mv_0^2}2}{mg\\cbr{1 + \\frac 1{n}}} = \\frac{v_0^2}{2g} * \\frac 1{1 + \\frac 1{n}} \\approx {h:V}.'
    ])
class Ek_ratio_Ep(variant.VariantTask):
    def GetUpdate(self, how=None, n=None, v=None):
        return dict(
            h=(v * v / 2 / Consts.g_ten / (1 + 1 / n)).SetLetter('h').IncPrecision(1),
        )
