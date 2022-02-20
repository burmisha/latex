import itertools

import generators.variant as variant
from generators.helpers import Consts

import math


@variant.lv_variant_task(
    {
        'индукция магнитного поля': '$B$',
        'магнитный поток': '$\\Phi$',
        'вектор нормали к поверхности': '$\\vec n$',
        'площадь контура': '$S$',
        'сопротивление контура': '$R$',
        'ЭДС индукции': '$\\ele$',
        'индукционый ток': '$\\eli$',
    },
    ['$D$', '$v$', '$U$', '$l$'],
    answers_count=2,
    mocks_count=2,
)
class Definitions01(variant.VariantTask):
    pass


@variant.lv_variant_task(
    {
        'индукция магнитного поля': 'Тл',
        'магнитный поток': 'Вб',
        'площадь контура': '$\\text{м}^2$',
        'ЭДС индукции': 'В',
        'индукционый ток': 'А',
    },
    ['Кл', 'Ом', 'Гц', 'Гн'],
    answers_count=3,
    mocks_count=2,
)
class Definitions02(variant.VariantTask):
    pass


@variant.lv_variant_task(
    {
        '$\\ele$': '$-\\frac{\\Delta \\Phi}{\\Delta t}$',
        '$\\Delta t$': '$t_2 - t_1$',
        '$\\Delta \\Phi$': '$\\Phi_2 - \\Phi_1$',
    },
    ['$t_1 - t_2$', '$\\Phi_1 - \\Phi_2$'],
    answers_count=3,
    mocks_count=2,
)
class Definitions03(variant.VariantTask):
    pass


@variant.text('''
    Однородное магнитное поле пронизывает плоский контур площадью {S:V:e}.
    Индукция магнитного поля равна {B:V:e}.
    Чему равен магнитный поток через контур, если его плоскость
    расположена под углом ${angle}\\degrees$ к вектору магнитной индукции?
    Ответ выразите в милливеберах и округлите до целого, единицы измерения писать не нужно.
''')
@variant.solution_space(100)
@variant.arg(S=('S = {} см^2', [200, 400, 600, 800]))
@variant.arg(B=('B = {} мТл', [300, 500, 700]))
@variant.arg(angle=[0, 30, 60, 90])
@variant.answer_short('\\alpha = {alpha}\\degrees, {Phi:Letter} = BS\\cos\\alpha = {Phi:V} \\to {PhiAnswer}')
@variant.answer_test('{PhiAnswer}')
class Find_F_easy(variant.VariantTask):
    def GetUpdate(self, S=None, B=None, angle=None):
        alpha = 90 - angle

        mul = 1000
        if alpha == 90:
            Phi = 0
            PhiAnswer = 0
        else:
            Phi = B * S * math.cos(alpha * math.pi / 180)
            PhiAnswer = int(Phi * mul + 0.5)
        assert PhiAnswer == 0 or PhiAnswer >= 2
        return dict(
            alpha=alpha,
            Phi=f'\\Phi_B = {Phi.SI_Value * mul:.2f} мВб',
            PhiAnswer=PhiAnswer,
        )


@variant.text('''
    Определите магнитный поток через контур,
    находящийся в однородном магнитном поле индукцией {B:V:e}.
    Контур имеет форму {figure} {a:V:e} и {b:V:e}.
    Угол между {between} и вектором индукции магнитного поля
    составляет ${angle}\\degrees$.
    Ответ выразите в милливеберах и округлите до целого, единицы измерения писать не нужно.
''')
@variant.solution_space(100)
@variant.arg(figure=['прямоугольного треугольника с катетами', 'прямоугольника со сторонами'])
@variant.arg(a=('a = {} см', [40, 50, 60]))
@variant.arg(b=('b = {} см', [45, 75, 80]))
@variant.arg(B=('B = {} мТл', [300, 500, 700]))
@variant.arg(between=['плоскостью контура', 'нормалью к плоскости контура'])
@variant.arg(angle=[10, 20, 40, 50, 70, 80])
@variant.answer_short('\\alpha={alpha}\\degrees, {Phi:L} = BS\\cos\\alpha = {Phi:V} \\to {PhiAnswer}')
@variant.answer_test('{PhiAnswer}')
class Find_F_hard(variant.VariantTask):
    def GetUpdate(self, figure=None, a=None, b=None, B=None, between=None, angle=None):
        S = a * b
        if 'треугольник' in figure:
            S /= 2

        if 'нормалью' in between:
            alpha = angle
        else:
            alpha = 90 - angle

        mul = 1000
        if alpha == 90:
            Phi = 0
            PhiAnswer = 0
        else:
            Phi = B * S * math.cos(alpha * math.pi / 180)
            PhiAnswer = int(Phi.SI_Value * mul + 0.5)

        assert PhiAnswer == 0 or PhiAnswer >= 10, [Phi, a, b, S, alpha, alpha * math.pi / 180]
        return dict(
            Phi=f'\\Phi_B = {Phi.SI_Value * mul:.2f} мВб',
            PhiAnswer=PhiAnswer,
            alpha=alpha,
        )


