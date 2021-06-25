import generators.variant as variant
from generators.helpers import UnitValue, Consts


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
@variant.arg(v_1=['количество теплоты', 'изменение внутренней энергии'])
@variant.arg(v_2=['работа газа', 'работа внешних сил'])
@variant.arg(v_3=['молярная теплоёмкость', 'удельная теплоёмкость'])
@variant.arg(v_4=['первое начало термодинамики', 'внутренняя энергия идеального одноатомного газа'])
class Definitions01(variant.VariantTask):
    pass


@variant.solution_space(20)
@variant.text('''
    Запишите формулы и рядом с каждой физичической величиной укажите её название и единицы измерения в СИ:
    \\begin{enumerate}
        \\item первое начало термодинамики,
        \\item внутренняя энергия идеального одноатомного газа.
    \\end{enumerate}
''')
@variant.no_args
class Definitions02(variant.VariantTask):
    pass


@variant.text('''
    Сколько льда при температуре $0\\celsius$ можно расплавить,
    сообщив ему энергию {Q:Value:e}?
    Здесь (и во всех следующих задачах) используйте табличные значения из учебника.
''')
@variant.answer_short('''
    Q
        = \\lambda m \\implies m
        = \\frac Q{\\lambda}
        = \\frac {Q:Value:s}{lmbd:Value:s}
        \\approx {m:Value}
''')
@variant.arg(Q=['Q = %d МДж' % Q for Q in [2, 3, 4, 5, 6, 7, 8, 9]])
class Ch_8_6(variant.VariantTask):
    def GetUpdate(self, Q=None, **kws):
        lmbd = Consts.water.lmbd
        return dict(
            lmbd=lmbd,
            m='m = %.1f кг' % (1000. * Q.Value / lmbd.Value),
        )


@variant.text('''
    Какое количество теплоты выделится при затвердевании {m:Value:e} расплавленного {metall} при температуре плавления?
''')
@variant.answer_short('''
    Q
        = - \\lambda m
        = - {lmbd:Value} * {m:Value}
        = - {Q:Value} \\implies \\abs{Q:L:s} = {Q:Value}
''')
@variant.arg(metall__lmbd=[
    ('свинца', Consts.lead.lmbd),
    ('меди', Consts.copper.lmbd),
    ('алюминия', Consts.aluminum.lmbd),
    ('стали', Consts.steel.lmbd),
])
@variant.arg(m=['m = %d кг' % m for m in [15, 20, 25, 30, 50, 75]])
class Ch_8_7(variant.VariantTask):
    def GetUpdate(self, m=None, metall=None, lmbd=None, **kws):
        return dict(
            Q='Q = %.1f МДж' % (0.001 * m.Value * lmbd.Value),
        )


@variant.text('''
    Какое количество теплоты необходимо для превращения воды массой {m:Value:e} при $t = {t}\\celsius$
    в пар при температуре $t_{100} = 100\\celsius$?
''')
@variant.answer_short('''
    Q
        = cm\\Delta t + Lm
        = m\\cbr{c(t_{100} - t) + L}
        = {m:Value} * \\cbr{{c:Value}\\cbr{100\\celsius - {t}\\celsius} + {L:Value}}
        = {Q:Value}
''')
@variant.arg(m=['m = %d кг' % m for m in [2, 3, 4, 5, 15]])
@variant.arg(t=[20, 30, 40, 50, 60, 70])
class Ch_8_10(variant.VariantTask):
    def GetUpdate(self, m=None, t=None, **kws):
        c = Consts.water.c
        L = Consts.water.L
        return dict(
            c=c,
            L=L,
            Q='Q = %.2f МДж' % (m.Value * ((100. - t) * c.Value / 10 ** 6 + L.Value)),
        )


@variant.text('''
    Воду температурой $t = {t}\\celsius$ нагрели и превратили в пар при температуре $t_{100} = 100\\celsius$,
    потратив {Q:Value:e}. Определите массу воды.
''')
@variant.answer_short('''
    Q
        = cm\\Delta t + Lm
        = m\\cbr{c(t_{100} - t) + L}
    \\implies
    m = \\frac Q{c(t_{100} - t) + L}
        = \\frac {Q:Value:s}{{c:Value}\\cbr{100\\celsius - {t}\\celsius} + {L:Value}}
        \\approx {m:Value}
''')
@variant.arg(Q=['Q = %d кДж' % Q for Q in [2000, 2500, 4000, 5000]])
@variant.arg(t=[10, 30, 40, 50, 60, 70])
class Ch_8_13(variant.VariantTask):
    def GetUpdate(self, Q=None, t=None, **kws):
        c =  Consts.water.c
        L = Consts.water.L
        return dict(
            c=c,
            L=L,
            m='Q = %.2f кг' % (1000. * Q.Value / ((100. - t) * c.Value + 1. * L.Value * 10 ** 6)),
        )


