import generators.variant as variant
from generators.helpers import Consts, n_times
import math

import logging
log = logging.getLogger(__name__)


@variant.text('''
    Укажите, верны ли утверждения («да» или «нет» слева от каждого утверждения):
    \\begin{itemize}
        \\item  Изображение предмета в {q} линзе всегда {q1}.
        \\item  Изображение предмета в {q} линзе всегда {q2}.
        \\item  Изображение предмета в {q} линзе всегда {q3}.
        \\item  Оптическая сила {lens} линзы {sign}.
    \\end{itemize}
''')
@variant.arg(q='рассеивающей/собирающей')
@variant.arg(q1='мнимое/действительное')
@variant.arg(q2='прямое/перевёрнутое')
@variant.arg(q3='увеличенное/уменьшенное')
@variant.arg(lens='рассеивающей/собирающей')
@variant.arg(sign='положительна/отрицательна')
@variant.solution_space(0)
@variant.answer_short('\\text{ {a1}, {a2}, {a3}, {a4} }')
class Theory01(variant.VariantTask):
    def GetUpdate(self, *, q=None, q1=None, q2=None, q3=None, lens=None, sign=None):
        a1 = {
            'рассеивающей': {'мнимое': 'да', 'действительное': 'нет'},
            'собирающей': {'мнимое': 'нет', 'действительное': 'нет'},
        }[q][q1]

        a2 = {
            'рассеивающей': {'прямое': 'да', 'перевёрнутое': 'нет'},
            'собирающей': {'прямое': 'нет', 'перевёрнутое': 'нет'},
        }[q][q2]

        a3 = {
            'рассеивающей': {'увеличенное': 'нет', 'уменьшенное': 'да'},
            'собирающей': {'увеличенное': 'нет', 'уменьшенное': 'нет'},
        }[q][q3]

        a4 = {
            'рассеивающей': {'положительна': 'да', 'отрицательна': 'нет'},
            'собирающей': {'положительна': 'нет', 'отрицательна': 'да'},
        }[lens][sign]

        return dict(
            a1=a1,
            a2=a2,
            a3=a3,
            a4=a4,
        )


@variant.text('{task}')
@variant.arg(task=[
    'Запишите формулу тонкой линзы и сделайте рисунок, указав на нём физические величины из этой формулы.',
    'Запишите известные вам виды классификации изображений.',
])
@variant.solution_space(60)
class Theory02(variant.VariantTask):
    pass


@variant.text('В каких линзах можно получить {which} изображение объекта?')
@variant.arg(which='прямое/обратное/мнимое/действительное/уменьшенное/увеличенное')
@variant.solution_space(40)
@variant.answer_short('\\text{ {a} }')
class Theory03(variant.VariantTask):
    def GetUpdate(self, *, which=None):
        a = {
            'прямое': 'собирающие и рассеивающие',
            'обратное': 'собирающие',
            'мнимое': 'собирающие и рассеивающие',
            'действительное': 'собирающие',
            'уменьшенное': 'собирающие и рассеивающие',
            'увеличенное': 'рассеивающие',
        }[which]

        return dict(
            a=a,
        )


@variant.text('Какое изображение называют {which}?')
@variant.arg(which='мнимым/действительным')
@variant.solution_space(40)
class Theory04(variant.VariantTask):
    pass


@variant.text('''
    Есть две линзы, обозначим их 1 и 2.
    Известно что {what} линзы {A} {how}, чем у линзы {B}.
    Какая линза сильнее преломляет лучи?
''')
@variant.arg(what=['фокусное расстояние', 'оптическая сила'])
@variant.arg(how='больше/меньше')
@variant.arg(A__B=[(1, 2), (2, 1)])
@variant.solution_space(40)
@variant.answer_short('{a}')
class Theory05(variant.VariantTask):
    def GetUpdate(self, *, what=None, how=None, A=None, B=None):
        a = {
            'фокусное расстояние': {'больше': B, 'меньше': A},
            'оптическая сила': {'больше': A, 'меньше': B},
        }[what][how]
        return dict(
            a=a,
        )


@variant.text('''
    Предмет находится на расстоянии {a:V:e} от {which} линзы с фокусным расстоянием {F:V:e}.
    Определите тип изображения, расстояние между предметом и его изображением, увеличение предмета.
    Сделайте схематичный рисунок (не обязательно в масштабе, но с сохранением свойств линзы и изображения).
''')
@variant.arg(a='10/20/30 см')
@variant.arg(F='6/8/12/15/25/40/50 см')
@variant.arg(which='собирающей/рассеивающей')
@variant.solution_space(100)
@variant.answer_short('b = \\frac{aF}{a - F} \\approx {b:V}, l = \\abs{a + b} = {l:V}, \\Gamma = {G:.2f}, \\text{{t}}')
class Formula01(variant.VariantTask):
    def GetUpdate(self, *, a=None, F=None, which=None):
        if which == 'собирающей':
            f = F
            if 2 * F.SI_Value < a.SI_Value:
                t = 'действительное, прямое, уменьшенное'
            elif a.SI_Value == 2 * F.SI_Value:
                t = 'действительное, прямое, равное'
            elif F.SI_Value < a.SI_Value < 2 * F.SI_Value:
                t = 'действительное, прямое, увеличенное'
            elif a.SI_Value < F.SI_Value:
                t = 'мнимое, прямое, увеличенное'
            else:
                log.error([
                    a.SI_Value,
                    F.SI_Value,
                    a.SI_Value < F.SI_Value,
                    2 * F.SI_Value < a.SI_Value,
                    F.SI_Value < a.SI_Value < 2 * F.SI_Value,
                    a.SI_Value < F.SI_Value,
                    type(a.SI_Value),
                    type(F.SI_Value)
                ])
                raise RuntimeError(f'Invalid a and F')
        elif which == 'рассеивающей':
            f = F * (-1)
            t = 'мнимое, прямое, уменьшенное'
        else:
            raise RuntimeError(f'Invalid which: {which}')
        b = f.SI_Value * a.SI_Value / (a.SI_Value - f.SI_Value)
        l = abs(a.SI_Value + b)
        return dict(
            b=f'{b * 100:.1f} см',
            l=f'{l * 100:.1f} см',
            D=f'{1 / f.SI_Value:.1f} дптр',
            G=abs(b / a.SI_Value),
            t=t,
        )



@variant.text('''
    Объект находится на расстоянии {a:V:e} от линзы, а его {which} изображение — в {b:V:e} от неё.
    Определите увеличение предмета, фокусное расстояние линзы, оптическую силу линзы и её тип.
''')
@variant.arg(a='115/25/45 см')
@variant.arg(b='10/20/30/40/50 см')
@variant.arg(which='действительное/мнимое')
@variant.answer_short('\\frac 1F = D = \\frac 1a + \\frac 1b, D \\approx{D:V}, F\\approx{F:V}, \\Gamma\\approx{G:.2f},\\text{{t}}')

