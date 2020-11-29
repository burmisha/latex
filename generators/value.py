# -*- coding: utf-8 -*-

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
        part = f'\\text{{{self.HumanUnit}}}'
        if self.HumanPower != 1:
            part += f'^{{{self.HumanPower}}}'
        return part

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

            return main, exponent * power, line, power
        except:
            log.error('Error in ParseItem on %r', line)
            raise

class UnitValue(object):
    def __init__(self, line, precision=None, viewPrecision=None):
        self.__raw_line = line
        self._load(line, precision=precision)
        self.ViewPrecision = viewPrecision
        self._value_str = None

    def _parse_precision(self, value_part):
        precisionStr = value_part.replace('.', '').lstrip('0')
        if not precisionStr:
            assert value_part == '0'
            precisionStr = '0'
        precision = len(precisionStr)
        if precisionStr[0] == '1' and precision >= 2:
            precision -= 1
        return precision

    def _load(self, line, precision=None):
        try:
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
        except Exception:
            log.error(f'Could not load unit from {self.__raw_line}')
            raise

    def __str__(self):
        return f'UVS {self.__raw_line}'

    def __repr__(self):
        return f'UVR {self.__raw_line!r}'

    def _get_units_tex(self):
        humanNom = '\\cdot'.join(unit.get_tex() for unit in self._units if unit.IsNumerator)
        humanDen = '\\cdot'.join(unit.get_tex() for unit in self._units if not unit.IsNumerator)
        if humanDen:
            units = '\,\\frac{%s}{%s}' % (humanNom, humanDen)
        elif humanNom:
            units = '\,' + humanNom
        else:
            units = ''
        return units

    def apply_pipes(self, line, pipes):
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
                raise RuntimeError(f'Unknown pipe {pipe} for {self}')
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
                assert all(i.isdigit() or i == '-' for i in self._precisionFmt2)
                return self._precisionFmt2
            elif main_format == 'Task':
                with_letter = True
                with_value = True
            elif main_format == 'Value':
                with_letter = False
                with_value = True
            elif main_format == 'Letter' or main_format == 'L':
                with_letter = True
                with_value = False
            else:
                raise RuntimeError(f'Error in __format__ for {fmt} and {self.__raw_line}')

            result = ' = '.join(i for i, j in [[self.Letter, with_letter], [value_str, with_value]] if j and i)
            result = self.apply_pipes(result, pipes)
            return result
        except Exception:
            log.error(f'Error in __format__ for {fmt} and {self.__raw_line}')
            raise

    def Other(self, other, action=None, precisionInc=0, units='', powerShift=0):
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

        power -= powerShift
        value *= 10 ** powerShift

        r = UnitValue('%.20f 10^%d %s' % (value, power, units), precision=precision)
        return r


assert UnitValue('50 мТл').Value * (10 ** UnitValue('50 мТл').Power) == 0.05, 'Got %r' % UnitValue('50 мТл').Value
assert '{v:Task}'.format(v=UnitValue('c = 3 10^{8} м / с')) == 'c = 3 \\cdot 10^{8}\\,\\frac{\\text{м}}{\\text{с}}', 'Got %r' %  '{v:Task}'.format(v=UnitValue('c = 3 10^{8} м / с'))
assert '{t:Task}'.format(t=UnitValue('t = 8 суток')) == 't = 8\\,\\text{суток}', 'Got %r' %  '{t:Task}'.format(t=UnitValue('t = 8 суток'))
assert '{:Value}'.format(UnitValue('m = 1.67 10^-27 кг')) == '1{,}67 \\cdot 10^{-27}\\,\\text{кг}'
assert '{:Value}'.format(UnitValue('T = 1.7 суток')) == '1{,}7\\,\\text{суток}'
assert '{:Value}'.format(UnitValue('12 км / ч')) == '12\\,\\frac{\\text{км}}{\\text{ч}}'
assert '{:Value}'.format(UnitValue('50 км / ч')) == '50\\,\\frac{\\text{км}}{\\text{ч}}'


class Matter(object):
    def __init__(self, name=None, **kws):
        self.Name = name
        for key, value in kws.items():
            assert key in ['c', 'lmbd', 'L']
            setattr(self, key, UnitValue(value))


class Consts(object):
    m_e = UnitValue('m_{e} = 9.1 10^{-31} кг')
    m_p = UnitValue('m_{p} = 1.672 10^{-27} кг')
    m_n = UnitValue('m_{n} = 1.675 10^{-27} кг')
    e = UnitValue('e = 1.60 10^{-19} Кл', viewPrecision=1)
    eV = UnitValue('1.60 10^{-19} Дж', viewPrecision=1)
    h = UnitValue('h = 6.626 10^{-34} Дж с')
    c = UnitValue('c = 3 10^{8} м / с', precision=3, viewPrecision=1)
    g_ten = UnitValue('g = 10 м / с^2', precision=2)
    aem = UnitValue('\\text{а.е.м.} = 1.66054 10^-27 кг')
    k = UnitValue('k = 9 10^9 Н м^2 / Кл^2')

    water = Matter(
        name='вода',
        c='4200 Дж / кг К',
        lmbd='340 кДж / кг',
        L='2.3 МДж / кг',
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


assert '{:Value}'.format(Consts.c.Other(UnitValue('l = 500 нм'), action='div', units='Гц', powerShift=3)) == '6{,}00 \\cdot 10^{14}\\,\\text{Гц}'
