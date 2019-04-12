# -*- coding: utf-8 -*-

import re
import logging
import random

import problems
import library

log = logging.getLogger('electricity')

PAPER_TEMPLATE = ur'''
\input{{main}}
\begin{{document}}
\noanswers

\setdate{{{date}}}
\setclass{{{classLetter}}}

{text}

\end{{document}}
'''.strip()


class VariantTask(object):
    pass


class FieldTaskGenerator(VariantTask):
    def __call__(self, charges=['+q', '+q'], points=['up', 'left'], letter='l'):
        allPoints = {
            'up': '(0; {})'.format(letter),
            'down': '(0; -{})'.format(letter),
            'left': '(-2{}; 0)'.format(letter),
            'right': '(2{}; 0)'.format(letter),
        }
        return problems.task.Task(u'''
            На координатной плоскости в точках $(-{letter}; 0)$ и $({letter}; 0)$
            находятся заряды, соответственно, ${leftCharge}$ и ${rightCharge}$.
            Сделайте рисунок, определите величину напряжённости электрического поля
            в точках ${firstPoint}$ и ${secondPoint}$ и укажите её направление.
        '''.format(
            letter=letter,
            leftCharge=charges[0],
            rightCharge=charges[1],
            firstPoint=allPoints[points[0]],
            secondPoint=allPoints[points[1]],
        ))


class SumTask(VariantTask):
    def __call__(self, angleLetter='\\alpha', values=[12, 5], angles=[60, 90]):
        return problems.task.Task(u'''
            Заряд $q_1$ создает в точке $A$ электрическое поле 
            по величине равное~$E_1={firstValue}\\funits{{В}}{{м}}$,
            а $q_2$~---$E_2={secondValue}\\funits{{В}}{{м}}$.
            Угол между векторами $\\vect{{E_1}}$ и $\\vect{{E_2}}$ равен ${angleLetter}$.
            Определите величину суммарного электрического поля в точке $A$,
            создаваемого обоими зарядами $q_1$ и $q_2$.
            Сделайте рисунок и вычислите её значение для двух значений угла ${angleLetter}$: 
            ${angleLetter}_1={firstAngle}^\\circ$ и ${angleLetter}_2={secondAngle}^\\circ$.
        '''.format(
            angleLetter=angleLetter,
            firstValue=values[0],
            secondValue=values[1],
            firstAngle=angles[0],
            secondAngle=angles[1],
        ))


class Variants(object):
    def __init__(self, names, seed, items):
        self.Names = names
        self.Seed = seed
        self.Items = list(items)
        log.info('Got %d students, %d items, seed is %r', len(self.Names), len(self.Items), self.Seed)

    def Iterate(self):
        random.seed(self.Seed)
        random.shuffle(self.Items)
        for index, name in enumerate(self.Names):
            itemIndex = index % len(self.Items)
            yield name, self.Items[itemIndex]



class MultiplePaper(object):
    def __init__(self, date=None, classLetter=None):
        self.Date = library.formatter.Date(date)
        self.Name = 'task'
        self.ClassLetter = classLetter

        filename = '%s-%s' % (self.Date.GetFilenameText(), self.ClassLetter)
        if self.Name:
            filename += '-' + self.Name
        filename += '.tex'
        log.debug('Got filename %r', filename)
        self._Filename = filename

    def GetTex(self, nameTasksIterator):
        text = ''
        for name, tasks in nameTasksIterator:
            text += u'\\addpersonalvariant{{{name}}}'.format(name=name)
            for index, task in enumerate(tasks):
                text += (u'\\tasknumber{{{index}}}{taskText}'.format(
                    index=index + 1, 
                    taskText=task.GetTex(),
                ))
        result = PAPER_TEMPLATE.format(
            date=self.Date.GetHumanText(),
            classLetter=self.ClassLetter,
            text=text,
        )
        return result        

    def GetFilename(self):
        return self._Filename