@variant.solution_space(80)
class Formula02(variant.VariantTask):
    def GetUpdate(self, *, a=None, b=None, which=None):
        aa = a.SI_Value
        if which == 'действительное':
            bb = b.SI_Value
        elif which == 'мнимое':
            bb = -b.SI_Value
        else:
            raise RuntimeError(f'Invalid which: {which}')
        F = aa * bb / (aa + bb)
        if F > 0:
            t = 'собирающая'
        elif F < 0:
            t = 'рассеивающая'
        else:
            raise RuntimeError()

        return dict(
            F=f'{F * 100:.1f} см',
            D=f'{1 / F:.1f} дптр',
            t=t,
            G=abs(bb / aa),
        )


@variant.text('''
    Известно, что из формулы тонкой линзы $\\cbr{\\frac 1F = \\frac 1a + \\frac 1b}$
    и определения увеличения $\\cbr{\\Gamma_y = \\frac ba}$ можно получить выражение
    для увеличения: $\\Gamma_y = \\frac {aF}{a - F} * \\frac 1a = \\frac {F}{a - F}.$
    Назовём такое увеличение «поперечным»: поперёк главной оптической оси (поэтому и ${}_y$).
    Получите формулу для «продольного» увеличения $\\Gamma_x$ небольшого предмета, находящегося на главной оптической оси.
    Можно ли применить эту формулу для предмета, не лежащего на главной оптической оси, почему?
''')
@variant.no_args
@variant.answer_align([
    '\\frac 1F &= \\frac 1a + \\frac 1b \\implies b = \\frac {aF}{a - F}',
    '\\frac 1F &= \\frac 1{a + x} + \\frac 1c \\implies c = \\frac {(a+x)F}{a + x - F}',
    'x\' &= \\abs{b - c} = \\frac {aF}{a - F} - \\frac {(a+x)F}{a + x - F} = '
    'F\\cbr{\\frac {a}{a - F} - \\frac {a+x}{a + x - F}} = ',
    '&= F * \\frac {a^2 + ax - aF - a^2 - ax + aF + xF}{(a - F)(a + x - F)} = '
    'F * \\frac {xF}{(a - F)(a + x - F)}',
    '\\Gamma_x &= \\frac{x\'}x = \\frac{F^2}{(a - F)(a + x - F)} \\to \\frac{F^2}{\\sqr{a - F}}.',
    '\\text{Нельзя: изображение по-разному растянет по осям $x$ и $y$ и понадобится теорема Пифагора}'
])
@variant.solution_space(150)
class Theory06(variant.VariantTask):
    pass


@variant.text('''
    Доказать формулу тонкой линзы для {which} линзы.
''')
@variant.arg(which='рассеивающей/собирающей')
class Theory07(variant.VariantTask):
    pass


@variant.text('''
    Постройте ход луча ${X}{Y}$ в тонкой линзе. Известно положение линзы и оба её фокуса (см. рис. на доске).
    Рассмотрите оба типа линзы, сделав 2 рисунка: собирающую и рассеивающую.
''')
@variant.arg(X='A/B/C')
@variant.arg(Y='K/L/M')
class Theory08(variant.VariantTask):
    pass


@variant.text('''
    (Задача-«гроб»: решать на обратной стороне) Квадрат со стороной {d:Task:e} расположен так,
    что 2 его стороны параллельны главной оптической оси {which} линзы,
    его центр удален на {h:Task:e} от этой оси и на {a:Task:e} от плоскости линзы.
    Определите площадь изображения квадрата, если фокусное расстояние линзы составляет {F:Task:e}.
    % (и сравните с площадью объекта, умноженной на квадрат увеличения центра квадрата).
''')
@variant.arg(d='d = 1/2/3 см')
@variant.arg(h='h = 4/5/6 см')
@variant.arg(a='a = 10/12/15 см')
@variant.arg(F='F = 18/20/25 см')
@variant.arg(which='собирающей/рассеивающей')
@variant.solution_space(80)
@variant.answer_align([
    '&\\text{Все явные вычисления — в см и $\\text{см}^2$,}',
    '\\frac 1 F &= \\frac 1{a + \\frac d2} + \\frac 1b '
        '\\implies b = \\frac 1{\\frac 1 F - \\frac 1{a + \\frac d2}} '
        '= \\frac{F(a + \\frac d2)}{a + \\frac d2 - F} = {b:LaTeX},',

    '\\frac 1 F &= \\frac 1{a - \\frac d2} + \\frac 1c '
        '\\implies c = \\frac 1{\\frac 1 F - \\frac 1{a - \\frac d2}} '
        '= \\frac{F(a - \\frac d2)}{a - \\frac d2 - F} = {c:LaTeX},',

    'c - b '
        '&= \\frac{F(a - \\frac d2)}{a - \\frac d2 - F} - \\frac{F(a + \\frac d2)}{a + \\frac d2 - F} '
        '= F\\cbr{ \\frac{a - \\frac d2}{a - \\frac d2 - F} - \\frac{a + \\frac d2}{a + \\frac d2 - F} } = ',
        '&= F * \\frac{'
            'a^2 + \\frac {ad}2 - aF - \\frac{ad}2 - \\frac{d^2}4 + \\frac{dF}2 '
            '- a^2 + \\frac {ad}2 + aF - \\frac{ad}2 + \\frac{d^2}4 + \\frac{dF}2'
        '}{\\cbr{a + \\frac d2 - F}\\cbr{a - \\frac d2 - F}}'
        '= F * \\frac {dF}{\\cbr{a + \\frac d2 - F}\\cbr{a - \\frac d2 - F}} = {c_m_b:LaTeX}.',

    '\\Gamma_b &= \\frac b{a + \\frac d2} = \\frac{ F }{a + \\frac d2 - F} = {Gb:LaTeX},',
    '\\Gamma_c &= \\frac c{a - \\frac d2} = \\frac{ F }{a - \\frac d2 - F} = {Gc:LaTeX},',

    '&\\text{ тут интересно отметить, что } '
    '\\Gamma_x = \\frac{ c - b}{ d } = \\frac{ F^2 }{\\cbr{a + \\frac d2 - F}\\cbr{a - \\frac d2 - F}} '
    '\\ne \\Gamma_b \\text{ или } \\Gamma_c \\text{ даже при малых $d$}.',

    'S\' '
        '&= \\frac{d * \\Gamma_b + d * \\Gamma_c}2 * (c - b) '
        '= \\frac d2 \\cbr{\\frac{ F }{a + \\frac d2 - F} + \\frac{ F }{a - \\frac d2 - F}} * \\cbr{c - b} = ',
        '&=\\frac {dF}2 \\cbr{\\frac 1{a + \\frac d2 - F} + \\frac 1{a - \\frac d2 - F}} * \\frac {dF^2}{\\cbr{a + \\frac d2 - F}\\cbr{a - \\frac d2 - F}} = ',
        '&=\\frac {dF}2 * \\frac{a - \\frac d2 - F + a + \\frac d2 - F}{\\cbr{a + \\frac d2 - F}\\cbr{a - \\frac d2 - F}} '
        '* \\frac {dF^2}{\\cbr{a + \\frac d2 - F}\\cbr{a - \\frac d2 - F}} = ',
        '&= \\frac {d^2F^3}{2\\sqr{a + \\frac d2 - F}\\sqr{a - \\frac d2 - F}} * (2a - 2F) '
        '= \\frac {d^2F^3(a - F)}{ \\sqr{\\sqr{a - F} - \\frac{d^2}4} } = {S:LaTeX}.',
    # 'S_0 = d^2 * \\Gamma_a^2 = d^2 \\sqr{\\frac{F a}{a - F} * \\frac 1a } = d^2 \\frac{F^2}{ \\sqr{a - F} }.'
])
class Square(variant.VariantTask):
    def GetUpdate(self, *, d=None, h=None, a=None, F=None, which=None):
        df = d.frac_value * 100
        hf = h.frac_value * 100
        af = a.frac_value * 100
        Ff = F.frac_value * 100
        if which == 'рассеивающей':
            Ff = -Ff

        b = Ff * (af + df / 2)/ (af + df / 2 - Ff)
        c = Ff * (af - df / 2)/ (af - df / 2 - Ff)
        Gb = Ff / (af + df / 2 - Ff)
        Gc = Ff / (af - df / 2 - Ff)
        c_m_b = c - b

        S = df**2 * Ff**3 * (af - Ff) / (((af - Ff)**2 - df**2/4) ** 2)

        return dict(
            b=b,
            c=c,
            Gb=Gb,
            Gc=Gc,
            c_m_b=c_m_b,
            S=S,
        )


