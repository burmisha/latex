import generators.variant as variant
from generators.helpers import UnitValue, Consts, Decimal


@variant.solution_space(80)
@variant.text('''
    При температуре ${t1}\\celsius$ относительная влажность воздуха составляет ${phi1}\%$.
    \\begin{itemize}
        \\item Определите точку росы для этого воздуха.
        \\item Какой станет относительная влажность этого воздуха, если нагреть его до ${t2}\\celsius$?
    \\end{itemize}
''')
@variant.arg(t1=[15, 20, 25, 30])
@variant.arg(t2=[40, 50, 60, 70, 80])
@variant.arg(phi1=[40, 45, 50, 55, 60, 65, 70, 75])
@variant.answer_align([
    '&\\text{Значения плотности насыщенного водяного пара определяем по таблице:}',
    '&{rho_np_1:Task}, {rho_np_2:Task}.',
    '\\varphi_1 &= \\frac{rho:L:s}{rho_np_1:L:s} \\implies {rho:L:s} = {rho_np_1:L} * \\varphi_1 = {rho_np_1:V} * {phi_1} = {rho:V}.',
    '&\\text{По таблице определяем, при какой температуре пар с такой плотностью станет насыщенным:} ',
    't_\\text{росы} &= {t}\\celsius,',
    '\\varphi_2 &= \\frac{rho:L:s}{rho_np_2:L:s} = \\frac{{rho_np_1:L} * \\varphi_1}{rho_np_2:L:s}'
    '= \\varphi_1 * \\frac{rho_np_1:L:s}{rho_np_2:L:s} = {phi_1} * \\frac{rho_np_1:V:s}{rho_np_2:V:s} = {phi_2:V} \\approx {phi2_percent:V}\\%.'
])
class GetPhi(variant.VariantTask):
    def GetUpdate(self, t1=None, t2=None, phi1=None):
        phi_1 = phi1 / 100
        rho_np_1 = Consts.vapor.get_rho_by_t(t1).SetLetter(f'\\rho_{{\\text{{нас. пара {t1}}} \\celsius}}')
        rho_np_2 = Consts.vapor.get_rho_by_t(t2).SetLetter(f'\\rho_{{\\text{{нас. пара {t2}}} \\celsius}}')
        rho = (rho_np_1 * phi_1).SetLetter('\\rho_\\text{пара}')
        t = '%.1f' % Consts.vapor.get_t_by_rho(rho)
        phi_2 = rho_np_1 / rho_np_2 * phi_1
        return dict(
            rho_np_1=rho_np_1,
            rho_np_2=rho_np_2,
            rho=rho.As('г / м^3'),
            t=t,
            phi_2=phi_2,
            phi_1=phi_1,
            phi2_percent=phi_2 * 100,
        )


