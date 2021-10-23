from generators.helpers.unit import OneUnit, BaseUnits, SimpleUnits, get_simple_unit
from generators.helpers.fraction import decimal_to_fraction

from library.logging import colorize_json, cm, color

import logging
log = logging.getLogger(__name__)
from decimal import Decimal, ROUND_05UP


def precisionFmt2(value, precision):
    if isinstance(value, int):
        return str(value)
    elif isinstance(value, str):
        if value.isdigit():
            return value

    assert isinstance(value, (float, Decimal)), f'{value} is {type(value)}'

    if int(value) == value:
        return str(int(value))

    isNegative = value < 0
    absValue = abs(value)
    assert absValue >= 10 ** -7, f'Got value of {absValue}'
    assert 1 <= precision <= 10, f'Got precision {precision} for {value}'

    decimal_value = Decimal(absValue)
    shift = 0
    while not (10 ** (precision - 1) <= decimal_value < 10 ** precision):
        if decimal_value < 10 ** (precision - 1):
            decimal_value *= 10
            shift += 1
        else:
            decimal_value /= 10
            shift -= 1

    if str(decimal_value)[0] == '1':
        precision += 1
        decimal_value *= 10
        shift += 1

    decimal_value += Decimal(0.5)
    decimal_value = Decimal(int(decimal_value))
    decimal_value *= Decimal(10) ** (-shift)
    decimal_value = decimal_value.quantize(Decimal(10) ** -shift)

    rawDigits = str(decimal_value)

    if isNegative:
        rawDigits = '-' + rawDigits
    return rawDigits


def test_precisionFmt2():
    for value, precision, result in [
        (1, 1, '1'),
        (1.0, 1, '1'),
        (Decimal(1), 1, '1'),
        (1.7, 1, '1.7'),
        (0.091, 2, '0.091'),
        (0.095, 2, '0.095'),
        (0.0949, 2, '0.095'),
        (-0.0949, 2, '-0.095'),
        (0.99, 2, '0.99'),
        (0.99, 1, '1.0'),
        (1.99, 2, '1.99'),
        (1.99, 3, '1.990'),
        (19.9, 2, '19.9'),
        (19.9, 1, '20'),
        (12, 1, '12'),
        (12, 2, '12'),
        (20, 2, '20'),
        (20, 1, '20'),
        (2.99, 2, '3.0'),
        (29.9, 2, '30'),
        (299., 2, '299'),
        (299, 2, '299'),
        (1 + 1. / 30, 2, '1.03'),
        (1 + 1. / 300, 2, '1.00'),
        (1 + 1. / 300, 3, '1.003'),
        (1. / 3, 2, '0.33'),
        (4. / 3, 2, '1.33'),
        (7. / 3, 2, '2.3'),
        (7. / 3, 3, '2.33'),
        (700. / 3, 3, '233'),
        (700. / 3, 3, '233'),
        (7000. / 3, 3, '2330'),
        (7000. / 3, 2, '2300'),
        (7000. / 3, 1, '2000'),
        (8000. / 3, 1, '3000'),
        (7000. / 3, 4, '2333'),
        (7000. / 3, 5, '2333.3'),
        (1000. / 3, 5, '333.33'),
        (100. / 3, 5, '33.333'),
        (10. / 3, 5, '3.3333'),
        (0.1 / 3, 5, '0.033333'),
        (0.01 / 3, 5, '0.0033333'),
        (0.001 / 3, 5, '0.00033333'),
        (0.0049594, 5, '0.0049594'),
        (0.0049594, 4, '0.004959'),
        (0.0049595, 4, '0.004960'),
        (0.0049594, 3, '0.00496'),
        (0.0049594, 2, '0.0050'),
        (0.0049594, 1, '0.005'),
    ]:
        res = precisionFmt2(value, precision)
        assert res == result, f'Expected {value}, {precision} -> {result}, got {res!r}'


test_precisionFmt2()


def get_precision(line):
    precisionStr = line.replace('-', '').replace('.', '').lstrip('0')
    if not precisionStr:
        assert line in ['0', '0.0', '0.00'], f'Could not get precision from {line!r}'
        is_zero = True
        precisionStr = '0'
    else:
        is_zero = False
    precision = len(precisionStr)
    if precisionStr[0] == '1' and precision >= 2:
        precision -= 1

    assert precision >= 1, f'Got invalid precision {self.Precision} from {line!r}'

    return is_zero, precision


