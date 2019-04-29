import random
import logging

import library

log = logging.getLogger(__name__)


PAPER_TEMPLATE = ur'''
\input{{main}}
\begin{{document}}
% \noanswers

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
                # text += '\n\\vspace{120pt}\n\n'
                text += '\n\n'
            # text += u'\n\\newpage\n\n'
            text += u'\n\n'
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