@variant.solution_space(160)
@variant.text('''
    Сколько молекул водяного пара содержится в сосуде объёмом {V:V:e} при температуре ${t}\\celsius$,
    и влажности воздуха ${phi}\%$?
''')
@variant.arg(V='3/6/7/12/15 л')
@variant.arg(t=[15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100])
@variant.arg(phi=[20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80])
@variant.answer_tex('''
    Уравнение состояния идеального газа (и учтём, что $R = {Consts.N_A:L} * {Consts.k_boltzmann:L}$,
    это чуть упростит выячичления, но вовсе не обязательно это делать):
    $$
        PV = \\nu RT = \\frac N{Consts.N_A:L:s} RT \\implies N = PV * \\frac{Consts.N_A:L:s}{RT}=  \\frac{PV}{{Consts.k_boltzmann:L}T}
    $$
    Плотность насыщенного водяного пара при ${t}\\celsius$ ищем по таблице: ${P_np:Task}.$

    Получаем плотность пара в сосуде $\\varphi = \\frac P{P_np:L:s} \\implies P = \\varphi {P_np:L}.$

    И подставляем в ответ (по сути, его можно было получить быстрее из формул $P = nkT, n = \\frac NV$):
    $$
        N = \\frac{\\varphi * {P_np:L} * V}{{Consts.k_boltzmann:L}T}
         = \\frac{{phi_share} * {P_np:V} * {V:V}}{{Consts.k_boltzmann:V} * {T:V}}
         \\approx {N:V} * 10^{{power}}.
    $$

    Другой вариант решения (через плотности) приводит в результату:
    $$
        N = {Consts.N_A:L} \\nu = {Consts.N_A:L} * \\frac m{mu:L:s}
          = {Consts.N_A:L} \\frac{\\rho V}{mu:L:s}
          = {Consts.N_A:L} \\frac{\\varphi * {rho_np:L} * V}{mu:L:s}
          = {Consts.N_A:V} * \\frac{{phi_share} * {rho_np:V} * {V:V}}{mu:V:s}
          \\approx {N2:V} * 10^{{power}}.
    $$
''')
class GetNFromPhi(variant.VariantTask):
    def GetUpdate(self, phi=None, V=None, t=None):
        mu = Consts.water.mu
        T = UnitValue(f'{t + 273} К')

        P_np = Consts.vapor.get_p_by_t(t).SetLetter(f'P_{{\\text{{нас. пара {t}}} \\celsius}}')
        rho_np = Consts.vapor.get_rho_by_t(t).SetLetter(f'\\rho_{{\\text{{нас. пара {t}}} \\celsius}}')

        power = 20

        N = phi / 100 * P_np * V / Consts.k_boltzmann / T / 10 ** power
        N2 = phi / 100 * rho_np * V / mu * Consts.N_A / 10 ** power

        return dict(
            P_np=P_np,
            rho_np=rho_np,
            T=T,
            phi_share=f'{phi / 100:.2f}',
            N=N.SetLetter('N').IncPrecision(1),
            N2=N2.SetLetter('N').IncPrecision(1),
            mu=mu,
            power=power,
        )