def test_get_precision():
    data = [
        ('-2.0', False, 2),
        ('2.0', False, 2),
        ('2.00', False, 3),
        ('0.0020', False, 2),
        ('0.00200', False, 3),
        ('20', False, 2),
        ('200', False, 3),
        ('192', False, 2),
        ('0', True, 1),
        ('0.0', True, 1),
        ('0.00', True, 1),
    ]
    for line, is_zero, precision in data:
        result = get_precision(line)
        assert result[0] == is_zero, f'Expected {is_zero},  got {result[0]} for {line}'
        assert result[1] == precision, f'Expected {precision},  got {result[1]} for {line}'


test_get_precision()


class Pipes:
    PIPES_DICT = {
        's': '{{{}}}',
        'e': '${}$',
        'sqr': '\\sqr{{{}}}',
        'sqrt': '\\sqrt{{{}}}',
        'cdot': '{} \\cdot'
    }

    def apply(self, line, pipes):
        for pipe in pipes:
            pipe_fmt = self.PIPES_DICT.get(pipe)
            if pipe_fmt is None:
                raise RuntimeError(f'Unknown pipe {pipe}')
            line = pipe_fmt.format(line)
        return line



class UnitValue:
    PIPES = Pipes()

    def __init__(self, line, precision=None, viewPrecision=None):
        self.__raw_line = line
        self._is_zero = None
        try:
            self._load(line, precision=precision)
        except Exception:
            log.error(f'Could not load unit from {cm(self.__raw_line, color=color.Red)}')
            raise
        self.ViewPrecision = viewPrecision
        self._value_str = None

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
            '^ ': '^',
        }.items():
            value_line = value_line.replace(key, value)

        self.ValuePower = 0
        self.Value = None
        self._units = []

        isNumerator = True
        for part in value_line.split():
            if self.Value is None:
                self.Value = Decimal(part)
                # self.Value = int(part) if part.isdigit() else float(part)

                if precision is None:
                    self._is_zero, self.Precision = get_precision(part)
                else:
                    self.Precision = precision

            elif part.startswith('10^'):
                self.ValuePower = int(part[3:].strip('{').strip('}'))

            elif part == '/':
                isNumerator = False

            else:
                self._units.append(OneUnit(part, isNumerator))

        self._power = sum(unit.SiPower if unit.IsNumerator else -unit.SiPower for unit in self._units) + self.ValuePower

    def __str__(self):
        return f'UVS {self.__raw_line}'

    def __repr__(self):
        return f'UVR {self.__raw_line!r}'

    def _get_units_tex(self):
        humanNom = '\\cdot'.join(unit.get_tex() for unit in self._units if unit.IsNumerator)
        humanDen = '\\cdot'.join(unit.get_tex() for unit in self._units if not unit.IsNumerator)
        if humanDen and humanNom:
            return f'\\,\\frac{{{humanNom}}}{{{humanDen}}}'
        elif humanDen and not humanNom:
            return f'\\,\\frac{{1}}{{{humanDen}}}'
        elif not humanDen and humanNom:
            return f'\\,{humanNom}'
        return ''

    def get_value_str(self):
        if self._value_str is None:
            if self._is_zero:
                valueStr = '0'
            else:
                valueStr = precisionFmt2(self.Value, self.ViewPrecision or self.Precision)
                # print(self.Value, self.ViewPrecision or self.Precision, valueStr)
            self._precisionFmt2 = str(valueStr)
            valueStr = valueStr.replace('.', '{,}')
            if self.ValuePower:
                valueStr += f' \\cdot 10^{{{self.ValuePower}}}'
            valueStr += self._get_units_tex()
            self._value_str = valueStr
        return self._value_str

    def get_base_units(self):
        total_units = {}
        for unit in self._units:
            mult = 1 if unit.IsNumerator else -1
            base_units = unit.simple_unit._base_units
            for base_unit, degree in base_units.items():
                if base_unit not in total_units:
                    total_units[base_unit] = 0
                total_units[base_unit] = total_units[base_unit] + degree * mult
        return total_units

    def __format__(self, fmt):
        try:
            fmt_parts = fmt.replace(':', '|').split('|')
            main_format, pipes = fmt_parts[0], fmt_parts[1:]

            value_str = self.get_value_str()
            if main_format == 'TestAnswer':
                # assert str(int(self._precisionFmt2)) == self._precisionFmt2
                return self._precisionFmt2
            elif main_format == 'Task':
                assert self.Letter and value_str
                result = f'{self.Letter} = {value_str}'
            elif main_format == 'Value' or main_format == 'V':
                assert value_str
                result = value_str
            elif main_format == 'Letter' or main_format == 'L':
                assert self.Letter
                result = self.Letter
            else:
                raise RuntimeError(f'Unknown main format: {main_format!r} from {fmt!r} for {self.__raw_line}')

            result = self.PIPES.apply(result, pipes)
            return result
        except Exception:
            log.error(f'Error in __format__ for {fmt} and {self.__raw_line}')
            raise

    def Mult(self, other, **kws):
        return self._calculate(other, action='mult', **kws)

    def Div(self, other, **kws):
        return self._calculate(other, action='div', **kws)

    def __mul__(self, other):
        return self.Mult(other)

    def __truediv__(self, other):
        return self.Div(other)

    def __rmul__(self, other):
        return self.Mult(other)

    @property
    def SI_Value(self):
        return self.Value * Decimal(10) ** self._power

    @property
    def frac_value(self):
        return decimal_to_fraction(self.Value)

    def _calculate(self, other, action=None, precisionInc=0, units='', powerShift=0):
        # TODO: skips units now

        if isinstance(other, UnitValue):
            precision = min(min(self.Precision, other.Precision) + precisionInc, 7)
            if action == 'mult':
                value = self.Value * other.Value
                power = self._power + other._power
            elif action == 'div':
                value = self.Value / other.Value
                power = self._power - other._power
            else:
                raise NotImplementedError(f'Could not apply {action}')
        elif isinstance(other, (int, float, Decimal)):
            precision = min(self.Precision + precisionInc, 7)
            power = self._power
            if action == 'mult':
                value = self.Value * Decimal(other)
            elif action == 'div':
                value = self.Value / Decimal(other)
            else:
                raise NotImplementedError(f'Could not apply {action}')
        else:
            raise NotImplementedError(f'Could not apply {action}')

        if powerShift:
            power -= powerShift
            value *= Decimal(10) ** powerShift
        elif abs(power) <= 2:
            value *= Decimal(10) ** power
            power -= power

        r = UnitValue('%.20f 10^%d %s' % (value, power, units), precision=precision)
        return r


