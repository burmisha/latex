# -*- coding: utf-8 -*-

import itertools
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

    def Shuffle(self, seed):
        tasks = list(self.All())
        random.seed(seed)
        random.shuffle(tasks)
        return tasks


class ExchangeTask(VariantTask):
    def __call__(self, charges=['+q', '+q'], letter='l'):
        return problems.task.Task(u'''
            Два одинаковых маленьких проводящих заряженных шарика находятся
            на расстоянии~${letter}$ друг от друга.
            Заряд первого равен~${charges[0]}$, второго~---${charges[1]}$.
            Шарики приводят в соприкосновение, а после опять разводят на то же самое расстояние~${letter}$.
            Каким стал заряд каждого из шариков?
            Определите характер (притяжение или отталкивание)
            и силу взаимодействия шариков до и после соприкосновения.
        '''.format(
            letter=letter,
            charges=charges,
        ))

    def All(self):
        signs = ['+', '-']
        chargeLetters = ['q', 'Q']
        chargeSizes = range(2, 6)
        for fs, ss, cl, fc, sc, l in itertools.product(signs, signs, chargeLetters, chargeSizes, chargeSizes, ['l', 'd', 'r']):
            if fc != sc:
                yield self.__call__(
                    letter=l,
                    charges=[
                        '{}{}{}'.format(fs, fc, cl),
                        '{}{}{}'.format(ss, sc, cl),
                    ],
                )


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
            находятся заряды, соответственно, ${charges[0]}$ и ${charges[1]}$.
            Сделайте рисунок, определите величину напряжённости электрического поля
            в точках ${firstPoint}$ и ${secondPoint}$ и укажите её направление.
        '''.format(
            letter=letter,
            charges=charges,
            firstPoint=allPoints[points[0]],
            secondPoint=allPoints[points[1]],
        ))

    def All(self):
        for charges in [['+q', '-q'], ['-q', '-q'], ['+Q', '+Q'], ['-Q', '+Q']]:
            for firstPoint in ['up', 'down']:
                for secondPoint in ['right', 'left']:
                    for letter in ['a', 'l', 'r', 'd']:
                        yield self.__call__(
                            charges=charges,
                            letter=letter,
                            points=[firstPoint, secondPoint],
                        )


class SumTask(VariantTask):
    def __call__(self, angleLetter='\\alpha', values=[12, 5], angles=[60, 90]):
        return problems.task.Task(u'''
            Заряд $q_1$ создает в точке $A$ электрическое поле
            по величине равное~$E_1={values[0]}\\funits{{В}}{{м}}$,
            а $q_2$~---$E_2={values[1]}\\funits{{В}}{{м}}$.
            Угол между векторами $\\vect{{E_1}}$ и $\\vect{{E_2}}$ равен ${angle}$.
            Определите величину суммарного электрического поля в точке $A$,
            создаваемого обоими зарядами $q_1$ и $q_2$.
            Сделайте рисунок и вычислите её значение для двух значений угла ${angle}$:
            ${angle}_1={angles[0]}^\\circ$ и ${angle}_2={angles[1]}^\\circ$.
        '''.format(
            angle=angleLetter,
            values=values,
            angles=angles,
        ))

    def All(self):
        for values, angles in [
            ((120, 50), (90, 180)),
            ((50, 120), (0, 90)),
            ((500, 500), (0, 120)),
            ((200, 200), (0, 60)),
            ((24, 7), (90, 180)),
            ((7, 24), (0, 90)),
            ((72, 72), (0, 120)),
            ((250, 250), (0, 60)),
            ((300, 400), (90, 180)),
            ((300, 400), (0, 90)),
        ]:
            for angleLetter in ['\\alpha', '\\varphi']:
                yield self.__call__(
                    angleLetter=angleLetter,
                    values=values,
                    angles=angles
                )


class Variants(object):
    def __init__(self, names, items):
        self.Names = names
        # self.Seed = seed
        self.Items = list(items)
        log.info('Got %d students, %d items', len(self.Names), len(self.Items))

    def Iterate(self):
        # random.seed(self.Seed)
        # random.shuffle(self.Items)
        for index, name in enumerate(self.Names):
            itemIndex = index % len(self.Items)
            yield name, self.Items[itemIndex]


class MultiplePaper(object):
    def __init__(self, date=None, classLetter=None):
        self.Date = library.formatter.Date(date)
        self.Name = 'task'
        self.ClassLetter = classLetter

    def GetTex(self, nameTasksIterator):
        text = ''
        for name, tasks in nameTasksIterator:
            text += u'\\addpersonalvariant{{{name}}}\n'.format(name=name)
            for index, task in enumerate(tasks):
                text += u'\\tasknumber{{{index}}}{taskText}'.format(
                    index=index + 1,
                    taskText=task.GetTex(),
                )
                text += '\n\\vspace{180pt}\n\n'
            text += u'\n\\newpage\n\n'
        result = PAPER_TEMPLATE.format(
            date=self.Date.GetHumanText(),
            classLetter=self.ClassLetter,
            text=text,
        )
        return result

    def GetFilename(self):
        filename = '%s-%s' % (self.Date.GetFilenameText(), self.ClassLetter)
        if self.Name:
            filename += '-' + self.Name
        filename += '.tex'
        log.debug('Got filename %r', filename)
        return filename
