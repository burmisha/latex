import generators.variant as variant
from generators.helpers import UnitValue, n_times


@variant.text('''
    Если батарею замкнуть на резистор сопротивлением $R_1$, то в цепи потечёт ток $\\eli_1$,
    а если на другой $R_2$ — то $\\eli_2$. Определите:
    \\begin{itemize}
        \\item ЭДС батареи,
        \\item внутреннее сопротивление батареи,
        \\item ток короткого замыкания.
    \\end{itemize}
''')
@variant.no_args
@variant.answer_tex('''
    Запишем закон Ома для полной цепи 2 раза для обоих способов подключения (с $R_1$ и с $R_2$),
    а короткое замыкание рассмотрим позже. Отметим, что для такой простой схемы он совпадает
    с законом Кирхгофа. Получим систему из 2 уравнений и 2 неизвестных, решим в удобном порядке,
    ибо нам всё равно понадобятся обе.

    \\begin{align*}
        &\\begin{cases}
            \\ele = \\eli_1(R_1 + r), \\\\
            \\ele = \\eli_2(R_2 + r); \\\\
        \\end{cases} \\\\
        &\\eli_1(R_1 + r) = \\eli_2(R_2 + r), \\\\
        &\\eli_1 R_1 + \\eli_1r = \\eli_2 R_2 + \\eli_2r, \\\\
        &\\eli_1 R_1 - \\eli_2 R_2 = - \\eli_1r  + \\eli_2r = (\\eli_2 - \\eli_1)r, \\\\
        r &= \\frac{\\eli_1 R_1 - \\eli_2 R_2}{\\eli_2 - \\eli_1}
            \\equiv \\frac{\\eli_2 R_2 - \\eli_1 R_1}{\\eli_1 - \\eli_2}, \\\\
        \\ele &= \\eli_1(R_1 + r)
            = \\eli_1\\cbr{R_1 + \\frac{\\eli_1 R_1 - \\eli_2 R_2}{\\eli_2 - \\eli_1}}
            = \\eli_1 * \\frac{R_1\\eli_2 - R_1\\eli_1 + \\eli_1 R_1 - \\eli_2 R_2}{\\eli_2 - \\eli_1} \\\\
            &= \\eli_1 * \\frac{R_1\\eli_2 - \\eli_2 R_2}{\\eli_2 - \\eli_1}
            = \\frac{\\eli_1 \\eli_2 (R_1 - R_2)}{\\eli_2 - \\eli_1}
            \\equiv \\frac{\\eli_1 \\eli_2 (R_2 - R_1)}{\\eli_1 - \\eli_2}.
    \\end{align*}

    Короткое замыкание происходит в ситуации, когда внешнее сопротивление равно 0
    (при этом цепь замкнута, хотя нагрузки и нет вовсе):
    $$
        \\eli_\\text{к. з.} = \\frac \\ele {0 + r} = \\frac \\ele r
            = \\frac{\\cfrac{\\eli_1 \\eli_2 (R_1 - R_2)}{\\eli_2 - \\eli_1}}{\\cfrac{\\eli_1 R_1 - \\eli_2 R_2}{\\eli_2 - \\eli_1}}
            = \\frac{\\eli_1 \\eli_2 (R_1 - R_2)}{\\eli_1 R_1 - \\eli_2 R_2}
            \\equiv \\frac{\\eli_1 \\eli_2 (R_2 - R_1)}{\\eli_2 R_2 - \\eli_1 R_1}.
    $$

    Важные пункты:
    \\begin{itemize}
        \\item В ответах есть только те величины, которые есть в условии
            (и ещё физические постоянные могут встретиться, но нам не понадобилось).
        \\item Мы упростили выражения, который пошли в ответы (благо у нас даже получилось:
            приведение к общему знаменателю укоротило ответ). Надо доделывать.
        \\item Всё ответы симметричны относительно замены резисторов 1 и 2 (ведь при этом изменятся и токи).
    \\end{itemize}
''')
class Short_i(variant.VariantTask):  # Вишнякова - 7
    pass


