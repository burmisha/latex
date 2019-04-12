# -*- coding: utf-8 -*-

import library
import logging

log = logging.getLogger(__name__)

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
    def __init__(self, date, tasks, name=None, classLetter=None, style=r'\variant'):
        self.Date = library.formatter.Date(date)

        assert isinstance(tasks, list)
        self.Tasks = tasks
        self.Name = name
        self.ClassLetter = classLetter
        self.Style = style

        filename = '%s-%s' % (self.Date.GetFilenameText(), self.ClassLetter)
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
            date=self.Date.GetHumanText(),
            classLetter=self.ClassLetter,
            tasks='\n\n'.join('    ' + task for task in tasks),
            style=self.Style,
        )
        return result        

    def GetFilename(self):
        return self._Filename


class PaperGenerator(object):
    def __call__(self):
        raise NotImplementedError()
