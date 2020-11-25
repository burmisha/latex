# -*- coding: utf-8 -*-

import generators.variant as variant

import logging
log = logging.getLogger(__name__)


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
    '{p1:Letter} &= {m1:Letter}{v1:Letter} = {m1:Value|cdot}{v1:Value} = {p1:Value},',
    '{p2:Letter} &= {m2:Letter}{v2:Letter} = {m2:Value|cdot}{v2:Value} = {p2:Value},',
    '{p:Letter} &= {p1:Letter} + {p2:Letter} = {m1:Letter}{v1:Letter} + {m2:Letter}{v2:Letter} = {p:Value}.',
])
@variant.answer_test('{p:TestAnswer}')
@variant.arg(m1__m2=[('m_1 = %d кг' % m1, 'm_2 = %d кг' % m2) for m1 in [1, 2, 3, 4] for m2 in [1, 2, 3, 4] if m1 != m2])
@variant.arg(v1=['v_1 = %d м / с' % v1 for v1 in [2, 4, 5, 10]])
@variant.arg(v2=['v_2 = %d м / с' % v2 for v2 in[3, 6, 8]])
class Ch_3_1(variant.VariantTask):
    def GetUpdate(self, m1=None, m2=None, v1=None, v2=None, **kws):
        return dict(
            p1='p_1 = %d кг м / с' % (m1.Value * v1.Value),
            p2='p_2 = %d кг м / с' % (m2.Value * v2.Value),
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
    '{p1:L} &= {m:L}{v1:L} = {m:Value|cdot}{v1:Value} = {p1:Value},',
    '{p2:L} &= {m:L}{v2:L} = {m:Value|cdot}{v2:Value} = {p2:Value},',
    '{p:L} &= {p1:L} - {p2:L} = {m:L}({v1:L} - {v2:L}) = {p:Value}.',
])
@variant.answer_test('{p:TestAnswer}')
@variant.arg(m=['m = %d кг' % m for m in [2, 5, 10]])
@variant.arg(v1=['v_1 = %d м / с' % v1 for v1 in [1, 2, 5, 10]])
@variant.arg(v2=['v_2 = %d м / с' % v2 for v2 in [3, 6, 8]])
class Ch_3_2(variant.VariantTask):
    def GetUpdate(self, m=None, v1=None, v2=None, **kws):
        return dict(
            p1='p_1 = %d кг м / с' % (m.Value * v1.Value),
            p2='p_2 = %d кг м / с' % (m.Value * v2.Value),
            p='p = %d кг м / с' % (m.Value * v1.Value - m.Value * v2.Value),
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
    '{p1:L} &= {m:L}{v1:L} = {m:Value|cdot}{v1:Value} = {p1:Value},',
    '{p2:L} &= {m:L}{v2:L} = {m:Value|cdot}{v2:Value} = {p2:Value},',
    '{p:L} &= \\sqrt{ {p1:L}^2 + {p2:L}^2 } = {m:L}\\sqrt{ {v1:L}^2 + {v2:L}^2 } = {p:Value}.',
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
    def GetUpdate(self, m=None, v1=None, v2=None, v=None, **kws):
        return dict(
            p1='p_1 = %d кг м / с' % (m.Value * v1.Value),
            p2='p_2 = %d кг м / с' % (m.Value * v2.Value),
            p='p = %d кг м / с' % (m.Value * v.Value),
        )


@variant.text('''
    Шарик массой {m:Value:e} свободно упал на горизонтальную площадку, имея в момент падения скорость {v:Value:e}.
    Считая удар абсолютно {which}, определите изменение импульса шарика. В ответе укажите модуль полученной величины.
''')
@variant.answer_align([
    '{delta_p:L} &= {mult} \\cdot {m:L}{v:L} = {mult} \\cdot {m:Value|cdot}{v:Value} = {delta_p:Value}.',
])
@variant.answer_test('{delta_p:TestAnswer}')
@variant.arg(which__mult=[('упругим', 2), ('неупругим', 1)])
@variant.arg(m=['m = %d кг' % m for m in [1, 2, 4]])
@variant.arg(v=['v = %d м / c' % v for v in [10, 15, 20, 25]])
class Ch_3_6(variant.VariantTask):
    def GetUpdate(self, m=None, v=None, which=None, mult=None, **kws):
        return dict(
            delta_p='\\Delta p = %d кг м / с' % (mult * m.Value * v.Value),
        )


@variant.text('''
    Паровоз массой {M:Task:e}, скорость которого равна {v:Task:e},
    сталкивается с {count} неподвижными вагонами массой {m:Task:e} каждый и сцепляется с ними.
    Запишите (формулами, не числами) импульсы каждого из тел до и после сцепки и после,
    а также определите скорость их совместного движения.
''')
@variant.answer_align([
    '\\text{ ЗСИ: } &M\\cdot v + {n} \\cdot{ m \\cdot 0 } =  M \\cdot u + {n} \\cdot \\cbr{ m \\cdot u } \\implies',
    '&\\implies u = v\\cdot \\frac{ M }{ M + nm } = {v:Value|cdot} \\frac{M:Value|s}{ {M:Value} + {n} \\cdot {m:Value} } \\approx {u:Value}.',
])
@variant.arg(M=['M = %d т' % M for M in [120, 150, 210]])
@variant.arg(m=['m = %d т' % m for m in [30, 40, 50]])
@variant.arg(v=['v = %.2f м / с' % v for v in [0.2, 0.4, 0.6]])
@variant.arg(count__n=[('двумя', 2), ('тремя', 3), ('четыремя', 4)])
class Ch_3_24(variant.VariantTask):
    def GetUpdate(self, m=None, M=None, n=None, v=None, **kws):
        return dict(
            u='u = %.2f м / с' % (1.0 * v.Value * M.Value / (M.Value + n * m.Value)),
        )


@variant.text('''
    Два тела двигаются навстречу друг другу. Скорость каждого из них составляет {v1:Value:e}.
    После соударения тела слиплись и продолжили движение уже со скоростью {v2:Value:e}.
    Определите отношение масс тел (большей к меньшей).
''')
# @variant.arg(v=['v = %f м / с' % v for v in [3, 4, 5, 6]])
# @variant.arg(u=['u = %.1f м / с' % u for u in [1.0, 1.5, 2.0]])
@variant.answer_short('{answer}')
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
    def GetUpdate(self, v1=None, v2=None, **kws):
        assert (v1.Value + v2.Value) % (v1.Value - v2.Value) == 0
        return dict(
            answer=int((v1.Value + v2.Value) / (v1.Value - v2.Value)),
        )


@variant.text('''
    Шар движется с некоторой скоростью и абсолютно неупруго соударяется с телом, масса которого в {N} раз больше.
    Определите во сколько раз уменьшилась скорость шара после столкновения.
''')
@variant.answer_short('{answer}')
@variant.answer_test('{answer}')
@variant.arg(N=list(range(5, 15)))
class Vishnyakova_1_4_6(variant.VariantTask):
    def GetUpdate(self, N=None, **kws):
        return dict(
            answer=N + 1,
        )


@variant.text('''
    Для того, чтобы разогать тело из состояния покоя до скорости $v$ с постоянным ускорением,
    требуется соверщить работу {A1:Value:e}. Какую работу нужно совершить, чтобы увеличить скорость этого тела от $v$ до ${n}v$?
''')
@variant.answer_short('{A2:Task}')
@variant.answer_test('{A2:TestAnswer}')
@variant.arg(A1=['A = %d Дж' % A for A in [10, 20, 40, 100, 200]])
@variant.arg(n=[2, 3, 4, 5])
class Vishnyakova_1_4_12(variant.VariantTask):
    def GetUpdate(self, A1=None, n=None, **kws):
        return dict(
            A2='A\' = %d Дж' % (A1.Value * (n ** 2 - 1)),
        )


@variant.text('''
    Определите работу силы, которая обеспечит {what} тела массой {m:Value:e} на высоту {h:Value:e} с постоянным ускорением {a:Value:e}.
    Примите {Consts.g_ten:Task:e}.
''')
@variant.answer_short('{A:Task}')
@variant.answer_test('{A:TestAnswer}')
@variant.arg(what__mult=[('подъём', +1), ('спуск', -1)])
@variant.arg(a=['a = %d м / c^2' % a for a in [2, 3, 4, 6]])
@variant.arg(m=['m = %d кг' % m for m in [2, 3, 5]])
@variant.arg(h=['h = %d м' % h for h in [2, 5, 10]])
class Ch_4_2(variant.VariantTask):
    def GetUpdate(self, what=None, mult=None, m=None, h=None, a=None, Consts=None, **kws):
        return dict(
            A='%d Дж' % (mult * m.Value * h.Value * (Consts.g_ten.Value + mult * a.Value))
        )


@variant.text('''
    Тело массой {m:Value} бросили с обрыва {how} с начальной скоростью {v0:Value:e}.
    Через некоторое время его скорость тела составила {v:Value:e}.
    Пренебрегая сопротивлением воздуха и считая падение тела свободным, определите работу силы тяжести в течение наблюдаемого промежутка времени.
''')
@variant.answer_short('{A:Task}')
@variant.answer_test('{A:TestAnswer}')
@variant.arg(how=['вертикально вверх', 'горизонтально', 'под углом $45\\degrees$ к горизонту', 'под углом $30\\degrees$ к горизонту'])
@variant.arg(m=['m = %d кг' % m for m in [1, 2, 3]])
@variant.arg(v0=['v_0 = %d м / c' % v for v in [2, 4, 6]])
@variant.arg(v=['v = %d м / c' % v for v in [8, 10, 12]])
class Ch_4_29(variant.VariantTask):
    def GetUpdate(self, what=None, m=None, v=None, v0=None, **kws):
        return dict(
            A='%d Дж' % (m.Value * (v.Value ** 2 - v0.Value ** 2) / 2)
        )


@variant.text('''
    Тонкий {what} длиной {l:Value:e} и массой {m:Value:e} лежит на горизонтальной поверхности.
    Какую минимальную работу надо совершить, чтобы поставить его на землю в вертикальное положение?
    Примите {Consts.g_ten:Task:e}.
''')
@variant.answer_short('{A:Task}')
@variant.answer_test('{A:TestAnswer}')
@variant.arg(what=['лом', 'шест', 'кусок арматуры'])
@variant.arg(m=['m = %d кг' % m for m in [10, 20, 30]])
@variant.arg(l=['l = %d м' % l for l in [1, 2, 3]])
class Ch_4_45(variant.VariantTask):
    def GetUpdate(self, what=None, m=None, l=None, Consts=None, **kws):
        return dict(
            A='%d Дж' % (m.Value * l.Value * Consts.g_ten.Value / 2)
        )