@variant.solution_space(180)
@variant.text('''
    При подключении к источнику тока с ЭДС равным {E:Value:e}
    резистора сопротивлением {R1:Value:e} в цепи течёт ток силой {I1:Value:e}.
    После этого {how} с первым проводником подключают ещё один сопротивлением {R2:Value:e}.
    Определите
    \\begin{itemize}
        \\item внутреннее сопротивление источника тока,
        \\item новую силу тока в цепи,
        \\item мощность тока во втором проводнике.
    \\end{itemize}
''')
@variant.arg(r=('r = {} Ом', [1, 2, 3]))
@variant.arg(how=['параллельно', 'последовательно'])
@variant.arg(R1=('R_1 = {} Ом', [6, 12, 20]))
@variant.arg(R2=('R_2 = {} Ом', [5, 10, 15]))
@variant.arg(I1=('\\eli_1 = {} А', [2, 3, 5, 7, 11]))
@variant.answer_align([
    '{I1:L} &= \\frac{E:L:s}{{R1:L} + {r:L}} \\implies {r:L} = \\frac{E:L:s}{I1:L:s} - {R1:L} = \\frac{E:V:s}{I1:V:s} - {R1:V} = {r:V},',
    'R\' &= {R_formula} = {R_ratio:LaTeX}\\units{Ом},',
    '{I2:L} &= \\frac{E:L:s}{R\' + {r:L}} = {I2_ratio:LaTeX}\\units{А} \\approx {I2:V},',
    '{P2:L} &= {P_formula} = {P2_ratio:LaTeX}\\units{Вт} \\approx {P2:V}.',
])
class Update_external_R(variant.VariantTask):
    def GetUpdate(self, r=None, how=None, R1=None, R2=None, I1=None):
        E_value = I1.frac_value * (r.frac_value + R1.frac_value)
        E = '\\ele = %d В' % E_value
        if how == 'параллельно':
            R_formula = f'\\frac{{{R1:L}{R2:L}}}{{{R1:L} + {R2:L}}}'
            R_ratio = R1.frac_value * R2.frac_value / (R1.frac_value + R2.frac_value)
            I2_ratio = E_value / (R_ratio + r.frac_value)
            P_formula = f'\\frac{{U_2^2}}{R2:L:s} \\equiv \\frac{{\\sqr{{\\eli_2 R\'}}}}{R2:L:s}'
            P2_ratio = (I2_ratio * R_ratio * I2_ratio * R_ratio) / R2.frac_value
        elif how == 'последовательно':
            R_formula = f'{R1:L} + {R2:L}'
            R_ratio = R1.frac_value + R2.frac_value
            I2_ratio = E_value / (R_ratio + r.frac_value)
            P_formula = f'\\eli_2^2 {R2:L:s}'
            P2_ratio = I2_ratio * I2_ratio * R2.frac_value

        return dict(
            E=E,
            R_formula=R_formula,
            R_ratio=R_ratio,
            I2_ratio=I2_ratio,
            I2='\\eli_2 = %.2f А' % float(I2_ratio),
            P_formula=P_formula,
            P2_ratio=P2_ratio,
            P2='P\'_2 = %.1f Вт' % float(P2_ratio),
        )