@variant.text('''
    Определите притягивается (А), не взаимодействует (Б) или отталкивается (В) металлическое кольцо к магниту,
    если {what} {pole} полюсом (см. рис).
''')
@variant.arg(pole=['южным', 'северным'])
@variant.arg(what__ans=[('вдвигать', 'В'), ('выдвигать', 'А')])
@variant.answer_test('{ans}')
@variant.answer('\\text{{ans}}')
@variant.solution_space(0)
class Action1(variant.VariantTask):
    pass


@variant.text('''
    Определите притягивается (А), не взаимодействует (Б) или отталкивается (В) кольцо из диэлектрика к магниту,
    если {what} {pole} полюсом (см. рис).
''')
@variant.arg(pole=['южным', 'северным'])
@variant.arg(what=['вдвигать магнит в кольцо', 'выдвигать магнит из кольца'])
@variant.answer_test('Б')
@variant.answer('\\text{Б}')
@variant.solution_space(0)
class Action2(variant.VariantTask):
    pass


@variant.text('''
    Магнитный поток, пронизывающий замкнутый контур, равномерно изменяется от {Phi1:V:e} до {Phi2:V:e} за {t:V:e}.
    Чему равна ЭДС в контуре? Ответ выразите в милливольтах и округлите до целого, единицы измерения писать не нужно.
''')
@variant.arg(Phi1=('\\Phi_1 = {} мВб', [35, 65, 95]))
@variant.arg(Phi2=('\\Phi_2 = {} мВб', [20, 50, 80, 110]))
@variant.arg(t=('t = {} c', [1.1, 1.3, 1.5]))
@variant.answer_test('{E_answer}')
@variant.answer_short('''
    {E:Letter}
    = \\frac{\\abs{\\Delta \\Phi}}{\\Delta t}
    = \\frac{\\abs{{Phi2:L} - {Phi1:L}}}{\\Delta t}
    = \\frac{\\abs{{Phi2:V} - {Phi1:V}}}{\\Delta t}
    = {E:V} \\to {E_answer}
''')
@variant.solution_space(60)
class Find_E_easy(variant.VariantTask):
    def GetUpdate(self, Phi1=None, Phi2=None, t=None):
        E = abs(Phi1.Value - Phi2.Value) / t.Value
        E_answer = int(E + 0.5)

        assert E_answer >= 10, [E_answer]
        return dict(
            E=f'\\ele = {E:.3f} мВ',
            E_answer=E_answer,
        )


@variant.text('''
    Какой средний индукционный ток возник в плоском контуре площадью {S:V:e}
    и сопротивлением {R:V:e}, если сперва он располагался {how} линиям индукции магнитного поля,
    а затем его за {t:V:e} повернули, и теперь угол между {between} и индукцией магнитного поля
    равен ${angle}\\degrees$. Магнитное поле однородно, его индукция равна {B:V:e}.
    Ответ выразите в микроамперах и округлите до целого, единицы измерения писать не нужно.
''')
@variant.solution_space(100)
@variant.arg(how=['параллельно', 'перпендикулярно'])
@variant.arg(S=('S = {} см^2', [120, 150, 250]))
@variant.arg(t=('t = {} мc', [0.2, 0.5, 0.6, 0.8]))
@variant.arg(B=('B = {} мТл', [50, 70, 80]))
@variant.arg(R=('R = {} Ом', [1.5, 2, 2.5, 3]))
@variant.arg(between=['плоскостью контура', 'нормалью к плоскости контура'])
@variant.arg(angle=[10, 20, 40, 50, 70, 80])
@variant.answer_align([
    '\\alpha_1 &= {alpha_1}\\degrees, \\alpha_2 = {alpha_2}\\degrees,',
    '\\ele &= \\abs{\\frac{\\Delta \\Phi}{\\Delta t}},',
    '{I:Letter} &= \\frac \\ele R = \\frac{\\Delta \\Phi}{R\\Delta t}'
    '= \\frac{ \\abs{ B S \\cos\\alpha_2 - B S \\cos\\alpha_1 } }{R\\Delta t}'
    '= \\frac{ B S \\abs{ \\cos\\alpha_2 -  \\cos\\alpha_1 } }{R\\Delta t} = ',
    '&= \\frac{ {B:V} * {S:V} \\abs{ \\cos{alpha_2}\\degrees -  \\cos{alpha_1}\\degrees } }{{R:V} * {t:V}}'
    '\\approx {I:V} \\to {I_answer}',
])
@variant.answer_test('{I_answer}')
class Find_I_hard(variant.VariantTask):
    def GetUpdate(self, how=None, S=None, t=None, B=None, R=None, between=None, angle=None):
        if 'перп' in how:
            alpha_1 = 0
        else:
            alpha_1 = 90

        if 'нормалью' in between:
            alpha_2 = angle
        else:
            alpha_2 = 90 - angle

        assert alpha_1 != alpha_2

        Phi_1 = B * S * math.cos(alpha_1 * math.pi / 180)
        Phi_2 = B * S * math.cos(alpha_2 * math.pi / 180)

        mul = 10 ** 6
        I = abs(Phi_2 - Phi_1) / t / R
        I_answer = int(I.SI_Value * mul + 0.5)

        assert I_answer >= 10, [I_answer]
        return dict(
            I=f'\\eli = {I.SI_Value * mul:.3f} мкА',
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            I_answer=I_answer,
        )
