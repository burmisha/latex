from generators.helpers.unit import OneUnit, BaseUnits, SimpleUnits, get_simple_unit
from generators.helpers.fraction import decimal_to_fraction

from library.logging import colorize_json, cm, color

import logging
log = logging.getLogger(__name__)
from decimal import Decimal
import math


def precisionFmt2(value, precision):
    assert isinstance(value, (int, float, Decimal)), f'Value {value} has type {type(value)}'
    assert isinstance(precision, int), f'Got precision {precision} for {value}'
    assert 1 <= precision <= 10, f'Got precision {precision} for {value}'

    if int(value) == value:
        return str(int(value))

    abs_value = float(abs(value))

    shift = 0
    lower = 10 ** (precision - 1)
    upper = 10 ** precision
    while not (lower <= abs_value < upper):
        if abs_value < lower:
            abs_value *= 10
            shift += 1
        else:
            abs_value /= 10
            shift -= 1

    leading_one = False
    if str(abs_value).startswith('1'):
        precision += 1
        abs_value *= 10
        shift += 1
        leading_one = True

    int_value = int(abs_value + 0.5)
    result = str(int_value)

    more_zeros = 0
    if len(result) < precision:
        more_zeros = precision - len(result)
        if more_zeros and leading_one:
            more_zeros -= 1
    result += '0' * more_zeros

    if shift < 0:
        result += '0' * (-shift)
    elif shift > 0:
        if len(result) >= shift + 1:
            result = result[:-shift] + '.' + result[-shift:]
        else:
            result = '0.' + '0' * (shift - len(result)) + result

    if value < 0:
        result = '-' + result
    return result


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
        (3 / 10 ** 7, 2, '0.00000030'),
        (3 / 10 ** 7, 1, '0.0000003'),
        (3 * 10 ** 7, 1, '30000000'),
        (3 * 10 ** 7, 2, '30000000'),
    ]:
        res = precisionFmt2(value, precision)
        assert res == result, f'Expected {value}, {precision} -> {result}, got {res!r}'


test_precisionFmt2()


def get_precision(line):
    precisionStr = line.replace('-', '').replace('.', '').lstrip('0')
    if not precisionStr:
        assert line in ['0', '0.0', '0.00'], f'Could not get precision from {line!r}'
        precisionStr = '0'

    precision = len(precisionStr)
    if precisionStr[0] == '1' and precision >= 2:
        precision -= 1

    assert precision >= 1, f'Got invalid precision {precision} from {line!r}'

    return precision


