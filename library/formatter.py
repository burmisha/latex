# -*- coding: utf-8 -*-

import logging
import re

log = logging.getLogger(__name__)


class Date(object):
    def __init__(self, date):
        assert isinstance(date, str), 'Invalid date type: %r' % date
        assert re.match(r'201\d-\d{2}-\d{2}', date), 'Invalid date format: %r' % date
        self.__DateStr = date
        log.debug('Date: %r -> %r', self.__DateStr, self.GetHumanText())

    def GetFilenameText(self):
        return str(self.__DateStr)

    def GetHumanText(self):
        year, month, day = self.__DateStr.split('-')
        textMonth = {
            '01': u'января',
            '02': u'февраля',
            '03': u'марта',
            '04': u'апреля',
            '05': u'мая',
            '06': u'июня',
            '07': u'июля',
            '08': u'августа',
            '09': u'сентября',
            '10': u'октября',
            '11': u'ноября',
            '12': u'декабря',
        }
        day = int(day)
        return u'{} {} {}'.format(int(day), textMonth[month], year)


class TextFormatter(object):
    def __init__(self, text):
        assert text.strip()
        self.Text = text.strip('\n')

    def FirstSpacesCount(self, line):
        return len(line) - len(line.lstrip(' '))

    def Format(self, addIndent=0):
        lines = self.Text.split('\n')
        minSpaces = min(self.FirstSpacesCount(line) for line in lines if line.strip())
        lastSpaces = None
        for line in lines:
            line = line[minSpaces:].rstrip(' ')
            if line.strip():
                log.debug('Line: %r', line)
                line = line.replace('. ', '.\n')
                spaces = self.FirstSpacesCount(line)
                log.debug('Line: |%s|, spaces: %d', line, spaces)
                for newLine in line.split('\n'):
                    yield ' ' * (addIndent + spaces) + newLine.strip(' ')
            else:
                yield ''


def formatText(text, addIndent=0):
    textFormatter = TextFormatter(text)
    formatted = '\n'.join(textFormatter.Format(addIndent=addIndent))
    formatted.replace('\n\n\n', '\n\n')
    formatted = formatted.strip('\n')
    return formatted
