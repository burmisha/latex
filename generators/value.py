# -*- coding: utf-8 -*-

import logging

log = logging.getLogger(__name__)


class UnitValue(object):
    def __init__(self, line, letter=None):
        self.Line = line
        self.Letter = letter
        self.Load()

    def Load(self):
        try:
            if self.Letter is None:
                if '=' in self.Line:
                    self.Letter, self.Line = self.Line.split('=', 1)
                    self.Letter = self.Letter.strip()
                    self.Line = self.Line.strip()
                else:
                    self.Letter = None
            else:
                self.Letter = self.Letter
            self.HumanUnits = [[], []]
            self.ReadyUnits = [[], []]
            isUp = True
            assert self.Line.count('/') <= 1
            self.Parts = []
            if ' ' in self.Line:
                value, unitsSuffix = self.Line.split(' ', 1)
            else:
                value = self.Line.strip()
                unitsSuffix = ''
            try:
                value = int(value)
            except ValueError:
                try:
                    signsCount = len([l for l in value if l != '.'])
                    value = float(value)
                except:
                    log.error('Could not get value from %r', value)
                    raise

            self.Value = value
            for part in unitsSuffix.split():
                log.debug('Part: %r', part)
                if part == '/':
                    isUp = False
                    continue
                mainUnit, mainPower, humanUnit, power = self.ParseItem(part)
                index = 0 if isUp else 1
                self.HumanUnits[index].append((humanUnit, power))
                self.ReadyUnits[index].append((mainUnit, mainPower))

            self.Power = sum(power for _, power in self.ReadyUnits[0]) - sum(power for _, power in self.ReadyUnits[1])
            log.debug('Letter: %r, Total power: %r', self.Letter, self.Power)
        except Exception:
            log.exception('Could not load |%s|', self.Line)

    def ParseItem(self, item):
        try:
            if '^' in item:
                item, power = item.split('^')
                power = int(power)
            else:
                power = 1

            prefix = ''
            main = item
            for suffix in [u'В', u'Дж', u'Н', u'Вт', u'Ом', u'Ф', u'А', u'Кл', u'г', u'с', u'м', u'Тл', u'т']:
                if item.endswith(suffix):
                    main = suffix
                    prefix = item[:-len(suffix)]
                    break
            exponent = {
                '': 0,
                u'к': 3,
                u'м': -3,
                u'с': -2,
                u'д': -1,
                u'М': 6,
                u'Г': 9,
                u'мк': -6,
                u'н': -9,
                u'п': -12,
            }[prefix]
            return main, exponent * power, item, power
        except:
            log.exception(u'Error in ParseItem on %r', item)
            raise

    def GetUnits(self, items):
        parts = []
        for unit, power in items:
            if power == 1:
                part = '\\text{%s}' % unit
            else:
                part = '\\text{%s}^{%d}' % (unit, power)
            parts.append(part)
        return '\\cdot'.join(parts)

    def __format__(self, format):
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
        humanNom = self.GetUnits(self.HumanUnits[0])
        humanDen = self.GetUnits(self.HumanUnits[1])
        if humanDen:
            units = '\\frac{%s}{%s}' % (humanNom, humanDen)
        else:
            units = humanNom
        valueStr = u'{self.Value}\\,{units}'.format(self=self, units=units).replace('.', '{,}')
        if format == 'Task':
            result = valueStr
            needLetter = True
        elif format == 'ShortTask' or format == 'Value':
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


class Units(object):
    def __init__(self, basic=None, standard=None, power=0):
        self.Basic = basic
        self.Standard = standard
        self.Power = power
        if self.Power == 0:
            assert self.Standard is not None
            if not self.Basic:
                self.Basic = self.Standard
            assert self.Basic == self.Standard
        else:
            assert self.Basic != self.Standard


class LetterValue(object):
    def __init__(self, Letter=None, Value=None, units=None):
        self.Letter = Letter
        self.Value = Value
        self.Units = units

    def __repr__(self):
        return ' '.join([
            'Letter: %r' % [self.Letter, type(self.Letter)],
            'Value: %r' % [self.Value, type(self.Value)],
            'Units: %r' % [self.Units, type(self.Units)],
        ])

    def __format__(self, format):
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
        if format == 'Task':
            result = u'{self.Letter}={self.Value}{self.Units.Basic}'.format(self=self)
        elif format == 'Letter':
            result = u'{self.Letter}'.format(self=self)
        elif format == 'Value':
            result = u'{self.Value}'.format(self=self).replace('.', '{,}')
        elif format == 'ShortAnswer':
            result = u'{value}{self.Units.Basic}'.format(self=self, value=value)
        elif format == 'Answer':
            if self.Units.Power != 0:
                result = u'{value} \\cdot 10^{{{self.Units.Power}}} {self.Units.Standard}'.format(self=self, value=value)
            else:
                result = u'{value} {self.Units.Standard}'.format(self=self, value=value)
        else:
            raise RuntimeError('Error on format %r' % format)

        if suffix == 's':
            result = u'{ ' + result + ' }'

        return result


assert UnitValue(u'50 мТл').Value * (10 ** UnitValue(u'50 мТл').Power) == 0.05, 'Got %r' % UnitValue(u'50 мТл').Value