@variant.text('''
    {metall} тело температурой $T = {T}\\celsius$ опустили
    в воду температурой $t = {t}\\celsius$, масса которой равна массе тела.
    Определите, какая температура установится в сосуде.
''')
@variant.answer_align([
    'Q_1 + Q_2 &= 0, ',
    'Q_1 &= c_1 m_1 \\Delta t_1 = c_1 m (\\theta - t_1), ',
    'Q_2 &= c_2 m_2 \\Delta t_2 = c_2 m (\\theta - t_2), ',
    'c_1 m (\\theta - t_1) + c_2 m (\\theta - t_2) &= 0, ',
    'c_1 (\\theta - t_1) + c_2 (\\theta - t_2) &= 0, ',
    'c_1 \\theta - c_1 t_1 + c_2 \\theta - c_2 t_2 &= 0, ',
    '(c_1 + c_2)\\theta &= c_1 t_1 + c_2 t_2, ',
    '''\\theta &= \\frac{c_1 t_1 + c_2 t_2}{c_1 + c_2}
        = \\frac{{c1:Value} * {t1}\\celsius + {c2:Value} *  {t2}\\celsius}{{c1:Value} + {c2:Value}}
        \\approx {theta} \\celsius.''',
])
@variant.arg(metall__c=[
    ('Стальное', Consts.steel.c),
    ('Алюминиевое', Consts.aluminum.c),
    ('Цинковое', Consts.zinc.c),
])
@variant.arg(T=[70, 80, 90, 100])
@variant.arg(t=[10, 20, 30])
class Ch_8_35(variant.VariantTask):
    def GetUpdate(self, metall=None, T=None, t=None, c=None, **kws):
        c_water = Consts.water.c
        return dict(
            c1=c_water,
            c2=c,
            t1=t,
            t2=T,
            theta='%.1f' % ((1. * c_water.Value * t + 1. * c.Value * T) / (1. * c_water.Value + 1. * c.Value)),
        )


@variant.solution_space(40)
@variant.text('''
    Определите давление одноатомного идеального газа, занимающего объём {V:Value:e},
    если его внутренняя энергия составляет {U:Value:e}.
''')
@variant.arg(V=('V = {} л', [2, 3, 4, 5, 6]))
@variant.arg(U=('U = {} Дж', [250, 300, 400, 500]))
@variant.answer_short(
    'U = \\frac 32 \\nu R T = \\frac 32 PV \\implies P = \\frac 23 * \\frac UV'
    '= \\frac 23 * \\frac{U:V:s}{V:V:s} \\approx {P:V}.'
)
class P_from_V_and_U(variant.VariantTask):
    def GetUpdate(self, U=None, V=None, **kws):
        return dict(
            P='%.2d кПа' % (2 / 3 * U.Value / V.Value),
        )


@variant.solution_space(40)
@variant.text('''
    Определите объём идеального одноатомного газа,
    если его внутренняя энергия при давлении {P:Value:e} составляет {U:Value:e}.
    {Consts.p_atm:Task:e}.
''')
@variant.arg(P=('P = {} атм', [2, 3, 4, 5, 6]))
@variant.arg(U=('U = {} кДж', [250, 300, 400, 500]))
@variant.answer_short(
    'U = \\frac 32 \\nu R T = \\frac 32 PV \\implies V = \\frac 23 * \\frac UP'
    '= \\frac 23 * \\frac{U:V:s}{P:V:s} \\approx {V:V}.'
)
class V_from_P_and_U(variant.VariantTask):
    def GetUpdate(self, U=None, P=None, **kws):
        return dict(
            V='%.2f м^3' % (2 / 3 * U.Value * 1000 / P.Value / 100000),
        )



