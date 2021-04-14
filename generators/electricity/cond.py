import generators.variant as variant
from generators.helpers import Fraction, n_times, letter_variants


@variant.solution_space(40)
@variant.text('''
    Напротив физических величин укажите их обозначения и единицы измерения в СИ:
    \\begin{{enumerate}}
        \\item ёмкость конденсатора,
        \\item индуктивность катушки.
    \\end{{enumerate}}
''')
@variant.no_args
class Definitions01(variant.VariantTask):
    pass


@variant.solution_space(40)
@variant.text('''
    Запишите формулы, выражающие:
    \\begin{{enumerate}}
        \\item заряд конденсатора через его ёмкость и поданное напряжение,
        \\item энергию конденсатора через {v_1},
        \\item {v_2} колебаний в электромагнитном контуре, состоящем из конденсатора и катушки индуктивности,
    \\end{{enumerate}}
''')
@variant.arg(v_1=['его ёмкость и поданное напряжение', 'его ёмкость и заряд', 'его заряд и поданное напряжение'])
@variant.arg(v_2=['период', 'частоту'])
class Definitions02(variant.VariantTask):
    pass



@variant.solution_space(40)
@variant.text('''
    Установите соответствие и запишите в ответ набор цифр (без других символов).

    {lv.Questions}.

    {lv.Options}.
''')
@variant.arg(lv=letter_variants(
    {
        'электроёмкость': 'фарад',
        'напряжённость электрического поля': 'Н / Кл',
        'энергия заряженного конденсатора': 'джоуль',
        'электрический заряд': 'кулон',
        'разность потенциалов': 'вольт',
    },
    ['генри', 'ватт', 'ампер'],
    answers_count=3,
    mocks_count=2,
))
class Definitions03(variant.VariantTask):
    pass



@variant.text('''
    Определите ёмкость конденсатора, если при его зарядке до напряжения
    {U:Task:e} он приобретает заряд {Q:Task:e}.
    Чему при этом равны заряды обкладок конденсатора (сделайте рисунок и укажите их)?
''')
@variant.answer_short('''
    {Q:L} = {C:L}{U:L} \\implies
    {C:L} = \\frac{Q:L:s}{U:L:s} = \\frac{Q:Value:s}{U:Value:s} = {C:Value}.
    \\text{ Заряды обкладок: ${Q:L}$ и $-{Q:L}$ }
''')
@variant.arg(U=['%s = %d кВ' % (Ul, Uv) for Ul in ['U', 'V'] for Uv in [2, 3, 5, 6, 12, 15, 20]])
@variant.arg(Q=['%s = %d нКл' % (ql, qv) for ql in ['Q', 'q'] for qv in [4, 6, 15, 18, 24, 25]])
class Rymkevich748(variant.VariantTask):
    def GetUpdate(self, U=None, Q=None, **kws):
        return dict(
            C='C = %.2f пФ' % (1. * Q.Value / U.Value)
        )


@variant.solution_space(80)
@variant.text('''
    На конденсаторе указано: {C:Task:e}, {U:Task:e}.
    Удастся ли его использовать для накопления заряда {Q:Task:e}?
''')
@variant.answer_short('''
    {Q_max:L} = {C:L}{U:L} = {C:Value} * {U:Value} = {Q_max:Value}
    \\implies {Q_max:L} {sign} {Q:L} \\implies \\text{ {result} }
''')
@variant.answer_test('{short}')
@variant.arg(U=['%s = %d В' % (Ul, Uv) for Ul in ['U', 'V'] for Uv in [200, 300, 400, 450]])
@variant.arg(Q=['%s = %d нКл' % (Ql, Qv) for Ql in ['Q', 'q'] for Qv in [30, 50, 60]])
@variant.arg(C=['C = %d пФ' % Cv for Cv in [50, 80, 100, 120, 150]])
class Rymkevich750(variant.VariantTask):
    def GetUpdate(self, U=None, Q=None, C=None, **kws):
        Q_max = C.Value * U.Value / 1000
        if Q_max >= Q.Value:
            sign = '\\ge'
            result = 'удастся'
            short = 'да'
        else:
            sign = ' < '
            result = 'не удастся'
            short = 'нет'
        return dict(
            Q_max='%s_{ \\text{ max } } = %d нКл' % (Q.Letter, Q_max),
            sign=sign,
            result=result,
            short=short
        )



