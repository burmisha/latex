# -*- coding: utf-8 -*-
import fractions

import logging
log = logging.getLogger(__name__)


def precisionFmt2(value, precision):
    isInt = False
    if isinstance(value, int):
        isInt = True
    elif isinstance(value, str):
        try:
            intValue = int(value)
        except ValueError:
            pass
        if str(intValue) == value:
            isInt = True
    if isInt:
        return str(value)

    isNegative = value < 0
    absValue = abs(value)
    assert absValue >= 10 ** -7
    assert 1 <= precision <= 10

    rawValue = '%.20f' % absValue
    assert 'e' not in rawValue
    dot_pos = rawValue.index('.')
    assert dot_pos is not None
    no_dot = rawValue.replace('.', '')
    rawDigits = no_dot.lstrip('0')
    leading_zeros = len(no_dot) - len(rawDigits)
    if rawDigits[0] == '1':
        rawDigits = rawDigits[:precision + 2]
    else:
        rawDigits = rawDigits[:(precision + 1)]
    if rawDigits[-1] >= '5':
        if len(str(int(rawDigits) + 5)) > len(rawDigits):
            leading_zeros -= 1
        rawDigits = str(int(rawDigits) + 5)
    rawDigits = '0' * leading_zeros + rawDigits[:-1]

    if dot_pos >= len(rawDigits):
        rawDigits += '0' * (dot_pos - len(rawDigits))
    else:
        rawDigits = rawDigits[:dot_pos] + '.' + rawDigits[dot_pos:]

    if isNegative:
        rawDigits = '-' + rawDigits
    return rawDigits.rstrip('.')


assert precisionFmt2(1.2, 1) == '1.2'
assert precisionFmt2(1.7, 1) == '1.7'
assert precisionFmt2(0.091, 2) == '0.091'
assert precisionFmt2(0.095, 2) == '0.095'
assert precisionFmt2(0.0949, 2) == '0.095'
assert precisionFmt2(-0.0949, 2) == '-0.095'
assert precisionFmt2(0.99, 2) == '0.99'
assert precisionFmt2(0.99, 1) == '1.0'
assert precisionFmt2(1.99, 2) == '1.99'
assert precisionFmt2(1.99, 3) == '1.990'
assert precisionFmt2(19.9, 2) == '19.9'
assert precisionFmt2(19.9, 1) == '20'
assert precisionFmt2(12, 2) == '12'
assert precisionFmt2(20, 2) == '20'
assert precisionFmt2(2.99, 2) == '3.0'
assert precisionFmt2(29.9, 2) == '30'
assert precisionFmt2(299., 2) == '300'
assert precisionFmt2(299, 2) == '299'
assert precisionFmt2(1 + 1. / 30, 2) == '1.03'
assert precisionFmt2(1 + 1. / 300, 2) == '1.00'
assert precisionFmt2(1 + 1. / 300, 3) == '1.003'
assert precisionFmt2(1. / 3, 2) == '0.33'
assert precisionFmt2(4. / 3, 2) == '1.33'
assert precisionFmt2(7. / 3, 2) == '2.3'
assert precisionFmt2(7. / 3, 3) == '2.33'
assert precisionFmt2(700. / 3, 3) == '233'
assert precisionFmt2(700. / 3, 3) == '233'
assert precisionFmt2(7000. / 3, 3) == '2330'
assert precisionFmt2(7000. / 3, 2) == '2300'
assert precisionFmt2(7000. / 3, 1) == '2000'
assert precisionFmt2(8000. / 3, 1) == '3000'
assert precisionFmt2(7000. / 3, 4) == '2333'
assert precisionFmt2(7000. / 3, 5) == '2333.3'
assert precisionFmt2(1000. / 3, 5) == '333.33'
assert precisionFmt2(100. / 3, 5) == '33.333'
assert precisionFmt2(10. / 3, 5) == '3.3333'
assert precisionFmt2(0.1 / 3, 5) == '0.033333'
assert precisionFmt2(0.01 / 3, 5) == '0.0033333'
assert precisionFmt2(0.001 / 3, 5) == '0.00033333'
assert precisionFmt2(0.0049594, 5) == '0.0049594'
assert precisionFmt2(0.0049594, 4) == '0.004959'
assert precisionFmt2(0.0049595, 4) == '0.004960'
assert precisionFmt2(0.0049594, 3) == '0.00496'
assert precisionFmt2(0.0049594, 2) == '0.0050'
assert precisionFmt2(0.0049594, 1) == '0.005'

