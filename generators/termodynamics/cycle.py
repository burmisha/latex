import fractions

import generators.variant as variant
from generators.helpers import UnitValue, Consts, Fraction, n_times


@variant.text('''
    Определите КПД цикла 12341, рабочим телом которого является идеальный одноатомный газ, если
    12 — изобарическое расширение газа в {alpha_text},
    23 — изохорическое охлаждение газа, при котором температура уменьшается в {beta_text},
    34 — изобара, 41 — изохора.
    % Для этого:
    % \\begin{{enumerate}}
    %     \\item сделайте рисунок в $PV$-координатах,
    %     \\item выберите удобные обозначения, чтобы не запутаться в множестве температур, давлений и объёмов,
    %     \\item вычислите необходимые соотнощения между температурами, давлениями и объёмами
    %     (некоторые сразу видны по рисунку, некоторые — надо считать),
    %     \\item определите для каждого участка поглощается или отдаётся тепло (и сколько именно:
    %     потребуется первое начало термодинамики, отдельный расчёт работ на участках через площади фигур и изменений внутренней энергии),
    %     \\item вычислите полную работу газа в цикле,
    %     \\item подставьте всё в формулу для КПД, упростите и доведите до ответа.
    % \\end{{enumerate}}
    Определите КПД цикла Карно, температура нагревателя которого равна максимальной температуре в цикле 12341, а холодильника — минимальной.
    Ответы в обоих случаях оставьте точными в виде нескоратимой дроби, никаких округлений.
''')
@variant.arg(alpha__alpha_text=n_times(2, 3, 4, 5, 6))
@variant.arg(beta__beta_text=n_times(2, 3, 4, 5, 6))
@variant.solution_space(360)
@variant.answer_align([
    'A_{ 12 } &> 0, \\Delta U_{ 12 } > 0, \\implies Q_{ 12 } = A_{ 12 } + \\Delta U_{ 12 } > 0,',
    'A_{ 23 } &= 0, \\Delta U_{ 23 } < 0, \\implies Q_{ 23 } = A_{ 23 } + \\Delta U_{ 23 } < 0,',
    'A_{ 34 } &< 0, \\Delta U_{ 34 } < 0, \\implies Q_{ 34 } = A_{ 34 } + \\Delta U_{ 34 } < 0,',
    'A_{ 41 } &= 0, \\Delta U_{ 41 } > 0, \\implies Q_{ 41 } = A_{ 41 } + \\Delta U_{ 41 } > 0.',

    'P_1V_1 &= \\nu R T_1, P_2V_2 = \\nu R T_2, P_3V_3 = \\nu R T_3, P_4V_4 = \\nu R T_4 \\text{  — уравнения состояния идеального газа },',

    '&\\text{ Пусть $P_0$, $V_0$, $T_0$ — давление, объём и температура в точке 4 (минимальные во всём цикле): }',
    'P_1 &= P_2, P_3 = P_4 = P_0, V_1 = V_4 = V_0, V_2 = V_3 = {alpha} V_1 = {alpha} V_0,, \\text{ остальные соотношения между объёмами и давлениями не даны, нужно считать }',
    'T_3 &= \\frac{ T_2 }{beta} \\text{ (по условию) } \\implies \\frac{ P_2 }{ P_3 } = \\frac{ P_2 V_2 }{ P_3 V_3 }'
    '= \\frac{ \\nu R T_2 }{ \\nu R T_3 } = \\frac{ T_2 }{ T_3 } = {beta} \\implies P_1 = P_2 = {beta} P_0',

    'A_\\text{ цикл } &= ({beta}P_0 - P_0)({alpha}V_0 - V_0) = {A}P_0V_0,',
    'A_{ 12 } &= {beta}P_0 * ({alpha}V_0 - V_0) = {A12}P_0V_0,',

    '\\Delta U_{ 12 } &= \\frac 32 \\nu R T_2 - \\frac 32 \\nu R T_1 = \\frac 32 P_2 V_2 - \\frac 32 P_1 V_1'
    ' = \\frac 32 * {beta} P_0 * {alpha} V_0 -  \\frac 32 * {beta} P_0 * V_0'
    ' = \\frac 32 * {U12} * P_0V_0,',

    '\\Delta U_{ 41 } &= \\frac 32 \\nu R T_1 - \\frac 32 \\nu R T_4 = \\frac 32 P_1 V_1 - \\frac 32 P_4 V_4'
    ' = \\frac 32 * {beta} P_0 V_0 - \\frac 32 P_0 V_0'
    ' = \\frac 32 * {U41} * P_0V_0.',

    '\\eta &= \\frac{ A_\\text{ цикл } }{ Q_+ } = \\frac{ A_\\text{ цикл } }{ Q_{ 12 } + Q_{ 41 } } '
    ' = \\frac{ A_\\text{ цикл } }{ A_{ 12 } + \\Delta U_{ 12 } + A_{ 41 } + \\Delta U_{ 41 } } = ',
    ' &= \\frac{ {A}P_0V_0 }{ {A12}P_0V_0 + \\frac 32 * {U12} * P_0V_0 + 0 + \\frac 32 * {U41} * P_0V_0 }'
    ' = \\frac{ {A} }{ {A12} + \\frac 32 * {U12} + \\frac 32 * {U41} } = \\frac{ {eta.numerator} }{ {eta.denominator} } \\approx {eta_f}.',

    '\\eta_\\text{ Карно } &= 1 - \\frac{ T_\\text{ х } }{ T_\\text{ н } } = 1 - \\frac{ T_\\text{ 4 } }{ T_\\text{ 2 } }'
    ' = 1 - \\frac{ \\frac{ P_4V_4 }{ \\nu R } }{ \\frac{ P_2V_2 }{ \\nu R } } = 1 - \\frac{ P_4V_4 }{ P_2V_2 }'
    ' = 1 - \\frac{ P_0V_0 }{ {beta}P_0 * {alpha}V_0 } = 1 - \\frac 1{ {beta} * {alpha} }  = \\frac{ {eta_max.numerator} }{ {eta_max.denominator} } \\approx {eta_max_f}.'
])
class Rectangle(variant.VariantTask):
    def GetUpdate(self, alpha=None, beta=None, **kws):
        A = (alpha - 1) * (beta - 1)
        A12 = (alpha - 1) * beta
        U12 = (alpha - 1) * beta
        U41 = beta - 1
        eta = fractions.Fraction(
            numerator= 2 * A,
            denominator=2 * A12 + 3 * U12 + 3 * U41,
        )
        eta_max = 1 - fractions.Fraction(
            numerator=1,
            denominator=alpha * beta,
        )
        return dict(
            A=A,
            A12=A12,
            U12=U12,
            U41=U41,
            eta=eta,
            eta_f='%.3f' % eta,
            eta_max=eta_max,
            eta_max_f='%.3f' % eta_max,
        )


