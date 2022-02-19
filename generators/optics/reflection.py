import generators.variant as variant

from generators.helpers import Fraction, Consts, UnitValue

import math


@variant.text('''
    Постройте изображения ${X}'{Y}'$ и ${U}'{V}'$ стрелок ${X}{Y}$ и ${U}{V}$
    в 2 плоских зеркалах соответственно (см. рис. на доске).
''')
@variant.solution_space(180)
@variant.arg(X='A/B/C')
@variant.arg(Y='D/E/F')
@variant.arg(U='K/L/M')
@variant.arg(V='P/R/S')
class Reflection01(variant.VariantTask):
    pass


@variant.text('''
    Постройте область видимости стрелки ${X}{Y}$ в плоском зеркале (см. рис. на доске).
''')
@variant.solution_space(120)
@variant.arg(X='A/B/C/D')
@variant.arg(Y='K/L/M/N')
class Reflection02(variant.VariantTask):
    pass


@variant.text('Докажите, что {what}.')
@variant.solution_space(120)
@variant.arg(what=[
    '''изображение точечного источника света в плоском зеркале можно получить,
    «удвоив» (в векторном смысле) перпендикуляр, опущенный из источника на плоскость зеркала''',
    '''при повороте плоского зеркала на угол $\\varphi$ вокруг оси, лежащей в плоскости зеркала
    и перпендикулярной падающему лучу, этот луч повернётся на угол $2\\varphi$''',
])
class Reflection03(variant.VariantTask):
    pass


@variant.text('''
    Плоское зеркало вращается с угловой скоростью {omega:V:e}.
    Ось вращения лежит в плоскости зеркала. На зеркало падает луч перпендикулярно оси вращения.
    Определите угловую скорость вращения отражённого луча.
''')
@variant.solution_space(80)
@variant.arg(omega='0.12/0.14/0.15/0.16/0.17/0.18/0.19/0.23/0.25/0.28 рад/с')
@variant.answer_short('\\omega\' = 2 \\omega = {omega2:V}')
class ReflectionRotate(variant.VariantTask):
    def GetUpdate(self, *, omega=None):
        return dict(
            omega2 = 2 * omega,
        )


@variant.text('''
    Плоское зеркало приближается к стационарному предмету размером {d:V:e}
    со скоростью {v:V:e}. Определите размер изображения предмета через {t:V:e} после начала движения,
    если изначальное расстояние между зеркалом и предметом было равно {h:V:e}.
''')
@variant.solution_space(80)
@variant.arg(d='5/6/7 см')
@variant.arg(v='1/2/3 см/с')
@variant.arg(h='50/60/70 см')
@variant.arg(t='2/3/4/5 с')
@variant.answer_short('{d:V}')
class ReflectionSize(variant.VariantTask):
    pass


@variant.text('''
    Предмет {what} со скоростью {v:V:e}. Определите скорость изображения, приняв зеркало стационарным.
''')
@variant.solution_space(80)
@variant.arg(v='2/3/4 см/с')
@variant.arg(what=['приближается к плоскому зеркалу', 'отдаляется от плоского зеркала'])
@variant.answer_short('{v:V}')
class ReflectionSpeed(variant.VariantTask):
    pass


@variant.text('''
    Запишите своё имя (не фамилию) печатными буквами
    и постройте их изображение в 2 зеркалах: вертикальном и горизонтальном.
    Не забудьте отметить зеркала.
''')
@variant.solution_space(120)
@variant.no_args
class ReflectionName(variant.VariantTask):
    pass


@variant.text('''
    Параллельный пучок света распространяется горизонтально.
    Под каким углом (в градусах) к горизонту следует расположить плоское зеркало,
    чтобы отраженный пучок распространялся вертикально?
''')
@variant.solution_space(80)
@variant.no_args
@variant.answer_short('45\\degrees')
class Chernoutsan_13_5(variant.VariantTask):
    pass


@variant.text('''
    Под каким углом (в градусах) к горизонту следует расположить плоское зеркало,
    чтобы осветить дно вертикального колодца отраженными от зеркала солнечными лучами,
    падающими под углом ${angle}\\degrees$ к {what}?
''')
@variant.solution_space(80)
@variant.arg(what='вертикали/горизонту')
@variant.arg(angle=list(range(22, 70, 2)))
@variant.answer_short('\\alpha = {alpha}\\degrees, (90\\degrees - \\beta + \\alpha) + (90\\degrees - \\beta) = 90\\degrees \\implies \\beta = 45\\degrees + \\frac \\alpha 2 = {beta}\\degrees')
class Chernoutsan_13_6(variant.VariantTask):
    def GetUpdate(self, *, what=None, angle=None):
        alpha = {
            'горизонту': angle,
            'вертикали': 90 - angle,
        }[what]
        return dict(
            alpha=alpha,
            beta=alpha // 2 + 45,
        )