@variant.solution_space(80)
@variant.text('''
    Конденсатор ёмкостью {C:Value:e} был заряжен до напряжения {U1:Value:e}.
    Затем напряжение уменьшают {what} {U2:Value:e}.
    Определите на сколько уменьшится заряд конденсатора, ответ выразите в микрокулонах.
''')
@variant.answer_short('''
    {Q_max:L} = {C:L}{U:L} = {C:Value} * {U:Value} = {Q_max:Value}
    \\implies {Q_max:L} {sign} {Q:L} \\implies \\text{ {result} }
''')
@variant.answer_test('{short}')
@variant.arg(U1=('U_1 = {} кВ', [45, 55, 65, 75]))
@variant.arg(what=['до', 'на'])
@variant.arg(U2=('U_2 = {} кВ', [10, 20, 30]))
@variant.arg(C=('C = {} нФ', [20, 30, 40]))
class Q_from_DeltaU_C(variant.VariantTask):  # Генденштейн-10-54-5
    def GetUpdate(self, what=None, U1=None, U2=None, C=None, **kws):
        if what == 'до':
            q = C.Value * (U1.Value - U2.Value)
        elif what == 'на':
            q = C.Value * U2.Value
        else:
            raise RuntimeError()
        return dict(
            q='q = %d мкКл' % q,
        )


@variant.solution_space(80)
@variant.text('''
    Как и во сколько раз изменится ёмкость плоского конденсатора
    при уменьшении площади пластин в {a} раз
    и уменьшении расстояния между ними в {b} раз?
    В ответе укажите дробь или число — отношение новой ёмкости к старой.
''')
@variant.answer_short('''
    \\frac{ C' }{ C }
        = \\frac{ \\eps_0\\eps \\frac S{a} }{ \\frac d{b} } \\Big/ \\frac{ \\eps_0\\eps S }{ d }
        = \\frac{ {b} }{ {a} } = {sign} 1 \\implies \\text{ {result} }
''')
@variant.answer_test('{ratio:Basic}')
@variant.arg(a=[2, 3, 4, 5, 6, 7, 8])
@variant.arg(b=[2, 3, 4, 5, 6, 7, 8])
# @variant.arg(a__a_times=n_times(2, 3, 4, 5, 6, 7, 8))
# @variant.arg(b__b_times=n_times(2, 3, 4, 5, 6, 7, 8))
class Rymkevich751(variant.VariantTask):
    def GetUpdate(self, a=None, b=None, **kws):
        value = Fraction() * b / a
        if value._fraction == 1:
            sign = '='
            result = 'не изменится'
        else:
            if value._fraction > 1:
                sign = '>'
                result = 'увеличится'
            elif value._fraction < 1:
                sign = '<'
                result = 'уменьшится'
                value = Fraction() / value
            result += ' в ${value:LaTeX}$ раз'.format(value=value)
        return dict(
            sign=sign,
            result=result,
            ratio=value,
        )


@variant.solution_space(80)
@variant.text('''
    Электрическая ёмкость конденсатора равна {C:Task:e},
    при этом ему сообщён заряд {Q:Task:e}. Какова энергия заряженного конденсатора?
    Ответ выразите в микроджоулях и округлите до целого.
''')
@variant.answer_short('''
    {W:L}
    = \\frac{ {Q:L}^2 }{ 2{C:L} }
    = \\frac{ \\sqr{Q:Value:s} }{ 2 * {C:Value} }
    = {W:Value}
''')
@variant.arg(Q=['%s = %s нКл' % (Ql, Qv) for Ql in ['Q', 'q'] for Qv in [300, 500, 800, 900]])
@variant.arg(C=['C = %s пФ' % Cv for Cv in [200, 400, 600, 750]])
class Rymkevich762(variant.VariantTask):
    def GetUpdate(self, C=None, Q=None, **kws):
        return dict(
            W='W = %.2f мкДж' % (1. * Q.Value ** 2 / 2 / C.Value),
        )


