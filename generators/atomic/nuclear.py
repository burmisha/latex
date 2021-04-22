import generators.variant as variant
from generators.helpers import UnitValue, Consts, Elements


@variant.text('''
    Определите число {what} в атоме {element:LaTeX}.
''')
@variant.answer('$Z = {element.protons}$ протонов и столько же электронов, $A - Z = {element.neutrons}$ нейтронов, {element.nuclons} нуклонов.')
@variant.answer_test('{answer}')
@variant.arg(what=['протонов', 'нейтронов', 'электронов', 'нуклонов'])
@variant.arg(element=[
    Elements.get_by_z_a(92, 238),
    Elements.get_by_z_a(60, 144),
    Elements.get_by_z_a(62, 147),
    Elements.get_by_z_a(62, 148),
    Elements.get_by_z_a(74, 180),
    Elements.get_by_z_a(63, 153),
    Elements.get_by_z_a(55, 137),
    Elements.get_by_z_a(11, 22),
])
class AtomCount(variant.VariantTask):
    def GetUpdate(self, element=None, what=None, **kws):
        answer = {
            'протонов': f'{element.protons}',
            'нейтронов': f'{element.neutrons}',
            'электронов': f'{element.electrons}', 
            'нуклонов': f'{element.nuclons}',
        }[what]
        return dict(
            N=N,
            answer=answer,
        )


@variant.text('''
    В ядре электрически нейтрального атома {nuclons} частиц.
    Вокруг ядра обращается {electrons} электронов.
    Сколько в ядре этого атома протонов и нейтронов?
''')
@variant.answer('$Z = {protons}$ протонов и $A - Z = {neutrons}$ нейтронов')
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
        )


@variant.text('Запишите реакцию ${fallType}$-распада {element}.')
@variant.arg(fallType__element=[
    ('\\alpha', '\ce{^{238}_{92}U}'),
    ('\\alpha', '\ce{^{144}_{60}Nd}'),
    ('\\alpha', '\ce{^{147}_{62}Sm}'),
    ('\\alpha', '\ce{^{148}_{62}Sm}'),
    ('\\alpha', '\ce{^{180}_{74}W}'),
    ('\\alpha', '\ce{^{153}_{61}Eu}'),
    ('\\beta', '\ce{^{137}_{55}Cs}'),
    ('\\beta', '\ce{^{22}_{11}Na}'),
])
class RadioFall(variant.VariantTask):
    pass
