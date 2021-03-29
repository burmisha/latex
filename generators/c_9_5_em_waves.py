import fractions

import generators.variant as variant
from generators.helpers import UnitValue, Consts, Fraction


@variant.solution_space(20)
@variant.text('''
    Напротив физических величин укажите их обозначения и единицы измерения в СИ, а в пункте «г)» запишите физический закон или формулу:
    \\begin{{enumerate}}
        \\item {v_1},
        \\item {v_2},
        \\item {v_3},
        \\item {v_4}.
    \\end{{enumerate}}
''')
@variant.arg(v_1=['скорость света в среде', 'корость света в вакууме'])
@variant.arg(v_2=['длина волны', 'частоты волны'])
@variant.arg(v_3=[
    'период колебаний напряжённости электрического поля в электромагнитной волне',
    'период колебаний индукции магнитного поля в электромагнитной волне',
])
@variant.arg(v_4=[
    'абсолютный показатель преломления среды',
    'относительный показатель преломления среды',
])
class Definitions01(variant.VariantTask):
    pass


@variant.solution_space(60)
@variant.text('''
    Выразите (нужен вывод из базовых физических законов):
    \\begin{{enumerate}}
        \\item {v_1},
        \\item {v_2},
        \\item {v_3}.
    \\end{{enumerate}}
''')
@variant.arg(v_1=[
    'период колебаний через длину волны и скорость её распространения',
    'частоту колебаний через длину волны и скорость её распространения',
])
@variant.arg(v_2=[
    'энергию фотона через период колебаний в электромагнитной волне',
    'энергию фотона через длину электромагнитной волны',
])
@variant.arg(v_3=[
    'скорость света в среде через её абсолютный показатель преломления и скорость света в вакууме',
    'скорость света в вакууме через скорость света в среде и её абсолютный показатель преломления',
])
class Deduce01(variant.VariantTask):
    pass


@variant.solution_space(100)
@variant.text('''
    Укажите букву, соответствующую физическую величину (из текущего раздела), её едииницы измерения в СИ и выразите её из какого-либо уравнения:
    \\begin{{enumerate}}
        \\item {v_1},
        \\item {v_2},
        \\item {v_3},
        \\item {v_4}.
    \\end{{enumerate}}
''')
@variant.arg(v_1=['«йэ»', '«л\'амбда»'])
@variant.arg(v_2=['«вэ»', '«цэ»'])
@variant.arg(v_3=['«н\'у»', '«аш»'])
@variant.arg(v_4=['«эн»', '«тэ»'])
class Sound_to_value(variant.VariantTask):
    pass


@variant.solution_space(0)
@variant.text('''
    Напротив каждой приставки единиц СИ укажите её полное название и соответствующий множитель:
    \\begin{{enumerate}}
        \\item {v_1},
        \\item {v_2},
        \\item {v_3},
        \\item {v_4}.
    \\end{{enumerate}}
''')
@variant.arg(v_1=['м', 'М'])
@variant.arg(v_2=['к', 'мк'])
@variant.arg(v_3=['н', 'Г'])
@variant.arg(v_4=['с', 'Т'])
class Prefix(variant.VariantTask):
    pass