@variant.solution_space(200)
@variant.text('''
    В герметичном сосуде находится влажный воздух при температуре ${t1}\\celsius$ и относительной влажности ${phi1}\%$.
    \\begin{enumerate}
        \\item Чему равно парциальное давление насыщенного водяного пара при этой температуре?
        \\item Чему равно парциальное давление водяного пара?
        \\item Определите точку росы этого пара?
        \\item Каким станет парциальное давление водяного пара, если сосуд нагреть до ${t2}\\celsius$?
        \\item Чему будет равна относительная влажность воздуха, если сосуд нагреть до ${t2}\\celsius$?
        \\item Получите ответ на предыдущий вопрос, используя плотности, а не давления.
    \\end{enumerate}
''')
@variant.arg(V='3/6/9/12/15 л')
@variant.arg(t1=[15, 20, 25, 30, 40])
@variant.arg(t2=[70, 80, 90])
@variant.arg(phi1=[20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80])
@variant.answer_tex('''
    Парциальное давление насыщенного водяного пара при ${t1}\\celsius$ ищем по таблице: $${P_np_1:Task}.$$

    Парциальное давление водяного пара
    $${P1:L} = \\varphi_1 * {P_np_1:L} = {phi_1} * {P_np_1:V} = {P1:V}.$$

    Точку росы определяем по таблице: при какой температуре пар с давлением {P1:Task:e} станет насыщенным: ${t}\\celsius$.

    После нагрева парциальное давление пара возрастёт:
    $$
        \\frac{{P1:L} * V}{T1:L:s} = \\nu R = \\frac{{P2:L} * V}{T2:L:s}
        \\implies {P2:L} = {P1:L} * \\frac{T2:L:s}{T1:L:s} = {P1:V} * \\frac{T2:V:s}{T1:V:s} \\approx {P2:V}.
    $$

    Парциальное давление насыщенного водяного пара при ${t2}\\celsius$ ищем по таблице: {P_np_2:Task:e}.
    Теперь определяем влажность:
    $$
        \\varphi_2 = \\frac{P2:L:s}{P_np_2:L:s} = \\frac{P2:V:s}{P_np_2:V:s} \\approx {phi2} = {phi2_percent:V}\%.
    $$

    Или же выражаем то же самое через плотности (плотность не изменяется при изохорном нагревании $\\rho_1 =\\rho_2 = \\rho$, в отличие от давления):
    $$
        \\varphi_2 = \\frac{\\rho}{rho_np_2:L:s} = \\frac{\\varphi_1{rho_np_1:L}}{rho_np_2:L:s}
        = \\frac{{phi_1} * {rho_np_1:V}}{rho_np_2:V:s} \\approx {phi_2_rho:V} = {phi2_percent_rho:V}\%.
    $$
    Сравните 2 последних результата.
''')
class GetPFromPhi(variant.VariantTask):
    def GetUpdate(self, phi1=None, V=None, t1=None, t2=None):
        T1 = t1 + 273
        T2 = t2 + 273

        P_np_1 = Consts.vapor.get_p_by_t(t1).SetLetter(f'P_{{\\text{{нас. пара {t1}}} \\celsius}}')
        P_np_2 = Consts.vapor.get_p_by_t(t2).SetLetter(f'P_{{\\text{{нас. пара {t2}}} \\celsius}}')

        rho_np_1 = Consts.vapor.get_rho_by_t(t1).SetLetter(f'\\rho_{{\\text{{нас. пара {t1}}} \\celsius}}')
        rho_np_2 = Consts.vapor.get_rho_by_t(t2).SetLetter(f'\\rho_{{\\text{{нас. пара {t2}}} \\celsius}}')

        phi_1 = phi1 / 100
        P1 = (P_np_1 * phi_1).SetLetter('P_\\text{пара 1}').As('кПа')
        P2 = (P1 * T2 / T1).SetLetter('P_\\text{пара 2}').As('кПа')
        phi2 = P2 / P_np_2
        phi_2_rho = phi_1 * Consts.vapor.get_rho_by_t(t1) / Consts.vapor.get_rho_by_t(t2)
        return dict(
            P_np_1=P_np_1,
            P_np_2=P_np_2,
            t='%.1f' % Consts.vapor.get_t_by_p(P1),
            phi_1='%.2f' % phi_1,
            P1=P1,
            P2=P2,
            T1='T_1 = %d К' % T1,
            T2='T_2 = %d К' % T2,
            phi2='%.3f' % phi2.SI_Value,
            phi2_percent=phi2 * 100,
            phi_2_rho=phi_2_rho,
            phi2_percent_rho=phi_2_rho * 100,
            rho_np_1=rho_np_1,
            rho_np_2=rho_np_2,
        )