@variant.solution_space(180)
@variant.text('''
    Замкнутая электрическая цепь состоит из ЭДС {E:Task:e} и сопротивлением ${r:L}$
    и резистора {R:Task:e}. Определите ток, протекающий в цепи. Какая тепловая энергия выделится на резисторе за время
    {t:Task:e}? Какая работа будет совершена ЭДС за это время? Каков знак этой работы? Чему равен КПД цепи?
    Вычислите значения для 2 случаев: ${r:L}=0$ и {r:Task:e}.
''')
@variant.answer_align([
    '''{I1:L} &= \\frac{E:L:s}{R:L:s} = \\frac{E:Value:s}{R:Value:s} = {I1_ratio:LaTeX}\\units{А} \\approx {I1:Value}, ''',
    '''{I2:L} &= \\frac{E:L:s}{{R:L} + {r:L}} = \\frac{E:Value:s}{{R:Value} + {r:Value}} = {I2_ratio:LaTeX}\\units{А} \\approx {I2:Value}, ''',
    '''{Q1:L} &= {I1:L}^2{R:L}{t:L} = \\sqr{\\frac{E:L:s}{R:L:s}} {R:L} {t:L}
        = \\sqr{\\frac{E:Value:s}{R:Value:s}} * {R:Value} * {t:Value} = {Q1_ratio:LaTeX}\\units{Дж} \\approx {Q1:Value}, ''',
    '''{Q2:L} &= {I2:L}^2{R:L}{t:L} = \\sqr{\\frac{E:L:s}{{R:L} + {r:L}}} {R:L} {t:L}
        = \\sqr{\\frac{E:Value:s}{{R:Value} + {r:Value}}} * {R:Value} * {t:Value} = {Q2_ratio:LaTeX}\\units{Дж} \\approx {Q2:Value}, ''',
    '''{A1:L} &= q_1{E:L} = {I1:L}{t:L}{E:L} = \\frac{E:L:s}{R:L:s} {t:L} {E:L}
        = \\frac{{E:L}^2 {t:L}}{R:L|s} = \\frac{{E:Value|sqr} * {t:Value}}{R:Value:s}
        = {A1_ratio:LaTeX}\\units{Дж} \\approx {A1:Value}, \\text{положительна}, ''',
    '''{A2:L} &= q_2{E:L} = {I2:L}{t:L}{E:L} = \\frac{E:L:s}{{R:L} + {r:L}} {t:L} {E:L}
        = \\frac{{E:L}^2 {t:L}}{{R:L} + {r:L}} = \\frac{{E:Value|sqr} * {t:Value}}{{R:Value} + {r:Value}}
        = {A2_ratio:LaTeX}\\units{Дж} \\approx {A2:Value}, \\text{положительна}, ''',
    '''{eta1:L} &= \\frac{Q1:L:s}{A1:L:s} = \\ldots = \\frac{R:L:s}{R:L:s} = {eta1:Value}, ''',
    '''{eta2:L} &= \\frac{Q2:L:s}{A2:L:s} = \\ldots = \\frac{R:L:s}{{R:L} + {r:L}} = {eta_2_ratio:LaTeX} \\approx {eta2:Value}.''',
])
@variant.arg(E=['\\ele = %d В' % E for E in [1, 2, 3, 4]])
@variant.arg(R=['R = %d Ом' % R for R in [10, 15, 24, 30]])
@variant.arg(r=['r = %d Ом' % r for r in [10, 20, 30, 60]])
@variant.arg(t=['\\tau = %d с' % t for t in [2, 5, 10]])
class Om_eta_full(variant.VariantTask):
    def GetUpdate(self, r=None, R=None, E=None, t=None):
        I1_ratio = E.frac_value / R.frac_value
        I2_ratio = E.frac_value / (R.frac_value + r.frac_value)
        eta_2_ratio = R.frac_value / (R.frac_value + r.frac_value)
        Q1_ratio = I1_ratio * I1_ratio * R.frac_value * t.frac_value
        Q2_ratio = I2_ratio * I2_ratio * R.frac_value * t.frac_value
        A1_ratio = I1_ratio * E.frac_value * t.frac_value
        A2_ratio = I2_ratio * E.frac_value * t.frac_value
        return dict(
            I1_ratio=I1_ratio,
            I2_ratio=I2_ratio,
            I1='\\eli_1 = %.2f А' % float(I1_ratio),
            I2='\\eli_2 = %.2f А' % float(I2_ratio),
            Q1_ratio=Q1_ratio,
            Q2_ratio=Q2_ratio,
            A1_ratio=A1_ratio,
            A2_ratio=A2_ratio,
            Q1='Q_1 = %.3f Дж' % float(Q1_ratio),
            Q2='Q_2 = %.3f Дж' % float(Q2_ratio),
            A1='A_1 = %.3f Дж' % float(A1_ratio),
            A2='A_2 = %.3f Дж' % float(A2_ratio),
            eta_2_ratio=eta_2_ratio,
            eta1='\\eta_1 = 1',
            eta2='\\eta_2 = %.2f' % float(eta_2_ratio),
        )


