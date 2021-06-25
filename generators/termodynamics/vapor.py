import generators.variant as variant
from generators.helpers import UnitValue, Consts


@variant.solution_space(80)
@variant.text('''
    При температуре ${t1}\\celsius$ относительная влажность воздуха составляет ${phi1}\%$.
    \\begin{itemize}
        \\item Определите точку росы для этого воздуха.
        \\item Какой станет относительная влажность этого воздуха, если нагреть его до ${t2}\\celsius$?
    \\end{itemize}
''')
@variant.arg(t1=('{}', [15, 20, 25, 30]))
@variant.arg(t2=('{}', [40, 50, 60, 70, 80]))
@variant.arg(phi1=('{}', [40, 45, 50, 55, 60, 65, 70, 75]))
@variant.answer_align([
    '&\\text{Значения плотности насыщенного водяного пара определяем по таблице:}',
    '&{rho_np_1:Task}, {rho_np_2:Task}.',
    '\\varphi_1 &= \\frac{rho:L:s}{rho_np_1:L:s} \\implies {rho:L:s} = {rho_np_1:L} * \\varphi_1 = {rho_np_1:V} * {phi1_ratio} = {rho:V}.',
    '&\\text{По таблице определяем, при какой температуре пар с такой плотностью станет насыщенным:} ',
    't_\\text{росы} &= {t}\\celsius,',
    '\\varphi_2 &= \\frac{rho:L:s}{rho_np_2:L:s} = \\frac{{rho_np_1:L} * \\varphi_1}{rho_np_2:L:s}'
    '= \\varphi_1 * \\frac{rho_np_1:L:s}{rho_np_2:L:s} = {phi1_ratio} * \\frac{rho_np_1:V:s}{rho_np_2:V:s} = {phi2} \\approx {phi2_ratio}\\%.'
])
class GetPhi(variant.VariantTask):
    def GetUpdate(self, t1=None, t2=None, phi1=None, **kws):
        np_1 = Consts.vapor.get_rho_by_t(int(t1))
        np_2 = Consts.vapor.get_rho_by_t(int(t2))
        rho_np_1 = f'\\rho_{{\\text{{нас. пара {t1}}} \\celsius}}= {np_1:.3f} г / м^3'
        rho_np_2 = f'\\rho_{{\\text{{нас. пара {t2}}} \\celsius}} = {np_2:.3f} г / м^3'
        rho = '\\rho_\\text{пара} = %.3f г / м^3' % (np_1 * int(phi1) / 100)
        t = '%.1f' % Consts.vapor.get_t_by_rho(np_1 * int(phi1) / 100)
        phi_2 = '%.3f' % (int(phi1) * np_1 / np_2 / 100)
        phi1_ratio = '%.2f' % (int(phi1) / 100)
        phi2_ratio = '%.1f' % (int(phi1) * np_1 / np_2)
        return dict(
            rho_np_1=rho_np_1,
            rho_np_2=rho_np_2,
            rho=rho,
            t=t,
            phi2=phi_2,
            phi1_ratio=phi1_ratio,
            phi2_ratio=phi2_ratio,
        )


@variant.solution_space(160)
@variant.text('''
    Сколько молекул водяного пара содержится в сосуде объёмом {V:V:e} при температуре ${t}\\celsius$,
    и влажности воздуха ${phi}\%$?
''')
@variant.arg(V=('{} л', [3, 6, 9, 12, 15]))
@variant.arg(t=('{}', [15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100]))
@variant.arg(phi=('{}', [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]))
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
         \\approx {N:V}.
    $$

    Другой вариант решения (через плотности) приводит в результату:
    $$
        N = {Consts.N_A:L} \\nu = {Consts.N_A:L} * \\frac m{mu:L:s}
          = {Consts.N_A:L} \\frac{\\rho V}{mu:L:s}
          = {Consts.N_A:L} \\frac{\\varphi * {rho_np:L} * V}{mu:L:s}
          = {Consts.N_A:V} * \\frac{{phi_share} * {rho_np:V} * {V:V}}{mu:V:s}
          \\approx {N2:V}.
    $$