@variant.text('''
    Определите КПД цикла 12341, рабочим телом которого является идеальный одноатомный газ, если
    12 — изохорический нагрев в {alpha_text},
    23 — изобарическое расширение, при котором температура растёт в {beta_text},
    34 — изохора, 41 — изобара.

    Определите КПД цикла Карно, температура нагревателя которого равна максимальной температуре в цикле 12341, а холодильника — минимальной.
    Ответы в обоих случаях оставьте точными в виде нескоратимой дроби, никаких округлений.
''')
@variant.arg(alpha__alpha_text=n_times(2, 3, 4, 5, 6))
@variant.arg(beta__beta_text=n_times(2, 3, 4, 5, 6))
@variant.solution_space(360)
@variant.answer_align([
    'A_{ 12 } &= 0, \\Delta U_{ 12 } > 0, \\implies Q_{ 12 } = A_{ 12 } + \\Delta U_{ 12 } > 0.',
    'A_{ 23 } &> 0, \\Delta U_{ 23 } > 0, \\implies Q_{ 23 } = A_{ 23 } + \\Delta U_{ 23 } > 0,',
    'A_{ 34 } &= 0, \\Delta U_{ 34 } < 0, \\implies Q_{ 34 } = A_{ 34 } + \\Delta U_{ 34 } < 0,',
    'A_{ 41 } &< 0, \\Delta U_{ 41 } < 0, \\implies Q_{ 41 } = A_{ 41 } + \\Delta U_{ 41 } < 0.',

    'P_1V_1 &= \\nu R T_1, P_2V_2 = \\nu R T_2, P_3V_3 = \\nu R T_3, P_4V_4 = \\nu R T_4 \\text{  — уравнения состояния идеального газа },',

    '&\\text{ Пусть $P_0$, $V_0$, $T_0$ — давление, объём и температура в точке 1 (минимальные во всём цикле): }',
    'P_1 &= P_4 = P_0, P_2 = P_3, V_1 = V_2 = V_0, V_3 = V_4, \\text{ остальные соотношения между объёмами и давлениями не даны, нужно считать }',

    'T_2 &= {alpha}T_1 = {alpha}T_0 \\text{ (по условию) } \\implies \\frac{ P_2 }{ P_1 } = \\frac{ P_2V_0 }{ P_1V_0 } = \\frac{ P_2 V_2 }{ P_1 V_1 }'
    '= \\frac{ \\nu R T_2 }{ \\nu R T_1 } = \\frac{ T_2 }{ T_1 } = {alpha} \\implies P_2 = P_3 = {alpha} P_1 = {alpha} P_0,',
    'T_3 &= {beta}T_2 = {t}T_0 \\text{ (по условию) } \\implies \\frac{ V_3 }{ V_2 } = \\frac{ P_3V_3 }{ P_2V_2 }'
    '= \\frac{ \\nu R T_3 }{ \\nu R T_2 } = \\frac{ T_3 }{ T_2 } = {beta} \\implies V_3 = V_4 = {beta} V_2 = {beta} V_0.',

    'A_\\text{ цикл } &= ({beta}P_0 - P_0)({alpha}V_0 - V_0) = {A}P_0V_0,',
    'A_{ 23 } &= {alpha}P_0 * ({beta}V_0 - V_0) = {A23}P_0V_0,',

    '\\Delta U_{ 23 } &= \\frac 32 \\nu R T_3 - \\frac 32 \\nu R T_3 = \\frac 32 P_3 V_3 - \\frac 32 P_2 V_2'
    ' = \\frac 32 * {alpha} P_0 * {beta} V_0 -  \\frac 32 * {alpha} P_0 * V_0'
    ' = \\frac 32 * {U23} * P_0V_0,',

    '\\Delta U_{ 12 } &= \\frac 32 \\nu R T_2 - \\frac 32 \\nu R T_1 = \\frac 32 P_2 V_2 - \\frac 32 P_1 V_1'
    ' = \\frac 32 * {alpha} P_0 V_0 - \\frac 32 P_0 V_0'
    ' = \\frac 32 * {U12} * P_0V_0.',

    '\\eta &= \\frac{ A_\\text{ цикл } }{ Q_+ } = \\frac{ A_\\text{ цикл } }{ Q_{ 12 } + Q_{ 23 } } '
    ' = \\frac{ A_\\text{ цикл } }{ A_{ 12 } + \\Delta U_{ 12 } + A_{ 23 } + \\Delta U_{ 23 } } = ',
    ' &= \\frac{ {A}P_0V_0 }{ 0 + \\frac 32 * {U12} * P_0V_0 + {A23}P_0V_0 + \\frac 32 * {U23} * P_0V_0 }'
    ' = \\frac{ {A} }{ \\frac 32 * {U12} + {A23} + \\frac 32 * {U23} } = {eta:LaTeX} \\approx {eta_f}.',

    '\\eta_\\text{ Карно } &= 1 - \\frac{ T_\\text{ х } }{ T_\\text{ н } } = 1 - \\frac{ T_\\text{ 1 } }{ T_\\text{ 3 } }'
    ' = 1 - \\frac{ T_0 }{ {t}T_0 } = 1 - \\frac 1{ {t} }  = {eta_max:LaTeX} \\approx {eta_max_f}.'
])
class Rectangle_T(variant.VariantTask):
    def GetUpdate(self, alpha=None, beta=None, **kws):
        t = alpha * beta
        A = (alpha - 1) * (beta - 1)
        A23 = (beta - 1) * alpha
        U23 = (beta - 1) * alpha
        U12 = alpha - 1
        eta = Fraction() * 2 * A / (2 * A23 + 3 * U12 + 3 * U23)
        eta_max = Fraction() / (alpha * beta) * (-1) + 1
        return dict(
            t=t,
            A=A,
            A23=A23,
            U23=U23,
            U12=U12,
            eta=eta,
            eta_f='%.3f' % float(eta),
            eta_max=eta_max,
            eta_max_f='%.3f' % float(eta_max),
        )


