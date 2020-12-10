from generators.variant import text, text_test, answer_short, answer_align, answer_test, arg, VariantTask

import logging
log = logging.getLogger(__name__)


@text('''
    Гидростатическое давление столба {matter} равно {p:Value|e}.
    Определите высоту столба жидкости. Принять {rho:Task|e}, {Consts.g_ten:Task|e}.
''')
@answer_short(
    '{p:L} = {rho:L}g{h:L} \\implies {h:L} = \\frac{ {p:L:s} }{ g{rho:L} } '
    '= \\frac{ {p:Value:s} }{ {Consts.g_ten:Value|cdot}{rho:Value} } = {h:Value}.'
)
@answer_test('{h:TestAnswer}')
@arg(matter__rho__p=[
    (m, '\\rho_{{\\text{{{m}.}}}} = {rho} кг/м^3'.format(m=m[0], rho=rho), 'p = %d кПа' % p) for m, rho, p in [
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
    def GetUpdate(self, matter=None, rho=None, p=None, Consts=None, **kws):
        return dict(
            h='h = %d м' % (1000 * p.Value / Consts.g_ten.Value / rho.Value),
        )


@text('''
    На какой глубине полное давление пресной воды превышает атмосферное в {N} раз?
    Принять {Consts.p_atm:Task|e}, {Consts.g_ten:Task|e}.
''')
@answer_short(
    'p = {Consts.water.rho:L} {Consts.g_ten:L} {h:L} + {Consts.p_atm:L} = {N} {Consts.p_atm:L} \\implies '
    '{h:L} = \\frac{ ({N}-1) {Consts.p_atm:L} }{ {Consts.g_ten:L} {Consts.water.rho:L} } '
    '= \\frac{ ({N}-1) \\cdot {Consts.p_atm:Value} }{ {Consts.g_ten:Value|cdot}{Consts.water.rho:Value} } = {h:Value}.'
)
@answer_test('{h:TestAnswer}')
@arg(N=[2, 3, 4, 5, 6, 7, 8, 9, 10])
class Ch_6_8(VariantTask):
    def GetUpdate(self, N=None, p=None, Consts=None, **kws):
        return dict(
            h='h = %d м' % (1000 * Consts.p_atm.Value * (N-1) / Consts.g_ten.Value / Consts.water.rho.Value),
        )


@text('''
    В сосуд с вертикальными стенками и площадью поперечного (горизонтального) сечения {S:Task|e}
    налили воду. На сколько увеличится {what}, если 
    на поверхность воды ещё будет плавать тело массой {m:Value|e}.
    Принять {Consts.p_atm:Task|e}, {Consts.g_ten:Task|e}.
''')
@answer_short(
    '\\Delta F = {m:L}{Consts.g_ten:L},'
    '\\Delta p = \\frac{ {m:L}{Consts.g_ten:L} }{S:L|s},'
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
    def GetUpdate(self, m=None, S=None, what=None, Consts=None, **kws):
        ans = {
            'сила давления на дно сосуда': '\\Delta F = %d Н' % (m.Value * Consts.g_ten.Value / 1000),
            'давление на дно сосуда': '\\Delta p = %d Па' % (m.Value * Consts.g_ten.Value / S.Value / 1000),
        }[what]
        return dict(
            ans=ans,
        )

