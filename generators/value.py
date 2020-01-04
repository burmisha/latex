# -*- coding: utf-8 -*-

import logging

log = logging.getLogger(__name__)


class UnitValue(object):
    def __init__(self, line):
        self.Line = line.strip()
        self.__RawLine = line
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

            self.HumanUnits = [[], []]
            self.ReadyUnits = [[], []]
            isNumerator = True
            for index, part in enumerate(self.Line.split()):
                if index == 0:
                    try:
                        self.RawValue = int(part)
                        self.Precision = len(part)
                    except ValueError:
                        try:
                            self.RawValue = float(part)
                            self.Precision = len(part.lstrip('0').lstrip('.').lstrip('0'))
                        except:
                            log.error('Could not get value from %r', part)
                            raise
                else:
                    if part == '/':
                        isNumerator = False
                    else:
                        mainUnit, mainPower, humanUnit, power = self.__ParseItem(part)
                        index = 0 if isNumerator else 1
                        self.HumanUnits[index].append((humanUnit, power))
                        self.ReadyUnits[index].append((mainUnit, mainPower))

            self.Value = self.RawValue  # TODO: use power
            self.Power = sum(power for _, power in self.ReadyUnits[0]) - sum(power for _, power in self.ReadyUnits[1])
        except Exception:
            log.error('Could not load unit %s (from %r)', self.Line, self.__RawLine)
            raise

    def __ParseItem(self, item):
        try:
            if '^' in item:
                item, power = item.split('^')
                power = int(power)
            else:
                power = 1

            prefix = ''
            main = item
            for suffix in [
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
        # TODO: use precision
        if isinstance(self.Value, int):
            fmt = '{:d}'
        else:
            fmt = '{:.2f}'
        if self.Value < 0:
            fmt = '(%s)' % fmt
        value = fmt.format(self.Value).replace('.', '{,}')

        if ':' in format:
            format, suffix = format.split(':')
        else:
            suffix = None

        needLetter = False
        humanNom = self.__GetUnits(self.HumanUnits[0])
        humanDen = self.__GetUnits(self.HumanUnits[1])
        if humanDen:
            units = u'\\frac{{{}}}{{{}}}'.format(humanNom, humanDen)
        else:
            units = humanNom
        valueStr = u'{self.Value}\\,{units}'.format(self=self, units=units).replace('.', '{,}')
        if format == 'Task':
            result = valueStr
            needLetter = True
        elif format == 'Value':
            result = valueStr
            needLetter = False
        elif format == 'Letter':
            result = self.Letter
            needLetter = False
        else:
            raise RuntimeError('Error in __format__ for %r' % format)

        if needLetter and self.Letter:
            result = '%s = %s' % (self.Letter, result)

        if suffix == 's':
            result = u'{ ' + result + ' }'
        elif suffix == 'b':
            result = u'\\left(' + result + '\\right)'
        elif suffix == 'e':
            result = u'$' + result + '$'

        return result


assert UnitValue(u'50 мТл').Value * (10 ** UnitValue(u'50 мТл').Power) == 0.05, 'Got %r' % UnitValue(u'50 мТл').Value
