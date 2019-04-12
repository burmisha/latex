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