@variant.text('''
    Найти оптическую силу собирающей линзы, если действительное изображение предмета,
    помещённого в {a:V:e} от линзы, получается на расстоянии {b:V:e} от неё.
''')
@variant.solution_space(180)
@variant.arg(a='a = 15/35/35/55 см')
@variant.arg(b='b = 20/30/40 см')
@variant.answer_short(
    'D = \\frac 1F = \\frac 1a + \\frac 1b = \\frac 1{a:V:s} + \\frac 1{b:V:s} \\approx {D:V}',
)
class Vishnyakova_3_6_6(variant.VariantTask):
    def GetUpdate(self, *, a=None, b=None):
        D_value = 1 / float(a.SI_Value) +  1 / float(b.SI_Value)
        return dict(
            D=f'D = {D_value:.2f} дптр',
        )


@variant.text('''
    Найти увеличение изображения, если изображение предмета, находящегося
    на расстоянии {a:V:e} от линзы, получается на расстоянии {b:V:e} от неё.
''')
@variant.solution_space(180)
@variant.arg(a='a = 15/20/25 см')
@variant.arg(b='b = 12/18/30 см')
@variant.answer_short('{G:L} = \\frac ba = \\frac {b:V:s}{a:V:s} \\approx {G:V}')
class Vishnyakova_3_6_7(variant.VariantTask):
    def GetUpdate(self, *, a=None, b=None):
        return dict(
            G=(b / a).SetLetter('\\Gamma')
        )


@variant.text('''
    Расстояние от предмета до линзы {a:V:e}, а от линзы до мнимого изображения {b:V:e}.
    Чему равно фокусное расстояние линзы?
''')
@variant.solution_space(180)
@variant.arg(a='a = 8/10/12 см')
@variant.arg(b='b = 20/25/30 см')
@variant.answer_short('\\pm \\frac 1F = \\frac 1a - \\frac 1b \\implies {F:L} = \\frac{a b}{\\abs{b - a}} \\approx {F:V}')
class Vishnyakova_3_6_8(variant.VariantTask):
    def GetUpdate(self, *, a=None, b=None):
        a_v = float(a.SI_Value)
        b_v = float(b.SI_Value)
        F_value = abs(a_v * b_v / (b_v - a_v))
        return dict(
            F=f'F = {F_value * 100:.1f} см',
        )


@variant.text('''
    Две тонкие собирающие линзы с фокусными расстояниями {f_1:V:e} и {f_2:V:e} сложены вместе.
    Чему равно фокусное расстояние такой оптической системы?
''')
@variant.solution_space(180)
@variant.arg(f_1='f_1 = 12/18/25 см')
@variant.arg(f_2='f_2 = 20/30 см')
@variant.answer_short(
    '\\frac 1{f_1:L:s} = \\frac 1a + \\frac 1b; '
    '\\frac 1{f_2:L:s} = - \\frac 1b + \\frac 1c \\implies '
    '\\frac 1{f_1:L:s} + \\frac 1{f_2:L:s} = \\frac 1a + \\frac 1c \\implies '
    '{f:L} = \\frac 1{\\frac 1{f_1:L:s} + \\frac 1{f_2:L:s}} = \\frac{{f_1:L} {f_2:L}}{{f_1:L} + {f_2:L}} '
    '\\approx {f:V}'
)
class Vishnyakova_3_6_9(variant.VariantTask):
    def GetUpdate(self, *, f_1=None, f_2=None):
        f1_v = float(f_1.SI_Value)
        f2_v = float(f_2.SI_Value)
        f_v = f1_v * f2_v / (f1_v + f2_v)
        return dict(
            f=f'f\' = {f_v * 100:.1f} см',
        )


@variant.text('''
    Линейные размеры прямого изображения предмета, полученного в собирающей линзе,
    в {n_word} больше линейных размеров предмета.
    Зная, что предмет находится на {l:V:e} ближе к линзе,
    чем его изображение, найти оптическую силу линзы.
''')
@variant.solution_space(180)
@variant.arg(l='\\ell = 20/25/30/35/40 см')
@variant.arg(n__n_word=n_times(2, 3, 4))
@variant.answer_align([
    'D &= \\frac 1F = \\frac 1a + \\frac 1b, \\qquad \\Gamma = \\frac ba, \\qquad b - a = {l:L} \\implies '
    'b = \\Gamma a \\implies {G:L} a - a = {l:L} \\implies ',
    'a &= \\frac {l:L:s}{{G:L} - 1} \\implies '
    'b = \\frac {{l:L:s} {G:L}}{{G:L} - 1} \\implies ',
    'D &= \\frac {{G:L} - 1}{l:L} + \\frac {{G:L} - 1}{{l:L} {G:L}} = \\frac 1{l:L} * \\cbr{{G:L} - 1 + \\frac {{G:L} - 1}{{G:L}} } ='
    '\\frac 1{l:L} * \\cbr{{G:L} - \\frac 1{G:L}} \\approx {D:V}.'
])
class Vishnyakova_3_6_10(variant.VariantTask):
    def GetUpdate(self, *, l=None, n=None, n_word=None):
        D = 1 / float(l.SI_Value) * (n - 1 / n)
        return dict(
            D=f'D = {D:.1f} дптр',
            G='\\Gamma = {n}',
        )


