from generators.helpers.value import UnitValue
from generators.helpers.matter import Matter
from generators.helpers.vapor import Vapor, T_P_Pmm_rho
from generators.helpers.fraction import Decimal

class ConstsBase:
    pi = 3.14159
    m_e = UnitValue('m_{e} = 9.1 10^{-31} кг')
    m_p = UnitValue('m_{p} = 1.672 10^{-27} кг')
    m_n = UnitValue('m_{n} = 1.675 10^{-27} кг')
    m_p_aem = UnitValue('m_{p} = 1.00728 а.е.м.')
    m_n_aem = UnitValue('m_{n} = 1.00867 а.е.м.')
    e = UnitValue('e = 1.60 10^{-19} Кл', viewPrecision=1)
    eV = UnitValue('1.60 10^{-19} Дж', viewPrecision=1)
    e_0 = UnitValue('8.85 * 10^-12 Ф / м')
    h = UnitValue('h = 6.626 10^{-34} Дж с')
    c = UnitValue('c = 3 10^{8} м / с', precision=3, viewPrecision=1)
    c_4 = UnitValue('c = 2.998 10^{8} м / с')
    g_ten = UnitValue('g = 10 м / с^2', precision=2)
    p_atm = UnitValue('p_{\\text{aтм}} = 100 кПа')
    aem = UnitValue('\\text{а.е.м.} = 1.66054 10^-27 кг')
    k = UnitValue('k = 9 10^9 Н м^2 / Кл^2')
    k_boltzmann = UnitValue('k = 1.38 10^-23 Дж / К')
    N_A = UnitValue('N_A = 6.02 10^23 / моль')
    R = UnitValue('R = 8.31 Дж / моль К')
    one_aem_eV = UnitValue('931.5 МэВ')

    vapor = Vapor(T_P_Pmm_rho)

    water = Matter(
        name='вода',
        c='4200 Дж / кг К',
        lmbd='340 кДж / кг',
        L='2.3 МДж / кг',
        rho='\\rho_{\\text{в}} = 1000 кг / м^3',
        mu='18 г / моль',
    )
    lead = Matter(
        name='свинец',
        lmbd='25 кДж / кг',
    )
    aluminum = Matter(
        name='алюминий',
        c='920 Дж / кг К',
        lmbd='390 кДж / кг',
    )
    copper = Matter(
        name='медь',
        lmbd='210 кДж / кг',
    )
    steel = Matter(
        name='сталь',
        c='500 Дж / кг К',
        lmbd='84 кДж / кг',
    )
    zinc = Matter(
        name='цинк',
        c='400 Дж / кг К',
    )
    gas_n2 = Matter(
        name='азот',
        mu='28 г / моль',
    )
    gas_air = Matter(
        name='воздух',
        mu='29 г / моль',
    )
    gas_o2 = Matter(
        name='кислород',
        mu='32 г / моль',
    )
    gas_o3 = Matter(
        name='озон',
        mu='48 г / моль',
    )
    gas_co2 = Matter(
        name='углекислый газ',
        mu='44 г / моль',
    )
    gas_ne = Matter(
        name='неон',
        mu='20 г / моль',
    )
    gas_ar = Matter(
        name='аргон',
        mu='40 г / моль',
    )


Consts = ConstsBase()


def test_calculation():
    data = [
        (Consts.c.Div(UnitValue('l = 500 нм'), units='Гц'), '600 \\cdot 10^{12}\\,\\text{Гц}'),
        (UnitValue('9 10^25').Div(Consts.N_A), '150'),
        (UnitValue('9 10^25').Div(UnitValue('6.03 10^23'), precisionInc=1), '149'),
        (UnitValue('9 10^25').Div(UnitValue('6.03 10^23'), precisionInc=0), '150'),
        ((UnitValue('E = 31.99 МэВ') * Consts.e / Consts.c / Consts.c).Div(Consts.aem, units='а.е.м.'),  '0{,}034\\,\\text{а.е.м.}'),
        ((UnitValue('E = 39.2 МэВ') * Consts.e / Consts.c).Div(Consts.c, units='кг'),  '70 \\cdot 10^{-30}\\,\\text{кг}'),
        (UnitValue('20 г') / UnitValue('142 г / моль') * Consts.N_A, '85 \\cdot 10^{21}'),
    ]
    for unit_value, answer in data:
        result = '{:V}'.format(unit_value)
        assert result == answer, f'Expected |{answer}|, got |{result}|'

    assert UnitValue('2 10^4 км/c').Value * Consts.m_p.Value / Consts.e.Value / UnitValue('200 мТл').Value * 10 ** 2 == Decimal('1.045')

test_calculation()