class OneUnit:
    def __init__(self, line, is_numenator):
        si_unit, si_power, human_unit, human_power = self._parse_line(line)
        self.SiUnit = si_unit
        self.SiPower = si_power
        self.HumanUnit = human_unit
        self.HumanPower = human_power
        self.IsNumerator = is_numenator
        assert isinstance(self.SiUnit, str)
        assert isinstance(self.SiPower, int)
        assert isinstance(self.HumanUnit, str)
        assert isinstance(self.HumanPower, int)

    def get_tex(self):
        res = f'\\text{{{self.HumanUnit}}}'
        if self.HumanPower != 1:
            res += f'^{{{self.HumanPower}}}'
        return res

    def _parse_line(self, line):
        try:
            if '^' in line:
                line, power = line.split('^')
                power = int(power)
            else:
                power = 1

            prefix = ''
            main = line
            for suffix in [
                'час',
                'сут',
                'атм',
                'эВ',  # электрон-вольт
                'В',   # вольт
                'Дж',  # джоуль
                'Н',   # ньютон
                'Вт',  # ватт
                'Ом',  # ом
                'Ф',   # фарад
                'А',   # ампер
                'Кл',  # кулон
                'кг',  # килограм
                'г',   # грам
                'с',   # секунда
                'м',   # метр
                'Тл',  # тесла
                'т',   # тонна
                'С',   # цельсий
                'C',   # celsium
                'К',   # кельвин
                'K',   # kelvin
                'моль',
            ]:
                if line.endswith(suffix):
                    main = suffix
                    prefix = line[:-len(suffix)]
                    break

            exponent = {
                '': 0,
                'к': 3,
                'М': 6,
                'Г': 9,
                'м': -3,
                'мк': -6,
                'н': -9,
                'п': -12,
                'с': -2,
                'д': -1,
            }[prefix]

            if main == 'г':
                main = 'кг'
                exponent -= 3
            # TODO: час, сутки

            return main, exponent * power, line, power
        except:
            log.error('Error in ParseItem on %r', line)
            raise

