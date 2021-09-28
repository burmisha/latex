import itertools

import generators.variant as variant
from generators.helpers import Consts, letter_variants

import math


@variant.solution_space(0)
@variant.text('''
    Установите каждой букве в соответствие ровно одну цифру и запишите ответ (только цифры, без других символов).

    {lv.Questions}.

    {lv.Options}.
''')
@variant.answer_test('{lv.Answer}')
@variant.arg(lv=letter_variants(
    {
        '$\\Phi$': '$L\\eli$',
        '$\\Delta \\eli$': '$\\eli_2 - \\eli_1$',
        '$\\Delta \\Phi$': '$\\Phi_2 - \\Phi_1$',
    },
    ['$\\frac{L}{\\eli}$', '$\\frac{\\eli}{L}$', '$\\eli_1 - \\eli_2$', '$\\Phi_1 - \\Phi_2$'],
    answers_count=3,
    mocks_count=3,
))
@variant.answer_short('{lv.Answer}')
class Definitions01(variant.VariantTask):
    pass


@variant.solution_space(0)
@variant.text('''
    Установите каждой букве в соответствие ровно одну цифру и запишите ответ (только цифры, без других символов).

    {lv.Questions}.

    {lv.Options}.
''')
@variant.answer_test('{lv.Answer}')
@variant.arg(lv=letter_variants(
    {
        'индукция магнитного поля': '$\\vec B$',
        'поток магнитной индукции': '$\\Phi$',
        'индуктивность': '$L$',
        'электрический ток': '$\\eli$',
        'электрический заряд': '$q$',
    },
    ['$R$', '$g$', '$\\phi$'],
    answers_count=3,
    mocks_count=2,
))
@variant.answer_short('{lv.Answer}')
class Definitions02(variant.VariantTask):
    pass


@variant.solution_space(0)
@variant.text('''
    Установите каждой букве в соответствие ровно одну цифру и запишите ответ (только цифры, без других символов).

    {lv.Questions}.

    {lv.Options}.
''')
@variant.answer_test('{lv.Answer}')
@variant.arg(lv=letter_variants(
    {
        'индукция магнитного поля': 'Тл',
        'поток магнитной индукции': 'Вб',
        'индуктивность': 'Гн',
        'время': 'с',
    },
    ['м', 'Кл', 'А'],
    answers_count=3,
    mocks_count=2,
))
@variant.answer_short('{lv.Answer}')
class Definitions03(variant.VariantTask):
    pass


@variant.text('''
	В катушке, индуктивность которой равна {L:V:e}, сила тока равномерно уменьшается
	с {I1:V:e} до {I2:V:e} за {t:V:e}. Определите ЭДС самоиндукции, ответ выразите в мВ и округлите до целых.
''')
@variant.arg(I1=('\\eli_1 = {} А', [7, 8, 9]))
@variant.arg(I2=('\\eli_2 = {} А', [1, 2, 3, 4]))
@variant.arg(L=('L = {} мГн', [4, 5, 6, 7]))
@variant.arg(t=('\\Delta t = {} c', [0.2, 0.3, 0.4, 0.5]))
@variant.answer_test('{E_answer}')
@variant.answer_short('''
    {E:Letter}
    = {L:L}\\frac{\\abs{\\Delta \\eli}}{{t:L}}
    = {L:L}\\frac{\\abs{{I2:L} - {I1:L}}}{{t:L}}
    = {L:V} * \\frac{\\abs{{I2:V} - {I1:V}}}{{t:V}}
    \\approx {E:V} \\to {E_answer}
''')
@variant.solution_space(60)
class Find_E_easy(variant.VariantTask):
    def GetUpdate(self, I1=None, I2=None, t=None, L=None):
        E = abs(I1.Value - I2.Value) / t.Value * L.Value
        E_answer = int(E + 0.5)

        assert E_answer >= 10, [E_answer]
        return dict(
            E=f'\\ele = {E:.3f} мВ',
            E_answer=E_answer,
        )


@variant.text('''
	В катушке, индуктивность которой равна {L:V:e}, течёт электрический ток силой {I:V:e}.
	Число витков в катушке: {n}. Определите магнитный поток, пронизывающий 1 виток катушки.
	Ответ выразите в милливеберах и округлите до целых.
''')
@variant.arg(I=('\\eli = {} А', [5, 6, 7]))
@variant.arg(L=('L = {} мГн', [50, 60, 70, 80, 90]))
@variant.arg(n=[20, 30, 40])
@variant.answer_test('{Phi1_answer}')
@variant.answer_short('''
    {Phi1:L}
    = \\frac{\\Phi}{N}
    = \\frac{{L:L}{I:L}}{N} 
    = \\frac{{L:V} * {I:V}}{{n}}
    \\approx {Phi1:V} 
    \\to {Phi1_answer}
''')
@variant.solution_space(60)
class Find_Phi_1(variant.VariantTask):
    def GetUpdate(self, I=None, L=None, n=None):
        Phi1 = L.Value * I.Value / n
        Phi1_answer = int(Phi1 + 0.5)

        assert Phi1_answer >= 5, [Phi1, Phi1_answer]
        return dict(
            Phi1=f'\\Phi_\\text{{1 виток}} = {Phi1:.3f} мВб',
            Phi1_answer=Phi1_answer,
        )