@variant.text('''
    Оптическая сила объектива фотоаппарата равна {D:V:e}.
    При фотографировании чертежа с расстояния {a:V:e} площадь изображения
    чертежа на фотопластинке оказалась равной {S:V:e}.
    Какова площадь самого чертежа? Ответ выразите в квадратных сантиметрах.
''')
@variant.solution_space(180)
@variant.arg(D='D = 3/4/5/6 дптр')
@variant.arg(a='a = 0.8/0.9/1.1/1.2 м')
@variant.arg(S='S = 4/9/16 см^2')
class Vishnyakova_3_6_11(variant.VariantTask):
    pass


@variant.text('''
    В каком месте на главной оптической оси {which} линзы
    нужно поместить точечный источник света,
    чтобы его изображение оказалось в главном фокусе линзы?
''')
@variant.arg(which='двояковыпуклой/двояковыгнутой')
@variant.answer_short('\\text{{answer}}')
class Baumanski_15_31(variant.VariantTask):
    def GetUpdate(self, *, which=None):
        answer = {
            'двояковыпуклой': 'для мнимого - на половине фокусного, для действительного - на бесконечности',
            'двояковыгнутой': 'на половине фокусного расстояния',
        }[which]
        return dict(
            answer=answer,
        )


@variant.text('''
    Предмет высотой {h:Task:e} находится на расстоянии {d:Task:e}
    от вертикально расположенной рассеивающей линзы с фокусным расстоянием {F:Task:e}.
    Где находится изображение предмета? Определите тип изображения и его высоту.
''')
@variant.arg(h='h = 30/40/50 см')
@variant.arg(d='d = 0.8/1.0/1.2 м')
@variant.arg(F='F = -15/20/25 см')
# @variant.answer_short('')
class Baumanski_15_32(variant.VariantTask):
    def GetUpdate(self, *, h=None, d=None, F=None):
        return dict(
        )


@variant.text('''
    На каком расстоянии от двояковыпуклой линзы с оптической силой {D:Task:e}
    надо поместить предмет, чтобы его изображение получилось на расстоянии {f:V:e} от линзы?
''')
@variant.arg(D='D = 1.5/2/2.5 дптр')
@variant.arg(f='f = 1.5/2/2.5 м')
# @variant.answer_short('')
class Baumanski_15_33(variant.VariantTask):
    def GetUpdate(self, *, D=None, f=None):
        return dict(
        )


@variant.text('''
    На экране, расположенном на расстоянии {b:V:e} от собирающей линзы,
    получено изображение точечного источника, расположенного на главной оптической оси линзы.
    На какое расстояние переместится изображение на экране,
    если {how} на {x:V:e} в плоскости, перпендикулярной главной оптической оси?
    Фокусное расстояние линзы равно {F:V:e}.
''')
@variant.arg(b='60/80/120 см')
@variant.arg(x='1/2/3 см')
@variant.arg(F='20/30/40 см')
@variant.arg(how=[
    'при неподвижном источнике переместить линзу',
    'при неподвижной линзе переместить источник',
])
@variant.answer_align([
    '\\frac 1F = \\frac 1a + \\frac 1b \\implies a = \\frac{bF}{b-F} \\implies \\Gamma = \\frac ba = \\frac{b-F}F',
    'y = x * \\Gamma = x * \\frac{b-F}F \\implies d = {what} = {d:V}.',
])
class Baumanski_15_34(variant.VariantTask):
    def GetUpdate(self, *, b=None, x=None, F=None, how=None):
        G = (b / F).SI_Value - 1
        if how == 'при неподвижном источнике переместить линзу':
            what = 'x + y'
            d = x * (G + 1)
        elif how == 'при неподвижной линзе переместить источник':
            what = 'y'
            d = x * G
        else:
            raise RuntimeError(f'Invalid how: {how}')

        return dict(
            d=d.As('см').IncPrecision(1),
            what=what,
        )


@variant.text('''
    Оптическая сила двояковыпуклой линзы в воздухе {D1:V:e}, а в воде {D2:V:e}.
    Определить показатель преломления $n$ материала, из которого изготовлена линза.
    Показатель преломления воды равен ${n2:.2f}$.
''')
@variant.arg(D1='4.5/5/5.5 дптр')
@variant.arg(D2='1.4/1.5/1.6 дптр')
@variant.answer_align([
    'D_1 &=\\cbr{\\frac n{n_1} - 1}\\cbr{\\frac 1{R_1} + \\frac 1{R_2}},',
    'D_2 &=\\cbr{\\frac n{n_2} - 1}\\cbr{\\frac 1{R_1} + \\frac 1{R_2}},',
    '\\frac {D_2}{D_1} &=\\frac{\\frac n{n_2} - 1}{\\frac n{n_1} - 1}'
    ' \\implies {D_2}\\cbr{\\frac n{n_1} - 1} = {D_1}\\cbr{\\frac n{n_2} - 1} '
    ' \\implies n\\cbr{\\frac{D_2}{n_1} - \\frac{D_1}{n_2}} = D_2 - D_1,',
    'n &= \\frac{D_2 - D_1}{\\frac{D_2}{n_1} - \\frac{D_1}{n_2}} = \\frac{n_1 n_2 (D_2 - D_1)}{D_2n_2 - D_1n_1} \\approx {n:.3f}.',
])
class Baumanski_15_35(variant.VariantTask):
    def GetUpdate(self, *, D1=None, D2=None):
        n1 = 1
        n2 = 1.33
        d1 = float(D1.SI_Value)
        d2 = float(D2.SI_Value)
        return dict(
            n = n1 * n2 * (d2 - d1) / (d2 * n2 - d1 * n1),
            n2=n2,
        )


@variant.text('''
    На каком расстоянии от собирающей линзы с фокусным расстоянием {F:V:e}
    следует надо поместить предмет, чтобы расстояние
    от предмета до его действительного изображения было наименьшим?
''')
@variant.arg(F='30/40/50 дптр')
@variant.answer_align([
    '\\frac 1a &+ \\frac 1b = D \\implies b = \\frac 1{D - \\frac 1a} '
    '\\implies \\ell = a + b = a + \\frac a{Da - 1} = \\frac{ Da^2 }{Da - 1} \\implies',
    '\\implies \\ell\'_a &= \\frac{ 2Da * (Da - 1) - Da^2 * D }{\\sqr{Da - 1}}'
    '= \\frac{ D^2a^2 - 2Da}{\\sqr{Da - 1}} = \\frac{ Da(Da - 2)}{\\sqr{Da - 1}}'
    '\\implies a_{\\min} = \\frac 2D \\approx {a:V}.'
])
class Baumanski_15_36(variant.VariantTask):
    def GetUpdate(self, *, F=None):
        a = 2 / F.SI_Value
        return dict(
            a=f'{a * 1000:.1f} мм',
        )