class UnitValue(object):
    def __init__(self, line, precision=None, viewPrecision=None):
        self.__raw_line = line
        try:
            self._load(line, precision=precision)
        except Exception:
            log.error(f'Could not load unit from {self.__raw_line}')
            raise
        self.ViewPrecision = viewPrecision
        self._value_str = None

    def _parse_precision(self, value_part):
        precisionStr = value_part.replace('.', '').lstrip('0')
        if not precisionStr:
            assert value_part == '0', f'Could not get precision from {value_part!r}'
            precisionStr = '0'
        precision = len(precisionStr)
        if precisionStr[0] == '1' and precision >= 2:
            precision -= 1
        return precision

    def _load(self, line, precision=None):
        line = line.strip()
        if '=' in line:
            letter_line, value_line = line.split('=', 1)
            letter_line = letter_line.strip()
            value_line = value_line.strip()
        else:
            letter_line = None
            value_line = line
        self.Letter = letter_line

        assert value_line.count('/') <= 1
        for key, value in {
            '/': ' / ',
            '**': '^',
            ' ^': '^',
        }.items():
            value_line = value_line.replace(key, value)

        self.ValuePower = 0

        self._units = []
        isNumerator = True
        for index, part in enumerate(value_line.split()):
            if index == 0:
                try:
                    self.Value = int(part)
                except ValueError:
                    self.Value = float(part)
                self.Precision = self._parse_precision(part) if precision is None else precision
                assert self.Precision >= 1
            elif part.startswith('10^'):
                self.ValuePower = int(part[3:].strip('{').strip('}'))
            else:
                if part == '/':
                    isNumerator = False
                else:
                    self._units.append(OneUnit(part, isNumerator))

        self.Power = sum(unit.SiPower if unit.IsNumerator else -unit.SiPower for unit in self._units) + self.ValuePower

    def __str__(self):
        return f'UVS {self.__raw_line}'

    def __repr__(self):
        return f'UVR {self.__raw_line!r}'

    def _get_units_tex(self):
        humanNom = '\\cdot'.join(unit.get_tex() for unit in self._units if unit.IsNumerator)
        humanDen = '\\cdot'.join(unit.get_tex() for unit in self._units if not unit.IsNumerator)
        if humanDen:
            if humanNom:
                units = '\,\\frac{%s}{%s}' % (humanNom, humanDen)
            else:
                units = '\,\\frac{1}{%s}' % (humanDen)
        elif humanNom:
            units = '\,' + humanNom
        else:
            units = ''
        return units

    def _apply_pipes(self, line, pipes):
        pipes_dict = {
            's': '{{ {} }}',
            'b': '\\left({}\\right)',
            'e': '${}$',
            'sqr': '\\sqr{{ {} }}',
            'sqrt': '\\sqrt{{ {} }}',
            'cdot': '{} \\cdot'
        }
        for pipe in pipes:
            pipe_fmt = pipes_dict.get(pipe)
            if pipe_fmt is None:
                raise RuntimeError(f'Unknown pipe {pipe}')
            line = pipe_fmt.format(line)
        return line

    def get_value_str(self):
        if self._value_str is None:
            valueStr = precisionFmt2(self.Value, self.ViewPrecision or self.Precision)
            self._precisionFmt2 = str(valueStr)
            valueStr = valueStr.replace('.', '{,}')
            if self.ValuePower:
                valueStr += f' \\cdot 10^{{{self.ValuePower}}}'
            valueStr += self._get_units_tex()
            self._value_str = valueStr
        return self._value_str

    def __format__(self, fmt):
        try:
            fmt_parts = fmt.replace(':', '|').split('|')
            main_format, pipes = fmt_parts[0], fmt_parts[1:]

            value_str = self.get_value_str()
            if main_format == 'TestAnswer':
                # assert str(int(self._precisionFmt2)) == self._precisionFmt2
                return self._precisionFmt2
            elif main_format == 'Task':
                with_letter = True
                with_value = True
            elif main_format == 'Value' or main_format == 'V':
                with_letter = False
                with_value = True
            elif main_format == 'Letter' or main_format == 'L':
                with_letter = True
                with_value = False
            else:
                raise RuntimeError(f'Unknown main format: {main_format!r} from {fmt!r}')

            result = ' = '.join(i for i, j in [[self.Letter, with_letter], [value_str, with_value]] if j and i)
            result = self._apply_pipes(result, pipes)
            return result
        except Exception:
            log.error(f'Error in __format__ for {fmt} and {self.__raw_line}')
            raise

    def Mult(self, other, **kws):
        return self._calculate(other, action='mult', **kws)

    def Div(self, other, **kws):
        return self._calculate(other, action='div', **kws)

    def _calculate(self, other, action=None, precisionInc=0, units='', powerShift=0):
        # TODO: skips units now

        if isinstance(other, UnitValue):
            precision = min(min(self.Precision, other.Precision) + precisionInc, 7)
            if action == 'mult':
                value = 1. * self.Value * other.Value
                power = self.Power + other.Power
            elif action == 'div':
                value = 1. * self.Value / other.Value
                power = self.Power - other.Power
            else:
                raise NotImplementedError('Could not apply %s' % action)
        elif isinstance(other, (int, float)):
            precision = min(self.Precision + precisionInc, 7)
            power = self.Power
            if action == 'mult':
                value = 1. * self.Value * other
            elif action == 'div':
                value = 1. * self.Value / other
            else:
                raise NotImplementedError('Could not apply %s' % action)

        if powerShift:
            power -= powerShift
            value *= 10 ** powerShift
        elif abs(power) <= 2:
            value *= 10 ** power
            power -= power

        r = UnitValue('%.20f 10^%d %s' % (value, power, units), precision=precision)
        return r


assert UnitValue('50 мТл').Value * (10 ** UnitValue('50 мТл').Power) == 0.05, 'Got %r' % UnitValue('50 мТл').Value
assert '{:Task}'.format(UnitValue('c = 3 10^{8} м / с')) == 'c = 3 \\cdot 10^{8}\\,\\frac{\\text{м}}{\\text{с}}', 'Got %r' % '{v:Task}'.format(v=UnitValue('c = 3 10^{8} м / с'))
assert '{:Task}'.format(UnitValue('t = 8 суток')) == 't = 8\\,\\text{суток}', 'Got %r' % '{t:Task}'.format(t=UnitValue('t = 8 суток'))
assert '{:Value}'.format(UnitValue('m = 1.67 10^-27 кг')) == '1{,}67 \\cdot 10^{-27}\\,\\text{кг}'
assert '{:Value}'.format(UnitValue('T = 1.7 суток')) == '1{,}7\\,\\text{суток}'
assert '{:Value}'.format(UnitValue('12 км / ч')) == '12\\,\\frac{\\text{км}}{\\text{ч}}'
assert '{:Value}'.format(UnitValue('50 км / ч')) == '50\\,\\frac{\\text{км}}{\\text{ч}}'
assert '{:TestAnswer}'.format(UnitValue('4 см')) == '4'
assert '{:TestAnswer}'.format(UnitValue('2.5 м')) == r'2.5', '{:TestAnswer}'.format(UnitValue('2.5 м'))


