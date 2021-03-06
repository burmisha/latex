from generators.helpers.unit import OneUnit

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
    assert absValue >= 10 ** -7, f'Got value of {absValue}'
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


def test_precisionFmt2():
    for value, precision, result in [
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
        (12, 2, '12'),
        (20, 2, '20'),
        (2.99, 2, '3.0'),
        (29.9, 2, '30'),
        (299., 2, '300'),
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
        assert res == result, f'Expected {value}, {precision} -> {result}, got {res}'


test_precisionFmt2()


class UnitValue:
    def __init__(self, line, precision=None, viewPrecision=None):
        self.__raw_line = line
        self._is_zero = None
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
            assert value_part in ['0', '0.0', '0.00'], f'Could not get precision from {value_part!r}'
            self._is_zero = True
            precisionStr = '0'
        else:
            self._is_zero = False
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
            's': '{{{}}}',
            'b': '\\left({}\\right)',
            'e': '${}$',
            'sqr': '\\sqr{{{}}}',
            'sqrt': '\\sqrt{{{}}}',
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
            if self._is_zero:
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
assert '{:Value}'.format(UnitValue('0 см')) == '0\\,\\text{см}'
assert '{:Value}'.format(UnitValue('0.0 см')) == '0\\,\\text{см}'
assert '{:TestAnswer}'.format(UnitValue('2.5 м')) == r'2.5', '{:TestAnswer}'.format(UnitValue('2.5 м'))
