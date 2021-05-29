import generators.variant as variant
from generators.helpers import Consts, Fraction, UnitValue


@variant.text('''
    {many} одинаковых брусков массой {m:V:e} каждый лежат на гладком горизонтальном столе.
    Бруски пронумерованы от 1 до {N} и последовательно связаны между собой
    невесомыми нерастяжимыми нитями: 1 со 2, 2 с 3 (ну и с 1) и т.д.
    Экспериментатор Глюк прикладывает постоянную горизонтальную силу {F:V:e} к бруску с {which} номером.
    С каким ускорением двигается система? Чему равна сила натяжения нити, связывающей бруски {i} и {j}?
''')
@variant.arg(many__N=[('Четыре', 4), ('Пять', 5), ('Шесть', 6)])
@variant.arg(which=['наибольшим', 'наименьшим'])
@variant.arg(i=[1, 2, 3])
@variant.arg(m=('m = {} кг', [2, 3]))
@variant.arg(F=('F = {} Н', [60, 90, 120]))
@variant.answer_align([
    'a &= \\frac{ {F:L} }{ {N} {m:L} } = \\frac{ {F:V} }{ {N} * {m:V} } \\approx {a:V},',
    'T &= m\'a = {k}m * \\frac{ {F:L} }{ {N} {m:L} } = \\frac{ {k} }{ {N} } {F:L} \\approx {T:V}.'
])
class Many_blocks(variant.VariantTask):
     def GetUpdate(self, many=None, N=None, which=None, i=None, F=None, m=None, **kws):
        k = {
            'наибольшим': i,
            'наименьшим':  N - i,
        }[which]
        return dict(
            j=i + 1,
            k=k,
            a='a = %.1f м / c^2' % (F.Value / N / m.Value),
            T='T = %.1f Н' % (F.Value * k / N),
        )


@variant.solution_space(80)
@variant.text('''
    Два бруска связаны лёгкой нерастяжимой нитью и перекинуты через неподвижный блок (см. рис.).
    Определите силу натяжения нити и ускорения брусков. Силами трения пренебречь, массы брусков
    равны {m1:Task:e} и {m2:Task:e}.
    % {Consts.g_ten:Task:e}.

    \\begin{tikzpicture}[x=1.5cm,y=1.5cm,thick]
        \\draw
            (-0.4, 0) rectangle (-0.2, 1.2)
            (0.15, 0.5) rectangle (0.45, 1)
            (0, 2) circle [radius=0.3] -- ++(up:0.5)
            (-0.3, 1.2) -- ++(up:0.8)
            (0.3, 1) -- ++(up:1)
            (-0.7, 2.5) -- (0.7, 2.5)
            ;
        \\draw[pattern={ Lines[angle=51,distance=3pt] },pattern color=black,draw=none] (-0.7, 2.5) rectangle (0.7, 2.75);
        \\node [left] (left) at (-0.4, 0.6) {m1:L:e:s};
        \\node [right] (right) at (0.4, 0.75) {m2:L:e:s};
    \\end{tikzpicture}
''')
@variant.arg(m1=('m_1 = {} кг', [5, 8, 11]))
@variant.arg(m2=('m_2 = {} кг', [4, 6, 10, 14]))
@variant.answer_tex('''
    Предположим, что левый брусок ускоряется вверх, тогда правый ускоряется вниз (с тем же ускорением).
    Запишем 2-й закон Ньютона 2 раза (для обоих тел) в проекции на вертикальную оси, направив её вверх.
    \\begin{align*}
        &\\begin{cases}
            T - {m1:L}g = {m1:L}a, \\\\
            T - {m2:L}g = -{m2:L}a,
        \\end{cases} \\\\
        &\\begin{cases}
            {m2:L}g - {m1:L}g = {m1:L}a + {m2:L}a, \\\\
            T = {m1:L}a + {m1:L}g, \\\\
        \\end{cases} \\\\
        a &= \\frac{ {m2:L} - {m1:L} }{ {m1:L} + {m2:L} } * g = \\frac{ {m2:V} - {m1:V} }{ {m1:V} + {m2:V} } * {Consts.g_ten:Value} \\approx {a:Value}, \\\\
        T &= {m1:L}(a + g) = {m1:L} * g * \\cbr{ \\frac{ {m2:L} - {m1:L} }{ {m1:L} + {m2:L} } + 1 } = {m1:L} * g * \\frac{ 2{m2:L} }{ {m1:L} + {m2:L} } = \\\\
            &= \\frac{ 2 {m2:L} {m1:L} g }{ {m1:L} + {m2:L} } = \\frac{ 2 * {m2:V} * {m1:V} * {Consts.g_ten:Value} }{ {m1:V} + {m2:V} } \\approx {T:Value}.
    \\end{align*}
    Отрицательный ответ говорит, что мы лишь не угадали с направлением ускорений. Сила же всегда положительна.
'''
)
class Two_blocks_on_block(variant.VariantTask):
    def GetUpdate(self, m1=None, m2=None, **kws):
        return dict(
            a='a = %.2f м / c^2' % ((m2.Value - m1.Value) / (m1.Value + m2.Value) * Consts.g_ten.Value),
            T='T = %.1f Н' % (2 * Consts.g_ten.Value * m1.Value * m2.Value / (m1.Value + m2.Value)),
        )


@variant.text('''
    Тело массой {m:V:e} лежит на горизонтальной поверхности. Коэффициент трения между поверхностью и телом {mu:V:e}.
    К телу приложена горизонтальная сила {F:V:e}. Определите силу трения, действующую на тело, и ускорение тела.
    % {Consts.g_ten:Task:e}.
''')
@variant.arg(m=('m = {} кг', ['1.4', '2', '2.7']))
@variant.arg(mu=('\\mu = {}', ['0.15', '0.2', '0.25']))
@variant.arg(F=('F = {} Н', ['2.5', '3.5', '4.5', '5.5']))
@variant.answer_align([
    '{F_max:L} = \\mu N = \\mu m g = {mu:Value} * {m:V} * {Consts.g_ten:V} = {F_max:V},',
    '{F_max:L} {sign} {F:L} \\implies {F_tren:L} = {F_tren:V}, {a:L} = \\frac{ {F:L} - {F_tren:L} }{m:L:s} = {a:V},',
    '\\text{ при равенстве возможны оба варианта: и едет, и не едет, но на ответы это не влияет. }',
])
class F_tren(variant.VariantTask):
    def GetUpdate(self, m=None, mu=None, F=None, **kws):
        F_max_value = mu.Value * m.Value * Consts.g_ten.Value
        if F_max_value > F.Value:
            sign = '>'
            F_tren_value = F.Value
            a_value = 0
        elif F_max_value <= F.Value:
            sign = '\\le'
            F_tren_value = F_max_value
            a_value = (F.Value - F_max_value) / m.Value
        return dict(
            sign=sign,
            F_max='F_\\text{ трения покоя $\\max$ } = %.2f Н' % F_max_value,
            F_tren='F_\\text{ трения } = %.2f Н' % F_tren_value,
            a='a = %.2f м / c^2' % a_value,
        )

