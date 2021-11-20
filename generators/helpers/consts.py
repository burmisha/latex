from generators.helpers.value import UnitValue
from generators.helpers.unit import BaseUnits
from generators.helpers.matter import Matter
from generators.helpers.vapor import Vapor, T_P_Pmm_rho
from generators.helpers.fraction import Decimal

class ConstsBase:
    pi = 3.14159
    m_e = UnitValue('m_{e} = 9.1 10^{-31} кг')
    m_p = UnitValue('m_{p} = 1.67262 10^{-27} кг', viewPrecision=3)
    m_n = UnitValue('m_{n} = 1.67493 10^{-27} кг', viewPrecision=3)
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
        (Consts.c / UnitValue('l = 500 нм'), '600 \\cdot 10^{12}\\,\\text{Гц}'),
        (UnitValue('9 10^25') / Consts.N_A, '150\\,\\text{моль}'),
        ((UnitValue('9 10^25') / UnitValue('6.03 10^23')).IncPrecision(), '149'),
        (UnitValue('9 10^25') / UnitValue('6.03 10^23'), '150'),
        ((UnitValue('E = 31.99 МэВ') / Consts.c / Consts.c).As('а.е.м.'), '0{,}0342\\,\\text{а.е.м.}'),
        (UnitValue('E = 39.2 МэВ') / Consts.c / Consts.c,  '69{,}7 \\cdot 10^{-30}\\,\\text{кг}'),
        (UnitValue('E = 39.2 МэВ') / Consts.c / Consts.c,  '69{,}7 \\cdot 10^{-30}\\,\\text{кг}'),
        (UnitValue('20 г') / UnitValue('142 г / моль') * Consts.N_A, '85 \\cdot 10^{21}'),
        (Consts.h * Consts.c, r'0{,}1988 \cdot 10^{-24}\,\frac{\text{кг}\cdot\text{м}^{3}}{\text{с}^{2}}'),
        (Consts.h * Consts.c / UnitValue('200 нм'), r'0{,}994 \cdot 10^{-18}\,\text{Дж}'),
        (UnitValue('10 м/с') / Consts.g_ten, r'1\,\text{с}'),
        (UnitValue('10 м/с') * UnitValue('10 м/с') / Consts.g_ten, r'10\,\text{м}'),
        (Consts.m_p_aem, r'1{,}00728\,\text{а.е.м.}'),
        (Consts.m_n_aem, r'1{,}00867\,\text{а.е.м.}'),
        (Consts.m_p.As('а.е.м.'), r'1{,}00727\,\text{а.е.м.}'),  # TODO
        (Consts.m_n.As('а.е.м.'), r'1{,}00867\,\text{а.е.м.}'),
        ((Consts.c / UnitValue('0.500 мкм')).As('ТГц'), r'600\,\text{ТГц}'),
    ]
    for unit_value, answer in data:
        result = '{:V}'.format(unit_value)
        assert result == answer, f'Expected |{answer}|, got |{result}|'

    assert UnitValue('2 10^4 км/c').Value * Consts.m_p.Value / Consts.e.Value / UnitValue('200 мТл').Value * 10 ** 2 == Decimal('1.0453875')


test_calculation()


def test_get_base_units():
    data = [
        (Consts.h, {BaseUnits.m: 2, BaseUnits.s: -1, BaseUnits.kg: 1}),
        (Consts.h * Consts.c, {BaseUnits.m: 3, BaseUnits.s: -2, BaseUnits.kg: 1}),
        (Consts.h * Consts.c / UnitValue('м'), {BaseUnits.m: 2, BaseUnits.s: -2, BaseUnits.kg: 1}),
    ]
    for unit_value, base_units in data:
        result = unit_value.get_base_units()
        assert result == base_units, f'Expected {base_units}, got {result} for {unit_value!r}'


test_get_base_units()