class Matter(object):
    def __init__(self, name=None, **kws):
        self.Name = name
        for key, value in kws.items():
            assert key in ['rho', 'c', 'lmbd', 'L', 'mu']
            setattr(self, key, UnitValue(value))


class Vapor:
    T_P_P_rho = [
        (0, 0.611, 4.58, 4.84),
        (1, 0.656, 4.92, 5.22),
        (2, 0.705, 5.29, 5.60),
        (3, 0.757, 5.68, 5.98),
        (4, 0.813, 6.10, 6.40),
        (5, 0.872, 6.54, 6.84),
        (6, 0.934, 7.01, 7.3),
        (7, 1.01, 7.57, 7.8),
        (8, 1.07, 8.05, 8.3),
        (9, 1.15, 8.61, 8.8),
        (10, 1.23, 9.21, 9.4),
        (11, 1.31, 9.84, 10.0),
        (12, 1.40, 10.52, 10.7),
        (13, 1.50, 11.23, 11.4),
        (14, 1.59, 11.99, 12.1),
        (15, 1.70, 12.79, 12.8),
        (16, 1.81, 13.63, 13.6),
        (17, 1.94, 14.53, 14.5),
        (18, 2.06, 15.48, 15.4),
        (19, 2.19, 16.48, 16.3),
        (20, 2.34, 17.54, 17.3),
        (21, 2.48, 18.6, 18.3),
        (22, 2.64, 19.8, 19.4),
        (23, 2.81, 21.1, 20.6),
        (24, 2.99, 22.4, 21.8),
        (25, 3.17, 23.8, 23.0),
        (30, 4.24, 31.8, 30.3),
        (40, 7.37, 55.3, 51.2),
        (50, 12.3, 92.5, 83.0),
        (60, 19.9, 149.4, 130),
        (70, 31.0, 233.7, 198),
        (80, 47.3, 355.1, 293),
        (90, 70.1, 525.8, 424),
        (100, 101.3, 760.0, 598),
    ]

    def _get_rows_pairs(self):
        for index in range(len(self.T_P_P_rho) - 1):
            yield self.T_P_P_rho[index], self.T_P_P_rho[index + 1]

    def get_rho_by_t(self, t):
        for row, next_row in self._get_rows_pairs():
            if row[0] <= t < next_row[0]:
                return (t - row[0]) / (next_row[0] - row[0]) * (next_row[3] - row[3]) + row[3]

        raise RuntimeError()

    def get_t_by_rho(self, rho):
        for row, next_row in self._get_rows_pairs():
            if row[3] <= rho < next_row[3]:
                return (rho - row[3]) / (next_row[3] - row[3]) * (next_row[0] - row[0]) + row[0]

        raise RuntimeError()


