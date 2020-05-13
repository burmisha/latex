# -*- coding: utf-8 -*-

import logging

log = logging.getLogger(__name__)


def precisionFmt2(value, precision):
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
    if rawDigits[-1] >= 5:
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
assert precisionFmt2(20, 2) == '20'
assert precisionFmt2(2.99, 2) == '3.0'
assert precisionFmt2(29.9, 2) == '30'
assert precisionFmt2(299, 2) == '300'
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


class UnitValue(object):
    def __init__(self, line, precision=None, viewPrecision=None):
        self.Line = line.strip()
        self.__RawLine = line
        self.Precision = precision
        self.ViewPrecision = viewPrecision
        self.Load()

    def Load(self):
        try:
            if '=' in self.Line:
                self.Letter, self.Line = self.Line.split('=', 1)
                self.Letter = self.Letter.strip()
                self.Line = self.Line.strip()
            else:
                self.Letter = None

            assert self.Line.count('/') <= 1
            self.Line = self.Line.replace('/', ' / ')
            self.Line = self.Line.replace('**', '^')
            self.Line = self.Line.replace(' ^', '^')

            self.BasePower = 0

            self.HumanUnits = [[], []]
            self.ReadyUnits = [[], []]
            isNumerator = True
            for index, part in enumerate(self.Line.split()):
                if index == 0:
                    try:
                        self.RawValue = int(part)
                        if self.Precision is None:
                            self.Precision = len(part)
                    except ValueError:
                        try:
                            self.RawValue = float(part)
                            if self.Precision is None:

                                precisionStr = part.lstrip('0').lstrip('.').lstrip('0').replace('.', '')
                                if self.Precision is None:
                                    self.Precision = len(precisionStr)
                                    try:
                                        if precisionStr[0] == '1' and self.Precision >= 2:
                                            self.Precision -= 1
                                    except:
                                        print part, precisionStr, self.__RawLine
                                        raise
                        except:
                            log.error('Could not get value from %r', part)
                            raise
                elif part.startswith('10^'):
                    self.BasePower = int(part[3:].strip('{').strip('}'))
                else:
                    if part == '/':
                        isNumerator = False
                    else:
                        mainUnit, mainPower, humanUnit, power = self.__ParseItem(part)
                        index = 0 if isNumerator else 1
                        self.HumanUnits[index].append((humanUnit, power))
                        self.ReadyUnits[index].append((mainUnit, mainPower))

            self.Value = self.RawValue  # TODO: use power
            self.Power = sum(power for _, power in self.ReadyUnits[0]) - sum(power for _, power in self.ReadyUnits[1]) + self.BasePower
        except Exception:
            log.error('Could not load unit %s (from %r)', self.Line, self.__RawLine)
            raise

    def __str__(self):
        return 'UV ' + '%s' % self.__RawLine

    def __repr__(self):
        return 'UVR ' + '%r' % self.__RawLine

    def __ParseItem(self, item):
        try:
            item = item.replace('**', '^')
            if '^' in item:
                item, power = item.split('^')
                power = int(power)
            else:
                power = 1

            prefix = ''
            main = item
            for suffix in [
                u'эВ',  # электрон-вольт
                u'В',   # вольт
                u'Дж',  # джоуль
                u'Н',   # ньютон
                u'Вт',  # ватт
                u'Ом',  # ом
                u'Ф',   # фарад
                u'А',   # ампер
                u'Кл',  # кулон
                u'кг',  # килограм
                u'г',   # грам
                u'с',   # секунда
                u'м',   # метр
                u'Тл',  # тесла
                u'т',   # тонна
                u'С',   # цельсий
                u'C',   # celsium
                u'К',   # кельвин
                u'K',   # kelvin
            ]:
                if item.endswith(suffix):
                    main = suffix
                    prefix = item[:-len(suffix)]
                    break

            exponent = {
                '': 0,
                u'к': 3,
                u'М': 6,
                u'Г': 9,
                u'м': -3,
                u'мк': -6,
                u'н': -9,
                u'п': -12,
                u'с': -2,
                u'д': -1,
            }[prefix]

            if main == u'г':
                main = u'кг'
                exponent -= 3

            return main, exponent * power, item, power
        except:
            log.error(u'Error in ParseItem on %r', item)
            raise

    def __GetUnits(self, items):
        parts = []
        for unit, power in items:
            if power == 1:
                part = '\\text{%s}' % unit
            else:
                part = '\\text{%s}^{%d}' % (unit, power)
            parts.append(part)
        return '\\cdot'.join(parts)

    def __format__(self, format):
        mainFormat = format.replace(':', '|')
        mainFormat, pipes = mainFormat.split('|')[0], mainFormat.split('|')[1:]

        needLetter = False
        humanNom = self.__GetUnits(self.HumanUnits[0])
        humanDen = self.__GetUnits(self.HumanUnits[1])
        if humanDen:
            units = u'\,\\frac{{{}}}{{{}}}'.format(humanNom, humanDen)
        else:
            units = '\,' + humanNom

        valueStr = precisionFmt2(self.Value, self.ViewPrecision or self.Precision)
        valueStr = valueStr.replace('.', '{,}')
        if self.BasePower:
            valueStr += ' \\cdot 10^{{{}}}'.format(self.BasePower)
        valueStr += u'{}'.format(units)

        if mainFormat == 'Task':
            result = valueStr
            needLetter = True
        elif mainFormat == 'Value':
            result = valueStr
            needLetter = False
        elif mainFormat == 'Letter':
            result = self.Letter
            needLetter = False
        else:
            print self.__RawLine
            raise RuntimeError('Error in __format__ for %r' % format)

        if needLetter and self.Letter:
            result = '%s = %s' % (self.Letter, result)

        for pipe in pipes:
            fmt = {
                's': u'{{ {} }}',
                'b': u'\\left({}\\right)',
                'e': u'${}$',
                'sqr': u'\\sqr{{ {} }}',
                'sqrt': u'\\sqrt{{ {} }}',
                'cdot': u'{} \\cdot'
            }.get(pipe)
            if fmt is None:
                raise RuntimeError('Unknown pipe in %s for %s' % (format, self))
            result = fmt.format(result)
        return result

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

        r = UnitValue(u'%.20f 10^%d %s' % (value, power, units), precision=precision)
        return r