@variant.text('''
    Предмет в виде отрезка длиной $\\ell$ расположен вдоль оптической оси
    собирающей линзы с фокусным расстоянием $F$. Середина отрезка расположена
    на расстоянии $a$ от линзы, которая даёт действительное изображение
    всех точек предмета. Определить продольное увеличение предмета.
''')
@variant.no_args
@variant.answer_align([
    '\\frac 1{a + \\frac \\ell 2} &+ \\frac 1b = \\frac 1F \\implies b = \\frac{F\\cbr{a + \\frac \\ell 2}}{a + \\frac \\ell 2 - F}',
    '\\frac 1{a - \\frac \\ell 2} &+ \\frac 1c = \\frac 1F \\implies c = \\frac{F\\cbr{a - \\frac \\ell 2}}{a - \\frac \\ell 2 - F}',
    '\\abs{b - c} &'
        '= \\abs{\\frac{F\\cbr{a + \\frac \\ell 2}}{a + \\frac \\ell 2 - F} - \\frac{F\\cbr{a - \\frac \\ell 2}}{a - \\frac \\ell 2 - F}}'
        '= F\\abs{\\frac{\\cbr{a + \\frac \\ell 2}\\cbr{a - \\frac \\ell 2 - F} - \\cbr{a - \\frac \\ell 2}\\cbr{a + \\frac \\ell 2 - F}}{ \\cbr{a + \\frac \\ell 2 - F} \\cbr{a - \\frac \\ell 2 - F} }} = ',
    '&= F\\abs{\\frac{'
            'a^2 - \\frac {a\\ell} 2 - Fa + \\frac {a\\ell} 2 - \\frac {\\ell^2} 4 - \\frac {F\\ell}2'
            ' - a^2 - \\frac {a\\ell}2 + aF + \\frac {a\\ell}2 + \\frac {\\ell^2} 4 - \\frac {F\\ell} 2'
        '}{'
            '\\cbr{a + \\frac \\ell 2 - F} \\cbr{a - \\frac \\ell 2 - F} '
        '}} =',
    '&= F\\frac{F\\ell}{\\sqr{a-F} - \\frac {\\ell^2}4} = \\frac{F^2\\ell}{\\sqr{a-F} - \\frac {\\ell^2}4}'
    '\\implies \\Gamma = \\frac{\\abs{b - c}}\\ell = \\frac{F^2}{\\sqr{a-F} - \\frac {\\ell^2}4}.',
])
class Baumanski_15_37(variant.VariantTask):
    def GetUpdate(self, *, F=None):
        return dict(
        )


@variant.text('''
    Даны точечный источник света $S$, его изображение $S_1$, полученное с помощью собирающей линзы,
    и ближайший к источнику фокус линзы $F$ (см. рис. на доске). Расстояния $SF = \\ell$ и $SS_1 = L$.
    Определить положение линзы и её фокусное расстояние.
''')
@variant.no_args
@variant.answer_align([
    '\\frac 1a + \\frac 1b &= \\frac 1F, \\ell = a - F, L = a + b \\implies a = \\ell + F, b = L - a = L - \\ell - F',
    '\\frac 1{\\ell + F} + \\frac 1{L - \\ell - F} &= \\frac 1F',
    'F\\ell + F^2 + LF - F\\ell - F^2 &= L\\ell - \\ell^2 - F\\ell + LF - F\\ell - F^2',
    '0 &= L\\ell - \\ell^2 - 2F\\ell - F^2',
    '0 &=  F^2 + 2F\\ell - L\\ell + \\ell^2',
    'F &= -\\ell \\pm \\sqrt{\\ell^2 +  L\\ell - \\ell^2} = -\\ell \\pm \\sqrt{L\\ell} \\implies F = \\sqrt{L\\ell} - \\ell',
    'a &= \\ell + F = \\ell + \\sqrt{L\\ell} - \\ell = \\sqrt{L\\ell}.',
])
class Baumanski_15_38(variant.VariantTask):
    def GetUpdate(self, *, F=None):
        return dict(
        )


@variant.text('''
    Расстояние от освещённого предмета до экрана {L:V:e}.
    Линза, помещенная между ними, даёт чёткое изображение предмета на
    экране при двух положениях, расстояние между которыми {l:V:e}.
    Найти фокусное расстояние линзы.
''')
@variant.arg(L='L = 80/100 см')
@variant.arg(l='\\ell = 20/30/40 см')
@variant.answer_align([
    '\\frac 1a + \\frac 1b &= \\frac 1F, \\frac 1{a-{l:L}} + \\frac 1{b+{l:L}} = \\frac 1F, a + b = L',
    '\\frac 1a + \\frac 1b &= \\frac 1{a-{l:L}} + \\frac 1{b+{l:L}}'
    '\\implies \\frac{a + b}{ab} = \\frac{(a-{l:L}) + (b+{l:L})}{(a-{l:L})(b+{l:L})}',
    'ab  &= (a - {l:L})(b+{l:L}) \\implies 0  = -b{l:L} + a{l:L} - {l:L}^2 \\implies 0 = -b + a - {l:L} \\implies b = a - {l:L}',
    'a + (a - {l:L}) &= L \\implies a = \\frac{L + {l:L}}2 \\implies b = \\frac{L - {l:L}}2',
    'F &= \\frac{ab}{a + b} = \\frac{L^2 -{l:L}^2}{4L} \\approx {F:V}.',
])
class Baumanski_15_39(variant.VariantTask):
    def GetUpdate(self, *, L=None, l=None):
        F = (L.SI_Value ** 2 - l.SI_Value ** 2) / 4 / L.SI_Value
        return dict(
            F=f'F = {F * 100:.1f} см',
        )


@variant.text('''
    Предмет находится на расстоянии {L:V:e} от экрана.
    Между предметом и экраном помещают линзу, причём при одном
    положении линзы на экране получается увеличенное изображение предмета,
    а при другом — уменьшенное. Каково фокусное расстояние линзы, если
    линейные размеры первого изображения в {n_word} больше второго?
''')
@variant.arg(L='L = 60/70/80/90 см')
@variant.arg(n__n_word=n_times(2, 3, 5))
@variant.answer_align([
    '\\frac 1a + \\frac 1{L-a} &= \\frac 1F, h_1 = h * \\frac{L-a}a,',
    '\\frac 1b + \\frac 1{L-b} &= \\frac 1F, h_2 = h * \\frac{L-b}b,',
    '\\frac{h_1}{h_2} &= {n} \\implies \\frac{(L-a)b}{(L-b)a} = {n},',
    '\\frac 1F &= \\frac{ L }{a(L-a)} = \\frac{ L }{b(L-b)} \\implies \\frac{L-a}{L-b} = \\frac b a \\implies \\frac {b^2}{a^2} = {n}.',
    '\\frac 1a + \\frac 1{L-a} &= \\frac 1b + \\frac 1{L-b} \\implies \\frac L{a(L-a)} = \\frac L{b(L-b)} \\implies',
    '\\implies aL - a^2 &= bL - b^2 \\implies (a-b)L = (a-b)(a+b) \\implies b = L - a,',
    '\\frac{\\sqr{L-a}}{a^2} &= {n} \\implies \\frac La - 1 = \\sqrt{{n}} \\implies a = \\frac{ L }{\\sqrt{{n}} + 1}',
    'F &= \\frac{a(L-a)}L = \\frac 1L * \\frac L{\\sqrt{{n}} + 1} * \\frac {L\\sqrt{{n}}}{\\sqrt{{n}} + 1}'
    '= \\frac { L\\sqrt{{n}} }{ \\sqr{\\sqrt{{n}} + 1} } \\approx {F:V}.',
])
class Baumanski_15_40(variant.VariantTask):
    def GetUpdate(self, *, L=None, n=None, n_word=None):
        s = n ** 0.5
        return dict(
            F=(L * s / ((s + 1) ** 2)).As('см'),
        )


