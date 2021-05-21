import generators.variant as variant
from generators.helpers import UnitValue, letter_variants, Fraction, n_times


@variant.text('''
    Определите ток, протекающий через резистор {R:Task:e} и разность потенциалов на нём (см. рис. на доске),
    если {r1:Task:e}, {r2:Task:e}, {E1:Task:e}, {E2:Task:e}.
''')
@variant.arg(R=['R = %d Ом' % RValue for RValue in [10, 12, 15, 18, 20]])
@variant.arg(r1=['r_1 = %d Ом' % r1Value for r1Value in [1, 2, 3]])
@variant.arg(r2=['r_2 = %d Ом' % r2Value for r2Value in [1, 2, 3]])
@variant.arg(E1=['\\ele_1 = %d В' % E1Value for E1Value in [20, 30, 40, 60]])
@variant.arg(E2=['\\ele_2 = %d В' % E2Value for E2Value in [20, 30, 40, 60]])
@variant.answer_tex('''
    Обозначим на рисунке все токи: направление произвольно, но его надо зафиксировать. Всего на рисунке 3 контура и 2 узла.
    Поэтому можно записать $3 - 1 = 2$ уравнения законов Кирхгофа для замкнутого контура и $2 - 1 = 1$ — для узлов
    (остальные уравнения тоже можно записать, но они не дадут полезной информации, а будут лишь следствиями уже записанных).

    Отметим на рисунке 2 контура (и не забуем указать направление) и 1 узел (точка «1»ы, выделена жирным). Выбор контуров и узлов не критичен: получившаяся система может быть чуть проще или сложнее, но не слишком.

    \\begin{ tikzpicture }[circuit ee IEC, thick]
        \\draw  (0, 0) to [current direction={ near end, info=$\\eli_1$ }] (0, 3)
                to [battery={ rotate=-180,info={ $\\ele_1, r_1 $ } }]
                (3, 3)
                to [battery={ info'={ $\\ele_2, r_2 $ } }]
                (6, 3) to [current direction'={ near start, info=$\\eli_2$ }] (6, 0) -- (0, 0)
                (3, 0) to [current direction={ near start, info=$\\eli$ }, resistor={ near end, info=$R$ }] (3, 3);
        \\draw [-{ Latex },color=red] (1.2, 1.7) arc [start angle = 135, end angle = -160, radius = 0.6];
        \\draw [-{ Latex },color=blue] (4.2, 1.7) arc [start angle = 135, end angle = -160, radius = 0.6];
        \\node [contact,color=green!71!black] (bottomc) at (3, 0) {  };
        \\node [below] (bottom) at (3, 0) { $2$ };
        \\node [above] (top) at (3, 3) { $1$ };
    \\end{ tikzpicture }

    \\begin{ align* }
        &\\begin{ cases }
            { \\color{ red } \\ele_1 = \\eli_1 r_1 - \\eli R }, \\\\
            { \\color{ blue } -\\ele_2 = -\\eli_2 r_2 + \\eli R }, \\\\
            { \\color{ green!71!black } - \\eli - \\eli_1 - \\eli_2 = 0 };
        \\end{ cases }
        \\qquad \\implies \\qquad
        \\begin{ cases }
            \\eli_1 = \\frac{ \\ele_1 + \\eli R }{ r_1 }, \\\\
            \\eli_2 = \\frac{ \\ele_2 + \\eli R }{ r_2 }, \\\\
            \\eli + \\eli_1 + \\eli_2 = 0;
        \\end{ cases } \\implies \\\\
        &\\implies
         \\eli + \\frac{ \\ele_1 + \\eli R }{ r_1 } + \\frac{ \\ele_2 + \\eli R }{ r_2 } = 0, \\\\
        &\\eli\\cbr{ 1 + \\frac{ R }{ r_1 } + \\frac{ R }{ r_2 } } + \\frac{ \\ele_1 }{ r_1 } + \\frac{ \\ele_2 }{ r_2 } = 0, \\\\
        &\\eli
            = - \\frac{ \\frac{ \\ele_1 }{ r_1 } + \\frac{ \\ele_2 }{ r_2 } }{ 1 + \\frac{ R }{ r_1 } + \\frac{ R }{ r_2 } }
            = - \\frac{ \\frac{E1:V|s}{r1:V|s} + \\frac{E2:V|s}{r2:V|s} }{ 1 + \\frac{R:V|s}{r1:V|s} + \\frac{R:V|s}{r2:V|s} }
            = - {I_ratio:LaTeX}\\units{ А }
            \\approx {I:Value}, \\\\
        &U  = \\varphi_2 - \\varphi_1 = \\eli R
            = - \\frac{ \\frac{ \\ele_1 }{ r_1 } + \\frac{ \\ele_2 }{ r_2 } }{ 1 + \\frac{ R }{ r_1 } + \\frac{ R }{ r_2 } } R
            \\approx {U:Value}.
    \\end{ align* }
    Оба ответа отрицательны, потому что мы изначально «не угадали» с направлением тока. Расчёт же показал,
    что ток через резистор $R$ течёт в противоположную сторону: вниз на рисунке, а потенциал точки 1 больше потенциала точки 2,
    а электрический ток ожидаемо течёт из точки с большим потенциалов в точку с меньшим.

    Кстати, если продолжить расчёт и вычислить значения ещё двух токов (формулы для $\\eli_1$ и $\\eli_2$, куда подставлять, выписаны выше),
    то по их знакам можно будет понять: угадали ли мы с их направлением или нет.
'''
)
class Kirchgof_double(variant.VariantTask):
    def GetUpdate(self, R=None, r1=None, r2=None, E1=None, E2=None, **kws):
        I_ratio = (
            Fraction(numerator=E1.Value, denominator=r1.Value) + Fraction(numerator=E2.Value, denominator=r2.Value)
        ) / (
            Fraction(base_value=1) + Fraction(numerator=R.Value, denominator=r1.Value) + Fraction(numerator=R.Value, denominator=r2.Value)
        )

        I = '\\eli = -%.1f А' % float(I_ratio)
        U = 'U = -%.1f В' % float(I_ratio * R.Value)
        return dict(
            I_ratio=I_ratio,
            I=I,
            U=U,
        )


