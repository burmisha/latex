import logging
import re

log = logging.getLogger(__name__)


class Date:
    def __init__(self, date):
        assert isinstance(date, str), f'Invalid date type: {date!r}'
        assert re.match(r'20\d\d-\d{2}-\d{2}', date), f'Invalid date format: {date!r}'
        self.__DateStr = date
        log.debug('Date: %r', self.__DateStr)
        parts = self.__DateStr.split('-')
        self._year = int(parts[0])
        self._month = int(parts[1])
        self._day = int(parts[2])
        assert 2018 <= self._year <= 2025, 'Error on year in %r' % self.__DateStr
        assert 1 <= self._month <= 12, 'Error on month in %r' % self.__DateStr
        assert 1 <= self._day <= 31, 'Error on day in %r' % self.__DateStr

    def GetFilenameText(self):
        return str(self.__DateStr)

    def __format__(self, fmt):
        try:
            if fmt == 'LaTeX':
                return self.GetHumanText()
            elif fmt == 'filename':
                return self.GetFilenameText()
            elif fmt == 'dots':
                return f'{self._year}.{self._month:02d}.{self._day:02d}'
            else:
                raise RuntimeError(f'Unknown format: {fmt!r}')
        except RuntimeError:
            raise
        except Exception:
            log.error(f'Error in __format__ for {fmt} and {self.__DateStr}')
            raise

    def GetHumanText(self):
        textMonth = {
            1: 'января',
            2: 'февраля',
            3: 'марта',
            4: 'апреля',
            5: 'мая',
            6: 'июня',
            7: 'июля',
            8: 'августа',
            9: 'сентября',
            10: 'октября',
            11: 'ноября',
            12: 'декабря',
        }[self._month]
        return '{}~{}~{}'.format(self._day, textMonth, self._year)

    def GetStudyYearPair(self):
        if self._month <= 7:
            return self._year - 1, self._year
        else:
            return self._year, self._year + 1


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
