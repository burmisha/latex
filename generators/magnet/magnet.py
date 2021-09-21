import itertools

import generators.variant as variant
from generators.helpers import Consts

import logging
log = logging.getLogger(__name__)


@variant.text('''
    Укажите, верны ли утверждения («да» или «нет» слева от каждого утверждения):
    \\begin{itemize}
        \\item  Если распилить постоянный магнит на 2, то мы получим 2 магнита:
                один только с южным полюсом, а второй — только с северным.
        \\item  Полосовой магнит можно распилить {q2} разрезами на {r2} магнита поменьше.
        \\item  Между линиями индукции магнитного поля величина этого поля пренебрежимо мала.
        \\item  Линии магнитного поля всегда замкнуты.
        \\item  Линии магнитного поля могут пересекаться в полюсах магнитов.
        \\item  Линии магнитного поля {q61} у северного полюса и {q62} у южного.
        \\item  Чем гуще линии — тем {q7} магнитное поле.
        \\item  Северный географический полюс Земли в точности совпадает с {q8} магнитным полюсом Земли.
        \\item  Если в компасе установить сильный магнит, то его не удастся отклонить магнитным полем неподалёку.
                Так не делают лишь потому, что компас станет слишком неудобным в бытовом использовании.
        \\item  Внутри магнита есть магнитное поле, поэтому для честности мы обязаны рисовать поле как снаружи, так и внутри него.
    \\end{itemize}
''')
@variant.arg(q2__r2=[(2, 3), (3, 4)])
@variant.arg(q61__q62=[('начинаются', 'заканчиваются'), ('заканчиваются', 'начинаются'),])
@variant.arg(q7__a7=[('слабее', 'нет'), ('сильнее', 'да'),])
@variant.arg(q8=['южным', 'северным'])
@variant.solution_space(0)
@variant.answer_short('\\text{нет, да, нет, да, нет, нет, {a7}, нет, нет, да}')
class ConstMagnet0(variant.VariantTask):
    pass


@variant.text('''
    Изобразите линии индукции магнитного поля вокруг постоянного магнита.

    \\begin{tikzpicture}[x=1cm,y=1cm,thick]
        \\draw (0, 0) rectangle (3, 0.6);
        \\node [right] (right) at (0, 0.3) {{L}};
        \\node [left] (left) at (3, 0.3) {{R}};
        \\node [right] (right) at (0, 2) {};
        \\node [right] (right) at (0, -2) {};
        \\node [right] (right) at (-2, 0) {};
        \\node [right] (right) at (5, 0) {};
    \\end{tikzpicture}
''')
@variant.arg(L__R=[('N', 'S'), ('S', 'N')])
@variant.solution_space(0)
class ConstMagnet01(variant.VariantTask):
    pass


@variant.text('Опишите {what}. Нужны рисунки и необходимый минимум пояснений и терминов, трактат не нужен.')
@variant.arg(what=[
    'опыт Эрстеда',
    'взаимодействие полосовых магнитов',
    'взаимодействие параллельных прямых токов',
])
@variant.solution_space(100)
class ConstMagnet02(variant.VariantTask):
    pass


@variant.text('''
    Для постоянного магнита, изображённого на рис. 1{variant})
    изобразите линии индукции магнитного поля
    и укажите, как соориентируются магнитные стрелки в точках {points}.
''')
@variant.arg(variant=['а', 'б', 'в', 'г'])
@variant.arg(points=[' и '.join(points) for points in itertools.combinations('ABCD', 2)])
@variant.solution_space(80)
class ConstMagnet1(variant.VariantTask):
    pass


@variant.text('''
    Магнитная стрелка вблизи длинного прямолинейного проводника
    повёрнута в точке ${point}$ северным полюсом {direction} (см. рис. 2{variant}).
    Сделайте рисунок, укажите направление протекания электрического тока,
    изобразите линии индукции магнитного поля.
''')
@variant.solution_space(80)
@variant.arg(variant__direction__point=itertools.chain(
    itertools.product(
        ['а', 'б'],
        ['налево', 'направо'],
        'AB',
    ),
    itertools.product(
        ['в', 'г'],
        ['вверх', 'вниз'],
        'AB',
    ),
))
class ConstMagnet2(variant.VariantTask):
    pass


@variant.text('''
    Рядом с каждой единицей измерения укажите физическую величину, которая в ней измеряется, и один из вариантов обозначений этой физической величины.
    \\begin{enumerate}
        \\item {first},
        \\item {second},
        \\item {third}.
    \\end{enumerate}
''')
@variant.solution_space(40)
@variant.arg(first=['Тл', 'Кл'])
@variant.arg(second=['м', 'м/с'])
@variant.arg(third=['А', 'радиан'])
class Force10(variant.VariantTask):
    pass


@variant.text('''
    Запишите формулой закон для вычисления модуля силы, действующей
    на {what1} в магнитном поле, и выразите из него {what2}.
''')
@variant.solution_space(40)
@variant.arg(what1=[
    'заряженную частицу, движущуюся',
    'проводник, по которому течёт электрический ток,'
])
@variant.arg(what2=['значение угла', 'индукцию магнитного поля'])
class Force11(variant.VariantTask):
    pass


@variant.text('''
    Запишите формулой закон {who} и укажите
    для каждой величины её название и единицы измерения в системе СИ.
''')
@variant.solution_space(80)
@variant.arg(who=['Ампера', 'Лоренца'])
class Force12(variant.VariantTask):
    pass


@variant.text('''
    Кольцевой ток (виток с током) ориентирован как указано на рисунке 3{variant}).
    Изобразите линии индукции магнитного поля.
    Укажите, как соориентируется магнитная стрелка в точках {points}.
    Как нужно расположить ещё один кольцевой ток, чтобы между ними возникло {what}
    (сделайте отдельный рисунок с витками, укажите направления протекания тока и направление сил)?
''')
@variant.arg(variant=['а', 'б', 'в', 'г'])
@variant.arg(points=[' и '.join(points) for points in itertools.combinations('ABCD', 2)])
@variant.arg(what=['притяжение', 'отталкивание'])
@variant.solution_space(80)
class ConstMagnet3(variant.VariantTask):
    pass