@variant.solution_space(40)
@variant.text('''
    Газ расширился от {V1:Value:e} до {V2:Value:e}.
    Давление газа при этом оставалось постоянным и равным {P:Value:e}.
    Определите работу газа, ответ выразите в килоджоулях. {Consts.p_atm:Task:e}.
''')
@variant.arg(V1=('V_1 = {} л', [150, 200, 250, 350]))
@variant.arg(V2=('V_2 = {} л', [450, 550, 650]))
@variant.arg(P=('P = {} атм', [1.2, 1.5, 1.8, 2.5, 3.5]))
@variant.answer_short(
    'A = P\\Delta V = P(V_2 - V_1) = {P:V} * \\cbr{{V2:V} - {V1:V}} = {A:V}.'
)
class A_on_P_const(variant.VariantTask):
    def GetUpdate(self, P=None, V1=None, V2=None, **kws):
        return dict(
            A='%.1f кДж' % (P.Value * 100000 * (V2.Value - V1.Value) / 1000 / 1000),
        )


@variant.solution_space(80)
@variant.text('''
    Как изменилась внутренняя энергия одноатомного идеального газа при переходе из состояния 1 в состояние 2?
    {P1:Task:e}, {V1:Task:e}, {P2:Task:e}, {V2:Task:e}.
    Как изменилась при этом температура газа?
''')
@variant.arg(P1=('P_1 = {} МПа', [2, 3, 4]))
@variant.arg(P2=('P_2 = {} МПа', [1.5, 2.5, 3.5, 4.5]))
@variant.arg(V1=('V_1 = {} л', [3, 5, 7]))
@variant.arg(V2=('V_2 = {} л', [2, 4, 6, 8]))
@variant.answer_align([
    'P_1V_1 &= \\nu R T_1, P_2V_2 = \\nu R T_2,',
    '\\Delta U &= U_2-U_1 = \\frac 32 \\nu R T_2- \\frac 32 \\nu R T_1 = \\frac 32 P_2 V_2 - \\frac 32 P_1 V_1'
    '= \\frac 32 * \\cbr{{P2:V} * {V2:V} - {P1:V} * {V1:V}} = {dU:V}.',
    '\\frac{T_2}{T_1} &= \\frac{\\frac{P_2V_2}{\\nu R}}{\\frac{P_1V_1}{\\nu R}} = \\frac{P_2V_2}{P_1V_1}'
    '= \\frac{{P2:V} * {V2:V}}{{P1:V} * {V1:V}} \\approx {ratio}.',
])
class DeltaU_on_P_const(variant.VariantTask):
    def GetUpdate(self, P1=None, P2=None, V1=None, V2=None, **kws):
        return dict(
            dU='%d Дж' % (1000 * 3 / 2 * (P2.Value * V2.Value - P1.Value * V1.Value)),
            ratio='%.2f' % (1. * P2.Value * V2.Value / (P1.Value * V1.Value)),
        )


@variant.solution_space(40)
@variant.text('''
    {nu:V:e} идеального одноатомного газа {what} на {dT:V:e}.
    Определите изменение внутренней энергии газа. Увеличилась она или уменьшилась?
    Универсальная газовая постоянная {Consts.R:Task:e}.
''')
@variant.arg(what__sign=[('нагрели', +1), ('охладили', -1)])
@variant.arg(nu=('\\nu = {} моль', [2, 3, 4, 5]))
@variant.arg(dT=('\\Delta T = {} К', [10, 20, 30]))
@variant.answer_short('''
    \\Delta U = \\frac 32 \\nu R {dT:Letter}
        = {sgn} \\frac 32 * {nu:V} * {Consts.R:V} * {dT:V}
        = {dU:V}. \\text{{ans}.}
''')
class DeltaU_from_DeltaT(variant.VariantTask):
    def GetUpdate(self, what=None, sign=None, nu=None, dT=None, **kws):
        return dict(
            sgn='-' if sign == -1 else '',
            dU='%d Дж' % (3 / 2 * nu.Value * Consts.R.Value * dT.Value * sign),
            ans='Увеличилась' if sign == 1 else 'Уменьшилась',
        )


