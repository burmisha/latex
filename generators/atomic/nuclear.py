import generators.variant as variant
from generators.helpers import UnitValue, Consts, AllElements
from generators.helpers.element import FallType
from library.util.asserts import assert_equals

def get_element_answer(what, element):
    return {
        'протонов': f'{element:protons}',
        'нейтронов': f'{element:neutrons}',
        'электронов': f'{element:electrons}',
        'нуклонов': f'{element:nuclons}',
    }[what]


all_particles = ['протонов', 'нейтронов', 'электронов', 'нуклонов']


def get_first_index(index):
    return index * (index + 1) // 2 + 2 * index


def test_get_first_index():
    assert_equals('Broken index', 0, get_first_index(0))
    assert_equals('Broken index', 3, get_first_index(1))
    assert_equals('Broken index', 7, get_first_index(2))
    assert_equals('Broken index', 12, get_first_index(3))


test_get_first_index()


def get_elements_sublist(index, shift=0):
    first = get_first_index(index) + shift
    last = get_first_index(index + 1) + shift
    return AllElements.stable_elements[first:last]


@variant.solution_space(0)
@variant.text('Определите число {what01} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what01=all_particles)
@variant.arg(element=get_elements_sublist(0))
class AtomCount01(variant.VariantTask):
    def GetUpdate(self, element=None, what01=None):
        return dict(answer=get_element_answer(what01, element))


@variant.solution_space(0)
@variant.text('Определите число {what02} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what02=all_particles)
@variant.arg(element=get_elements_sublist(1))
class AtomCount02(variant.VariantTask):
    def GetUpdate(self, element=None, what02=None):
        return dict(answer=get_element_answer(what02, element))


@variant.solution_space(0)
@variant.text('Определите число {what03} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what03=all_particles)
@variant.arg(element=get_elements_sublist(2))
class AtomCount03(variant.VariantTask):
    def GetUpdate(self, element=None, what03=None):
        return dict(answer=get_element_answer(what03, element))


@variant.solution_space(0)
@variant.text('Определите число {what04} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what04=all_particles)
@variant.arg(element=get_elements_sublist(3))
class AtomCount04(variant.VariantTask):
    def GetUpdate(self, element=None, what04=None):
        return dict(answer=get_element_answer(what04, element))


@variant.solution_space(0)
@variant.text('Определите число {what05} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what05=all_particles)
@variant.arg(element=get_elements_sublist(4))
class AtomCount05(variant.VariantTask):
    def GetUpdate(self, element=None, what05=None):
        return dict(answer=get_element_answer(what05, element))


@variant.solution_space(0)
@variant.text('Определите число {what06} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what06=all_particles)
@variant.arg(element=get_elements_sublist(5))
class AtomCount06(variant.VariantTask):
    def GetUpdate(self, element=None, what06=None):
        return dict(answer=get_element_answer(what06, element))


@variant.solution_space(0)
@variant.text('Определите число {what07} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what07=all_particles)
@variant.arg(element=get_elements_sublist(6))
class AtomCount07(variant.VariantTask):
    def GetUpdate(self, element=None, what07=None):
        return dict(answer=get_element_answer(what07, element))


@variant.solution_space(0)
@variant.text('Определите число {what08} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what08=all_particles)
@variant.arg(element=get_elements_sublist(7))
class AtomCount08(variant.VariantTask):
    def GetUpdate(self, element=None, what08=None):
        return dict(answer=get_element_answer(what08, element))


@variant.solution_space(0)
@variant.text('Определите число {what09} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what09=all_particles)
@variant.arg(element=get_elements_sublist(8))
class AtomCount09(variant.VariantTask):
    def GetUpdate(self, element=None, what09=None):
        return dict(answer=get_element_answer(what09, element))


@variant.solution_space(0)
@variant.text('Определите число {what10} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what10=all_particles)
@variant.arg(element=get_elements_sublist(9))
class AtomCount10(variant.VariantTask):
    def GetUpdate(self, element=None, what10=None):
        return dict(answer=get_element_answer(what10, element))


@variant.solution_space(0)
@variant.text('Определите число {what11} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what11=all_particles)
@variant.arg(element=get_elements_sublist(10))
class AtomCount11(variant.VariantTask):
    def GetUpdate(self, element=None, what11=None):
        return dict(answer=get_element_answer(what11, element))


@variant.solution_space(0)
@variant.text('Определите число {what12} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what12=all_particles)
@variant.arg(element=get_elements_sublist(11))
class AtomCount12(variant.VariantTask):
    def GetUpdate(self, element=None, what12=None):
        return dict(answer=get_element_answer(what12, element))


@variant.solution_space(0)
@variant.text('Определите число {what01} в атоме ${element01:RuText}$.')
@variant.answer('$Z = {element01:protons}$ протонов и столько же электронов, $A = {element01:nuclons}$ нуклонов, $A - Z = {element01:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what01=all_particles)
@variant.arg(element01=get_elements_sublist(0, shift=1))
class AtomCount01_Text(variant.VariantTask):
    def GetUpdate(self, element01=None, what01=None):
        return dict(answer=get_element_answer(what01, element01))


@variant.solution_space(0)
@variant.text('Определите число {what02} в атоме ${element02:RuText}$.')
@variant.answer('$Z = {element02:protons}$ протонов и столько же электронов, $A = {element02:nuclons}$ нуклонов, $A - Z = {element02:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what02=all_particles)
@variant.arg(element02=get_elements_sublist(1, shift=1))
class AtomCount02_Text(variant.VariantTask):
    def GetUpdate(self, element02=None, what02=None):
        return dict(answer=get_element_answer(what02, element02))


@variant.solution_space(0)
@variant.text('Определите число {what03} в атоме ${element03:RuText}$.')
@variant.answer('$Z = {element03:protons}$ протонов и столько же электронов, $A = {element03:nuclons}$ нуклонов, $A - Z = {element03:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what03=all_particles)
@variant.arg(element03=get_elements_sublist(2, shift=1))
class AtomCount03_Text(variant.VariantTask):
    def GetUpdate(self, element03=None, what03=None):
        return dict(answer=get_element_answer(what03, element03))


@variant.solution_space(0)
@variant.text('Определите число {what04} в атоме ${element04:RuText}$.')
@variant.answer('$Z = {element04:protons}$ протонов и столько же электронов, $A = {element04:nuclons}$ нуклонов, $A - Z = {element04:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what04=all_particles)
@variant.arg(element04=get_elements_sublist(3, shift=1))
class AtomCount04_Text(variant.VariantTask):
    def GetUpdate(self, element04=None, what04=None):
        return dict(answer=get_element_answer(what04, element04))


@variant.solution_space(0)
@variant.text('Определите число {what05} в атоме ${element05:RuText}$.')
@variant.answer('$Z = {element05:protons}$ протонов и столько же электронов, $A = {element05:nuclons}$ нуклонов, $A - Z = {element05:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what05=all_particles)
@variant.arg(element05=get_elements_sublist(4, shift=1))
class AtomCount05_Text(variant.VariantTask):
    def GetUpdate(self, element05=None, what05=None):
        return dict(answer=get_element_answer(what05, element05))


@variant.solution_space(0)
@variant.text('Определите число {what06} в атоме ${element06:RuText}$.')
@variant.answer('$Z = {element06:protons}$ протонов и столько же электронов, $A = {element06:nuclons}$ нуклонов, $A - Z = {element06:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what06=all_particles)
@variant.arg(element06=get_elements_sublist(5, shift=1))
class AtomCount06_Text(variant.VariantTask):
    def GetUpdate(self, element06=None, what06=None):
        return dict(answer=get_element_answer(what06, element06))


@variant.solution_space(0)
@variant.text('Определите число {what07} в атоме ${element07:RuText}$.')
@variant.answer('$Z = {element07:protons}$ протонов и столько же электронов, $A = {element07:nuclons}$ нуклонов, $A - Z = {element07:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what07=all_particles)
@variant.arg(element07=get_elements_sublist(6, shift=1))
class AtomCount07_Text(variant.VariantTask):
    def GetUpdate(self, element07=None, what07=None):
        return dict(answer=get_element_answer(what07, element07))


@variant.solution_space(0)
@variant.text('Определите число {what08} в атоме ${element08:RuText}$.')
@variant.answer('$Z = {element08:protons}$ протонов и столько же электронов, $A = {element08:nuclons}$ нуклонов, $A - Z = {element08:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what08=all_particles)
@variant.arg(element08=get_elements_sublist(7, shift=1))
class AtomCount08_Text(variant.VariantTask):
    def GetUpdate(self, element08=None, what08=None):
        return dict(answer=get_element_answer(what08, element08))


@variant.solution_space(0)
@variant.text('Определите число {what09} в атоме ${element09:RuText}$.')
@variant.answer('$Z = {element09:protons}$ протонов и столько же электронов, $A = {element09:nuclons}$ нуклонов, $A - Z = {element09:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what09=all_particles)
@variant.arg(element09=get_elements_sublist(8, shift=1))
class AtomCount09_Text(variant.VariantTask):
    def GetUpdate(self, element09=None, what09=None):
        return dict(answer=get_element_answer(what09, element09))


@variant.solution_space(0)
@variant.text('Определите число {what10} в атоме ${element10:RuText}$.')
@variant.answer('$Z = {element10:protons}$ протонов и столько же электронов, $A = {element10:nuclons}$ нуклонов, $A - Z = {element10:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what10=all_particles)
@variant.arg(element10=get_elements_sublist(9, shift=1))
class AtomCount10_Text(variant.VariantTask):
    def GetUpdate(self, element10=None, what10=None):
        return dict(answer=get_element_answer(what10, element10))


@variant.solution_space(0)
@variant.text('Определите число {what11} в атоме ${element11:RuText}$.')
@variant.answer('$Z = {element11:protons}$ протонов и столько же электронов, $A = {element11:nuclons}$ нуклонов, $A - Z = {element11:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what11=all_particles)
@variant.arg(element11=get_elements_sublist(10, shift=1))
class AtomCount11_Text(variant.VariantTask):
    def GetUpdate(self, element11=None, what11=None):
        return dict(answer=get_element_answer(what11, element11))


@variant.solution_space(0)
@variant.text('Определите число {what12} в атоме ${element12:RuText}$.')
@variant.answer('$Z = {element12:protons}$ протонов и столько же электронов, $A = {element12:nuclons}$ нуклонов, $A - Z = {element12:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what12=all_particles)
@variant.arg(element12=get_elements_sublist(11, shift=1))
class AtomCount12_Text(variant.VariantTask):
    def GetUpdate(self, element12=None, what12=None):
        return dict(answer=get_element_answer(what12, element12))


@variant.text('''
    В ядре электрически нейтрального атома {nuclons} частиц.
    Вокруг ядра обращается {electrons} электронов.
    Сколько в ядре этого атома протонов и нейтронов?
    Назовите этот элемент.
''')
@variant.answer('$Z = {protons}$ протонов и $A - Z = {neutrons}$ нейтронов, так что это {element:RuText}: ${element:LaTeX}$')
@variant.arg(nuclons__electrons=[
    (108, 47),  # Al
    (65, 29),  # Cu
    (63, 29),  # Cu
    (121, 51),  # Sb
    (123, 51),  # Cu
    (190, 78),  # Pt
])
@variant.is_one_arg
class KernelCount(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            neutrons=a.nuclons - a.electrons,
            protons=a.electrons,
            element=AllElements.get_by_z_a(z=a.electrons, a=a.nuclons)
        )


@variant.solution_space(80)
@variant.text('Запишите реакцию ${fallType}$-распада ${element:LaTeX}$.')
@variant.answer_short('{reaction}')
@variant.arg(fallType__element=[
    ('\\alpha', AllElements.get_by_z_a(92, 238)),
    ('\\alpha', AllElements.get_by_z_a(60, 144)),
    ('\\alpha', AllElements.get_by_z_a(62, 147)),
    ('\\alpha', AllElements.get_by_z_a(62, 148)),
    ('\\alpha', AllElements.get_by_z_a(74, 180)),
    ('\\alpha', AllElements.get_by_z_a(63, 153)),
    ('\\beta', AllElements.get_by_z_a(55, 137)),
    ('\\beta', AllElements.get_by_z_a(11, 22)),
])
@variant.is_one_arg
class RadioFall(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            reaction=FallType.get_reaction(a.element, a.fallType),
        )


@variant.text('''
    Во сколько раз меньше нейтронов содержит ядро атома азота с массовым
    и зарядовым числами 14 и 7, чем ядро цинка с массовым и зарядовым числамн 65 и 30?
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Chernoutsan_13_78(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    Ядро урана с массовым числом 239 и зарядовым числом 92, являясь радиоактивным,
    после испускания электрона превращается в ядро некоторого элемента.
    Каков порядковый номер этого элемента в периодической системе элементов Менделеева?
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Chernoutsan_13_79(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    В реакции изотопа п А] и углерода 2 образуется альфа-частица, нейтрон
    и ядро некоторого изотопа.  Определите количество нейтронов в образующемся ядре.
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Chernoutsan_13_80(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    При бомбардировке лития SLi нейтронами образуется ядро гелия-4 и изотоп некоторого элемента.
    Определите количество нейтронов в ядре этого изотопа.
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Chernoutsan_13_81(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    При бомбардировке нейтронами ядра атома алюминия 71 А1 испускается альфа-частица
    и образуется ядро некоторого изотопа. Определите количество нейтронов в ядре вновь образовавшегося изотопа.
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Chernoutsan_13_82(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    Ядро изотопа бериллия 3Be, поглотив ядро дейтерия, превращается в ядро некоторого элемента.
    При этом испускается один нейтрон. Каков порядковый номер образовавшегося элемента в таблице Менделеева?
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Chernoutsan_13_83(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    Когда ядро атома алюминия захватывает альфа-частицу, то образуется нейтрон
    и радиоактивный изотоп некоторого элемента. При его распаде испускается позитрон.
    Каков порядковый номер элемента, образующегося при этом распаде? Порядковый номер алюминня 13.
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Chernoutsan_13_84(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    После захвата нейтрона ядро изотопа урана 280 превращается в радиоактивный изотоп урана,
    который после двух последовательных бета-распадов превращается в плутоний.
    Сколько нейтронов содержит ядро атома плутония?
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Chernoutsan_13_85(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    В цепочке радиоактивных превращений после 5 бета-распадов и нескольких альфа-распадов
    ядро тяжелого элемента превращается в ядро устойчивого атома,
    порядковый номер которого на 13 меньше первоначального.
    На сколько меньше первоначального становится массовое число ядра?
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Chernoutsan_13_86(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    В цепочке радиоактивных превращений после нескольких альфа- и бета-распадов
    ядро некоторого тяжелого атома превращается в ядро устойчивого атома,
    у которого число нейтронов на 27 меньше, чем у первоначального ядра.
    Известно, что число альфа-распадов равно числу бета-распадов.
    Чему равно общее число распадов?
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Chernoutsan_13_87(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    Ядро некоторого элемента Х захватывает альфа-частицу.
    При этом испускается нейтрон и образуется ядро элемента У.
    Это ядро в свою очередь распадается с испусканием позитрона, образуя ядро элемента 7.
    Определите, на сколько больше нейтронов в ядре элемента 2, чем в первоначальном ядре Х.
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Chernoutsan_13_88(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )


@variant.text('''
    За время 150 с распалось 7/8 первоначального числа радиоактивных ядер.
    Чему равен период полураспада этого элемента?
''')
@variant.solution_space(80)
@variant.arg(A='A = 1/2/3 a')
@variant.answer_align([
])
@variant.is_one_arg
class Chernoutsan_13_89(variant.VariantTask):
    def GetUpdateOneArg(self, a):
        return dict(
            B=a.A,
        )
