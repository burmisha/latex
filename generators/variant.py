# -*- coding: utf-8 -*-

import collections
import hashlib
import itertools
import re

import value

import library
import problems

import logging
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

def check_unit_value(v):
    try:
        if isinstance(v, (str, unicode)) and ('=' in v or re.match(r'\d \w', v, re.UNICODE)):
            return value.UnitValue(v)
        else:
            return v
    except:
        print v
        raise


assert isinstance(check_unit_value(u'2 суток'), value.UnitValue)

def form_args(kwargs):
    keys = []
    values = []
    for k, v in kwargs.iteritems():
        keys.append(k)
        values.append(v)
    for row in itertools.product(*values):
        result = {}
        for k, v in zip(keys, row):
            if isinstance(k, tuple):
                for kk, vv in zip(k, v):
                    result[kk] = check_unit_value(vv)
            else:
                result[k] = check_unit_value(v)
        yield result


class VariantTask(object):
    def __init__(self):
        self.__TasksList = None
        self.__TaskCount = None
        self.__Stats = collections.defaultdict(int)
        # self.SolutionSpace = None

    def GetArgs(self):
        raise NotImplementedError

    def GetAnswer(self):
        return None

    def GetUpdate(self, **kws):
        return {}

    def GetSolutionSpace(self):
        if hasattr(self, 'SolutionSpace'):
            return self.SolutionSpace
        else:
            return 120

    def All(self):
        try:
            argsDict = self.GetArgs()
        except NotImplementedError:
            raise
        else:
            if argsDict is None:  # only one variant
                args = {'Consts': value.Consts}
                if hasattr(self, 'GetText'):
                    textTemplate = self.GetText()
                    answerTemplate = self.GetAnswer()
                    kwsUpdate = self.GetUpdate(**args)
                    args.update(kwsUpdate)
                    yield problems.task.Task(
                        textTemplate.format(**args),
                        answer=answerTemplate.format(**args) if answerTemplate else None,
                        solutionSpace=self.GetSolutionSpace(),
                    )
                else:
                    yield self.__call__(**args)
                return
            for args in form_args(argsDict):
                args['Consts'] = value.Consts
                if hasattr(self, 'GetText'):
                    textTemplate = self.GetText()
                    answerTemplate = self.GetAnswer()
                    kwsUpdate = self.GetUpdate(**args)
                    args.update(kwsUpdate)
                    yield problems.task.Task(
                        textTemplate.format(**args),
                        answer=answerTemplate.format(**args) if answerTemplate else None,
                        solutionSpace=self.GetSolutionSpace(),
                    )
                else:
                    yield self.__call__(**args)

    def GetTasksCount(self):
        if self.__TaskCount is None:
            self.__TaskCount = len(self.GetTasksList())
        return self.__TaskCount

    def GetTasksList(self):
        if self.__TasksList is None:
            self.__TasksList = list(self.All())
        return self.__TasksList

    def GetRandomTask(self, randomStr):
        hash_md5 = hashlib.md5()
        hash_md5.update(randomStr)
        randomHash = hash_md5.hexdigest()[8:16] # use only part of hash
        randomIndex = int(randomHash, 16) % self.GetTasksCount()
        self.__Stats[randomIndex] += 1
        return self.GetTasksList()[randomIndex]

    def GetStats(self):
        return self.__Stats


class Variants(object):
    def __init__(self, variantTasks, date=None, pupils=None):
        self.Date = date
        self.PupilsRandomSeedPart = pupils.GetRandomSeedPart()
        self.VariantTasks = variantTasks

    def GetPupilTasks(self, pupil):
        for variantTask in self.VariantTasks:
            randomStr = '_'.join([
                pupil.GetRandomSeedPart(),
                self.Date,
                self.PupilsRandomSeedPart,
            ]).encode('utf-8')
            yield variantTask.GetRandomTask(randomStr)

    def GetStats(self):
        for variantTask in self.VariantTasks:
            stats = [0] * variantTask.GetTasksCount()
            for index, value in variantTask.GetStats().iteritems():
                stats[index] = value
            log.debug('Stats for %s: %r', type(variantTask).__name__, stats)
            log.info('Stats for %s: %r', type(variantTask).__name__, collections.OrderedDict(sorted(variantTask.GetStats().iteritems())))


class MultiplePaper(object):
    def __init__(self, date=None, pupils=None):
        self.Date = library.formatter.Date(date)
        self.Pupils = pupils

    def GetTex(self, variants, withAnswers=False):
        if withAnswers:
            variantsJoiner = u''
        else:
            variantsJoiner = u'\n\\newpage'
        # variantsJoiner = u'\n\\newpage'
        variantsJoiner += '\n\n'
        variantsTex = []
        for pupil in self.Pupils.Iterate():
            variantText = u'\\addpersonalvariant{{{name}}}\n'.format(name=pupil.GetFullName())
            pupilTasksTex = u''
            pupilTasks = list(variants.GetPupilTasks(pupil))
            for index, task in enumerate(pupilTasks, 1):
                pupilTasksTex += u'\n\n\\tasknumber{%d}' % index
                pupilTasksTex += task.GetTex().strip()
                if not withAnswers and index != len(pupilTasks):
                    pupilTasksTex += u'\n\\vspace{%dpt}' % task.GetSolutionSpace()
            variantsTex.append(variantText + pupilTasksTex)
        variants.GetStats()
        text = variantsJoiner.join(variantsTex)
        result = PAPER_TEMPLATE.format(
            date=self.Date.GetHumanText(),
            classLetter=self.Pupils.Grade,
            text=text,
            noanswers='' if withAnswers else u'\\noanswers',
        )
        return result

    def GetFilename(self, name='task'):
        filename = '%s-%s' % (self.Date.GetFilenameText(), self.Pupils.Grade)
        if self.Pupils.Letter:
            letter = {
                u'А': 'A',
                u'Т': 'T',
                u'Л': 'L',
                u'М': 'M',
            }[self.Pupils.Letter]
            filename += letter

        if name:
            filename += '-' + name
        filename += '.tex'
        log.debug('Got filename %r', filename)
        return filename


def solution_space(space):
    def decorator(cls):
        cls.SolutionSpace = space
        return cls
    return decorator
