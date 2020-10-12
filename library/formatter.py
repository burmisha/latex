import logging
import re

log = logging.getLogger(__name__)


class Date(object):
    def __init__(self, date):
        assert isinstance(date, str), 'Invalid date type: %r' % date
        assert re.match(r'20\d\d-\d{2}-\d{2}', date), 'Invalid date format: %r' % date
        self.__DateStr = date
        log.debug('Date: %r -> %r', self.__DateStr, self.GetHumanText())

    def GetFilenameText(self):
        return str(self.__DateStr)

    def GetHumanText(self):
        year, month, day = self.__DateStr.split('-')
        textMonth = {
            '01': 'января',
            '02': 'февраля',
            '03': 'марта',
            '04': 'апреля',
            '05': 'мая',
            '06': 'июня',
            '07': 'июля',
            '08': 'августа',
            '09': 'сентября',
            '10': 'октября',
            '11': 'ноября',
            '12': 'декабря',
        }[month]
        day = int(day)
        assert 1 <= day <= 31, 'Error on day in %r' % self.__DateStr
        assert 2018 <= int(year) <= 2025, 'Error on year in %r' % self.__DateStr
        return '{}~{}~{}'.format(int(day), textMonth, year)


class TextFormatter(object):
    def __init__(self, text):
        assert text.strip()
        self.Text = text.strip('\n')

    def __FirstSpacesCount(self, line):
        return len(line) - len(line.lstrip(' '))

    def Format(self, addIndent=0):
        lines = self.Text.split('\n')
        minSpaces = min(self.__FirstSpacesCount(line) for line in lines if line.strip())
        lastSpaces = None
        for line in lines:
            line = line[minSpaces:].rstrip(' ')
            if line.strip():
                log.debug('Line: %r', line)
                line = line.replace('. ', '.\n')
                spaces = self.__FirstSpacesCount(line)
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