@variant.solution_space(150)
@variant.text('''
    Закрытый сосуд объёмом {V:V:e} заполнен сухим воздухом при давлении {P_air_old:V:e} и температуре ${t1}\\celsius$.
    Каким станет давление в сосуде, если в него налить {m:V:e} воды и нагреть содержимое сосуда до ${t2}\\celsius$?
''')
@variant.arg(P_air_old=['P = 100 кПа'])
@variant.arg(V='10/15/20 л')
@variant.arg(t1=[10, 20, 30])
@variant.arg(t2=[100, 90, 80])
@variant.arg(m='5/10/20/30 г')
@variant.answer_tex('''
    Конечное давление газа в сосуде складывается по закону Дальтона из давления нагретого сухого воздуха {P_air_new:L:e} и
    давления насыщенного пара {P_vapor_1:L:e}:
    $$P' = {P_air_new:L} + {P_vapor_1:L}.$$

    Сперва определим новое давление сухого воздуха из уравнения состояния идеального газа:
    $$
        \\frac{{P_air_new:L} * V}{T2:L:s} = \\nu R = \\frac{{P_air_old:L} * V}{T1:L:s}
        \\implies {P_air_new:L} = {P_air_old:L} * \\frac{T2:L:s}{T1:L:s} = {P_air_old:V} * \\frac{T2:V:s}{T1:V:s} \\approx {P_air_new:V}.
    $$

    Чтобы найти давление пара, нужно понять, будет ли он насыщенным после нагрева или нет.

    Плотность насыщенного пара при температуре ${t2}\\celsius$ равна {rho:V:e}, тогда для того,
    чтобы весь сосуд был заполнен насыщенным водяным паром нужно
    ${m_np:L} = {rho:L} * V = {rho:V} * {V:V} \\approx {m_np:V}$ воды.
    Сравнивая эту массу с массой воды из условия, получаем массу жидкости, которая испарится: {m_vapor:Task:e}.
    Осталось определить давление этого пара:
    $${P_vapor_1:L} = \\frac{{m_vapor:L}R{T2:L}}{\\mu V} = \\frac{{m_vapor:V} * {Consts.R:Value} * {T2:Value}}{{mu:Value} * {V:Value}} \\approx {P_vapor_1:V}.$$

    Получаем ответ: {P_1:Task:e}.

    Другой вариант решения для давления пара:
    Определим давление пара, если бы вся вода испарилась (что не факт):
    $${P_max:L} = \\frac{mR{T2:L}}{\\mu V} = \\frac{{m:V} * {Consts.R:V} * {T2:V}}{{mu:Value} * {V:Value}} \\approx {P_max:V}.$$
    Сравниваем это давление с давлением насыщенного пара при этой температуре {P_np:Task:e}:
    если у нас получилось меньше табличного значения,
    то вся вода испарилась, если же больше — испарилась лишь часть, а пар является насыщенным.
    Отсюда сразу получаем давление пара: {P_vapor_2:Task:e}. Сравните этот результат с первым вариантом решения.

    Тут получаем ответ: {P_2:Task:e}.
''')
class GetPFromM(variant.VariantTask):
    def GetUpdate(self, *, P_air_old=None, V=None, t1=None, t2=None, m=None):
        mu = Consts.water.mu

        T1 = UnitValue(f'T = {t1 + 273} К')
        T2 = UnitValue(f'T\' = {t2 + 273} К')

        P_air_new = (P_air_old * T2 / T1).SetLetter('P\'_\\text{воздуха}').As('кПа')

        rho = Consts.vapor.get_rho_by_t(t2).SetLetter(f'\\rho_\\text{{н. п. {t2} $\\celsius$}}')

        m_np = (rho * V).SetLetter('m_\\text{н. п.}').As('г').IncPrecision(1)
        m_vapor = UnitValue('%.1f г' % (min(m_np.SI_Value, m.SI_Value) * 1000)).SetLetter('m_\\text{пара}')
        P_vapor_1 = (m_vapor * Consts.R * T2 / mu / V).SetLetter('P_\\text{пара}').IncPrecision(2).As('кПа')

        P_np = Consts.vapor.get_p_by_t(t2).SetLetter(f'P_\\text{{н. п. {t2} $\\celsius$}}')
        P_max = (m * Consts.R * T2 / mu / V).SetLetter('P_\\text{max}').IncPrecision(2).As('кПа')
        P_vapor_2 = 'P\'_\\text{пара} = %.1f кПа' % (min(P_max.SI_Value, P_np.SI_Value) / 1000)

        P_1 = 'P\'_\\text{пара} = %.1f кПа' % ((P_air_new.SI_Value + P_vapor_1.SI_Value) / 1000)
        P_2 = 'P\'_\\text{пара} = %.1f кПа' % ((P_air_new.SI_Value + min(P_max.SI_Value, P_np.SI_Value)) / 1000)
        return dict(
            T1=T1,
            T2=T2,
            rho=rho,
            m_np=m_np,
            m_vapor=m_vapor,
            P_vapor_1=P_vapor_1,
            P_air_new=P_air_new,
            P_np=P_np,
            P_max=P_max,
            mu=mu,
            P_vapor_2=P_vapor_2,
            P_1=P_1,
            P_2=P_2,
        )


@variant.solution_space(40)
@variant.text('''
    Напротив физических величин запишите определение, обозначение и единицы измерения в системе СИ (если есть):
    \\begin{enumerate}
        \\item {v_1},
        \\item {v_2}.
    \\end{enumerate}
''')
@variant.arg(v_1=['абсолютная влажность', 'относительная влажность'])
@variant.arg(v_2=['насыщенный пар', 'динамическое равновесие'])
class Vapor01(variant.VariantTask):
    pass