@variant.text('''
    Лампочки, сопротивления которых {R1:Task:e} и {R2:Task:e}, поочерёдно подключённные к некоторому источнику тока,
    потребляют одинаковую мощность. Найти внутреннее сопротивление источника и КПД цепи в каждом случае.
''')
@variant.answer_align([
    '''
    P_1 &= \\sqr{\\frac{E:L:s}{{R1:L} + {r:L}}}{R1:L},
    P_2  = \\sqr{\\frac{E:L:s}{{R2:L} + {r:L}}}{R2:L},
    P_1 = P_2 \\implies ''',
    '''
    &\\implies {R1:L} \\sqr{{R2:L} + {r:L}} = {R2:L} \\sqr{{R1:L} + {r:L}} \\implies ''',
    '''
    &\\implies {R1:L} {R2:L}^2 + 2 {R1:L} {R2:L} {r:L} + {R1:L} {r:L}^2 =
                {R2:L} {R1:L}^2 + 2 {R2:L} {R1:L} {r:L} + {R2:L} {r:L}^2  \\implies ''',
    '''&\\implies {r:L}^2 ({R2:L} - {R1:L}) = {R2:L}^2 {R2:L} - {R1:L}^2 {R2:L} \\implies ''',
    '''&\\implies {r:L}
        = \\sqrt{{R1:L} {R2:L} \\frac{{R2:L} - {R1:L}}{{R2:L} - {R1:L}}}
        = \\sqrt{{R1:L} {R2:L}}
        = \\sqrt{{R1:Value} * {R2:Value}}
        = {r:Value}. '''
   ,
   '''{eta1:L}
        &= \\frac{R1:L:s}{{R1:L} + {r:L}}
        = \\frac{{R1:L|sqrt}}{{R1:L|sqrt} + {R2:L|sqrt}}
        = {eta1:Value}, '''
   ,
   '''{eta2:L}
        &= \\frac{R2:L:s}{{R2:L} + {r:L}}
        = \\frac{R2:L|sqrt|s}{{R2:L|sqrt} + {R1:L|sqrt}}
        = {eta2:Value}''',
])
@variant.arg(R1__R2=[('R_1 = %.2f Ом' % R_1, 'R_2 = %.2f Ом' % R_2) for R_1, R_2 in [
    (0.25, 16), (0.25, 64), (0.25, 4),
    (0.5, 18),  (0.5, 2),   (0.5, 4.5),
    (1, 4),     (1, 9),     (1, 49),
    (3, 12),    (3, 48),
    (4, 36),    (4, 100),
    (5, 45),    (5, 80),
    (6, 24),    (6, 54),
]])
class r_eta_from_Rs(variant.VariantTask):
    def GetUpdate(self, R1=None, R2=None):
        r = UnitValue('r = %.1f Ом' % (float((R1 * R2).SI_Value) ** 0.5))
        return dict(
            R1=R1,
            R2=R2,
            r=r,
            eta1='\\eta_1 = %.3f ' % (R1.frac_value / (R1.frac_value + r.frac_value)),
            eta2='\\eta_2 = %.3f ' % (R2.frac_value / (R2.frac_value + r.frac_value)),
            E='\\ele = 1 В',
        )