@variant.text('''
    Определите ток, протекающий через резистор $R_{index}$, разность потенциалов на нём (см. рис.)
    и выделяющуюся на нём мощность, если известны $r_1, r_2, \\ele_1, \\ele_2, R_1, R_2$.

    \\begin{ tikzpicture }[circuit ee IEC, thick]
        \\draw  (0, 0) -- ++(up:2)
                to [
                    battery={ very near start, rotate={rotate1}, info={ $\\ele_1, r_1 $ } },
                    resistor={ midway, info=$R_1$ },
                    battery={ very near end, rotate={rotate2}, info={ $\\ele_2, r_2 $ } }
                ] ++(right:5)
                -- ++(down:2)
                to [resistor={ info=$R_2$ }] ++(left:5);
    \\end{ tikzpicture }
''')
@variant.arg(index=[1, 2])
@variant.arg(rotate1=[0, -180])
@variant.arg(rotate2=[0, -180])
@variant.answer_tex('''
    Нетривиальных узлов нет, поэтому все законы Кирхгофа для узлов будут иметь вид
    $\\eli-\\eli=0$ и ничем нам не помогут. Впрочем, если бы мы обозначили токи на разных участках контура $\\eli_1, \\eli_2, \\eli_3, \\ldots$,
    то именно эти законы бы помогли понять, что все эти токи равны: $\\eli_1 - \\eli_2 = 0$ и т.д.
    Так что запишем закон Кирхгофа для единственного замкнутого контура:

    \\begin{ tikzpicture }[circuit ee IEC, thick]
        \\draw  (0, 0) -- ++(up:2)
                to [
                    battery={ very near start, rotate={rotate1}, info={ $\\ele_1, r_1 $ } },
                    resistor={ midway, info=$R_1$ },
                    battery={ very near end, rotate={rotate2}, info={ $\\ele_2, r_2 $ } }
                ] ++(right:5)
                -- ++(down:2)
                to [resistor={ info=$R_2$ }, current direction={ near end, info=$\\eli$ }] ++(left:5);
        \\draw [-{ Latex }] (2, 1.4) arc [start angle = 135, end angle = -160, radius = 0.6];
    \\end{ tikzpicture }

    \\begin{ align* }
        &{sign1} \\ele_1 + {sign2} \\ele_2 = \\eli R_1 + \\eli r_2 + \\eli R_2 + \\eli r_1, \\\\
        &{sign1} \\ele_1 + {sign2} \\ele_2 = \\eli (R_1 + r_2 + R_2 + r_1), \\\\
        &\\eli = \\frac{ {sign1} \\ele_1 + {sign2} \\ele_2 }{ R_1 + r_2 + R_2 + r_1 }, \\\\
        &U_{index} = \\eli R_{index} = \\frac{ {sign1} \\ele_1 + {sign2} \\ele_2 }{ R_1 + r_2 + R_2 + r_1 } * R_{index}, \\\\
        &P_{index} = \\eli^2 R_{index} = \\frac{ \\sqr{ {sign1} \\ele_1 + {sign2} \\ele_2 } R_{index} }{ \\sqr{ R_1 + r_2 + R_2 + r_1 } }.
    \\end{ align* }

    Отметим, что ответ для тока $\\eli$ меняет знак, если отметить его на рисунке в другую сторону.
    Поэтому критично важно указывать на рисунке направление тока, иначе невозможно утверждать, что ответ верный.
    А вот выбор направления контура — не повлияет на ответ, но для проверки корректности записи законо Кирхгофа,
    там тоже необходимо направление.
''')
class Kirchgof_plain(variant.VariantTask):
    def GetUpdate(self, index=None, rotate1=None, rotate2=None, **kws):
        signs = {
            0: '-',
            -180: '',
        }
        return dict(
            sign1=signs[rotate1],
            sign2=signs[rotate2],
        )



