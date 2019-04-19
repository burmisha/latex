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
        log.info('Got %d tasks for %r', len(tasks), self)
        return tasks


class ForceTask(VariantTask):
    def __call__(self, charges=['2', '4'], letter='l', distance='3'):
        return problems.task.Task(u'''
            С какой силой взаимодействуют 2 точечных заряда $q_1={charges[0]}\\units{{нКл}}$ и $q_2={charges[1]}\\units{{нКл}}$,
            находящиеся на расстоянии ${letter}={distance}\\units{{см}}$?
        '''.format(
            charges=charges,
            letter=letter,
            distance=distance,
        ))

    def All(self):
        for first, second, letter, distance in itertools.product(range(2, 5), range(2, 5), ['r', 'l', 'd'], [2, 3, 5, 6]):
            if first != second:
                yield self.__call__(charges=[first, second], letter=letter, distance=distance)




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


class Fotons(VariantTask):
    def __call__(self, time=30, power=2, length=750):
        return problems.task.Task(u'''
            Сколько фотонов испускает за {time} минут лазер,
            если мощность его излучения {power} мВт.
            Длина волны излучения {length} нм.
        '''.format(
            time=time,
            power=power,
            length=length,
        ))

    def All(self):
        for time, power, length in itertools.product(
            [5, 10, 20, 30, 40, 60, 120],
            [15, 40, 75, 200],
            [500, 600, 750],
        ):
            yield self.__call__(
                time=time,
                power=power,
                length=length,
            )

class KernelCount(VariantTask):
    def __call__(self, nuclons=108, electrons=47):
        return problems.task.Task(u'''
            В ядре электрически нейтрального атома {nuclons} частиц.
            Вокруг ядра обращается {electrons} электронов.
            Сколько в ядре этого атома протонов и нейтронов?
        '''.format(
            nuclons=nuclons,
            electrons=electrons,
        ))

    def All(self):
        for nuclons, electrons in [
            (108, 47),  # Al
            (65, 29),  # Cu
            (63, 29),  # Cu
            (121, 51),  # Sb
            (123, 51),  # Cu
            (190, 78),  # Pt
        ]:
            yield self.__call__(
                nuclons=nuclons,
                electrons=electrons,
            )


class RadioFall(VariantTask):
    def __call__(self, fallType='alpha', element='^{238}_{92}U'):
        typeFmt = {
            'alpha': '\\alpha',
            'beta': '\\beta',
        }[fallType]
        return problems.task.Task(u'''
            Запишите реакцию ${typeFmt}$-распада \ce{{{element}}}.
        '''.format(
            typeFmt=typeFmt,
            element=element,
        ))

    def All(self):
        for fallType, element in [
            ('alpha', '^{238}_{92}U'),
            ('alpha', '^{144}_{60}Nd'),
            ('alpha', '^{147}_{62}Sm'),
            ('alpha', '^{148}_{62}Sm'),
            ('alpha', '^{180}_{74}W'),
            ('alpha', '^{153}_{61}Eu'),
            ('beta', '^{137}_{55}Cs'),
            ('beta', '^{22}_{11}Na'),
        ]:
            yield self.__call__(
                fallType=fallType,
                element=element,
            )


class RadioFall2(VariantTask):
    def __call__(self, time=12, delta=7500, total=8000):
        return problems.task.Task(u'''
            Какой период полураспада радиоактивного изотопа,
            если за {time} ч в среднем распадается {delta} атомов из {total}?
        '''.format(
            time=time,
            delta=delta,
            total=total,
        ))

    def All(self):
        for time, delta, total in [
            (12, 7500, 8000),
            (24, 75000, 80000),
            (6, 3500, 4000),
            (8, 37500, 40000),
            (8, 300, 400),
        ]:
            yield self.__call__(
                time=time,
                delta=delta,
                total=total,
            )



class Variants(object):
    def __init__(self, names, items):
        self.Names = names
        self.Items = list(items)
        log.info('Got %d students, %d items', len(self.Names), len(self.Items))

    def Iterate(self):
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
                text += '\n\\vspace{120pt}\n\n'
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
