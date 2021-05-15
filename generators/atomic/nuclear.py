import generators.variant as variant
from generators.helpers import UnitValue, Consts, Elements, ElementsList


def get_element_answer(what, element):
	return {
        'протонов': f'{element:protons}',
        'нейтронов': f'{element:neutrons}',
        'электронов': f'{element:electrons}',
        'нуклонов': f'{element:nuclons}',
    }[what]


all_particles = ['протонов', 'нейтронов', 'электронов', 'нуклонов']


@variant.solution_space(0)
@variant.text('Определите число {what01} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what01=all_particles)
@variant.arg(element=ElementsList[0:3])
class AtomCount01(variant.VariantTask):
    def GetUpdate(self, element=None, what01=None, **kws):
        return dict(answer=get_element_answer(what01, element))


@variant.solution_space(0)
@variant.text('Определите число {what02} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what02=all_particles)
@variant.arg(element=ElementsList[3:7])
class AtomCount02(variant.VariantTask):
    def GetUpdate(self, element=None, what02=None, **kws):
        return dict(answer=get_element_answer(what02, element))


@variant.solution_space(0)
@variant.text('Определите число {what03} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what03=all_particles)
@variant.arg(element=ElementsList[7:12])
class AtomCount03(variant.VariantTask):
    def GetUpdate(self, element=None, what03=None, **kws):
        return dict(answer=get_element_answer(what03, element))


@variant.solution_space(0)
@variant.text('Определите число {what04} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what04=all_particles)
@variant.arg(element=ElementsList[12:18])
class AtomCount04(variant.VariantTask):
    def GetUpdate(self, element=None, what04=None, **kws):
        return dict(answer=get_element_answer(what04, element))


@variant.solution_space(0)
@variant.text('Определите число {what05} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what05=all_particles)
@variant.arg(element=ElementsList[18:25])
class AtomCount05(variant.VariantTask):
    def GetUpdate(self, element=None, what05=None, **kws):
        return dict(answer=get_element_answer(what05, element))


@variant.solution_space(0)
@variant.text('Определите число {what06} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what06=all_particles)
@variant.arg(element=ElementsList[25:33])
class AtomCount06(variant.VariantTask):
    def GetUpdate(self, element=None, what06=None, **kws):
        return dict(answer=get_element_answer(what06, element))


@variant.solution_space(0)
@variant.text('Определите число {what07} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what07=all_particles)
@variant.arg(element=ElementsList[33:42])
class AtomCount07(variant.VariantTask):
    def GetUpdate(self, element=None, what07=None, **kws):
        return dict(answer=get_element_answer(what07, element))


@variant.solution_space(0)
@variant.text('Определите число {what08} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what08=all_particles)
@variant.arg(element=ElementsList[42:52])
class AtomCount08(variant.VariantTask):
    def GetUpdate(self, element=None, what08=None, **kws):
        return dict(answer=get_element_answer(what08, element))


@variant.solution_space(0)
@variant.text('Определите число {what09} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what09=all_particles)
@variant.arg(element=ElementsList[52:63])
class AtomCount09(variant.VariantTask):
    def GetUpdate(self, element=None, what09=None, **kws):
        return dict(answer=get_element_answer(what09, element))


@variant.solution_space(0)
@variant.text('Определите число {what10} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what10=all_particles)
@variant.arg(element=ElementsList[63:75])
class AtomCount10(variant.VariantTask):
    def GetUpdate(self, element=None, what10=None, **kws):
        return dict(answer=get_element_answer(what10, element))


@variant.solution_space(0)
@variant.text('Определите число {what11} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what11=all_particles)
@variant.arg(element=ElementsList[75:88])
class AtomCount11(variant.VariantTask):
    def GetUpdate(self, element=None, what11=None, **kws):
        return dict(answer=get_element_answer(what11, element))


@variant.solution_space(0)
@variant.text('Определите число {what12} в атоме ${element:LaTeX}$.')
@variant.answer('$Z = {element:protons}$ протонов и столько же электронов $A = {element:nuclons}$ нуклонов, $A - Z = {element:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what12=all_particles)
@variant.arg(element=ElementsList[88:102])
class AtomCount12(variant.VariantTask):
    def GetUpdate(self, element=None, what12=None, **kws):
        return dict(answer=get_element_answer(what12, element))



@variant.solution_space(0)
@variant.text('Определите число {what01} в атоме ${element01:RuText}$.')
@variant.answer('$Z = {element01:protons}$ протонов и столько же электронов, $A = {element01:nuclons}$ нуклонов, $A - Z = {element01:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what01=all_particles)
@variant.arg(element01=ElementsList[1:4])
class AtomCount01_Text(variant.VariantTask):
    def GetUpdate(self, element01=None, what01=None, **kws):
        return dict(answer=get_element_answer(what01, element01))


@variant.solution_space(0)
@variant.text('Определите число {what02} в атоме ${element02:RuText}$.')
@variant.answer('$Z = {element02:protons}$ протонов и столько же электронов, $A = {element02:nuclons}$ нуклонов, $A - Z = {element02:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what02=all_particles)
@variant.arg(element02=ElementsList[4:8])
class AtomCount02_Text(variant.VariantTask):
    def GetUpdate(self, element02=None, what02=None, **kws):
        return dict(answer=get_element_answer(what02, element02))


@variant.solution_space(0)
@variant.text('Определите число {what03} в атоме ${element03:RuText}$.')
@variant.answer('$Z = {element03:protons}$ протонов и столько же электронов, $A = {element03:nuclons}$ нуклонов, $A - Z = {element03:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what03=all_particles)
@variant.arg(element03=ElementsList[8:13])
class AtomCount03_Text(variant.VariantTask):
    def GetUpdate(self, element03=None, what03=None, **kws):
        return dict(answer=get_element_answer(what03, element03))


@variant.solution_space(0)
@variant.text('Определите число {what04} в атоме ${element04:RuText}$.')
@variant.answer('$Z = {element04:protons}$ протонов и столько же электронов, $A = {element04:nuclons}$ нуклонов, $A - Z = {element04:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what04=all_particles)
@variant.arg(element04=ElementsList[13:19])
class AtomCount04_Text(variant.VariantTask):
    def GetUpdate(self, element04=None, what04=None, **kws):
        return dict(answer=get_element_answer(what04, element04))


@variant.solution_space(0)
@variant.text('Определите число {what05} в атоме ${element05:RuText}$.')
@variant.answer('$Z = {element05:protons}$ протонов и столько же электронов, $A = {element05:nuclons}$ нуклонов, $A - Z = {element05:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what05=all_particles)
@variant.arg(element05=ElementsList[19:26])
class AtomCount05_Text(variant.VariantTask):
    def GetUpdate(self, element05=None, what05=None, **kws):
        return dict(answer=get_element_answer(what05, element05))


@variant.solution_space(0)
@variant.text('Определите число {what06} в атоме ${element06:RuText}$.')
@variant.answer('$Z = {element06:protons}$ протонов и столько же электронов, $A = {element06:nuclons}$ нуклонов, $A - Z = {element06:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what06=all_particles)
@variant.arg(element06=ElementsList[26:34])
class AtomCount06_Text(variant.VariantTask):
    def GetUpdate(self, element06=None, what06=None, **kws):
        return dict(answer=get_element_answer(what06, element06))


@variant.solution_space(0)
@variant.text('Определите число {what07} в атоме ${element07:RuText}$.')
@variant.answer('$Z = {element07:protons}$ протонов и столько же электронов, $A = {element07:nuclons}$ нуклонов, $A - Z = {element07:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what07=all_particles)
@variant.arg(element07=ElementsList[34:43])
class AtomCount07_Text(variant.VariantTask):
    def GetUpdate(self, element07=None, what07=None, **kws):
        return dict(answer=get_element_answer(what07, element07))


@variant.solution_space(0)
@variant.text('Определите число {what08} в атоме ${element08:RuText}$.')
@variant.answer('$Z = {element08:protons}$ протонов и столько же электронов, $A = {element08:nuclons}$ нуклонов, $A - Z = {element08:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what08=all_particles)
@variant.arg(element08=ElementsList[43:53])
class AtomCount08_Text(variant.VariantTask):
    def GetUpdate(self, element08=None, what08=None, **kws):
        return dict(answer=get_element_answer(what08, element08))


@variant.solution_space(0)
@variant.text('Определите число {what09} в атоме ${element09:RuText}$.')
@variant.answer('$Z = {element09:protons}$ протонов и столько же электронов, $A = {element09:nuclons}$ нуклонов, $A - Z = {element09:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what09=all_particles)
@variant.arg(element09=ElementsList[53:64])
class AtomCount09_Text(variant.VariantTask):
    def GetUpdate(self, element09=None, what09=None, **kws):
        return dict(answer=get_element_answer(what09, element09))


@variant.solution_space(0)
@variant.text('Определите число {what10} в атоме ${element10:RuText}$.')
@variant.answer('$Z = {element10:protons}$ протонов и столько же электронов, $A = {element10:nuclons}$ нуклонов, $A - Z = {element10:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what10=all_particles)
@variant.arg(element10=ElementsList[64:76])
class AtomCount10_Text(variant.VariantTask):
    def GetUpdate(self, element10=None, what10=None, **kws):
        return dict(answer=get_element_answer(what10, element10))


@variant.solution_space(0)
@variant.text('Определите число {what11} в атоме ${element11:RuText}$.')
@variant.answer('$Z = {element11:protons}$ протонов и столько же электронов, $A = {element11:nuclons}$ нуклонов, $A - Z = {element11:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what11=all_particles)
@variant.arg(element11=ElementsList[76:89])
class AtomCount11_Text(variant.VariantTask):
    def GetUpdate(self, element11=None, what11=None, **kws):
        return dict(answer=get_element_answer(what11, element11))


@variant.solution_space(0)
@variant.text('Определите число {what12} в атоме ${element12:RuText}$.')
@variant.answer('$Z = {element12:protons}$ протонов и столько же электронов, $A = {element12:nuclons}$ нуклонов, $A - Z = {element12:neutrons}$ нейтронов. Ответ: {answer}')
@variant.answer_test('{answer}')
@variant.arg(what12=all_particles)
@variant.arg(element12=ElementsList[89:103])
class AtomCount12_Text(variant.VariantTask):
    def GetUpdate(self, element12=None, what12=None, **kws):
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
class KernelCount(variant.VariantTask):
    def GetUpdate(self, nuclons=None, electrons=None, **kws):
        return dict(
            neutrons=nuclons - electrons,
            protons=electrons,
            element=Elements.get_by_z_a(z=electrons, a=nuclons)
        )


@variant.solution_space(80)
@variant.text('Запишите реакцию ${fallType}$-распада ${element:LaTeX}$.')
@variant.answer('${element:LaTeX} \\to {res:LaTeX} + {add}$')
@variant.arg(fallType__element=[
    ('\\alpha', Elements.get_by_z_a(92, 238)),
    ('\\alpha', Elements.get_by_z_a(60, 144)),
    ('\\alpha', Elements.get_by_z_a(62, 147)),
    ('\\alpha', Elements.get_by_z_a(62, 148)),
    ('\\alpha', Elements.get_by_z_a(74, 180)),
    ('\\alpha', Elements.get_by_z_a(63, 153)),
    ('\\beta', Elements.get_by_z_a(55, 137)),
    ('\\beta', Elements.get_by_z_a(11, 22)),
])
class RadioFall(variant.VariantTask):
    def GetUpdate(self, fallType, element, **kws):
        if 'alpha' in fallType:
            res = element.alpha()
            add = '\\ce{ ^4_2 He }'
        elif 'beta' in fallType:
            res = element.beta()
            add = 'e^- + \\tilde\\nu_e'
        else:
            raise RuntimeError(f'Unknown fallType: {fallType}')
        return dict(
            res=res,
            add=add,
        )