@variant.text('''
    {who} стоит перед плоским зеркалом, укрепленным на вертикальной стене.
    Какова должна быть минимальная высота зеркала, чтобы {who} {who2} видеть себя в полный рост?
    Рост {who3} {h:V:e}. Определите также расстояние от пола до нижнего края зеркала,
    приняв высоту головы равной {d:V:e}, и считая, что глаза находятся посередине (по высоте) головы.
''')
@variant.solution_space(80)
@variant.arg(d='30/32/34 см')
@variant.arg(h=('h = {} см', list(range(156, 194, 2))))
@variant.arg(who__who2__who3=[
    ('Аня', 'могла', 'Ани'),
    ('Борис', 'мог', 'Бориса'),
    ('Варя', 'могла', 'Вари'),
    ('Григорий', 'мог', 'Григория'),
    ('Денис', 'мог', 'Дениса'),
    ('Жанна', 'могла', 'Жанны'),
    ('Женя', 'могла', 'Жени'),
    ('Женя', 'мог', 'Жени'),
    ('Залина', 'могла', 'Залина'),
    ('Ираклий', 'мог', 'Ираклия'),
    ('Камиля', 'могла', 'Камили'),
    ('Лиана', 'могла', 'Лианы'),
    ('Малика', 'могла', 'Малики'),
    ('Нелли', 'могла', 'Нелли'),
    ('Осип', 'мог', 'Осипа'),
    ('Полина', 'могла', 'Полины'),
    ('Рипсиме', 'могла', 'Рипсиме'),
    ('Савелий', 'мог', 'Савелия'),
    ('Тимур', 'мог', 'Тимура'),
    ('Ульяна', 'могла', 'Ульяны'),
    ('Феофан', 'мог', 'Феофана'),
])
@variant.answer_short('{l:V}, {H:V}')
class Chernoutsan_13_7(variant.VariantTask):
    def GetUpdate(self, *, h=None, d=None, who=None, who2=None, who3=None):
        H = float((h / 2).SI_Value - (d / 4).SI_Value)
        return dict(
            l=(h / 2).IncPrecision(1).As('см'),
            H=f'{H * 100:.1f} см',
        )


@variant.text('''
    Во сколько раз увеличится расстояние между предметом и его изображением
    в плоском зеркале, если зеркало переместить в то место, где было изображение? Предмет остаётся неподвижным.
''')
@variant.solution_space(80)
@variant.no_args
@variant.answer_short('2')
class Chernoutsan_13_8(variant.VariantTask):
    pass


@variant.text('''
    Плоское зеркало движется по направлению к точечному источнику света со скоростью {v:V:e}.
    Определите скорость движения изображения относительно {what}.
    Направление скорости зеркала перпендикулярно плоскости зеркала.
''')
@variant.solution_space(80)
@variant.arg(v='10/12/15/18/20 см/с')
@variant.arg(what=['зеркала', 'источника света'])
@variant.answer_short('{v2:V}')
class Chernoutsan_13_9(variant.VariantTask):
    def GetUpdate(self, *, v=None, what=None):
        v2 = {
            'зеркала': v,
            'источника света': v * 2,
        }[what]
        return dict(
            v2=v2.As('см/с'),
        )


@variant.text('''
    Сколько изображений получится от предмета в двух плоских зеркалах,
    поставленных под углом ${angle}\\degrees$ друг к другу?
''')
@variant.solution_space(80)
@variant.arg(angle=[30, 45, 60, 90])
@variant.answer_short('{ans}')
class Chernoutsan_13_10(variant.VariantTask):
    def GetUpdate(self, *, angle=None):
        ans = 360 // angle - 1
        assert isinstance(ans, int)
        return dict(
            ans=ans,
        )


@variant.text('''
    Два плоских зеркала располагаются под углом друг к другу
    и между ними помещается точечный источник света.
    Расстояние от этого источника до одного зеркала {a:V:e}, до другого {b:V:e}.
    Расстояние между первыми изображениями в зеркалах {c:V:e}.
    Найдите угол (в градусах) между зеркалами.
''')
@variant.solution_space(80)
@variant.arg(a='3/4/5 см')
@variant.arg(b='6/7/8/9 см')
@variant.arg(angle=[30, 45, 60])
@variant.answer_short('\\cos \\alpha = \\frac{c^2 - \\sqr{2a} - \\sqr{2b}}{2 * 2a * 2b} \\approx {cos:.3f} \\implies \\alpha = {alpha:.1f}\\degrees')
class Chernoutsan_13_11(variant.VariantTask):
    def GetUpdate(self, *, a=None, b=None, angle=None):
        a2 = float(a.SI_Value) * 2
        b2 = float(b.SI_Value) * 2
        c_exact = (a2 ** 2 + b2 ** 2 - 2 * a2 * b2 * math.cos((180 - angle) / 180 * math.pi)) ** 0.5
        c = UnitValue(f'{c_exact * 100:.2f} см')
        cos = (float(c.SI_Value) ** 2 - a2 ** 2 - b2 ** 2) / 2 / a2 / b2
        alpha = math.acos(cos) / math.pi * 180
        return dict(
            c=c,
            cos=cos,
            alpha=alpha,
        )