def test_unit_value():
    data = [
        (UnitValue('50 мТл').Value * (Decimal(10) ** UnitValue('50 мТл')._power), Decimal('0.050')),
        ('{:Task}'.format(UnitValue('c = 3 10^{8} м / с')), 'c = 3 \\cdot 10^{8}\\,\\frac{\\text{м}}{\\text{с}}'),
        ('{:Task}'.format(UnitValue('t = 8 суток')), 't = 8\\,\\text{суток}'),
        ('{:Value}'.format(UnitValue('m = 1.67 10^-27 кг')), '1{,}67 \\cdot 10^{-27}\\,\\text{кг}'),
        ('{:Value}'.format(UnitValue('T = 1.7 суток')), '1{,}7\\,\\text{суток}'),
        ('{:Value}'.format(UnitValue('12 км / ч')), '12\\,\\frac{\\text{км}}{\\text{ч}}'),
        ('{:Value}'.format(UnitValue('50 км / ч')), '50\\,\\frac{\\text{км}}{\\text{ч}}'),
        ('{:TestAnswer}'.format(UnitValue('4 см')), '4'),
        ('{:Value}'.format(UnitValue('0 см')), '0\\,\\text{см}'),
        ('{:Value}'.format(UnitValue('0 см')), '0\\,\\text{см}'),
        ('{:Task}'.format(UnitValue('A = 200 Дж')), 'A = 200\\,\\text{Дж}'),
        ('{:TestAnswer}'.format(UnitValue('2.5 м')), r'2.5'),
        ('{:Value}'.format(UnitValue('2 10^4 км/c')), '2 \\cdot 10^{4}\\,\\frac{\\text{км}}{\\text{c}}'),
    ]
    for src, canonic in data:
        assert src == canonic, f'Expected {canonic}, got {src}'


test_unit_value()


def test_get_base_units():
    data = [
        ('50 мДж', {BaseUnits.m: 2, BaseUnits.s: -2, BaseUnits.kg: 1}),
        ('50 Дж с', {BaseUnits.m: 2, BaseUnits.s: -1, BaseUnits.kg: 1}),
        ('50 мВт мс', {BaseUnits.m: 2, BaseUnits.s: -2, BaseUnits.kg: 1}),
    ]
    for line, base_units in data:
        unit_value = UnitValue(line)
        result = unit_value.get_base_units()
        assert result == base_units, f'Expected {base_units}, got {result}'

    unit_value = UnitValue('50 мВт мс')
    result = get_simple_unit(unit_value.get_base_units())
    assert result == SimpleUnits.joule, result

    # assert unit_value.SI_Value == 50e-6, unit_value.SI_Value


test_get_base_units()