@variant.text('''
    Определите ток, протекающий через резистор {R:Task:e} и разность потенциалов на нём (см. рис.),
    если {E1:Task:e}, {E2:Task:e}, {r1:Task:e}, {r2:Task:e}.

    \\begin{ tikzpicture }[circuit ee IEC, thick]
        \\draw  (0, 0) to [battery={ rotate=-180,info={ $\\ele_1, r_1 $ } }] (0, 3)
                -- (5, 3)
                to [battery={ rotate=-180, info'={ $\\ele_2, r_2 $ } }] (5, 0)
                -- (0, 0)
                (2.5, 0) to [resistor={ info=$R$ }] (2.5, 3);
    \\end{ tikzpicture }
''')
@variant.arg(R=['R = %d Ом' % RValue for RValue in [10, 12, 15, 18, 20]])
@variant.arg(r1=['r_1 = %d Ом' % r1Value for r1Value in [1, 2, 3]])
@variant.arg(r2=['r_2 = %d Ом' % r2Value for r2Value in [2, 4, 6]])
@variant.arg(E1=['\\ele_1 = %d В' % E1Value for E1Value in [6, 12, 18]])
@variant.arg(E2=['\\ele_2 = %d В' % E2Value for E2Value in [5, 15, 25]])
@variant.answer_tex('''
    Выберем 2 контура и один узел, запишем для них законы Кирхгофа:

    \\begin{ tikzpicture }[circuit ee IEC, thick]
        \\draw  (0, 0) to [battery={ rotate=-180,info={ $\\ele_1, r_1 $ } }, current direction={ near end, info=$\\eli_1$ }] (0, 3)
                -- (5, 3)
                to [battery={ rotate=-180, info'={ $\\ele_2, r_2 $ } }, current direction={ near end, info=$\\eli_2$ }] (5, 0)
                -- (0, 0)
                (2.5, 0) to [resistor={ info=$R$ }, current direction'={ near end, info=$\\eli$ }] (2.5, 3);
        \\draw [-{ Latex },color=red] (0.8, 1.9) arc [start angle = 135, end angle = -160, radius = 0.6];
        \\draw [-{ Latex },color=blue] (3.5, 1.9) arc [start angle = 135, end angle = -160, radius = 0.6];
        \\node [contact,color=green!71!black] (topc) at (2.5, 3) {  };
        \\node [above] (top) at (2.5, 3) { $1$ };
    \\end{ tikzpicture }

    \\begin{ align* }
        &\\begin{ cases }
            { \\color{ red } {E1:L} = \\eli_1 {r1:L} + {I:L} {R:L} }, \\\\
            { \\color{ blue } {E2:L} = \\eli_2 {r2:L} - {I:L} {R:L} }, \\\\
            { \\color{ green!71!black } {I:L} - \\eli_1 - \\eli_2 = 0 };
        \\end{ cases }
        \\qquad \\implies \\qquad
        \\begin{ cases }
            \\eli_1 = \\frac{ {E1:L} - {I:L} {R:L} }{r1:L:s}, \\\\
            \\eli_2 = \\frac{ {E2:L} + {I:L} {R:L} }{r2:L:s}, \\\\
            {I:L} - \\eli_1 - \\eli_2 = 0;
        \\end{ cases } \\implies \\\\
        &\\implies {I:L} - \\frac{ {E1:L} - {I:L} {R:L} }{r1:L:s} + \\frac{ {E2:L} + {I:L} {R:L} }{r2:L:s} = 0, \\\\
        &{I:L}\\cbr{ 1 + \\frac{R:L:s}{r1:L:s} + \\frac{R:L:s}{r2:L:s} } - \\frac{E1:L:s}{r1:L:s} + \\frac{E2:L:s}{r2:L:s} = 0, \\\\
        &{I:L}
            = \\frac{ \\frac{E1:L:s}{r1:L:s} - \\frac{E2:L:s}{r2:L:s} }{ 1 + \\frac{R:L:s}{r1:L:s} + \\frac{R:L:s}{r2:L:s} }
            = \\frac{ \\frac{E1:V:s}{r1:V:s} - \\frac{E2:V:s}{r2:V:s} }{ 1 + \\frac{R:V:s}{r1:V:s} + \\frac{R:V:s}{r2:V:s} }
            = {I_ratio:LaTeX}\\units{ А }
            \\approx {I:Value}, \\\\
        &U  = {I:L} {R:L} = \\frac{ \\frac{E1:L:s}{r1:L:s} - \\frac{E2:L:s}{r2:L:s} }{ 1 + \\frac{R:L:s}{r1:L:s} + \\frac{R:L:s}{r2:L:s} } R
            \\approx {U:Value}.
    \\end{ align* }
'''
)
class Kirchgof_double_2(variant.VariantTask):
    pass
    def GetUpdate(self, R=None, r1=None, r2=None, E1=None, E2=None, **kws):
        I_ratio = (
            Fraction(numerator=E1.Value, denominator=r1.Value) - Fraction(numerator=E2.Value, denominator=r2.Value)
        ) / (
            Fraction(base_value=1) + Fraction(numerator=R.Value, denominator=r1.Value) + Fraction(numerator=R.Value, denominator=r2.Value)
        )

        I = '\\eli = %.3f А' % float(I_ratio)
        U = 'U = %.3f В' % float(I_ratio * R.Value)
        return dict(
            I_ratio=I_ratio,
            I=I,
            U=U,
        )