@variant.text('''
    На экране с помощью тонкой линзы получено изображение предмета
    с увеличением {G1:V:e}. Предмет передвинули на {d:V:e}.
    Для того, чтобы получить резкое изображение, пришлось передвинуть экран.
    При этом увеличение оказалось равным {G2:V:e}. На какое расстояние
    пришлось передвинуть экран?
''')
@variant.arg(d='d = 2/4/6/8/10 см')
@variant.arg(G1='\\Gamma_1 = 2/4')
@variant.arg(G2='\\Gamma_2 = 6/8')
# @variant.answer_short('')
class Baumanski_15_41(variant.VariantTask):
    def GetUpdate(self, *, d=None, G1=None, G2=None):
        return dict(
        )


@variant.text('''
    Тонкая собирающая линза дает изображение предмета на экране высотой $H_1$,
    и $H_2$, при двух положениях линзы между предметом и экраном.
    Расстояние между ними неизменно. Чему равна высота предмета $h$?
''')
@variant.no_args
@variant.answer_short('h = \\sqrt{H_1 H_2}')
class Baumanski_15_42(variant.VariantTask):
    pass


@variant.text('''
    Какие предметы можно рассмотреть на фотографии, сделанной со спутника,
    если разрешающая способность пленки {d:V:e}? Каким должно быть
    время экспозиции $\\tau$ чтобы полностью использовать возможности пленки?
    Фокусное расстояние объектива используемого фотоаппарата {F:V:e},
    высота орбиты спутника {H:V:e}.
''')
@variant.arg(F='F = 10/15/20 cм')
@variant.arg(d='\\delta = 0.01/0.02 мм')
@variant.arg(H='H = 80/100/120/150 км')
# @variant.answer_short('')
class Baumanski_15_43(variant.VariantTask):
    def GetUpdate(self, *, F=None, d=None, H=None):
        return dict(
        )


@variant.text('''
    При аэрофотосъемках используется фотоаппарат, объектив которого
    имеет фокусиое расстояние {F:V:e}. Разрешающая способность пленки {d:V:e}.
    На какой высоте должен лететь самолет, чтобы на фотографии можно
    было различить листья деревьев размером {l:V:e}?
    При какой скорости самолета изображение не будет размытым,
    если время зкспозиции {t:V:e}?
''')
@variant.arg(F='F = 8/10/12 cм')
@variant.arg(l='\\ell = 4/5/6 cм')
@variant.arg(t='\\tau = 1/2 мс')
@variant.arg(d='\\delta = 0.01/0.015/0.02 мм')
# @variant.answer_short('')
class Baumanski_15_44(variant.VariantTask):
    def GetUpdate(self, *, F=None, l=None, t=None, d=None):
        return dict(
        )


# ход лучей


@variant.text('''
    На собирающую линзу с фокусным расстоянием {F1:V:e} падает пучок света,
    параллельный её главной оптической оси. На каком расстоянии
    от этой линзы нужно поставить рассеивающую линзу с фокусным расстоянием {F2:V:e},
    чтобы пучок, пройдя обе линзы, остался параллельным?
''')
@variant.arg(F1='17 см')
@variant.arg(F2='0.09 м')
@variant.answer_short('')
class Chernoutsan_13_24(variant.VariantTask):
    def GetUpdate(self, *, F1=None, F2=None):
        return dict(
        )


@variant.text('''
    На рассеивающую линзу с фокусным расстоянием {F:V:e} падает
    цилиндрический пучок лучей, параллельных главной оптической оси.
    За линзой на расстоянии {l:V:e} от неё установлен экран,
    на котором получается круглое светлое пятно диаметром {D:V:e}.
    Определите диаметр пучка лучей.
''')
@variant.arg(F='10 см')
@variant.arg(l='26 см')
@variant.arg(D='15 см')
@variant.answer_short('')
class Chernoutsan_13_25(variant.VariantTask):
    def GetUpdate(self, *, F=None, l=None, D=None):
        return dict(
        )


@variant.text('''
    На собирающую линзу падает цилиндрический пучок лучей диаметром {D:V:e},
    параллельных главной оптической оси. Ось симметрии пучка проходит
    через оптический центр линзы. Когда за линзой установили экран
    один раз на расстоянии {d:V:e}‚ а другой раз на расстоянии {f:V:e}
    от линзы, диаметр светлого пятна на экране получился одинаковым.
    Чему равен этот диаметр?
''')
@variant.arg(D='15 мм')
@variant.arg(d='8 см')
@variant.arg(f='12 см')
@variant.answer_short('')
class Chernoutsan_13_26(variant.VariantTask):
    def GetUpdate(self, *, D=None, d=None, f=None):
        return dict(
        )


@variant.text('''
    Точечный источник света помещен в фокусе собирающей линзы
    с фокусным расстоянием {F:V:e}. За линзой на расстоянии {f:V:e}
    от неё расположен плоский экран, на котором видно круглое светлое пятно.
    На какое расстояние от фокуса линзы надо переместить вдоль оптической оси
    источник света, чтобы радиус светлого пятна на экране увеличился в {n_word}?
''')
@variant.arg(F='6 см')
@variant.arg(f='12 см')
@variant.arg(n__n_word=n_times(2, 3, 4))
@variant.answer_short('')
class Chernoutsan_13_27(variant.VariantTask):
    def GetUpdate(self, *, F=None, f=None, n=None, n_word=None):
        return dict(
        )


# формула линзы
@variant.text('''
    Предмет находится на расстоянии {a:V:e} от собирающей линзы
    с фокусным расстоянием {F:V:e}. Найдите расстояние от изображения до линзы.
''')
@variant.arg(a='12 см')
@variant.arg(F='15 мм')
@variant.answer_short('')
class Chernoutsan_13_28(variant.VariantTask):
    def GetUpdate(self, *, a=None, F=None):
        return dict(
        )


@variant.text('''
    Фокусное расстояние собирающей линзы {F:V:e}. Найдите расстояние (в см)
    от предмета до переднего фокуса линзы, если экран, на котором получается
    чёткое изображение предмета, расположен на расстоянии {c:V:e} от заднего фокуса линзы.
''')
@variant.arg(F='20 см')
@variant.arg(c='40 см')
@variant.answer_short('')
class Chernoutsan_13_29(variant.VariantTask):
    def GetUpdate(self, *, F=None, c=None):
        return dict(
        )