def test_get_precision():
    data = [
        ('-2.0', 2),
        ('2.0', 2),
        ('2.00', 3),
        ('0.0020', 2),
        ('0.00200', 3),
        ('20', 2),
        ('200', 3),
        ('192', 2),
        ('0', 1),
        ('0.0', 1),
        ('0.00', 1),
    ]
    for line, precision in data:
        result = get_precision(line)
        assert result == precision, f'Expected {precision},  got {result} for {line}'


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
        self._letter = None
        try:
            self._load(line, precision=precision)
        except Exception:
            log.error(f'Could not load unit from {cm(self.__raw_line, color=color.Red)}')
            raise
        self.ViewPrecision = viewPrecision
        self._value_str = None

    def SetLetter(self, letter):
        if self._letter:
            raise RuntimeError(f'Could not overwrite letter for {self} to {letter}')
        assert isinstance(letter, str)
        self._letter = letter.strip()
        return self

    def IncPrecision(self, incPrecision=1):
        assert isinstance(incPrecision, int)
        assert incPrecision >= 1, incPrecision
        self.Precision += 1
        if self.ViewPrecision:
            self.ViewPrecision += 1

        return self

    def _load(self, line, precision=None):
        assert isinstance(line, str)
        assert line.count('/') <= 1
        assert line.count('=') <= 1

        line = line.strip()

        if '=' in line:
            letter_line, value_line = line.split('=', 1)
            value_line = value_line.strip()
            self.SetLetter(letter_line)
        else:
            value_line = line

        for key, value in {
            '/': ' / ',
            '**': '^',
            ' ^': '^',
            '^ ': '^',
        }.items():
            value_line = value_line.replace(key, value)

        self.ValuePower = 0
        self.Value = Decimal(1)
        self.Precision = 1  # TODO
        self._ValueWasSet = False
        self._units = []

        isNumerator = True
        for part in value_line.split():
            try:
                float(part)
            except ValueError:
                is_value = False
            else:
                is_value = True

            if is_value:
                if self._ValueWasSet:
                    raise RuntimeError('Multiple values')
                self.Value = Decimal(part)
                self.Precision = get_precision(part) if precision is None else precision
                self._ValueWasSet = True


            elif part.startswith('10^'):
                self.ValuePower = int(part[3:].strip('{').strip('}'))

            elif part == '/':
                isNumerator = False

            elif part == '*':
                continue

            else:
                self._units.append(OneUnit(part, isNumerator))

    def __str__(self):
        return f'UVS {self.__raw_line!r}'

    def __repr__(self):
        return f'UVR {self.__raw_line!r}@{self.ViewPrecision or self.Precision}'

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
            if self.Value.is_zero():
                valueStr = '0'
            else:
                valueStr = precisionFmt2(self.Value, self.ViewPrecision or self.Precision)
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
                total_units[base_unit] = total_units[base_unit] + degree * mult * unit.HumanPower
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
                assert self._letter and value_str
                result = f'{self._letter} = {value_str}'
            elif main_format == 'Value' or main_format == 'V':
                assert value_str
                result = value_str
            elif main_format == 'Letter' or main_format == 'L':
                assert self._letter
                result = self._letter
            else:
                raise RuntimeError(f'Unknown main format: {main_format!r} from {fmt!r} for {self.__raw_line!r}')

            result = self.PIPES.apply(result, pipes)
            return result
        except Exception:
            log.error(f'Error in __format__ for format {fmt!r} and raw line {self.__raw_line!r}')
            raise

    def __mul__(self, other):
        return self._calculate(other, action='mult')

    def __truediv__(self, other):
        return self._calculate(other, action='div')

    def __rmul__(self, other):
        return self._calculate(other, action='mult')

    @property
    def SI_Value(self):
        result = self.Value * Decimal(10) ** self.ValuePower
        for unit in self._units:
            if unit.IsNumerator:
                result *= unit.SiMultiplier
            else:
                result /= unit.SiMultiplier
        return result

    @property
    def frac_value(self):
        return decimal_to_fraction(self.Value)

    def _calculate(self, other, action=None, units=None):
        MAX_PRECISION = 7

        if isinstance(other, (int, float, Decimal)):
            other = UnitValue(str(other))

        assert isinstance(other, UnitValue)

        this_units = self.get_base_units()
        other_units = other.get_base_units()
        used_units = set(this_units) | set(other_units)

        calced_units = {}

        if other._ValueWasSet:
            precision = min(self.Precision, other.Precision)
        else:
            precision = self.Precision
        precision = min(precision, MAX_PRECISION)

        if action == 'mult':
            value = self.SI_Value * other.SI_Value
            for key in used_units:
                calced_units[key] = this_units.get(key, 0) + other_units.get(key, 0)

        elif action == 'div':
            value = self.SI_Value / other.SI_Value
            for key in used_units:
                calced_units[key] = this_units.get(key, 0) - other_units.get(key, 0)
        else:
            raise NotImplementedError(f'Could not apply unknown action {action!r}')

        t = value
        if value > 10 ** 5 or value < 10 ** -4:
            power = int(abs(value).log10()) // 3 * 3
            value *= Decimal(10) ** -power
        else:
            power = 0

        if not units:
            simple_unit = get_simple_unit(calced_units)
            if simple_unit:
                units = simple_unit._short_name

            else:
                sorted_units = sorted(calced_units.items())
                nom_units = [(key, value) for key, value in sorted_units if value > 0]
                denom_units = [(key, abs(value)) for key, value in sorted_units if value < 0]
                units = ' '.join([f'{key._name}^{value}' for key, value in nom_units])
                if denom_units:
                    units += ' / '
                    units += ' '.join([f'{key._name}^{value}' for key, value in denom_units])

        line = f'{value}'
        if power:
            line += f' 10^{{{power}}}'
        if units:
            line += f' {units}'

        r = UnitValue(line, precision=precision)
        return r

    def As(self, other):
        assert isinstance(other, str)
        other_uv = UnitValue(other)
        this_units = self.get_base_units()
        other_units = other_uv.get_base_units()
        assert this_units == other_units, f'Got {this_units} and {other_units} for {self!s} and {other!s}'
        result = self._calculate(other_uv, action='div', units=other)
        return result