@variant.text('''
    Определите КПД (оставив ответ точным в виде нескоратимой дроби) цикла 1231, рабочим телом которого является идеальный одноатомный газ, если
    \\begin{{itemize}}
        \\item 12 — изохорический нагрев в {alpha_text},
        \\item 23 — изобарическое расширение, при котором температура растёт в {beta_text},
        \\item 31 — процесс, график которого в $PV$-координатах является отрезком прямой.
    \\end{{itemize}}
    Бонус: замените цикл 1231 циклом, в котором 12 — изохорический нагрев в {alpha_text}, 23 — процесс, график которого в $PV$-координатах является отрезком прямой, 31 — изобарическое охлаждение, при котором температура падает в {alpha_text}.
''')
@variant.arg(alpha__alpha_text=n_times(2, 3, 4, 5, 6))
@variant.arg(beta__beta_text=n_times(2, 3, 4, 5, 6))
@variant.solution_space(360)
@variant.answer_align([
    'A_{ 12 } &= 0, \\Delta U_{ 12 } > 0, \\implies Q_{ 12 } = A_{ 12 } + \\Delta U_{ 12 } > 0.',
    'A_{ 23 } &> 0, \\Delta U_{ 23 } > 0, \\implies Q_{ 23 } = A_{ 23 } + \\Delta U_{ 23 } > 0,',
    'A_{ 31 } &= 0, \\Delta U_{ 31 } < 0, \\implies Q_{ 31 } = A_{ 31 } + \\Delta U_{ 31 } < 0.',

    'P_1V_1 &= \\nu R T_1, P_2V_2 = \\nu R T_2, P_3V_3 = \\nu R T_3 \\text{  — уравнения состояния идеального газа },',

    '&\\text{ Пусть $P_0$, $V_0$, $T_0$ — давление, объём и температура в точке 1 (минимальные во всём цикле): }',
    'P_1 &= P_0, P_2 = P_3, V_1 = V_2 = V_0, \\text{ остальные соотношения нужно считать }',

    'T_2 &= {alpha}T_1 = {alpha}T_0 \\text{ (по условию) } \\implies \\frac{ P_2 }{ P_1 } = \\frac{ P_2V_0 }{ P_1V_0 } = \\frac{ P_2 V_2 }{ P_1 V_1 }'
    '= \\frac{ \\nu R T_2 }{ \\nu R T_1 } = \\frac{ T_2 }{ T_1 } = {alpha} \\implies P_2 = {alpha} P_1 = {alpha} P_0,',
    'T_3 &= {beta}T_2 = {t}T_0 \\text{ (по условию) } \\implies \\frac{ V_3 }{ V_2 } = \\frac{ P_3V_3 }{ P_2V_2 }'
    '= \\frac{ \\nu R T_3 }{ \\nu R T_2 } = \\frac{ T_3 }{ T_2 } = {beta} \\implies V_3 = {beta} V_2 = {beta} V_0.',

    'A_\\text{ цикл } &= \\frac 12 ({beta}P_0 - P_0)({alpha}V_0 - V_0) = \\frac 12 * {A} * P_0V_0,',
    'A_{ 23 } &= {alpha}P_0 * ({beta}V_0 - V_0) = {A23}P_0V_0,',

    '\\Delta U_{ 23 } &= \\frac 32 \\nu R T_3 - \\frac 32 \\nu R T_2 = \\frac 32 P_3 V_3 - \\frac 32 P_2 V_2'
    ' = \\frac 32 * {alpha} P_0 * {beta} V_0 -  \\frac 32 * {alpha} P_0 * V_0'
    ' = \\frac 32 * {U23} * P_0V_0,',

    '\\Delta U_{ 12 } &= \\frac 32 \\nu R T_2 - \\frac 32 \\nu R T_1 = \\frac 32 P_2 V_2 - \\frac 32 P_1 V_1'
    ' = \\frac 32 * {alpha} P_0V_0 - \\frac 32 P_0V_0'
    ' = \\frac 32 * {U12} * P_0V_0.',

    '\\eta &= \\frac{ A_\\text{ цикл } }{ Q_+ } = \\frac{ A_\\text{ цикл } }{ Q_{ 12 } + Q_{ 23 } } '
    ' = \\frac{ A_\\text{ цикл } }{ A_{ 12 } + \\Delta U_{ 12 } + A_{ 23 } + \\Delta U_{ 23 } } = ',
    ' &= \\frac{ \\frac 12 * {A} * P_0V_0 }{ 0 + \\frac 32 * {U12} * P_0V_0 + {A23}P_0V_0 + \\frac 32 * {U23} * P_0V_0 }'
    ' = \\frac{ \\frac 12 * {A} }{ \\frac 32 * {U12} + {A23} + \\frac 32 * {U23} } = {eta:LaTeX} \\approx {eta_f}.',
])
@variant.answer_tex('''
    График процесса не в масштабе (эта часть пока не готова и сделать автоматически аккуратно сложно), но с верными подписями (а для решения этого достаточно):

    \\begin{ tikzpicture }[thick]
        \\draw[-{ Latex }] (0, 0) -- (0, 7) node[above left] { $P$ };
        \\draw[-{ Latex }] (0, 0) -- (10, 0) node[right] { $V$ };

        \\draw[dashed] (0, 2) node[left] { $P_1 = P_0$ } -| (3, 0) node[below] { $V_1 = V_2 = V_0$  };
        \\draw[dashed] (0, 6) node[left] { $P_2 = P_3 = {alpha}P_0$ } -| (9, 0) node[below] { $V_3 = {beta}V_0$ };

        \\draw (3, 2) node[above left]{ 1 } node[below left]{ $T_1 = T_0$ } 
               (3, 6) node[below left]{ 2 } node[above]{ $T_2 = {alpha}T_0$ } 
               (9, 6) node[above right]{ 3 } node[below right]{ $T_3 = {t}T_0$ };
        \\draw[midar] (3, 2) -- (3, 6);
        \\draw[midar] (3, 6) -- (9, 6);
        \\draw[midar] (9, 6) -- (3, 2);
    \\end{ tikzpicture }

    Решение бонуса:
    \\begin{ align* }
        A_{ 12 } &= 0, \\Delta U_{ 12 } > 0, \\implies Q_{ 12 } = A_{ 12 } + \\Delta U_{ 12 } > 0, \\\\
        A_{ 23 } &> 0, \\Delta U_{ 23 } \\text{  — ничего нельзя сказать, нужно исследовать отдельно }, \\\\
        A_{ 31 } &< 0, \\Delta U_{ 31 } < 0, \\implies Q_{ 31 } = A_{ 31 } + \\Delta U_{ 31 } < 0. \\\\
    \\end{ align* }

    Уравнения состояния идеального газа для точек 1, 2, 3: $P_1V_1 = \\nu R T_1, P_2V_2 = \\nu R T_2, P_3V_3 = \\nu R T_3$.
    Пусть $P_0$, $V_0$, $T_0$ — давление, объём и температура в точке 1 (минимальные во всём цикле).

    12 --- изохора, $\\frac{ P_1V_1 }{ T_1 } = \\nu R = \\frac{ P_2V_2 }{ T_2 }, V_2=V_1=V_0 \\implies \\frac{ P_1 }{ T_1 } =  \\frac{ P_2 }{ T_2 } \\implies P_2 = P_1 \\frac{ T_2 }{ T_1 } = {alpha}P_0$,

    31 --- изобара, $\\frac{ P_1V_1 }{ T_1 } = \\nu R = \\frac{ P_3V_3 }{ T_3 }, P_3=P_1=P_0 \\implies \\frac{ V_3 }{ T_3 } =  \\frac{ V_1 }{ T_1 } \\implies V_3 = V_1 \\frac{ T_3 }{ T_1 } = {alpha}V_0$,

    Таким образом, используя новые обозначения, состояния газа в точках 1, 2 и 3 описываются макропараметрами $(P_0, V_0, T_0), ({alpha}P_0, V_0, {alpha}T_0), (P_0, {alpha}V_0, {alpha}T_0)$ соответственно.

    \\begin{ tikzpicture }[thick]
        \\draw[-{ Latex }] (0, 0) -- (0, 7) node[above left] { $P$ };
        \\draw[-{ Latex }] (0, 0) -- (10, 0) node[right] { $V$ };

        \\draw[dashed] (0, 2) node[left] { $P_1 = P_3 = P_0$ } -| (9, 0) node[below] { $V_3 = {alpha}V_0$ };
        \\draw[dashed] (0, 6) node[left] { $P_2 = {alpha}P_0$ } -| (3, 0) node[below] { $V_1 = V_2 = V_0$ };

        \\draw[dashed] (0, 5) node[left] { $P$ } -| (4.5, 0) node[below] { $V$ };
        \\draw[dashed] (0, 4.6) node[left] { $P'$ } -| (5.1, 0) node[below] { $V'$ };

        \\draw (3, 2) node[above left]{ 1 } node[below left]{ $T_1 = T_0$ } 
               (3, 6) node[below left]{ 2 } node[above]{ $T_2 = {alpha}T_0$ } 
               (9, 2) node[above right]{ 3 } node[below right]{ $T_3 = {alpha}T_0$ };
        \\draw[midar] (3, 2) -- (3, 6);
        \\draw[midar] (3, 6) -- (9, 2);
        \\draw[midar] (9, 2) -- (3, 2);
        \\draw   (4.5, 5) node[above right]{ $T$ } (5.1, 4.6) node[above right]{ $T'$ };
    \\end{ tikzpicture }


    Теперь рассмотрим отдельно процесс 23, к остальному вернёмся позже. Уравнение этой прямой в $PV$-координатах: $P(V) = {a1}P_0 - \\frac{ P_0 }{ V_0 } V$.
    Это значит, что при изменении объёма на $\\Delta V$ давление изменится на $\\Delta P = - \\frac{ P_0 }{ V_0 } \\Delta V$, обратите внимание на знак.

    Рассмотрим произвольную точку в процессе 23 и дадим процессу ещё немного свершиться, при этом объём изменится на $\\Delta V$, давление — на $\\Delta P$, температура (иначе бы была гипербола, а не прямая) — на $\\Delta T$,
    т.е. из состояния $(P, V, T)$ мы перешли в $(P', V', T')$, причём  $P' = P + \\Delta P, V' = V + \\Delta V, T' = T + \\Delta T$.

    При этом изменится внутренняя энергия:
    \\begin{ align* }
    \\Delta U
        &= U' - U = \\frac 32 \\nu R T' - \\frac 32 \\nu R T = \\frac 32 (P+\\Delta P) (V+\\Delta V) - \\frac 32 PV\\\\
        &= \\frac 32 ((P+\\Delta P) (V+\\Delta V) - PV) = \\frac 32 (P\\Delta V + V \\Delta P + \\Delta P \\Delta V).
    \\end{ align* }

    Рассмотрим малые изменения объёма, тогда и изменение давления будем малым (т.к. $\\Delta P = - \\frac{ P_0 }{ V_0 } \\Delta V$),
    а третьим слагаемым в выражении для $\\Delta U$  можно пренебречь по сравнению с двумя другими:
    два первых это малые величины, а третье — произведение двух малых.
    Тогда $\\Delta U = \\frac 32 (P\\Delta V + V \\Delta P)$.

    Работа газа при этом малом изменении объёма — это площадь трапеции (тут ещё раз пренебрегли малым слагаемым):
    $$A = \\frac{ P + P\' }2 \\Delta V = \\cbr{ P + \\frac{ \\Delta P }2 } \\Delta V = P \\Delta V.$$

    Подведённое количество теплоты, используя первое начало термодинамики, будет равно
    \\begin{ align* }
    Q
        &= \\frac 32 (P\\Delta V + V \\Delta P) + P \\Delta V =  \\frac 52 P\\Delta V + \\frac 32 V \\Delta P = \\\\
        &= \\frac 52 P\\Delta V + \\frac 32 V * \\cbr{ - \\frac{ P_0 }{ V_0 } \\Delta V } = \\frac{ \\Delta V }2 * \\cbr{ 5P - \\frac{ P_0 }{ V_0 } V } = \\\\
        &= \\frac{ \\Delta V }2 * \\cbr{ 5 * \\cbr{ {a1}P_0 - \\frac{ P_0 }{ V_0 } V } - \\frac{ P_0 }{ V_0 } V }
         = \\frac{ \\Delta V * P_0 }2 * \\cbr{ 5 * {a1} - 8\\frac{ V }{ V_0 } }.
    \\end{ align* }

    Таком образом, знак количества теплоты $Q$ на участке 23 зависит от конкретного значения $V$:
    \\begin{ itemize }
        \\item $\\Delta V > 0$ на всём участке 23, поскольку газ расширяется,
        \\item $P > 0$ — всегда, у нас идеальный газ, удары о стенки сосуда абсолютно упругие, а молекулы не взаимодействуют и поэтому давление только положительно,
        \\item если $5 * {a1} - 8\\frac{ V }{ V_0 } > 0$ — тепло подводят, если же меньше нуля — отводят.
    \\end{ itemize }
    Решая последнее неравенство, получаем конкретное значение $V^*$: при $V < V^*$ тепло подводят, далее~— отводят.
    Тут *~--- некоторая точка между точками 2 и 3, конкретные значения надо досчитать:
    $$V^* = V_0 * \\frac{ 5 * {a1} }8 = {V_star:LaTeX} * V_0 \\implies P^* = {a1}P_0 - \\frac{ P_0 }{ V_0 } V^* = \\ldots = {P_star:LaTeX} * P_0.$$

    Т.е. чтобы вычислить $Q_+$, надо сложить количества теплоты на участке 12 и лишь части участка 23 — участке 2*,
    той его части где это количество теплоты положительно. Имеем: $Q_+ = Q_{ 12 } + Q_{ 2* }$.

    Теперь возвращаемся к циклу целиком и получаем:
    \\begin{ align* }
    A_\\text{ цикл } &= \\frac 12 * ({alpha}P_0 - P_0) * ({alpha}V_0 - V_0) = {A_bonus_cycle:LaTeX} * P_0V_0, \\\\
    A_{ 2* } &= \\frac{ P^* + {alpha}P_0 }2 * (V^* - V_0)
        = \\frac{ {P_star:LaTeX} * P_0 + {alpha}P_0 }2 * \\cbr{ {V_star:LaTeX} * V_0 - V_0 }
        = \\ldots = {A_bonus_plus:LaTeX} * P_0 V_0, \\\\
    \\Delta U_{ 2* } &= \\frac 32 \\nu R T^* - \\frac 32 \\nu R T_2 = \\frac 32 (P^*V^* - P_0 * {alpha}V_0)
        = \\frac 32 \\cbr{ {P_star:LaTeX} * P_0 * {V_star:LaTeX} * V_0 - P_0 * {alpha}V_0 }
        = {U_bonus_plus:LaTeX} * P_0 V_0, \\\\
    \\Delta U_{ 12 } &= \\frac 32 \\nu R T_2 - \\frac 32 \\nu R T_1 = \\frac 32 ({alpha}P_0V_0 - P_0V_0) = \\ldots = {U_bonus_12:LaTeX} * P_0 V_0, \\\\
    \\eta &= \\frac{ A_\\text{ цикл } }{ Q_+ } = \\frac{ A_\\text{ цикл } }{ Q_{ 12 } + Q_{ 2* } }
        = \\frac{ A_\\text{ цикл } }{ A_{ 12 } + \\Delta U_{ 12 } + A_{ 2* } + \\Delta U_{ 2* } } = \\\\
        &= \\frac{ {A_bonus_cycle:LaTeX} * P_0V_0 }{ 0 + {U_bonus_12:LaTeX} * P_0 V_0 + {A_bonus_plus:LaTeX} * P_0 V_0 + {U_bonus_plus:LaTeX} * P_0 V_0 }
         = \\frac{ {A_bonus_cycle:LaTeX} }{ {U_bonus_12:LaTeX} + {A_bonus_plus:LaTeX} + {U_bonus_plus:LaTeX} }
         = {eta_bonus:LaTeX} \\leftarrow \\text{ вжух и готово! }
    \\end{ align* }
'''
)
class TriangleUp_T(variant.VariantTask):
    def GetUpdate(self, alpha=None, beta=None, **kws):
        t = alpha * beta
        A = (alpha - 1) * (beta - 1)
        A23 = (beta - 1) * alpha
        U23 = (beta - 1) * alpha
        U12 = alpha - 1
        eta = Fraction() * A / (2 * A23 + 3 * U12 + 3 * U23)

        a1 = alpha + 1
        A_bonus_cycle = Fraction() * (alpha - 1) ** 2 / 2
        A_bonus_plus = Fraction() * (11 * alpha + 3) * (5 * alpha - 3) / (16 * 8)
        U_bonus_plus = (Fraction() * 15 * (alpha + 1) ** 2 / 64 - alpha) * 3 / 2
        U_bonus_12 = Fraction() * (alpha - 1) / 1 * 3 / 2
        eta_bonus = Fraction() * A_bonus_cycle / (U_bonus_plus + A_bonus_plus + U_bonus_12)
        V_star = Fraction() * (alpha + 1) * 5 / 8
        P_star = Fraction() * (alpha + 1) * 3 / 8
        # a1=42
        # A_bonus_cycle=Fraction() * 42 / 23
        # A_bonus_plus=Fraction() * 42 / 23
        # U_bonus_plus=Fraction() * 42 / 23
        # U_bonus_12=Fraction() * 42 / 23
        # eta_bonus=Fraction() * 42 / 23
        # V_star=Fraction() * 42 / 23
        # P_star=Fraction() * 42 / 23

        return dict(
            t=t,
            A=A,
            A23=A23,
            U23=U23,
            U12=U12,
            eta=eta,
            eta_f='%.3f' % eta,
            a1=a1,
            A_bonus_cycle=A_bonus_cycle,
            A_bonus_plus=A_bonus_plus,
            U_bonus_plus=U_bonus_plus,
            U_bonus_12=U_bonus_12,
            eta_bonus=eta_bonus,
            V_star=V_star,
            P_star=P_star,
        )