@variant.solution_space(40)
@variant.text('''
    {nu:V:e} идеального одноатомного газа в результате адиабатического процесса {what} на {dT:V:e}.
    Определите работу газа. Кто совершил положительную работу: газ или внешние силы?
    Универсальная газовая постоянная {Consts.R:Task:e}.
''')
@variant.arg(what__sign=[('нагрелись', +1), ('остыли', -1)])
@variant.arg(nu=('\\nu = {} моль', [30, 40, 50, 60]))
@variant.arg(dT=('\\Delta T = {} К', [15, 25, 45, 60, 80, 120]))
@variant.answer_align([
    'Q &= 0, Q = \\Delta U + A_\\text{газа} \\implies',
    '\\implies A_\\text{газа} &= - \\Delta U = - \\frac 32 \\nu R \\Delta T '
    '= {sgn} \\frac 32 * {nu:V} * {Consts.R:V} * {dT:V}'
    '= {A:V}, \\text{{ans}.}'
])
class A_from_DeltaT(variant.VariantTask):
    def GetUpdate(self, what=None, sign=None, nu=None, dT=None, **kws):
        return dict(
            sgn='' if sign == -1 else '-',
            A='%.1f кДж' % (- 3 / 2 * nu.Value * Consts.R.Value * dT.Value * sign / 1000),
            ans='внешние силы' if sign == 1 else 'газ',
        )


@variant.solution_space(60)
@variant.text('''
    Газу сообщили некоторое количество теплоты,
    при этом {ratio} его он потратил на совершение работы,
    одновременно увеличив свою внутреннюю энергию на {dU:V:e}.
    Определите {what}.
''')
@variant.arg(ratio__N=[('половину', 2), ('треть', 3), ('четверть', 4)])
@variant.arg(dU=('\\Delta U = {} Дж', [1200, 1500, 2400, 3000]))
@variant.arg(what=['количество теплоты, сообщённое газу', 'работу, совершённую газом'])
@variant.answer_align([
    '''Q &= A' + \\Delta U, A' = \\frac 1{N} Q \\implies Q * \\cbr{1 - \\frac 1{N}} = \\Delta U \\implies '''
    '''Q = \\frac{\\Delta U}{1 - \\frac 1{N}} = \\frac{dU:V:s}{1 - \\frac 1{N}} \\approx {Q:V}.''',
    '''A' &= \\frac 1{N} Q
    = \\frac 1{N} * \\frac{\\Delta U}{1 - \\frac 1{N}}
    = \\frac{\\Delta U}{{N} - 1}
    = \\frac{dU:V:s}{{N} - 1} \\approx {A:V}.''',
])
class Q_from_DeltaU(variant.VariantTask):
    def GetUpdate(self, N=None, dU=None, **kws):
        return dict(
            Q='%d Дж' % (dU.Value * N / (N - 1)),
            A='%d Дж' % (dU.Value / (N - 1)),
        )


@variant.solution_space(40)
@variant.text('''
    В некотором процессе {who} работу {A:V:e},
    при этом его внутренняя энергия {what} на {dU:V:e}.
    Определите количество тепла, переданное при этом процессе газу.
    Явно пропишите, подводили газу тепло или же отводили.
''')
@variant.arg(who__sign_who=[('внешние силы совершили над газом', -1), ('газ совершил', +1)])
@variant.arg(what__sign_what=[('увеличилась', +1), ('уменьшилась', -1)])
@variant.arg(dU=('\\Delta U = {} Дж', [150, 250, 350, 450]))
@variant.arg(A=('{} Дж', [100, 200, 300]))
@variant.answer_short('''
    Q = A_\\text{газа} + \\Delta U, A_\\text{газа} = -A_\\text{внешняя}
    \\implies Q = A_\\text{газа} + \\Delta U = {sign_who} {A:V} + {sign_what} {dU:V} = {Q:V}.
    \\text{{ans}.}
''')
class Q_from_DeltaU_and_A(variant.VariantTask):
    def GetUpdate(self, A=None, dU=None, what=None, sign_what=None, who=None, sign_who=None, **kws):
        Q = dU.Value * sign_what + A.Value * sign_who
        return dict(
            Q='%d Дж' % Q,
            ans=' Подводили' if Q > 0 else ' Отводили',
            sign_who='-' if sign_who == -1 else '',
            sign_what='-' if sign_what == -1 else '',
        )


