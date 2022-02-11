from generators.helpers.unit import OneUnit, BaseUnits, SimpleUnits, get_simple_unit
from generators.helpers.fraction import decimal_to_fraction
from generators.helpers.precision import format_with_precision, get_precision
from library.util.asserts import assert_equals

from library.logging import colorize_json, cm, color

import logging
log = logging.getLogger(__name__)

from decimal import Decimal

import math


class Calculation:
    PLUS = 'plus'
    MINUS = 'minus'
    DIV = 'div'
    MULT = 'mult'


class Pipes:
    PIPES_DICT = {
        's': '{{{}}}',
        'e': '${}$',
        'sqr': '\\sqr{{{}}}',
        'sqrt': '\\sqrt{{{}}}',
        'cdot': '{} \\cdot',
        'inv': '\\frac 1{{{}}}',
    }

    def apply(self, line, pipes):
        for pipe in pipes:
            pipe_fmt = self.PIPES_DICT.get(pipe)
            if pipe_fmt is None:
                raise RuntimeError(f'Unknown pipe {pipe}')
            line = pipe_fmt.format(line)
        return line


PIPES = Pipes()


class UnitValue:
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
        assert isinstance(letter, str)
        if self._letter:
            raise RuntimeError(f'Could not overwrite letter for {self} to {letter}')
        self._letter = letter.strip()
        return self

    def IncPrecision(self, incPrecision=1):
        assert isinstance(incPrecision, int)
        assert incPrecision >= 1, incPrecision
        self.Precision += incPrecision
        if self.ViewPrecision:
            self.ViewPrecision += incPrecision

        return self

    def _substitute_calc(self, line):
        for key, value in [
            ('/', ' / '),
            ('**', '^'),
            (' ^', '^'),
            ('^ ', '^'),
            (' * ', ' '),
            ('  ', ' '),
        ]:
            line = line.replace(key, value)
        return line

    def _load(self, line, precision=None):
        assert isinstance(line, str)
        assert line.count('/') <= 1
        assert line.count('=') <= 1

        if '=' in line:
            letter_line, line = line.split('=', 1)
            self.SetLetter(letter_line)

        line = line.strip()
        line = self._substitute_calc(line)

        self.ValuePower = 0
        self.Value = None
        self._units = []

        is_numerator = True
        for part in line.split():
            try:
                float(part)
            except ValueError:
                if part.startswith('10^'):
                    self.ValuePower = int(part[3:].strip('{').strip('}'))
                elif part == '/':
                    is_numerator = False
                else:
                    self._units.append(OneUnit(part, is_numerator))
            else:
                assert self.Value is None
                self.Value = Decimal(part)
                self.Precision = get_precision(part) if precision is None else precision

        if self.Value is None:
            assert self._units, f'No units for {line!r}'
            self.Value = Decimal(1)
            self.Precision = None

    def __str__(self):
        return f'UVS {self.__raw_line!r}'

    def __repr__(self):
        return f'UVR {self.__raw_line!r}@{self.Precision}'

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
                valueStr = format_with_precision(self.Value, self.ViewPrecision or self.Precision or 1)
            self._format_with_precision = str(valueStr)
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
            base_units = unit.base_units
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
                # assert str(int(self._format_with_precision)) == self._format_with_precision
                return self._format_with_precision
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

            result = PIPES.apply(result, pipes)
            return result
        except Exception:
            log.error(f'Error in __format__ for format {fmt!r} and raw line {self.__raw_line!r}')
            raise

    def __mul__(self, other):
        return calculate(self, other, action=Calculation.MULT)

    def __truediv__(self, other):
        return calculate(self, other, action=Calculation.DIV)

    def __rmul__(self, other):
        return calculate(self, other, action=Calculation.MULT)

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
        return decimal_to_fraction(self.SI_Value)

    def As(self, other):
        assert isinstance(other, str)
        other_uv = UnitValue(other)
        this_units = self.get_base_units()
        other_units = other_uv.get_base_units()
        assert this_units == other_units, f'Got {this_units} and {other_units} for {self!s} and {other!s}'
        result = calculate(self, other_uv, action=Calculation.DIV, units=other)

        # preserve letter if exists
        if self._letter:
            result.SetLetter(self._letter)

        return result