def test_unit_value():
    UV = UnitValue
    data = [
        ('{:Task}', UnitValue('c = 3 10^{8} м / с'), 'c = 3 \\cdot 10^{8}\\,\\frac{\\text{м}}{\\text{с}}'),
        ('{:Task}', UnitValue('t = 8 суток'), 't = 8\\,\\text{суток}'),
        ('{:Value}', UnitValue('m = 1.67 10^-27 кг'), '1{,}67 \\cdot 10^{-27}\\,\\text{кг}'),
        ('{:Value}', UnitValue('T = 1.7 суток'), '1{,}7\\,\\text{суток}'),
        ('{:Value}', UnitValue('12 км / ч'), '12\\,\\frac{\\text{км}}{\\text{ч}}'),
        ('{:Value}', UnitValue('50 км / ч'), '50\\,\\frac{\\text{км}}{\\text{ч}}'),
        ('{:TestAnswer}', UnitValue('4 см'), '4'),
        ('{:Value}', UnitValue('0 см'), '0\\,\\text{см}'),
        ('{:Value}', UnitValue('0 см'), '0\\,\\text{см}'),
        ('{:Value}', UnitValue('2 а.е.м.'), '2\\,\\text{а.е.м.}'),
        ('{:Task}', UnitValue('A = 200 Дж'), 'A = 200\\,\\text{Дж}'),
        ('{:TestAnswer}', UnitValue('2.5 м'), r'2.5'),
        ('{:V}', UnitValue(''), '1'),
        ('{:V}', UnitValue('0'), '0'),
        ('{:V}', UnitValue('1'), '1'),
        ('{:V}', UnitValue('1230 10^2'), '1230 \\cdot 10^{2}'),
        ('{:V}', UnitValue('1230 * 10^2'), '1230 \\cdot 10^{2}'),
        ('{:V}', UnitValue('Гц'), '1\\,\\text{Гц}'),
        ('{:V}', UnitValue('Гц') * UnitValue('500'), '500\\,\\text{Гц}'),
        ('{:V}', UnitValue('Гц') * UnitValue('500'), '500\\,\\text{Гц}'),
        ('{:V}', UnitValue('2 кг') * UnitValue('5 м / с') * 3, '30\\,\\frac{\\text{кг}\\cdot\\text{м}}{\\text{с}}'),
        ('{:V}', UnitValue('20 м/с') / UnitValue('10 м/с^2'), '2\\,\\text{с}'),
        ('{:V}', UnitValue('20 м/с') * UnitValue('20 м/с'), '400\\,\\text{Гр}'),
        ('{:V}', UnitValue('400 Гр') / UnitValue('10 м/с^2'), '40\\,\\text{м}'),
        ('{:V}', UnitValue('20 м/с') * UnitValue('20 м/с') / UnitValue('10 м/с^2'), '40\\,\\text{м}'),
        ('{:V}', UnitValue('10 мин') * UnitValue('5 Гц'), '3000'),
        ('{:Task}', (UnitValue('10 мин') * UnitValue('5 Гц')).SetLetter('l'), 'l = 3000'),
        ('{:Value}', UnitValue('2 10^4 км/c'), '2 \\cdot 10^{4}\\,\\frac{\\text{км}}{\\text{c}}'),
        ('{:Value}', (UV('0.0288 А') / UV('6.18 с') * 3 * math.pi**2).IncPrecision(1), '0{,}138\\,\\frac{\\text{А}}{\\text{с}}'),
        # ('{:Value}', UV('0.94') * UV('859 мА') * UV('200 В') / UV('4.3 А'), '0{,}95'),
        # ('{:Value}', UV('38 В') * UV('4.3 А') / (UV('859 мА') * UV('200 В')), '0{,}95'),
        # ('{:V}'.format(UnitValue('600000000000000000 Гц', precision=3)), '6 \\cdot 10^{14}\\,\\text{Гц}'),  # TODO
    ]
    for fmt, unit_value, canonic in data:
        result = fmt.format(unit_value)
        assert result == canonic, f'Expected {canonic!r} for {unit_value!r}, got {result!r}'

    assert UnitValue('1230 * 10^2').SI_Value == 123000


test_unit_value()


def test_get_base_units():
    data = [
        ('', {}),
        ('1', {}),
        ('Гц', {BaseUnits.s: -1}),
        ('м^3 кг^1 / с^2', {BaseUnits.m: 3, BaseUnits.s: -2, BaseUnits.kg: 1}),
        ('50 мДж', {BaseUnits.m: 2, BaseUnits.s: -2, BaseUnits.kg: 1}),
        ('50 Дж с', {BaseUnits.m: 2, BaseUnits.s: -1, BaseUnits.kg: 1}),
        ('50 мВт мс', {BaseUnits.m: 2, BaseUnits.s: -2, BaseUnits.kg: 1}),
        ('50 Гц', {BaseUnits.s: -1}),
        ('1 Гр', {BaseUnits.m: 2, BaseUnits.s: -2}),
        ('1 г', {BaseUnits.kg: 1}),
        ('1 а.е.м.', {BaseUnits.kg: 1}),
    ]
    for line, base_units in data:
        unit_value = UnitValue(line)
        result = unit_value.get_base_units()
        assert result == base_units, f'Expected {base_units}, got {result} for {unit_value!r}'

    unit_value = UnitValue('50 мВт мс')
    result = get_simple_unit(unit_value.get_base_units())
    assert result == SimpleUnits.joule, result
    assert unit_value.SI_Value == Decimal('0.00005')


test_get_base_units()


def test_as_conversion():
    data = [
        ('10^-17 Дж', 'эВ', '60\\,\\text{эВ}'),
        ('10^-12 Дж', 'МэВ', '6\\,\\text{МэВ}'),
        ('100 10^-12 Дж', 'МэВ', '625\\,\\text{МэВ}'),
        ('100 кэВ', 'Дж', '16 \\cdot 10^{-15}\\,\\text{Дж}'),
        ('10^-24 кг', 'а.е.м.', '600\\,\\text{а.е.м.}'),
        ('1000 10^-27 кг', 'а.е.м.', '602\\,\\text{а.е.м.}'),
        ('10^-24 г', 'а.е.м.', '0{,}6\\,\\text{а.е.м.}'),
    ]
    for line, as_to, canonic in data:
        unit_value = UnitValue(line)
        result = '{:V}'.format(unit_value.As(as_to))
        assert result == canonic, f'Expected {canonic}, got {result} for {line!r} to {as_to}'


test_as_conversion()
