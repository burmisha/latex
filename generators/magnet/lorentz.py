import itertools

import generators.variant as variant
from generators.helpers import Consts

import logging
log = logging.getLogger(__name__)


@variant.text('''
    Частица, обладающая массой $m$ и положительным зарядом $q$, движется со скоростью $v$
    в магнитном поле перпендикулярно линиям его индукции. Индукция магнитного поля равна $B$.
    Выведите из базовых физических законов формулы для радиуса траектории частицы: сделайте рисунок, укажите вид движения и названия физических законов.
''')
@variant.solution_space(100)
@variant.no_args
@variant.answer_short('F = ma, F = qvB, a = v^2 / R \\implies R = \\frac{mv}{qB}.')
class BaseR(variant.VariantTask):
    pass


@variant.text('''
    Положительно заряженная частица движется со скоростью $v$ в магнитном поле перпендикулярно линиям его индукции.
    Индукция магнитного поля равна $B$, масса частицы $m$, её заряд — $q$.
    Выведите из базовых физических законов формулы для радиуса траектории частицы и её {what}.
''')
@variant.solution_space(120)
@variant.arg(what=['периода обращения', 'угловой скорости', 'частоты обращения'])
@variant.answer_short('''
    F = ma, F = qvB, a = v^2 / R \\implies R = \\frac{mv}{qB}.
    \\quad T = \\frac{2\\pi R}{v} = \\frac{2\\pi m}{qB}.
    \\quad \\omega = \\frac vR = \\frac{qB}{m}.
    \\quad \\nu = \\frac 1T = \\frac{qB}{2\\pi m}.
''')
class Force13(variant.VariantTask):
    pass


@variant.text('''
    {what} со скоростью {v:V:e} влетает в магнитное поле индукцией {B:V:e} перпендикулярно линиям его индукции.
    Определите радиус траектории частицы, для вычислений воспользуйтесь табличными значениями.
''')
@variant.solution_space(120)
@variant.arg(what__m=[('Электрон', Consts.m_e), ('Протон', Consts.m_p)])
@variant.arg(v=('v = {} км/c', ['2 10^3', '3 10^3', '5 10^3', '2 10^4', '3 10^4', '5 10^4']))
@variant.arg(B=('B = {} мТл', [20, 40, 50, 200, 300, 500]))
@variant.answer_short('''
    F = ma, F = evB, a = v^2 / R \\implies R = \\frac{mv}{eB} = \\frac{{m:V} * {v:V}}{{e:V} * {B:V}} \\approx {R:V}.
''')
class Force14(variant.VariantTask):
    def GetUpdate(self, what=None, m=None, v=None, B=None):
        # TODO: WTF
        R = (m.Value * v.Value) / (Consts.e.Value * B.Value) * 10 ** (v.Power + B.Power - 2)
        return dict(R='R = %.2f м' % R, e=Consts.e)


@variant.text('''
    {which} частица находится в постоянном {field} поле, а её мгновенная скорость {how} линиям его {lines}.
    По какой траектории движется частица? (прямая, гипербола, парабола, окружность, спираль, ...)
    Действием всех других полей пренебречь.
''')
@variant.solution_space(120)
@variant.arg(which=['Незаряженная', 'Заряженная'])
@variant.arg(field__lines=[('магнитном', 'индукции'), ('электростатическом', 'напряжённости')])
@variant.arg(how=['параллельна', 'перпендикулярна'])
@variant.answer_short('\\text{{answer}}')
class Force15(variant.VariantTask):
    def GetUpdate(self, which=None, field=None, lines=None, how=None):
        if 'езаряжен' in which:
            answer = 'Прямая'
        else:
            if 'магн' in field:
                if 'паралл' in how:
                    answer = 'Прямая'
                else:
                    answer = 'Окружность'
            else:
                if 'паралл' in how:
                    answer = 'Прямая'
                else:
                    answer = 'Парабола'

        return dict(answer=answer)


@variant.text('''
    Узкий пучок протонов, нейтронов и электронов влетает в однородное магнитное поле перпендикулярно его линиям (см. рис).
    Определите по трекам частиц {first} и {second} отношение радиусов их траекторий и их {what}.
''')
@variant.solution_space(100)
@variant.arg(what=['скоростей', 'кинетических энергий', 'импульсов'])
@variant.arg(first=[1, 2, 3])
@variant.arg(second=[5, 6, 7])
class Force16(variant.VariantTask):
    pass


@variant.text('''
    Частица массой $m$ и зарядом $q$ влетает со скоростью $v$ в однородное магнитное поле индукцией $B$ перпендикулярно его линиям.
    Определите, за какое время вектор скорости частицы повернётся на ${angle}\\degrees$ (впервые, если таких моментов будет несколько).
''')
@variant.solution_space(120)
@variant.arg(angle=[30, 45, 60, 90, 120, 135, 160, 180])
class Force17(variant.VariantTask):
    pass


@variant.text('''
    {particle}, прошедший через ускоряющую разность потенциалов, оказывается в магнитном поле индукцией {B:V:e}
    и движется по окружности диаметром {d:V:e}. Сделайте рисунок, определите значение разности потенциалов
    и укажите, в какой области потенциал больше, а где меньше.
''')
@variant.solution_space(100)
@variant.arg(particle=['Электрон', 'Позитрон', 'Протон'])
@variant.arg(B=('B = {} мТл', [20, 40, 50]))
@variant.arg(d=('d = {} мм', [4, 6, 8]))
class Force18(variant.VariantTask):
    pass