def get_calc_precision(left, other_value, left_precision, right_precision, action):
    MAX_PRECISION = 7

    if action in [Calculation.MULT, Calculation.DIV]:
        if left_precision is not None and right_precision is not None:
            precision = min(left_precision, right_precision)
        elif left_precision is None and right_precision is not None:
            precision = right_precision
        elif left_precision is not None and right_precision is None:
            precision = left_precision
        else:
            precision = None

        if precision is None:
            precision = MAX_PRECISION
        else:
            precision = min(precision, MAX_PRECISION)

    elif action in [Calculation.PLUS]:
        value = left.SI_Value + other_value
        assert this_units == other_units
        calced_units = this_units

    else:
        raise NotImplementedError(f'Could not apply unknown action {action!r}')

    return precision


def calculate(left, right, action=None, units=None):
    this_units = left.get_base_units()

    if isinstance(right, UnitValue):
        other_units = right.get_base_units()
        other_precision = right.Precision
        other_value = right.SI_Value
    elif isinstance(right, (int, float, Decimal)):
        other_units = {}
        other_precision = None
        other_value = Decimal(str(right))
    else:
        raise RuntimeError('right {!r} is not supported')

    precision = get_calc_precision(left, other_value, left.Precision, other_precision, action)

    if action in [Calculation.MULT, Calculation.DIV]:
        used_units = set(this_units) | set(other_units)
        calced_units = {}
        if action == Calculation.MULT:
            value = left.SI_Value * other_value
            for key in used_units:
                calced_units[key] = this_units.get(key, 0) + other_units.get(key, 0)

        elif action == Calculation.DIV:
            value = left.SI_Value / other_value
            for key in used_units:
                calced_units[key] = this_units.get(key, 0) - other_units.get(key, 0)

    elif action in [Calculation.PLUS]:
        value = left.SI_Value + other_value
        assert this_units == other_units
        calced_units = this_units

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

    # print(self, other, action, line, precision)
    r = UnitValue(line, precision=precision)
    return r


def test_unit_value():
    UV = UnitValue

    assert UV('2').Precision == 1
    assert UV('2').IncPrecision(2).Precision == 3

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
        ('{:Value}', (UV('0.0288 А') / UV('6.18 с') * 3 * math.pi**2), '0{,}1380\\,\\frac{\\text{А}}{\\text{с}}'),
        (
            '{:V}',
            UnitValue('h = 6.626 10^{-34} Дж с') * UnitValue('c = 3 10^{8} м / с', precision=3) / UnitValue('200 нм'),
            r'0{,}994 \cdot 10^{-18}\,\text{Дж}',
        ),
        ('{:V}', (UV('0.94') * UV('859 мА') * UV('200 В') / UV('4.3 А')).As('В'), '38\\,\\text{В}'),
        ('{:V}', UV('38 В') * UV('4.3 А') / (UV('859 мА') * UV('200 В')), '0{,}95'),
        ('{:V}', (UV('70 мГн') * UV('6 А')).As('мВб'), '420\\,\\text{мВб}'),
        # ('{:V}', UnitValue('600000000000000000 Гц', precision=3), '6 \\cdot 10^{14}\\,\\text{Гц}'),  # TODO
        ('{:V}', UV('2').IncPrecision(2), '2'),
        ('{:V}', UV('2.').IncPrecision(2), '2'),
    ]
    for fmt, unit_value, canonic in data:
        result = fmt.format(unit_value)
        assert_equals(f'unit_value {unit_value!r}', canonic, result)

    assert UnitValue('1230 * 10^2').SI_Value == 123000


test_unit_value()


def test_get_base_units():
    data = [
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
        assert_equals(f'unit_value {unit_value!r}', base_units, result)

    unit_value = UnitValue('50 мВт мс')
    result = get_simple_unit(unit_value.get_base_units())
    assert result == SimpleUnits.joule, result
    assert unit_value.SI_Value == Decimal('0.00005')


test_get_base_units()


def test_as_conversion():
    data = [
        ('1 10^-17 Дж', 'эВ', '60\\,\\text{эВ}'),
        ('100 10^-12 Дж', 'МэВ', '625\\,\\text{МэВ}'),
        ('100 кэВ', 'Дж', '16 \\cdot 10^{-15}\\,\\text{Дж}'),
        ('10^-24 кг', 'а.е.м.', '602{,}2137\\,\\text{а.е.м.}'),
        ('1000 10^-27 кг', 'а.е.м.', '602\\,\\text{а.е.м.}'),
        ('10^-24 г', 'а.е.м.', '0{,}6022137\\,\\text{а.е.м.}'),
    ]
    for line, as_to, canonic in data:
        unit_value = UnitValue(line)
        result = '{:V}'.format(unit_value.As(as_to))
        assert_equals(f'{line!r} to {as_to!r}', canonic, result)


test_as_conversion()
