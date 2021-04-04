# -*- coding: utf-8 -*-

import library
import logging
import os

log = logging.getLogger(__name__)

PAPER_TEMPLATE = r'''
\newcommand\rootpath{{../..}}
\input{{\rootpath/school-554/main}}
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


class Paper:
    def __init__(self, date, tasks, name=None, classLetter=None, style=r'\variant'):
        self.Date = library.formatter.Date(date)

        assert isinstance(tasks, list)
        self.Tasks = tasks
        self.Name = name
        self.ClassLetter = classLetter
        self.Style = style

    def GetTex(self):
        tasks = []
        index = 0
        for book, problems in self.Tasks:
            for problem in problems:
                taskMarker = 'tasknumber'
                if problem.endswith('*'):
                    problem = problem.strip('*')
                    taskMarker = 'starnumber'
                index += 1
                tasks.append(r'\%s{%d}\libproblem{%s}{%s}' % (taskMarker, index, book, problem))
        result = PAPER_TEMPLATE.format(
            date=self.Date.GetHumanText(),
            classLetter=self.ClassLetter,
            tasks='\n\n'.join('    ' + task for task in tasks),
            style=self.Style,
        )
        return result

    def GetFilename(self):
        filename = '%s-%s' % (self.Date.GetFilenameText(), self.ClassLetter)
        if self.Name:
            filename += '-' + self.Name
        filename += '.tex'
        filename = os.path.join('%s-class' % self.ClassLetter, filename)
        log.debug('Got filename %r', filename)
        return filename


class PaperGenerator(object):
    def __call__(self):
        raise NotImplementedError()
