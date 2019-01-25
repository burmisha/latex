# -*- coding: utf-8 -*-

import re
import logging

log = logging.getLogger('task')

PAPER_TEMPLATE = ur'''
\input{{main}}
\begin{{document}}
\noanswers

\setdate{{{date}}}
\setclass{{{classLetter}}}

\def\variant{{
    \insertclassdate
{tasks}
}}

{style}
\end{{document}}
'''.strip()

class Paper(object):
    def __init__(self, date, tasks, name=None, classLetter=None):
        assert isinstance(date, str)
        assert isinstance(tasks, list)
        assert re.match(r'201\d-\d{2}-\d{2}', date)
        assert name in [None, 'hometask', 'task'], 'Invalid name: %r' % name

        self.Date = date
        self.Tasks = tasks
        self.Name = name
        self.ClassLetter = classLetter

        filename = '%s-%s' % (self.Date, self.ClassLetter)
        if self.Name:
            filename += '-' + self.Name
        filename += '.tex'
        log.debug('Got filename %r', filename)
        self._Filename = filename

    def GetTex(self):
        tasks = []
        index = 0
        for book, problems in self.Tasks:
            for problem in problems:
                index += 1
                tasks.append('\\tasknumber{%d}\\libproblem{%s}{%s}' % (index, book, problem))
        result = PAPER_TEMPLATE.format(
            date=self.GetTextDate(),
            classLetter=self.ClassLetter,
            tasks='\n\n'.join('    ' + task for task in tasks),
            style=ur'\twocolumns{30pt}{\variant}{\variant}',
        )
        return result        

    def GetTextDate(self):
        year, month, day = self.Date.split('-')
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
        return u'%d %s %s' % (int(day), textMonth[month], year)

    def GetFilename(self):
        return self._Filename


class PaperGenerator(object):
    def __call__(self):
        raise NotImplementedError()