@variant.text('''
    \\begin{{tikzpicture}}[circuit ee IEC, x=1cm, y=1cm, semithick]
        \\draw  (0, 0) -- (0, 2) to [capacitor={ info={ {C1:L:e} } }] (2, 2)
                (0, 0) -- (2, 0) to [capacitor={ info={ {C2:L:e} } }] (0, 0)
        ;
        \\draw [-o] (0, 1) -- ++(-1, 0) node[left] { $-$ };
        \\draw [-o] (2, 1) -- ++(1, 0) node[right] { $+$ };

        \\node [right,text width = 14cm, align=justify] at (3.5,1.5) {
        Два конденсатора ёмкостей {C1:Task:e} и {C2:Task:e} параллельно подключают
        к источнику напряжения {U:Task:e} (см. рис.). Определите заряды каждого из конденсаторов.
        };
    \\end{{tikzpicture}}
''')
@variant.answer_short('''
    Q_1
        = Q_2
        = C{U:L}
        = \\frac{ {U:L} }{ \\frac1{ C_1 } + \\frac1{ C_2 } }
        = \\frac{ C_1C_2{U:L} }{ C_1 + C_2 }
        = \\frac{
            {C1:Value} * {C2:Value} * {U:Value}
         }{
            {C1:Value} + {C2:Value}
         }
        = {Q:Value}
''')
@variant.arg(C1__C2=[('C_1 = %s нФ' % C1, 'C_2 = %s нФ' % C2) for C1 in [20, 30, 40, 60] for C2 in [20, 30, 40, 60] if C1 != C2])
@variant.arg(U=['%s = %s В' % (Ul, Uv) for  Ul in ['U', 'V'] for Uv in [150, 200, 300, 400, 450]])
class CondPosl(variant.VariantTask):
    def GetUpdate(self, C1=None, C2=None, U=None, **kws):
        return dict(
            Q='Q = %.2f нКл' % (1. * C1.Value * C2.Value * U.Value / (C1.Value + C2.Value)),
        )


@variant.text('''
    \\begin{{tikzpicture}}[circuit ee IEC, x=1cm, y=1cm, semithick]
        \\draw  (0, 0) to [capacitor={ info={ {C1:L:e} } }] (1, 0)
                       to [capacitor={ info={ {C2:L:e} } }] (2, 0)
        ;
        \\draw [-o] (0, 0) -- ++(-0.5, 0) node[left] { $-$ };
        \\draw [-o] (2, 0) -- ++(0.5, 0) node[right] { $+$ };

        \\node [right,text width = 14cm, align=justify] at (3.5,0) {
        Два конденсатора ёмкостей {C1:Task:e} и {C2:Task:e} последовательно подключают
        к источнику напряжения {U:Task:e} (см. рис.). Определите заряды каждого из конденсаторов.
        };
    \\end{{tikzpicture}}
''')
@variant.answer_short('''
    Q_1
        = Q_2
        = C{U:L}
        = \\frac{ {U:L} }{ \\frac1{ C_1 } + \\frac1{ C_2 } }
        = \\frac{ C_1C_2{U:L} }{ C_1 + C_2 }
        = \\frac{
            {C1:Value} * {C2:Value} * {U:Value}
         }{
            {C1:Value} + {C2:Value}
         }
        = {Q:Value}
''')
@variant.arg(C1__C2=[('C_1 = %s нФ' % C1, 'C_2 = %s нФ' % C2) for C1 in [20, 30, 40, 60] for C2 in [20, 30, 40, 60] if C1 != C2])
@variant.arg(U=['%s = %s В' % (Ul, Uv) for  Ul in ['U', 'V'] for Uv in [150, 200, 300, 400, 450]])
class Cond1(variant.VariantTask):
    def GetUpdate(self, C1=None, C2=None, U=None, **kws):
        return dict(
            Q='Q = %.2f нКл' % (1. * C1.Value * C2.Value * U.Value / (C1.Value + C2.Value)),
        )
