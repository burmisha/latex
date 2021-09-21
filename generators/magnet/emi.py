import itertools

import generators.variant as variant
from generators.helpers import Consts, letter_variants

import math


@variant.solution_space(20)
@variant.text('''
    Установите каждой букве в соответствие ровно одну цифру и запишите ответ (только цифры, без других символов).

    {lv.Questions}.

    {lv.Options}.
''')
@variant.answer_test('{lv.Answer}')
@variant.arg(lv=letter_variants(
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
))
@variant.answer_short('{lv.Answer}')
class Definitions01(variant.VariantTask):
    pass


@variant.solution_space(20)
@variant.text('''
    Установите каждой букве в соответствие ровно одну цифру и запишите ответ (только цифры, без других символов).

    {lv.Questions}.

    {lv.Options}.
''')
@variant.answer_test('{lv.Answer}')
@variant.arg(lv=letter_variants(
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
))
@variant.answer_short('{lv.Answer}')
class Definitions02(variant.VariantTask):
    pass



@variant.text('''
    Определите магнитный поток через контур,
    находящийся в однородном магнитном поле индукцией {B:V:e}.
    Контур имеет форму {figure} {a:V:e} и {b:V:e}.
    Угол между {between} и вектором индукции магнитного поля 
    составляет ${angle}\\degrees$ градусов.
    Ответ выразите в милливеберах и округлите до целого.
''')
@variant.solution_space(100)
@variant.arg(figure=['прямоугольного треугольника с катетами', 'прямоугольника со сторонами'])
@variant.arg(a=('a = {} см', [40, 50, 60]))
@variant.arg(b=('b = {} см', [45, 75, 80]))
@variant.arg(B=('B = {} мТл', [300, 500, 700]))
@variant.arg(between=['плоскостью контура', 'нормалью к плоскости контура'])
@variant.arg(angle=[10, 20, 40, 50, 70, 80])
@variant.answer_short('{Phi:Task} \\to {PhiAnswer}')
@variant.answer_test('{PhiAnswer}')
class Find_F_hard(variant.VariantTask):
    def GetUpdate(self, figure=None, a=None, b=None, B=None, between=None, angle=None, **kws):
        S = a.Value * b.Value * 10 ** (a.Power + b.Power)
        if 'треугольник' in figure:
            S /= 2

        if 'нормалью' in between:
            alpha = angle
        else:
            alpha = 90 - angle

        if alpha == 90:
            Phi = 0
            PhiAnswer = 0
        else:
            Phi = B.Value * S * math.cos(alpha * math.pi / 180)
            PhiAnswer = int(Phi + 0.5)

        assert PhiAnswer == 0 or PhiAnswer >= 10, [Phi, a, b, S, alpha, alpha * math.pi / 180]
        return dict(
            Phi=f'\\Phi_B = {Phi:.2f} мВб',
            PhiAnswer=PhiAnswer,
        )


@variant.text('''
    Определите притягивается (А), не взаимодействует (Б) или отталкивается (В) металлическое кольцо к магниту,
    если {what} {pole} полюсом (см. рис).
''')
@variant.arg(pole=['южным', 'северным'])
@variant.arg(what__ans=[('вдвигать', 'Б'), ('выдвигать', 'В')])
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
    Какой средний индукционный ток возник в плоском контуре площадью {S:V:e}
    и сопротивлением {R:V:e}, если сперва он располагался {how} линиям индукции магнитного поля,
    а затем его за {t:V:e} повернули, и теперь угол между {between} и индукцией магнитного поля 
    равен ${angle}\\degrees$. Магнитное поле однородно, его индукция равна {B:V:e}. 
    Ответ выразите в микроамперах и округлите до целых (в ответ запишите только число).
''')
@variant.solution_space(100)
@variant.arg(how=['параллельной', 'перпендикулярно'])
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
    '&= \\frac{ {B:V} * {S:V} \\abs{ \\cos{alpha_2}\\degrees -  \\cos{alpha_1}\\degrees } }{{R:Value} * {t:Value}}'
    '\\approx {I:Value} \\to {I_answer}',
])
@variant.answer_test('{I_answer}')
class Find_I_hard(variant.VariantTask):
    def GetUpdate(self, how=None, S=None, t=None, B=None, R=None, between=None, angle=None, **kws):
        if 'перп' in how:
            alpha_1 = 0
        else:
            alpha_1 = 90

        if 'нормалью' in between:
            alpha_2 = angle
        else:
            alpha_2 = 90 - angle

        assert alpha_1 != alpha_2

        Phi_1 = B.Value * S.Value * math.cos(alpha_1 * math.pi / 180) * 10 ** (S.Power + B.Power)
        Phi_2 = B.Value * S.Value * math.cos(alpha_2 * math.pi / 180) * 10 ** (S.Power + B.Power)

        I = abs(Phi_2 - Phi_1) / t.Value / R.Value * 10 ** (-t.Power - R.Power) * 10 ** 6
        I_answer = int(I + 0.5)

        assert I_answer >= 10, [I_answer]
        return dict(
            I=f'\\eli = {I:.3f} мкА',
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            I_answer=I_answer,
        )
