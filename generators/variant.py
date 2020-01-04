# -*- coding: utf-8 -*-

import random
import logging

import library

log = logging.getLogger(__name__)


PAPER_TEMPLATE = ur'''
\input{{main}}
\begin{{document}}
{noanswers}

\setdate{{{date}}}
\setclass{{{classLetter}}}

{text}

\end{{document}}
'''.strip()


class VariantTask(object):
    pass

    def Shuffle(self, seed, minCount=None):
        tasks = list(self.All())
        log.info('Got %d tasks for %r', len(tasks), self)

        if minCount:
            periods = int((minCount - 1) / len(tasks)) + 1
            if periods > 1:
                log.info('  Expanding task %s to %d periods', self, periods)
            tasks *= periods

        random.seed(seed)
        random.shuffle(tasks)
        return tasks



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
        self.Vspace = 120

    def GetTex(self, nameTasksIterator, withAnswers=False):
        if withAnswers:
            variantsJoiner = u''
        else:
            variantsJoiner = u'\n\\newpage'
        variantsJoiner += '\n\n'
        variants = []
        for name, tasks in nameTasksIterator:
            variantText = u'\\addpersonalvariant{{{name}}}\n'.format(name=name)
            tasksTexts = u''
            previousTask = None
            for index, task in enumerate(tasks):
                if previousTask:
                    if not withAnswers:
                        tasksTexts += u'\n\\vspace{%dpt}' % task.GetSolutionSpace()
                    tasksTexts += '\n\n'
                tasksTexts += u'\\tasknumber{{{index}}}{taskText}'.format(
                    index=index + 1,
                    taskText=task.GetTex().strip(),
                )
                previousTask = task
            variants.append(variantText + tasksTexts)
        text = variantsJoiner.join(variants)
        result = PAPER_TEMPLATE.format(
            date=self.Date.GetHumanText(),
            classLetter=self.ClassLetter,
            text=text,
            noanswers='' if withAnswers else u'\\noanswers',
        )
        return result

    def GetFilename(self):
        filename = '%s-%s' % (self.Date.GetFilenameText(), self.ClassLetter)
        if self.Name:
            filename += '-' + self.Name
        filename += '.tex'
        log.debug('Got filename %r', filename)
        return filename