@variant.text('''
    Определите КПД (оставив ответ точным в виде нескоратимой дроби) цикла 1231, рабочим телом которого является идеальный одноатомный газ, если
    \\begin{{itemize}}
        \\item 12 — изобарическое расширение,
        \\item 23 — процесс, график которого в $PV$-координатах является отрезком прямой, а объём уменьшается в {beta_text},
        \\item 31 — изохорический нагрев с увеличением давления в {alpha_text},
    \\end{{itemize}}
''')
@variant.arg(alpha__alpha_text=n_times(2, 3, 4, 5, 6))
@variant.arg(beta__beta_text=n_times(2, 3, 4, 5, 6))
@variant.solution_space(360)
@variant.answer_align([
    'A_{ 12 } &> 0, \\Delta U_{ 12 } > 0, \\implies Q_{ 12 } = A_{ 12 } + \\Delta U_{ 12 } > 0.',
    'A_{ 23 } &< 0, \\Delta U_{ 23 } < 0, \\implies Q_{ 23 } = A_{ 23 } + \\Delta U_{ 23 } < 0,',
    'A_{ 31 } &= 0, \\Delta U_{ 31 } > 0, \\implies Q_{ 31 } = A_{ 31 } + \\Delta U_{ 31 } > 0.',

    'P_1V_1 &= \\nu R T_1, P_2V_2 = \\nu R T_2, P_3V_3 = \\nu R T_3 \\text{  — уравнения состояния идеального газа },',

    '&\\text{ Пусть $P_0$, $V_0$, $T_0$ — давление, объём и температура в точке 3 (минимальные во всём цикле): }',
    'P_3 &= P_0, P_1 = P_2 = {alpha}P_0, V_1 = V_3 = V_0, V_2 = {beta}V_3 = {beta}V_0',

    'A_\\text{ цикл } &= \\frac 12 (P_2-P_1)(V_1-V_2) = \\frac 12 ({alpha}P_0 - P_0)({beta}V_0 - V_0) = \\frac 12 * {A} * P_0V_0,',
    'A_{ 12 } &= {beta}P_0 * ({alpha}V_0 - V_0) = {A12}P_0V_0,',

    '\\Delta U_{ 12 } &= \\frac 32 \\nu R T_2 - \\frac 32 \\nu R T_1 = \\frac 32 P_2 V_2 - \\frac 32 P_1 V_1'
    ' = \\frac 32 * {alpha} P_0 * {beta} V_0 -  \\frac 32 * {beta} P_0 * V_0'
    ' = \\frac 32 * {U12} * P_0V_0,',

    '\\Delta U_{ 31 } &= \\frac 32 \\nu R T_1 - \\frac 32 \\nu R T_3 = \\frac 32 P_1 V_1 - \\frac 32 P_3 V_3'
    ' = \\frac 32 * {alpha} P_0V_0 - \\frac 32 P_0V_0'
    ' = \\frac 32 * {U31} * P_0V_0.',

    '\\eta &= \\frac{ A_\\text{ цикл } }{ Q_+ } = \\frac{ A_\\text{ цикл } }{ Q_{ 12 } + Q_{ 31 } } '
    ' = \\frac{ A_\\text{ цикл } }{ A_{ 12 } + \\Delta U_{ 12 } + A_{ 31 } + \\Delta U_{ 31 } } = ',
    ' &= \\frac{ \\frac 12 * {A} * P_0V_0 }{ {A12}P_0V_0 + \\frac 32 * {U12} * P_0V_0 + 0 + \\frac 32 * {U31} * P_0V_0 }'
    ' = \\frac{ \\frac 12 * {A} }{ {A12} + \\frac 32 * {U12} + \\frac 32 * {U31} } = \\frac{ {eta.numerator} }{ {eta.denominator} } \\approx {eta_f}.',
])
class TriangleUp(variant.VariantTask):
    def GetUpdate(self, alpha=None, beta=None, **kws):
        t = alpha * beta
        A = (alpha - 1) * (beta - 1)
        A12 = (alpha - 1) * beta
        U12 = (alpha - 1) * beta
        U31 = alpha - 1
        eta = fractions.Fraction(
            numerator=A,
            denominator=2 * A12 + 3 * U31 + 3 * U12,
        )
        return dict(
            t=t,
            A=A,
            A12=A12,
            U12=U12,
            U31=U31,
            eta=eta,
            eta_f='%.3f' % eta,
        )
