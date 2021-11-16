import generators.variant as variant
from generators.helpers import UnitValue, Consts


@variant.text('''
    Длина волны света в~вакууме {lmbd:Task:e}.
    Какова частота этой световой волны?
    Какова длина этой волны в среде с показателем преломления {n:Task:e}?
    Может ли человек увидеть такую волну света, и если да, то какой именно цвет соответствует этим волнам в вакууме и в этой среде?
''')
@variant.arg(n=['n = 1.%d' % n for n in [3, 4, 5, 6, 7]])
@variant.arg(lmbd=['\\lambda = %d нм' % lmbd for lmbd in [400, 500, 600, 700]])
@variant.answer_align([
    '''\\nu &= \\frac 1T = \\frac 1{\\lambda/c} = \\frac c\\lambda = \\frac{Consts.c:Value|s}{lmbd:Value|s} \\approx {nu:Value},''',
    '''\\nu' = \\nu &\\cbr{\\text{или } T' = T} \\implies \\lambda' = v'T' = \\frac vn T = \\frac{ vt }n = \\frac \\lambda n = \\frac{lmbd:Value|s}{n:Value|s} \\approx {lmbd_1:Value}.''',
    '&\\text{380 нм---фиол---440---син---485---гол---500---зел---565---жёл---590---оранж---625---крас---780 нм},',
    '\\text{{see}}'
])
@variant.solution_space(180)
class Gendenshteyn_11_11_18(variant.VariantTask):
    def GetUpdate(self, n=None, lmbd=None):
        lmbd_1 = lmbd / n
        if 380 <= (lmbd_1.SI_Value * 10 ** 9) <= 780:
            see = 'увидит'
        else:
            see = 'не увидит'
        return dict(
            nu=Consts.c / lmbd,
            lmbd_1=lmbd_1.IncPrecision(3),
            see=see,
        )


@variant.solution_space(20)
@variant.text('''
    Напротив физических величин укажите их обозначения и единицы измерения в СИ, а в пункте «г)» запишите физический закон или формулу:
    \\begin{enumerate}
        \\item {v_1},
        \\item {v_2},
        \\item {v_3},
        \\item {v_4}.
    \\end{enumerate}
''')
@variant.arg(v_1=['скорость света в среде', 'скорость света в вакууме'])
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
    Получите из базовых физических законов:
    \\begin{enumerate}
        \\item {v_1},
        \\item {v_2},
        \\item {v_3}.
    \\end{enumerate}
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
    Укажите букву, соответствующую физическую величину (из текущего раздела), её единицы измерения в СИ и выразите её из какого-либо физического закона:
    \\begin{enumerate}
        \\item {v_1},
        \\item {v_2},
        \\item {v_3},
        \\item {v_4}.
    \\end{enumerate}
''')
@variant.arg(v_1=['«йэ»', '«л\'амбда»'])
@variant.arg(v_2=['«вэ»', '«цэ»'])
@variant.arg(v_3=['«н\'у»', '«аш»'])
@variant.arg(v_4=['«эн»', '«тэ»'])
class Sound_to_value(variant.VariantTask):
    pass



@variant.solution_space(30)
@variant.text('''
    Укажите букву, соответствующую физическую величину (из текущего раздела), её единицы измерения в СИ и выразите её из какого-либо физического закона:
    \\begin{enumerate}
        \\item {v_1},
        \\item {v_2},
        \\item {v_3},
        \\item {v_4}.
    \\end{enumerate}
''')
@variant.arg(v_1=['«эл\'»', '«л\'амбда»'])
@variant.arg(v_2=['«вэ»', '«цэ»'])
@variant.arg(v_3=['«н\'у»', '«бал\'шайа цэ»'])
@variant.arg(v_4=['«эн»', '«тэ»'])
class Sound_to_value_no_quant(variant.VariantTask):
    pass


@variant.solution_space(0)
@variant.text('''
    Напротив каждой приставки единиц СИ укажите её полное название и соответствующий множитель:
    \\begin{enumerate}
        \\item {v_1},
        \\item {v_2},
        \\item {v_3},
        \\item {v_4},
        \\item {v_5}.
    \\end{enumerate}
''')
@variant.arg(v_1=['м', 'М'])
@variant.arg(v_2=['к', 'мк'])
@variant.arg(v_3=['н', 'Г'])
@variant.arg(v_4=['с', 'Т'])
@variant.arg(v_5=['п', 'д'])
class Prefix(variant.VariantTask):
    pass


@variant.text('''
    На какую {what} волны настроен радиоприемник, если его колебательный контур
    обладает индуктивностью {L:V:e} и ёмкостью {C:V:e}?
''')
@variant.solution_space(100)
@variant.arg(what=['длину', 'частоту'])
@variant.arg(L='L = 200/300/600 мкГн')
@variant.arg(C='C = 600/650/700/750/800 пФ')
class Chernoutsan_12_50(variant.VariantTask):
    pass


@variant.text('''
    Колебательный контур настроен на частоту {nu:V:e}.
    Во сколько раз и как надо изменить {what} для перестройки контура на длину волны {lmbd:V:e}?
''')
@variant.solution_space(100)
@variant.arg(what=['ёмкость конденсатора', 'индуктивность катушки'])
@variant.arg(nu='\\nu = 0.5/0.8/1.5/1.8/2.5/3.2/4.5 10^7 Гц')
@variant.arg(lmbd='\\lambda = 20/25/30/40/50 м')
class Chernoutsan_12_51(variant.VariantTask):
    pass


@variant.text('''
    Колебательный контур, состоящий из катушки индуктивности
    и воздушного конденсатора, настроен на длину волны {lmbd_1:V:e}.
    При этом расстояние между пластинами конденсатора {d:V:e}.
    Каким должно быть это расстояние, чтобы контур был настроен на длину волны {lmbd_2:V:e}?
''')
@variant.arg(lmbd_1='\\lambda_1 = 20/30/50/120/180 м')
@variant.arg(lmbd_2='\\lambda_2 = 45/60/80/100/150 м')
@variant.arg(d='d = 2.0/2.5/3.0/3.5/4.0/4.5/5.0 мм')
@variant.solution_space(100)
class Chernoutsan_12_52(variant.VariantTask):
    pass