''')
class GetNFromPhi(variant.VariantTask):
    def GetUpdate(self, phi=None, V=None, t=None, **kws):
        mu_value = 18

        t_int = int(t)
        T = t_int + 273

        P_np_value = Consts.vapor.get_p_by_t(t_int)
        rho_np_value = Consts.vapor.get_rho_by_t(t_int)

        N = 1. * int(phi) / 100 * P_np_value * V.Value / Consts.k_boltzmann.Value / T * 1000
        N2 = 1. * int(phi) / 100 * rho_np_value * V.Value / mu_value * Consts.N_A.Value
        return dict(
            P_np=f'P_{{\\text{{нас. пара {t}}} \\celsius}} = %.3f кПа' % P_np_value,
            rho_np=f'\\rho_{{\\text{{нас. пара {t}}} \\celsius}} = %.3f г/м^3' % rho_np_value,
            T='T = %d К' % T,
            phi_share='%.2f' % (int(phi) / 100),
            N='N = %.1f 10^20' % N,
            N2='N = %.1f 10^20' % N2,
            mu=f'\\mu = {mu_value} г / моль',
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
@variant.arg(V=('{} л', [3, 6, 9, 12, 15]))
@variant.arg(t1=('{}', [15, 20, 25, 30, 40]))
@variant.arg(t2=('{}', [70, 80, 90]))
@variant.arg(phi1=('{}', [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]))
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
        \\varphi_2 = \\frac{P2:L:s}{P_np_2:L:s} = \\frac{P2:V:s}{P_np_2:V:s} \\approx {phi2} = {phi2_percent}\%.
    $$

    Или же выражаем то же самое через плотности (плотность не изменяется при изохорном нагревании $\\rho_1 =\\rho_2 = \\rho$, в отличие от давления):
    $$
        \\varphi_2 = \\frac{\\rho}{rho_np_2:L:s} = \\frac{\\varphi_1{rho_np_1:L}}{rho_np_2:L:s}
        = \\frac{{phi_1} * {rho_np_1:V}}{rho_np_2:V:s} \\approx {phi_2_rho} = {phi2_percent_rho}\%.
    $$
    Сравните 2 последних результата.
''')
class GetPFromPhi(variant.VariantTask):
    def GetUpdate(self, phi1=None, V=None, t1=None, t2=None, **kws):
        P_np_1_value = Consts.vapor.get_p_by_t(int(t1))
        P_np_2_value = Consts.vapor.get_p_by_t(int(t2))
        phi_1 = 1. * int(phi1) / 100
        P1_value = P_np_1_value * phi_1
        T1 = int(t1) + 273
        T2 = int(t2) + 273
        P2_value = P1_value * T2 / T1
        phi2 = P2_value / P_np_2_value
        phi_2_rho = phi_1 * Consts.vapor.get_rho_by_t(int(t1)) / Consts.vapor.get_rho_by_t(int(t2))
        return dict(
            P_np_1=f'P_{{\\text{{нас. пара {t1}}} \\celsius}} = %.3f кПа' % P_np_1_value,
            P_np_2=f'P_{{\\text{{нас. пара {t2}}} \\celsius}} = %.3f кПа' % P_np_2_value,
            t='%.1f' % Consts.vapor.get_t_by_p(P1_value),
            phi_1='%.2f' % phi_1,
            P1='P_\\text{пара 1} = %.3f кПа' % P1_value,
            P2='P_\\text{пара 2} = %.3f кПа' % P2_value,
            T1='T_1 = %d К' % T1,
            T2='T_2 = %d К' % T2,
            phi2='%.3f' % phi2,
            phi2_percent='%.1f' % (phi2 * 100),
            phi_2_rho='%.3f' % phi_2_rho,
            phi2_percent_rho='%.1f' % (phi_2_rho * 100),
            rho_np_1=f'\\rho_{{\\text{{нас. пара {t1}}} \\celsius}} = %.3f г/м^3' % Consts.vapor.get_rho_by_t(int(t1)),
            rho_np_2=f'\\rho_{{\\text{{нас. пара {t2}}} \\celsius}} = %.3f г/м^3' % Consts.vapor.get_rho_by_t(int(t2)),
        )


@variant.solution_space(150)
@variant.text('''
    Закрытый сосуд объёмом {V:V:e} заполнен сухим воздухом при давлении {P_air_old:V:e} и температуре ${t1}\\celsius$.
    Каким станет давление в сосуде, если в него налить {m:V:e} воды и нагреть содержимое сосуда до ${t2}\\celsius$?
''')
@variant.arg(P_air_old=('P = {} кПа', [100]))
@variant.arg(V=('{} л', [10, 15, 20]))
@variant.arg(t1=('{}', [10, 20, 30]))
@variant.arg(t2=('{}', [100, 90, 80]))
@variant.arg(m=('{} г', [5, 10, 20, 30]))
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
    def GetUpdate(self, P_air_old=None, V=None, t1=None, t2=None, m=None, **kws):
        mu_value = 18
        mu = f'\\mu = {mu_value} г / моль'

        T1 = f'T = {int(t1) + 273} К'
        T2 = f'T\' = {int(t2) + 273} К'

        P_air_new_value = P_air_old.Value * (int(t2) + 273) / (int(t1) + 273)
        P_air_new = 'P\'_\\text{воздуха} = %.1f кПа' % P_air_new_value

        rho_value = Consts.vapor.get_rho_by_t(int(t2))
        rho = '\\rho_\\text{н. п. %d $\\celsius$} = %.2f г / м^3' % (int(t2), rho_value)

        m_np_value = 1. * rho_value * V.Value / 1000
        m_np = 'm_\\text{н. п.} = %.1f г' % m_np_value
        m_vapor = 'm_\\text{пара} = %.1f г' % min(m_np_value, m.Value)
        P_vapor_1_value = 1. * min(m_np_value, m.Value) * Consts.R.Value * (int(t2) + 273) / mu_value / V.Value
        P_vapor_1 = 'P_\\text{пара} = %.1f кПа' % P_vapor_1_value

        P_np_value = Consts.vapor.get_p_by_t(int(t2))
        P_np = 'P_\\text{н. п. %d $\\celsius$} = %.1f кПа' % (int(t2), P_np_value)
        P_max_value = 1. * m.Value * Consts.R.Value * (int(t2) + 273) / mu_value / V.Value
        P_max = 'P_\\text{max} = %.1f кПа' % P_max_value
        P_vapor_2 = 'P\'_\\text{пара} = %.1f кПа' % min(P_max_value, P_np_value)

        P_1 = 'P\'_\\text{пара} = %.1f кПа' % (P_air_new_value + P_vapor_1_value)
        P_2 = 'P\'_\\text{пара} = %.1f кПа' % (P_air_new_value + min(P_max_value, P_np_value))
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