@variant.text('''
    Расстояние от предмета до собирающей линзы в {n_word} больше фокусного.
    Во сколько раз больше фокусного расстояние от изображения до линзы?
''')
@variant.arg(n__n_word=n_times(2, 3, 4))
@variant.answer_short('')
class Chernoutsan_13_30(variant.VariantTask):
    def GetUpdate(self, *, n=None, n_word=None):
        return dict(
        )


@variant.text('''
    Предмет находится на расстоянии {a:V:e} от собирающей линзы с оптической силой {D:V:e}.
    На каком расстоянии от линзы находится изображение предмета?
''')
@variant.arg(a='8 см')
@variant.arg(D='10 дптр')
@variant.answer_short('')
class Chernoutsan_13_31(variant.VariantTask):
    def GetUpdate(self, *, a=None, D=None):
        return dict(
        )


@variant.text('''
    Собирающая линза с фокусным расстоянием {F:V:e} формирует мнимое изображение
    на расстоянии {b:V:e} от линзы. На каком расстоянии от этого изображения
    находится предмет?
''')
@variant.arg(F='10 см')
@variant.arg(b='15 см')
@variant.answer_short('')
class Chernoutsan_13_32(variant.VariantTask):
    def GetUpdate(self, *, F=None, b=None):
        return dict(
        )


@variant.text('''
    Расстояние от предмета до рассеивающей линзы с фокусным расстоянием {F:V:e} равно {a:V:e}.
    Найдите расстояние от изображения до предмета.
''')
@variant.arg(F='4 см')
@variant.arg(a='12 см')
@variant.answer_short('')
class Chernoutsan_13_33(variant.VariantTask):
    def GetUpdate(self, *, F=None, a=None):
        return dict(
        )


@variant.text('''
    Мнимое изображение предмета в рассеивающей линзе находится от неё
    на расстоянии в {n_word} меньшем, чем расстояние от линзы до предмета.
    Найдите расстояние от линзы до изображения, если фокусное расстояние линзы {F:V:e}.
''')
@variant.arg(F='40/50/60 см')
@variant.arg(n__n_word=n_times(2, 3, 4))
@variant.answer_short('')
class Chernoutsan_13_34(variant.VariantTask):
    def GetUpdate(self, *, F=None, n=None, n_word=None):
        return dict(
        )


@variant.text('''
    Действительное изображение предмета, полученное с помощью собирающей линзы,
    находится от неё на расстоянии {l:V:e}. Если собирающую линзу заменить рассеивающей
    с таким же по величине фокусным расстоянием, мнимое изображение этого предмета
    будет отстоять от линзы на {b:V:e}. Найдите абсолютную величину фокусного расстояния линз.
''')
@variant.arg(l='8 см')
@variant.arg(b='2 см')
@variant.answer_short('')
class Chernoutsan_13_35(variant.VariantTask):
    def GetUpdate(self, *, l=None, b=None):
        return dict(
        )


@variant.text('''
    Точечный источник света находится на расстоянии {a:V:e} от собирающей линзы
    с фокусным расстоянием {f:V:e}. За линзой на расстоянии {l:V:e} установлено
    плоское зеркало, перпендикулярное главной оптической оси линзы.
    На каком расстоянии от линзы находится изображение, образованное лучами,
    прошедшими через линзу после отражения от зеркала?
''')
@variant.arg(a='12 см')
@variant.arg(f='10 см')
@variant.arg(l='10 см')
@variant.answer_short('')
class Chernoutsan_13_36(variant.VariantTask):
    def GetUpdate(self, *, a=None, f=None, l=None):
        return dict(
        )


@variant.text('''
    Точечный источник света находится
    на расстоянии {a:V:e} от собирающей линзы с фокусным расстоянием {F1:V:e}.
    За ней на расстоянии, {l:V:e} находится рассеивающая линза с фокусным расстоянием {F2:V:e}.
    На каком расстоянии от этой линзы находится изображение источника,
    сформированное системой линз?
''')
@variant.arg(a='8 cм')
@variant.arg(F1='6 cм')
@variant.arg(l='15 cм')
@variant.arg(F2='12 cм')
@variant.answer_short('')
class Chernoutsan_13_37(variant.VariantTask):
    def GetUpdate(self, *, a=None, F1=None, l=None, F2=None):
        return dict(
        )


@variant.text('''
    Светящаяся точка находится на расстоянии {a:V:e} от собирающей линзы
    с фокусным расстоянием {F:V:e}. На какое расстояние (в мм) сместится
    изображение точки, если между ней и линзой поставить
    стеклянную плоскопараллельную пластину? Пластина установлена
    перпендикулярно оптической оси линзы, толщина пластины {h:V:e},
    показатель преломления стекла {n:V:e}.
''')
@variant.arg(a='6 см')
@variant.arg(F='5 см')
@variant.arg(h='4.5 см')
@variant.arg(n='1.4/1.5/1.6')
@variant.answer_short('')
class Chernoutsan_13_38(variant.VariantTask):
    def GetUpdate(self, *, a=None, F=None, h=None, n=None):
        return dict(
        )


# увеличение линзы

@variant.text('''
    Фокусное расстояние объектива проекционного фонаря {F:V:e}.
    Какое увеличение диапозитива дает фонарь, если экран удален
    от объектива на расстояние {l:V:e}?
''')
@variant.arg(F='25 см')
@variant.arg(l='200 см')
@variant.answer_short('')
class Chernoutsan_13_39(variant.VariantTask):
    def GetUpdate(self, *, F=None, l=None):
        return dict(
        )


@variant.text('''
    Высота изображения человека ростом {h:V:e} на фотопленке {d:V:e}.
    Найдите оптическую силу (в диоптриях) объектива фотоаппарата,
    если человек сфотографирован с расстояния {l:V:e}.
''')
@variant.arg(h='160 см')
@variant.arg(d='2 см')
@variant.arg(l='9 м')
@variant.answer_short('')
class Chernoutsan_13_40(variant.VariantTask):
    def GetUpdate(self, *, h=None, d=None, l=None):
        return dict(
        )


@variant.text('''
    На каком расстоянии от собирающей линзы с фокусным расстоянием {F:V:e}
    следует поместить предмет, чтобы получить действительное изображение, увеличенное в {n_word}?
''')
@variant.arg(F='30 см')
@variant.arg(n__n_word=n_times(2, 3, 4))
@variant.answer_short('')
class Chernoutsan_13_41(variant.VariantTask):
    def GetUpdate(self, *, F=None, n=None, n_word=None):
        return dict(
        )


@variant.text('''
    Расстояние от предмета до собирающей линзы составляет {n:.2f}
    от фокусного расстояния. Найдите увеличение линзы.
''')
@variant.arg(n=[1.25, 1.35, 1.45, 1.55, 1.65, 1.75])
@variant.answer_short('')
class Chernoutsan_13_42(variant.VariantTask):
    def GetUpdate(self, *, n=None):
        return dict(
        )


