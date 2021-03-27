from generators.variant import text, text_test, answer_short, answer_align, answer_test, arg, VariantTask
from generators.helpers import Consts


@text('''
    Гидростатическое давление столба {matter} равно {p:Value|e}.
    Определите высоту столба жидкости. Принять {rho:Task|e}, {Consts.g_ten:Task|e}.
''')
@answer_short(
    '{p:L} = {rho:L}g{h:L} \\implies {h:L} = \\frac{ {p:L:s} }{ g{rho:L} } '
    '= \\frac{ {p:Value:s} }{ {Consts.g_ten:Value} * {rho:Value} } = {h:Value}.'
)
@answer_test('{h:TestAnswer}')
@arg(matter__rho__p=[
    (m, '\\rho_{{\\text{{{m}}}}} = {rho} кг/м^3'.format(m=m[0], rho=rho), 'p = %d кПа' % p) for m, rho, p in [
        ('воды', 1000, 50),
        ('воды', 1000, 100),
        ('воды', 1000, 150),
        ('воды', 1000, 200),
        ('воды', 1000, 250),
        ('масла', 900, 9),
        ('масла', 900, 18),
        ('масла', 900, 27),
        ('нефти', 800, 20),
        ('нефти', 800, 40),
        ('нефти', 800, 400),
        ('нефти', 800, 600),
        ('нефти', 800, 800),
    ]
])
class Ch_6_3(VariantTask):
    def GetUpdate(self, matter=None, rho=None, p=None, **kws):
        value = 1000 * p.Value / Consts.g_ten.Value / rho.Value
        if int(value) == value:
            h = 'h = %d м' % value
        else:
            h = 'h = %.1f м' % value
        return dict(
            h=h,
        )


@text('''
    На какой глубине полное давление пресной воды превышает атмосферное в {N} раз?
    Принять {Consts.p_atm:Task|e}, {Consts.g_ten:Task|e}, {Consts.water.rho:Task|e}.
''')
@answer_short(
    'p = {Consts.water.rho:L} {Consts.g_ten:L} {h:L} + {Consts.p_atm:L} = {N} {Consts.p_atm:L} \\implies '
    '{h:L} = \\frac{ ({N}-1) {Consts.p_atm:L} }{ {Consts.g_ten:L} {Consts.water.rho:L} } '
    '= \\frac{ ({N}-1) * {Consts.p_atm:Value} }{ {Consts.g_ten:Value} * {Consts.water.rho:Value} } = {h:Value}.'
)
@answer_test('{h:TestAnswer}')
@arg(N=[2, 3, 4, 5, 6, 7, 8, 9, 10])
class Ch_6_8(VariantTask):
    def GetUpdate(self, N=None, p=None, **kws):
        return dict(
            h='h = %d м' % (1000 * Consts.p_atm.Value * (N-1) / Consts.g_ten.Value / Consts.water.rho.Value),
        )


@text('''
    В сосуд с вертикальными стенками и площадью горизонтального поперечного сечения {S:Task|e}
    налили воду. На сколько увеличится {what}, если
    на поверхности воды ещё будет плавать тело массой {m:Value|e}.
    Принять {Consts.p_atm:Task|e}, {Consts.g_ten:Task|e}.
''')
@answer_short(
    '\\Delta F = {m:L}{Consts.g_ten:L}, '
    '\\Delta p = \\frac{ \\Delta F }{S:L|s} = \\frac{ {m:L}{Consts.g_ten:L} }{S:L|s}, '
    '{ans:Task}.'
)
@answer_test('{ans:TestAnswer}')
@arg(S=['S = 0.0%d м^2' % S for S in [1, 2, 3, 5]])
@arg(m=['m = %d г' % m for m in [150, 300, 600, 900]])
@arg(what=[
    'давление на дно сосуда',
    'сила давления на дно сосуда',
    # 'уровень жидкости',  # not for test
])
class Ch_6_10(VariantTask):
    def GetUpdate(self, m=None, S=None, what=None, **kws):
        ans = {
            'сила давления на дно сосуда': '\\Delta F = %d Н' % (m.Value * Consts.g_ten.Value / 1000),
            'давление на дно сосуда': '\\Delta p = %d Па' % (m.Value * Consts.g_ten.Value / S.Value / 1000),
        }[what]
        return dict(
            ans=ans,
        )