@variant.text('''
    Укажите, верны ли утверждения («да» или «нет» слева от каждого утверждения):
    \\begin{enumerate}
        \\item При {q1} расширении идеальный газ совершает ровно столько работы, сколько внутренней энергии теряет.
        % \\item В силу третьего закона Ньютона, совершённая газом работа и работа, совершённая над ним, всегда равны по модулю и противоположны по знаку.
        \\item Работу газа в некотором процессе можно вычислять как площадь под графиком в системе координат {q3}, главное лишь правильно расположить оси.
        % \\item Дважды два {q4}.
        \\item При {q5} процессе внутренняя энергия идеального одноатомного газа не изменяется, даже если ему подводят тепло.
        \\item Газ может совершить ненулевую работу в {q6} процессе.
        % \\item Адиабатический процесс лишь по воле случая не имеет приставки «изо»: в нём изменяются давление, температура и объём, но это не все макропараметры идеального газа.
        \\item Полученное выражение для внутренней энергии идеального газа ($\\frac 32 \\nu RT$) применимо к {q8} газу, при этом, например, уравнение состояния идеального газа применимо независимо от числа атомов в молекулах газа.
    \\end{enumerate}
''')
@variant.arg(q1__a1=[('адиабатическом', 'да'), ('изобарном', 'нет')])
@variant.arg(q3__a3=[('$PV$', 'да'), ('$VT$', 'нет'), ('$PT$', 'нет')])
@variant.arg(q4__a4=[('три', 'нет'), ('четыре', 'да'), ('пять', 'нет')])
@variant.arg(q5__a5=[('изохорном', 'нет'), ('изобарном', 'нет'), ('изотермическом', 'да')])
@variant.arg(q6__a6=[('изохорном', 'нет'), ('изобарном', 'да'), ('изотермическом', 'да')])
@variant.arg(q8__a8=[('одноатомному', 'да'), ('двухоатомному', 'нет'), ('трёхатомному', 'нет')])
@variant.solution_space(0)
# @variant.answer_short('''\\text{{a1}, да, {a3}, {a4}, да, нет, да, {a8}}''')
@variant.answer_short('''\\text{{a1}, {a3}, {a5}, {a6}, {a8}}''')
class YesNo(variant.VariantTask):
    pass


@variant.solution_space(150)
@variant.text('''
    Порция идеального одноатомного газа перешла из состояния 1 в состояние 2: {P1:Task:e}, {V1:Task:e}, {P2:Task:e}, {V2:Task:e}.
    Известно, что в $PV$-координатах график процесса 12 представляет собой отрезок прямой.
    Определите,
    \\begin{itemize}
        \\item какую работу при этом совершил газ,
        \\item чему равно изменение внутренней энергии газа,
        \\item сколько теплоты подвели к нему в этом процессе?
    \\end{itemize}
    При решении обратите внимание на знаки искомых величин.
''')
@variant.arg(P1=('P_1 = {} МПа', [2, 3, 4]))
@variant.arg(P2=('P_2 = {} МПа', [1.5, 2.5, 3.5, 4.5]))
@variant.arg(V1=('V_1 = {} л', [3, 5, 7]))
@variant.arg(V2=('V_2 = {} л', [2, 4, 6, 8]))
@variant.answer_align([
    'P_1V_1 &= \\nu R T_1, P_2V_2 = \\nu R T_2,',
    '\\Delta U &= U_2-U_1 = \\frac 32 \\nu R T_2- \\frac 32 \\nu R T_1 = \\frac 32 P_2 V_2 - \\frac 32 P_1 V_1'
    '= \\frac 32 * \\cbr{{P2:V} * {V2:V} - {P1:V} * {V1:V}} = {dU:V}.',
    'A_\\text{газа} &= \\frac{P_2 + P_1} 2 * (V_2 - V_1) = \\frac{{P2:V} + {P1:V}} 2 * ({V2:V} - {V1:V}) = {A:V},',
    'Q &= A_\\text{газа} + \\Delta U = \\frac 32 (P_2 V_2 - P_1 V_1) + \\frac{P_2 + P_1} 2 * (V_2 - V_1) = {dU:V} + {A:V} = {Q:V}.'
])
class DeltaQ_from_states(variant.VariantTask):
    def GetUpdate(self, P1=None, P2=None, V1=None, V2=None, **kws):
        A = (1000 * 1 / 2 * (P2.Value + P1.Value) * (V2.Value - V1.Value))
        dU = (1000 * 3 / 2 * (P2.Value * V2.Value - P1.Value * V1.Value))
        return dict(
            A='%.2f кДж' % (A / 1000),
            dU=('%.2f кДж' % (dU / 1000)) if dU else '0 кДж',
            Q='%.2f кДж' % ((A + dU) / 1000),
        )