class Consts(object):
    m_e = UnitValue('m_{e} = 9.1 10^{-31} кг')
    m_p = UnitValue('m_{p} = 1.672 10^{-27} кг')
    m_n = UnitValue('m_{n} = 1.675 10^{-27} кг')
    e = UnitValue('e = 1.60 10^{-19} Кл', viewPrecision=1)
    eV = UnitValue('1.60 10^{-19} Дж', viewPrecision=1)
    h = UnitValue('h = 6.626 10^{-34} Дж с')
    c = UnitValue('c = 3 10^{8} м / с', precision=3, viewPrecision=1)
    g_ten = UnitValue('g = 10 м / с^2', precision=2)
    p_atm = UnitValue('p_{\\text{aтм}} = 100 кПа')
    aem = UnitValue('\\text{а.е.м.} = 1.66054 10^-27 кг')
    k = UnitValue('k = 9 10^9 Н м^2 / Кл^2')
    N_A = UnitValue('N_A = 6.02 10^23 / моль')
    R = UnitValue('R = 8.31 Дж / моль К')

    vapor = Vapor()

    water = Matter(
        name='вода',
        c='4200 Дж / кг К',
        lmbd='340 кДж / кг',
        L='2.3 МДж / кг',
        rho='\\rho_{\\text{в}} = 1000 кг / м^3',
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


class Fraction:
    def __init__(self, base_value=1):
        assert base_value == 1 or base_value == 0
        self._fraction = fractions.Fraction(numerator=base_value, denominator=1)

    def __mul__(self, other):
        if isinstance(other, Fraction):
            self._fraction = self._fraction * other._fraction
        else:
            self._fraction = self._fraction * other
        return self

    def __add__(self, other):
        if isinstance(other, Fraction):
            self._fraction = self._fraction + other._fraction
        else:
            self._fraction = self._fraction + other
        return self

    def __sub__(self, other):
        if isinstance(other, Fraction):
            self._fraction = self._fraction - other._fraction
        else:
            self._fraction = self._fraction - other
        return self

    def __truediv__(self, other):
        if isinstance(other, Fraction):
            self._fraction = self._fraction / other._fraction
        else:
            self._fraction = self._fraction / other
        return self

    def __float__(self):
        return float(self._fraction)

    def _escape_int(self, value):
        assert isinstance(value, int)
        if len(f'{value}') == 1:
            return f'{value}'
        else:
            return f'{{{value}}}'

    def __format__(self, fmt):
        try:
            fmt_parts = fmt.replace(':', '|').split('|')
            if len(fmt_parts) == 1:
                main_format = fmt_parts[0]
                if main_format == 'LaTeX':
                    if self._fraction.denominator == 1:
                        return str(self._fraction.numerator)
                    else:
                        nom = self._escape_int(int(self._fraction.numerator))
                        denom = self._escape_int(int(self._fraction.denominator))
                        return f'\\frac{nom}{denom}'
                else:
                    raise RuntimeError(f'Unknown main format: {main_format!r} from {fmt!r}')
            else:
                raise RuntimeError()
        except Exception:
            log.error(f'Error in __format__ for {fmt} and {self._fraction}')
            raise


def test_fraction():
    for template, frac, result in [
        ('{f:LaTeX}', Fraction(), '1'),
        ('{f:LaTeX}', Fraction(0), '0'),
        ('{f:LaTeX}', Fraction(1), '1'),
        ('{f:LaTeX}', Fraction(1) * (-2), '-2'),
        ('{f:LaTeX}', Fraction(1) * 2, '2'),
        ('{f:LaTeX}', Fraction(1) * 2 / 2, '1'),
        ('{f:LaTeX}', Fraction(1) * 2 / 2, '1'),
        ('{f:LaTeX}', Fraction(1) * 2 / 4, '\\frac12'),
        ('{f:LaTeX}', Fraction(1) * 19 / 20, '\\frac{19}{20}'),
        ('{f:LaTeX}', Fraction(1) * (-19) / 20, '\\frac{-19}{20}'),
        ('{f:LaTeX}', Fraction() / (2 * 3) * (-1) + 1, '\\frac56'),
    ]:
        res = template.format(f=frac)
        assert res == result, f'Expected {result}, got {res}'

    alpha = 3
    A_bonus_cycle = Fraction() * (alpha - 1) ** 2 / 2
    assert f'{A_bonus_cycle:LaTeX}'
    A_bonus_plus = Fraction() * (11 * alpha + 3) * (5 * alpha - 3) / (16 * 8)
    assert f'{A_bonus_plus:LaTeX}'
    U_bonus_plus = (Fraction() * 15 * (alpha + 1) ** 2 / 64 - alpha) * 3 / 2
    assert f'{U_bonus_plus:LaTeX}'
    U_bonus_12 = Fraction() * (alpha - 1) / 1 * 3 / 2
    assert f'{U_bonus_12:LaTeX}'
    eta_bonus = Fraction() * A_bonus_cycle / (U_bonus_plus + A_bonus_plus + U_bonus_12)
    assert f'{eta_bonus:LaTeX}'


test_fraction()

def test_vapor():
    vapor = Vapor()
    assert vapor.get_rho_by_t(80) == 293
    assert vapor.get_rho_by_t(65) == 164
    assert vapor.get_t_by_rho(293) == 80


test_vapor()


def test_calculation():
    for expr, answer in [
        ('{:Value}'.format(Consts.c.Div(UnitValue('l = 500 нм'), units='Гц', powerShift=3)), '6{,}00 \\cdot 10^{14}\\,\\text{Гц}'),
        ('{:Value}'.format(UnitValue('9 10^25').Div(Consts.N_A)), '150'),
        ('{:V}'.format(UnitValue('9 10^25').Div(UnitValue('6.03 10^23'), precisionInc=1)), '149'),
        ('{:V}'.format(UnitValue('9 10^25').Div(UnitValue('6.03 10^23'), precisionInc=0)), '150'),
    ]:
        assert expr == answer, f'Expected |{answer}|, got |{expr}|'

test_calculation()