@text('''
    В два сообщающихся сосуда налита вода. В один из соcудов наливают {matter} так,
    что столб этой жидкости имеет высоту {h1:Value:e}.
    На сколько теперь уровень воды в этом сосуде ниже, чем в другом?
    Ответ выразите в сантиметрах. {Consts.water.rho:Task|e}, {rho:Task:e}.
''')
@answer_short(
    '{rho:L}{Consts.g_ten:L}{h1:L} = {Consts.water.rho:L}{Consts.g_ten:L}{h2:L} \\implies '
    '{h2:L} = {h1:L} \\frac{ {rho:L} }{ {Consts.water.rho:L} } '
    '= {h1:Value} * \\frac{ {rho:Value} }{ {Consts.water.rho:Value} } '
    '= {h2:Value}'
)
@answer_test({'{h2:TestAnswer}': 1, '{h2_m:TestAnswer}': 0.7})
@arg(matter__rho__h1=[
    (m, '\\rho_{{\\text{{{m}}}}} = {rho} кг/м^3'.format(m=m[0], rho=rho), 'h_1 = %d см' % h) for m, rho, h in [
        ('масло', 900, 90),
        ('масло', 900, 80),
        ('масло', 900, 70),
        ('масло', 900, 60),
        ('масло', 900, 50),
        ('масло', 900, 40),
        ('масло', 900, 30),
        ('масло', 900, 20),
        ('нефть', 800, 5),
        ('нефть', 800, 10),
        ('нефть', 800, 15),
        ('нефть', 800, 20),
        ('нефть', 800, 25),
        ('нефть', 800, 30),
        ('нефть', 800, 40),
    ]
])
class Ch_6_16(VariantTask):
    def GetUpdate(self, h1=None, rho=None, **kws):
        return dict(
            h2='h_2 = %d см' % (h1.Value * rho.Value / Consts.water.rho.Value),
            h2_m = 'h_2 = %.2f м' % (h1.Value * rho.Value / Consts.water.rho.Value / 100),
        )


@text('''
    В два сообщающихся сосуда сечений {S1:Value:e} и {S2:Value:e} налита вода.
    Оба сосуда закрыты лёгкими поршнями и находятся в равновесии.
    На больший из поршней кладут груз массой {m:Value:e}.
    Определите, на сколько поднимется меньший поршень.
    Ответ выразите в сантиметрах. {Consts.water.rho:Task|e}.
''')
@answer_align([
    '{S1:L}h_1 &= {S2:L}h_2 \\implies h_1 = h_2 \\frac{ {S2:L} }{ {S1:L} } ',
    '\\frac{ {m:L}{Consts.g_ten:L} }{ {S1:L} } &= {Consts.water.rho:L}{Consts.g_ten:L}(h_1 + h_2) '
    '= {Consts.water.rho:L}{Consts.g_ten:L} * h_2 \\cbr{ 1 + \\frac{ {S2:L} }{ {S1:L} } }',
    'h_2 &= \\frac{ {m:L}{Consts.g_ten:L} }{ {S1:L}{Consts.water.rho:L}{Consts.g_ten:L} } * '
    '\\frac{ {S1:L} }{ {S1:L} + {S2:L} } = \\frac{ {m:L} }{ {Consts.water.rho:L}({S1:L} + {S2:L}) }'
    ' = {h2:Value}',
])
@answer_test('{h2:TestAnswer}')
@arg(m=['m = %d г' % m for m in [200, 300, 400, 500]])
@arg(S1__S2=[
    ('S_1 = %d см^2' % S1, 'S_2 = %d см^2' % S2) for S1, S2 in [
        (45, 5),
        (40, 10),
        (32, 18),
        (30, 20),
        (90, 10),
        (80, 20),
        (64, 36),
        (60, 40),
    ]
])
class Ch_6_20(VariantTask):
    def GetUpdate(self, S1=None, S2=None, m=None, **kws):
        return dict(
            h2='h_2 = %d см' % (100 * 10 * m.Value / Consts.water.rho.Value / (S1.Value + S2.Value)),
        )

