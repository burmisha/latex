# -*- coding: utf-8 -*-

import task


class Savchenko(task.TasksGenerator):
    def GetBookName(self):
        return 'savchenko'

    def __call__(self):
        tasks = {
            '6-4-4': ur'''
                Площадь обкладок плоского конденсатора $S$, расстояние между пластинами $d$.
                \begin{itemize}
                    \item Определите его ёмкость.
                    \item Как изменится ёмкость конденсатора, если между его обкладками поместить металлическую пластину толщины $\tfrac d3$ и площади $S$?
                    \item Как изменится ёмкость конденсатора, если между его обкладками поместить металлическую пластину той же толщины $\tfrac d3$, но площади $S' < S$?
                    \item Изменится ли ёмкость конденсатора, если эта пластина коснётся одной из обкладок?
                \end{itemize}
            ''',
        }
        for number, text in tasks.iteritems():
            yield task.Task(text, number=number)
