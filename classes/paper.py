# -*- coding: utf-8 -*-

import library
import logging
import os

log = logging.getLogger(__name__)

PAPER_TEMPLATE = r'''
\newcommand\rootpath{{../../..}}
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
    def __init__(self, date, tasks, classLetter=None, style=None):
        self.Date = library.formatter.Date(date)

        assert isinstance(tasks, list)
        assert isinstance(classLetter, str)
        assert isinstance(style, str)
        self.Tasks = tasks
        self.ClassLetter = classLetter
        self.Style = style

    def GetTex(self):
        tasks = []
        index = 0
        for book, problems in self.Tasks:
            for problem in problems:
                if problem.endswith('*'):
                    problem = problem.strip('*')
                    taskMarker = 'starnumber'
                else:
                    taskMarker = 'tasknumber'
                index += 1
                tasks.append('\\%s{%d}\\libproblem{%s}{%s}' % (taskMarker, index, book, problem))
        result = PAPER_TEMPLATE.format(
            date=self.Date.GetHumanText(),
            classLetter=self.ClassLetter,
            tasks='\n\n'.join('    ' + task for task in tasks),
            style=self.Style,
        )
        return result

    def GetFilename(self):
        pupils = library.pupils.get_class_from_string(f'{self.Date.GetFilenameText()} {self.ClassLetter}')
        filename = f'{self.Date.GetFilenameText()}-{pupils.Grade}.tex'

        # filename = f'{self.Date.GetFilenameText()}-{pupils.Grade}'
        # if self.Pupils.LatinLetter:
        #     filename += self.Pupils.LatinLetter

        return filename