@variant.text('''
    Изображение предмета, помещенного перед собирающей линзой на расстоянии {a:V:e},
    получено по другую сторону линзы в натуральную величину.
    Во сколько раз увеличится размер изображения, если предмет передвинуть в сторону линзы на {x:V:e}?
''')
@variant.arg(a='60 см')
@variant.arg(x='20 см')
@variant.answer_short('')
class Chernoutsan_13_43(variant.VariantTask):
    def GetUpdate(self, *, a=None, x=None):
        return dict(
        )


@variant.text('''
    Предмет расположен на расстоянии {a:V:e} перед собирающей линзой,
    с помощью которой получено увеличенное в {n_word} мнимое изображение предмета.
    Определите оптическую силу линзы в диоптриях.
''')
@variant.arg(a='0.2 м')
@variant.arg(n__n_word=n_times(3, 4, 5, 6))
@variant.answer_short('')
class Chernoutsan_13_44(variant.VariantTask):
    def GetUpdate(self, *, a=None, n=None, n_word=None):
        return dict(
        )


@variant.text('''
    Мнимое изображение предмета, полученное собирающей линзой,
    в {n_word} дальше от линзы, чем её фокус. Определите увеличение линзы.
''')
@variant.arg(n__n_word=n_times(3, 4, 5, 6))
@variant.answer_short('')
class Chernoutsan_13_45(variant.VariantTask):
    def GetUpdate(self, *, n=None, n_word=None):
        return dict(
        )


@variant.text('''
    Расстояние между предметом и его увеличенным в {n_word} действительным изображением {l:V:e}.
    Найдите фокусное расстояние линзы.
''')
@variant.arg(l='80 см')
@variant.arg(n__n_word=n_times(3, 4, 5, 6))
@variant.answer_short('')
class Chernoutsan_13_46(variant.VariantTask):
    def GetUpdate(self, *, l=None, n=None, n_word=None):
        return dict(
        )


@variant.text('''
    Расстояние между предметом и его увеличенным в {n_word} мнимым изображением {l:V:e}.
    Найдите расстояние от предмета до линзы.
''')
@variant.arg(l='80 см')
@variant.arg(n__n_word=n_times(3, 4, 5, 6))
@variant.answer_short('')
class Chernoutsan_13_47(variant.VariantTask):
    def GetUpdate(self, *, l=None, n=None, n_word=None):
        return dict(
        )


@variant.text('''
    Рассеивающая линза с фокусным расстоянием {F:V:e} уменьшает предмет в {n_word}.
    Найдите расстояние от предмета до линзы.
''')
@variant.arg(F='8 см')
@variant.arg(n__n_word=n_times(2, 3, 4, 5))
@variant.answer_short('')
class Chernoutsan_13_48(variant.VariantTask):
    def GetUpdate(self, *, F=None, n=None, n_word=None):
        return dict(
        )


@variant.text('''
    Линза с фокусным расстоянием {F:V:e} формирует уменьшенное в {n_word}
    действительное изображение предмета. Другая линза, помещенная на место первой,
    формирует его увеличенное в 3 раза действительное изображение.
    Найдите фокусное расстояние второй линзы.
''')
@variant.arg(F='12 см')
@variant.arg(n__n_word=n_times(2, 3, 4, 5))
@variant.answer_short('')
class Chernoutsan_13_49(variant.VariantTask):
    def GetUpdate(self, *, F=None, n=None, n_word=None):
        return dict(
        )


@variant.text('''
    Линза с фокусным расстоянием {F:V:e} формирует увеличенное в {n_word}
    действительное изображение предмета. Каким должно быть фокусное расстояние (в см)
    другой линзы, чтобы, поместив её на место первой, мы получили увеличенное в 5 раз
    мнимое изображение?
''')
@variant.arg(F='8 см')
@variant.arg(n__n_word=n_times(3, 4, 5, 6))
@variant.answer_short('')
class Chernoutsan_13_50(variant.VariantTask):
    def GetUpdate(self, *, F=None, n=None, n_word=None):
        return dict(
        )


@variant.text('''
    Собирающая линза дает изображение некоторого предмета на экране.
    Высота изображения {h1:V:e}. Оставляя неподвижным экран и предмет,
    линзу передвинули к экрану и получили второе чёткое изображение высотой {h2:V:e}.
    Найдите высоту предмета.
''')
@variant.arg(h1='9 см')
@variant.arg(h2='4 см')
@variant.answer_short('')
class Chernoutsan_13_51(variant.VariantTask):
    def GetUpdate(self, *, h1=None, h2=None):
        return dict(
        )


@variant.text('''
    Тонкий стержень расположен вдоль главной оптической оси собирающей линзы.
    Каково продольное увеличение стержня, если объект, расположенный у одного конца стержня,
    изображается с увеличением {G1}, а у другого конца — с увеличением {G2:.1f}?
    Оба конца стержня располагаются от линзы на расстоянии больше фокусного.
''')
@variant.arg(G1=[4, 5, 6])
@variant.arg(G2=[2.5, 3.0, 3.5])
@variant.answer_short('')
class Chernoutsan_13_52(variant.VariantTask):
    def GetUpdate(self, *, G1=None, G2=None):
        return dict(
        )


@variant.text('''
    Точечный источник, находящийся на главной оптической оси собирающей линзы
    на расстоянии от неё, в {n_word} большем фокусного, начинает смещаться
    со скоростью {v:V:e} перпендикулярно оси. С какой скоростью
    движется изображение источника?
''')
@variant.arg(v='4 мм/с')
@variant.arg(n__n_word=n_times(2, 3))
@variant.answer_short('')
class Chernoutsan_13_53(variant.VariantTask):
    def GetUpdate(self, *, v=None, n=None, n_word=None):
        return dict(
        )


@variant.text('''
    Точечный источник находится на главной оптической оси собирающей линзы
    с фокусным расстоянием {F:V:e} на расстоянии {a:V:e} от линзы.
    Линзу начинают смещать со скоростью {v:V:e} в направлении,
    перпендикулярном оптической оси. С какой скоростью движется изображение источника?
''')
@variant.arg(F='6 см')
@variant.arg(a='8 см')
@variant.arg(v='3 мм/с')
@variant.answer_short('')
class Chernoutsan_13_54(variant.VariantTask):
    def GetUpdate(self, *, F=None, a=None, v=None):
        return dict(
        )


@variant.text('''
    Точечный источник движется со скоростью {v:V:e} вдоль
    главной оптической оси собирающей линзы с фокусным расстоянием {F:V:e}.
    С какой скоростью движется изображение источника в тот момент,
    когда источник находится от линзы на расстоянии {a:V:e}?
''')
@variant.arg(v='2 мм/с')
@variant.arg(F='8 см')
@variant.arg(a='10 см')
@variant.answer_short('')
class Chernoutsan_13_55(variant.VariantTask):
    def GetUpdate(self, *, v=None, F=None, a=None):
        return dict(
        )