@variant.text('''
    Определите ток $\\eli_{index}$, протекающий через резистор $R_{index}$ (см. рис.),
    направление этого тока и разность потенциалов $U_{index}$ на этом резисторе,
    если {R1:Task:e}, {R2:Task:e}, {R3:Task:e}, {E1:Task:e}, {E2:Task:e}, {E3:Task:e}.
    Внутренним сопротивлением всех трёх ЭДС пренебречь.
    Ответы получите в виде несократимых дробей, а также определите приближённые значения.

    \\begin{ tikzpicture }[circuit ee IEC, thick]
        \\foreach \\contact/\\x in { 1/0, 2/3, 3/6 }
        {
            \\node [contact] (top contact \\contact) at (\\x, 0) {  };
            \\node [contact] (bottom contact \\contact) at (\\x, 4) {  };
        }
        \\draw  (bottom contact 1) -- (bottom contact 2) -- (bottom contact 3);
        \\draw  (top contact 1) -- (top contact 2) -- (top contact 3);
        \\draw  (bottom contact 1) to [resistor={ near start, info={R1:Letter:e} }, battery={ near end, info={E1:Letter:e} }] (top contact 1);
        \\draw  (bottom contact 2) to [resistor={ near start, info={R2:Letter:e} }, battery={ near end, info={E2:Letter:e} }] (top contact 2);
        \\draw  (bottom contact 3) to [resistor={ near start, info={R3:Letter:e} }, battery={ near end, info={E3:Letter:e} }] (top contact 3);
    \\end{ tikzpicture }

''')
@variant.arg(index=[1, 2, 3])
@variant.arg(R1=('R_1 = {} Ом', [2, 3, 4]))
@variant.arg(R2=('R_2 = {} Ом', [5, 6, 8]))
@variant.arg(R3=('R_3 = {} Ом', [10, 12, 15]))
@variant.arg(E1=('\\ele_1 = {} В', [4, 5]))
@variant.arg(E2=('\\ele_2 = {} В', [3, 6]))
@variant.arg(E3=('\\ele_3 = {} В', [2, 8]))
@variant.answer_tex('''
    План:
    \\begin{{itemize}}
        \\item отметим на рисунке произвольно направления токов (если получим отрицательный ответ, значит не угадали направление и только),
        \\item выберем и обозначим на рисунке контуры (здесь всего 3, значит будет нужно $3-1=2$), для них запишем законы Кирхгофа,
        \\item выберем и выделим на рисунке нетривиальные узлы (здесь всего 2, значит будет нужно $2-1=1$), для него запишем закон Кирхгофа,
        \\item попытаемся решить получившуюся систему. В конкретном решении мы пытались первым делом найти {I2:L:e}, но, возможно, в вашем варианте будет быстрее решать систему в другом порядке. Мы всё же проделаем всё в лоб, подробно и целиком.
    \\end{{itemize}}


    \\begin{ tikzpicture }[circuit ee IEC, thick]
        \\foreach \\contact/\\x in { 1/0, 2/3, 3/6 }
        {
            \\node [contact] (top contact \\contact) at (\\x, 0) {  };
            \\node [contact] (bottom contact \\contact) at (\\x, 4) {  };
        }
        \\draw  (bottom contact 1) -- (bottom contact 2) -- (bottom contact 3);
        \\draw  (top contact 1) -- (top contact 2) -- (top contact 3);
        \\draw  (bottom contact 1) to [resistor={ near start, info={R1:Letter:e} }, current direction'={ midway, info={I1:Letter:e} }, battery={ near end, info={E1:Letter:e} }] (top contact 1);
        \\draw  (bottom contact 2) to [resistor={ near start, info={R2:Letter:e} }, current direction'={ midway, info={I2:Letter:e} }, battery={ near end, info={E2:Letter:e} }] (top contact 2);
        \\draw  (bottom contact 3) to [resistor={ near start, info={R3:Letter:e} }, current direction'={ midway, info={I3:Letter:e} }, battery={ near end, info={E3:Letter:e} }] (top contact 3);
        \\draw [-{ Latex },color=red] (1.2, 2.5) arc [start angle = 135, end angle = -160, radius = 0.6];
        \\draw [-{ Latex },color=blue] (4.2, 2.5) arc [start angle = 135, end angle = -160, radius = 0.6];
        \\node [contact,color=green!71!black] (bottomc) at (bottom contact 2) {  };
    \\end{ tikzpicture }

    \\begin{ align* }
        &\\begin{ cases }
            { \\color{ red } {I1:L}{R1:L} - {I2:L}{R2:L} = {E1:L} - {E2:L} }, \\\\
            { \\color{ blue } {I2:L}{R2:L} - {I3:L}{R3:L} = {E2:L} - {E3:L} }, \\\\
            { \\color{ green!71!black } {I1:L} + {I2:L} + {I3:L} = 0 };
        \\end{ cases }
        \\qquad \\implies \\qquad
        \\begin{ cases }
            {I1:L} = \\frac{ {E1:L} - {E2:L} + {I2:L}{R2:L} }{R1:L:s}, \\\\
            {I3:L} = \\frac{ {I2:L}{R2:L} - {E2:L} + {E3:L} }{R3:L:s}, \\\\
            {I1:L} + {I2:L} + {I3:L} = 0, \\\\
        \\end{ cases } \\implies \\\\
        \\implies
            &{I2:L} + \\frac{ {E1:L} - {E2:L} + {I2:L}{R2:L} }{R1:L:s} + \\frac{ {I2:L}{R2:L} - {E2:L} + {E3:L} }{R3:L:s} = 0, \\\\
        &   {I2:L}\\cbr{ 1 + \\frac{R2:L:s}{R1:L:s} + \\frac{R2:L:s}{R3:L:s} } + \\frac{ {E1:L} - {E2:L} }{R1:L:s} + \\frac{ {E3:L} - {E2:L} }{R3:L:s} = 0, \\\\
        &   {I2:L} = \\cfrac{ \\cfrac{ {E2:L} - {E1:L} }{R1:L:s} + \\cfrac{ {E2:L} - {E3:L} }{R3:L:s} }{ 1 + \\cfrac{R2:L:s}{R1:L:s} + \\cfrac{R2:L:s}{R3:L:s} }
            = \\cfrac{ \\cfrac{ {E2:V} - {E1:V} }{R1:V:s} + \\cfrac{ {E2:V} - {E3:V} }{R3:V:s} }{ 1 + \\cfrac{R2:V:s}{R1:V:s} + \\cfrac{R2:V:s}{R3:V:s} }
            = {I2_ratio:LaTeX}\\units{ А } \\approx {I2:Value}, \\\\
        &   {U2:L} = {I2:L}{R2:L} = \\cfrac{ \\cfrac{ {E2:L} - {E1:L} }{R1:L:s} + \\cfrac{ {E2:L} - {E3:L} }{R3:L:s} }{ 1 + \\cfrac{R2:L:s}{R1:L:s} + \\cfrac{R2:L:s}{R3:L:s} } * {R2:L}
            = \\cfrac{ \\cfrac{ {E2:V} - {E1:V} }{R1:V:s} + \\cfrac{ {E2:V} - {E3:V} }{R3:V:s} }{ 1 + \\cfrac{R2:V:s}{R1:V:s} + \\cfrac{R2:V:s}{R3:V:s} } * {R2:V}
            = {I2_ratio:LaTeX}\\units{ А } * {R2:V} = {U2_ratio:LaTeX}\\units{ В } \\approx {U2:Value}.
    \\end{ align* }

    Одну пару силы тока и напряжения получили. Для некоторых вариантов это уже ответ, но не у всех.
    Для упрощения записи преобразуем (чтобы избавитсья от 4-этажной дроби) и подставим в уже полученные уравнения:

    \\begin{ align* }
    {I2:L}
        &=
        \\frac{ \\frac{ {E2:L} - {E1:L} }{R1:L:s} + \\frac{ {E2:L} - {E3:L} }{R3:L:s} }{ 1 + \\frac{R2:L:s}{R1:L:s} + \\frac{R2:L:s}{R3:L:s} }
        =
        \\frac{ ({E2:L} - {E1:L}){R3:L} + ({E2:L} - {E3:L}){R1:L} }{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} },
        \\\\
    {I1:L}
        &=  \\frac{ {E1:L} - {E2:L} + {I2:L}{R2:L} }{R1:L:s}
        =   \\frac{ {E1:L} - {E2:L} + \\cfrac{ ({E2:L} - {E1:L}){R3:L} + ({E2:L} - {E3:L}){R1:L} }{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} } * {R2:L} }{R1:L:s} = \\\\
        &=  \\frac{
            {E1:L}{R1:L}{R3:L} + {E1:L}{R2:L}{R3:L} + {E1:L}{R2:L}{R1:L}
            - {E2:L}{R1:L}{R3:L} - {E2:L}{R2:L}{R3:L} - {E2:L}{R2:L}{R1:L}
            + {E2:L}{R3:L}{R2:L} - {E1:L}{R3:L}{R2:L} + {E2:L}{R1:L}{R2:L} - {E3:L}{R1:L}{R2:L}
        }{ {R1:L} * \\cbr{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} } }
        = \\\\ &=
        \\frac{
            {E1:L}\\cbr{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} - {R3:L}{R2:L} }
            + {E2:L}\\cbr{ - {R1:L}{R3:L} - {R2:L}{R3:L} - {R2:L}{R1:L} + {R3:L}{R2:L} + {R1:L}{R2:L} }
            - {E3:L}{R1:L}{R2:L}
        }{ {R1:L} * \\cbr{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} } }
        = \\\\ &=
        \\frac{
            {E1:L}\\cbr{ {R1:L}{R3:L} + {R2:L}{R1:L} }
            + {E2:L}\\cbr{ - {R1:L}{R3:L} }
            - {E3:L}{R1:L}{R2:L}
        }{ {R1:L} * \\cbr{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} } }
        =
        \\frac{
            {E1:L}\\cbr{ {R3:L} + {R2:L} } - {E2:L}{R3:L} - {E3:L}{R2:L}
        }{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} }
        = \\\\ &=
        \\frac{
            ({E1:L} - {E3:L}){R2:L} + ({E1:L} - {E2:L}){R3:L}
        }{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} }
        =
        \\frac{
            \\cfrac{ {E1:L} - {E3:L} }{R3:L:s} + \\cfrac{ {E1:L} - {E2:L} }{R2:L:s}
        }{ \\cfrac{R1:L:s}{R2:L:s} + 1 + \\cfrac{R1:L:s}{R3:L:s} }
        =
        \\frac{
            \\cfrac{ {E1:V} - {E3:V} }{R3:V:s} + \\cfrac{ {E1:V} - {E2:V} }{R2:V:s}
        }{ \\cfrac{R1:V:s}{R2:V:s} + 1 + \\cfrac{R1:V:s}{R3:V:s} }
        = {I1_ratio:LaTeX}\\units{ А } \\approx {I1:Value}. \\\\
    {U1:L}
        &=
        {I1:L}{R1:L}
        =
        \\frac{
            \\cfrac{ {E1:L} - {E3:L} }{R3:L:s} + \\cfrac{ {E1:L} - {E2:L} }{R2:L:s}
        }{ \\cfrac{R1:L:s}{R2:L:s} + 1 + \\cfrac{R1:L:s}{R3:L:s} } * {R1:L}
        =
        {I1_ratio:LaTeX}\\units{ А } * {R1:V} = {U1_ratio:LaTeX}\\units{ В } \\approx {U1:Value}.
    \\end{ align* }

    Если вы проделали все эти вычисления выше вместе со мной, то
    \\begin{{itemize}}
        \\item вы совершили ошибку, выбрав неверный путь решения:
        слишком длинное решение, очень легко ошибиться в индексах, дробях, знаках или потерять какой-то множитель,
        \\item можно было выразить из исходной системы другие токи и получить сразу нажный вам,
        а не какой-то 2-й,
        \\item можно было сэкономить: все три резистора и ЭДС соединены одинаково,
        поэтому ответ для 1-го резистора должен отличаться лишь перестановкой индексов (этот факт крайне полезен при проверке ответа, у нас всё сошлось),
        я специально подгонял выражение для {I1:L:e} к этому виду, вынося за скобки и преобразуя дробь,
        \\item вы молодец, потому что не побоялись и получили верный ответ грамотным способом,
    \\end{{itemize}}
    так что переходим к третьему резистору. Будет похоже, но кого это когда останавливало...

    \\begin{ align* }
    {I3:L}
        &=  \\frac{ {I2:L}{R2:L} - {E2:L} + {E3:L} }{R3:L:s}
        =
        \\cfrac{
            \\cfrac{
                ({E2:L} - {E1:L}){R3:L} + ({E2:L} - {E3:L}){R1:L}
            }{
                {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L}
            } * {R2:L} - {E2:L} + {E3:L} }{R3:L:s}
        = \\\\ &=
        \\frac{
            {E2:L}{R3:L}{R2:L} - {E1:L}{R3:L}{R2:L} + {E2:L}{R1:L}{R2:L} - {E3:L}{R1:L}{R2:L}
            - {E2:L}{R1:L}{R3:L} - {E2:L}{R2:L}{R3:L} - {E2:L}{R2:L}{R1:L}
            + {E3:L}{R1:L}{R3:L} + {E3:L}{R2:L}{R3:L} + {E3:L}{R2:L}{R1:L}
        }{ \\cbr{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} } * {R3:L} }
        = \\\\ &=
        \\frac{
            - {E1:L}{R3:L}{R2:L} - {E2:L}{R1:L}{R3:L} + {E3:L}{R1:L}{R3:L} + {E3:L}{R2:L}{R3:L}
        }{ \\cbr{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} } * {R3:L} }
        =
        \\frac{
            - {E1:L}{R2:L} - {E2:L}{R1:L} + {E3:L}{R1:L} + {E3:L}{R2:L}
        }{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} }
        = \\\\ &=
        \\frac{
            {R1:L}({E3:L} - {E2:L}) + {R2:L}({E3:L} - {E1:L})
        }{ {R1:L}{R3:L} + {R2:L}{R3:L} + {R2:L}{R1:L} }
        =
        \\frac{
            \\cfrac{ {E3:L} - {E2:L} }{R2:L:s} + \\cfrac{ {E3:L} - {E1:L} }{R1:L:s}
        }{ \\cfrac{R3:L:s}{R2:L:s} + \\cfrac{R3:L:s}{R1:L:s} + 1 }
        =
        \\frac{
            \\cfrac{ {E3:V} - {E2:V} }{R2:V:s} + \\cfrac{ {E3:V} - {E1:V} }{R1:V:s}
        }{ \\cfrac{R3:V:s}{R2:V:s} + \\cfrac{R3:V:s}{R1:V:s} + 1 }
        = {I3_ratio:LaTeX}\\units{ А } \\approx {I3:Value}. \\\\
    {U3:L}
        &=
        {I3:L}{R3:L}
        =
        \\frac{
            \\cfrac{ {E3:L} - {E2:L} }{R2:L:s} + \\cfrac{ {E3:L} - {E1:L} }{R1:L:s}
        }{ \\cfrac{R3:L:s}{R2:L:s} + \\cfrac{R3:L:s}{R1:L:s} + 1 } * {R3:L}
        =
        {I3_ratio:LaTeX}\\units{ А } * {R3:V} = {U3_ratio:LaTeX}\\units{ В } \\approx {U3:Value}.
    \\end{ align* }

    Положительные ответы говорят, что мы угадали на рисунке направление тока (тут нет нашей заслуги, повезло),
    отрицательные — что не угадали (и в этом нет ошибки), и ток течёт в противоположную сторону.
    Напомним, что направление тока — это направление движения положительных зарядов,
    а в металлах носители заряда — электроны, которые заряжены отрицательно.
'''
)
class Kirchgof_triple(variant.VariantTask):
    def GetUpdate(self, R1=None, R2=None, R3=None, E1=None, E2=None, E3=None, **kws):
        I1_ratio = (
            Fraction(numerator=E1.Value - E3.Value, denominator=R3.Value)
            + Fraction(numerator=E1.Value - E2.Value, denominator=R2.Value)
        ) / (
            Fraction(numerator=R1.Value, denominator=R2.Value)
            + Fraction(numerator=R1.Value, denominator=R3.Value)
            + 1
        )
        I2_ratio = (
            Fraction(numerator=E2.Value - E1.Value, denominator=R1.Value)
            + Fraction(numerator=E2.Value - E3.Value, denominator=R3.Value)
        ) / (
            Fraction(numerator=R2.Value, denominator=R1.Value)
            + Fraction(numerator=R2.Value, denominator=R3.Value)
            + 1
        )
        I3_ratio = (
            Fraction(numerator=E3.Value - E1.Value, denominator=R1.Value)
            + Fraction(numerator=E3.Value - E2.Value, denominator=R2.Value)
        ) / (
            Fraction(numerator=R3.Value, denominator=R1.Value)
            + Fraction(numerator=R3.Value, denominator=R2.Value)
            + 1
        )
        I1 = '\\eli_1 = %.2f А' % float(I1_ratio)
        I2 = '\\eli_2 = %.2f А' % float(I2_ratio)
        I3 = '\\eli_3 = %.2f А' % float(I3_ratio)
        U1_ratio = I1_ratio * R1.Value
        U2_ratio = I2_ratio * R2.Value
        U3_ratio = I3_ratio * R3.Value
        U1 = 'U_1 = %.2f В' % float(U1_ratio)
        U2 = 'U_2 = %.2f В' % float(U2_ratio)
        U3 = 'U_3 = %.2f В' % float(U3_ratio)
        return dict(
            I1_ratio=I1_ratio,
            I2_ratio=I2_ratio,
            I3_ratio=I3_ratio,
            I1=I1,
            I2=I2,
            I3=I3,
            U1_ratio=U1_ratio,
            U2_ratio=U2_ratio,
            U3_ratio=U3_ratio,
            U1=U1,
            U2=U2,
            U3=U3,
        )