assert UnitValue(u'50 мТл').Value * (10 ** UnitValue(u'50 мТл').Power) == 0.05, 'Got %r' % UnitValue(u'50 мТл').Value
assert u'{v:Task}'.format(v=UnitValue(u'c = 3 10^{8} м / с')) == u'c = 3 \\cdot 10^{8}\\,\\frac{\\text{м}}{\\text{с}}', 'Got %r' %  u'{v:Task}'.format(v=UnitValue(u'c = 3 10^{8} м / с'))
assert u'{t:Task}'.format(t=UnitValue(u't = 8 суток')) == u't = 8\\,\\text{суток}', 'Got %r' %  u'{t:Task}'.format(t=UnitValue(u't = 8 суток'))
assert u'{:Value}'.format(UnitValue(u'm = 1.67 10^-27 кг')) == u'1{,}67 \\cdot 10^{-27}\\,\\text{кг}'
assert u'{:Value}'.format(UnitValue(u'T = 1.7 суток')) == u'1{,}7\\,\\text{суток}'


class Consts(object):
    m_e = UnitValue(u'm_{e} = 9.1 10^{-31} кг')
    m_p = UnitValue(u'm_{p} = 1.672 10^{-27} кг')
    m_n = UnitValue(u'm_{n} = 1.675 10^{-27} кг')
    e = UnitValue(u'e = 1.60 10^{-19} Кл', viewPrecision=1)
    eV = UnitValue(u'1.60 10^{-19} Дж', viewPrecision=1)
    h = UnitValue(u'h = 6.626 10^{-34} Дж с')
    c = UnitValue(u'c = 3 10^{8} м / с', precision=3, viewPrecision=1)
    g_ten = UnitValue(u'g = 10 м / с^2', precision=2)
    aem = UnitValue(u'1.66054 10^-27 кг')


assert u'{:Value}'.format(Consts.c.Other(UnitValue(u'l = 500 нм'), action='div', units=u'Гц', powerShift=3)) == u'6{,}00 \\cdot 10^{14}\\,\\text{Гц}'
