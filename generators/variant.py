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
        if isinstance(v, (str, unicode)) and (('=' in v and len(v) >= 3) or re.match(r'\d.* \w', v, re.UNICODE)):
            return value.UnitValue(v)
        else:
            return v
    except:
        print v
        raise


assert isinstance(check_unit_value(u'2 суток'), value.UnitValue)
assert isinstance(check_unit_value(u'2 см'), value.UnitValue)
# assert isinstance(check_unit_value(u'1.6 м'), value.UnitValue)  # TODO

def form_args(kwargs):
    keys = []
    values = []
    for key, value in kwargs.iteritems():
        value = list(value)
        if any(isinstance(v, tuple) or isinstance(v, list) for v in value):
            for v in value:
                assert isinstance(v, tuple) or isinstance(v, list)
            if isinstance(key, (str, unicode)) and '__' in key:
                key = tuple(part.strip() for part in key.split('__'))
                for v in value:
                    assert len(key) == len(v), '%r' % [key, value]

        keys.append(key)
        values.append(value)
    for row in itertools.product(*values):
        result = {}
        for key, value in zip(keys, row):
            if isinstance(key, tuple):
                result.update(dict(zip(key, value)))
            else:
                result[key] = value
        yield result


class VariantTask(object):
    def __init__(self):
        self.__TasksList = None
        self.__TaskCount = None
        self.__Stats = collections.defaultdict(int)

    def GetUpdate(self, **kws):
        return {}

    def GetSolutionSpace(self):
        if hasattr(self, 'SolutionSpace'):
            return self.SolutionSpace
        else:
            return problems.task.DEFAULT_SOLUTION_SPACE

    def GetTextTemplate(self):
        if hasattr(self, 'TextTemplate'):
            return self.TextTemplate
        else:
            raise RuntimeError('No text for task')

    def GetAnswerTemplate(self):
        if hasattr(self, 'AnswerTemplate'):
            return self.AnswerTemplate
        else:
            return None

    def GetArgs(self):
        if self.ArgsList is None:  # only one variant
            args = {}
        else:
            args = self.ArgsList

        for res in form_args(args):
            for k, v in res.iteritems():
                res[k] = check_unit_value(v)
            res['Consts'] = value.Consts
            for k, v in self.GetUpdate(**res).iteritems():
                res[k] = check_unit_value(v)
            yield res

    def All(self):
        textTemplate = self.GetTextTemplate()
        answerTemplate = self.GetAnswerTemplate()
        for args in self.GetArgs():
            try:
                text = textTemplate.format(**args)
                text = re.sub('(\\d)\.(\\d)', '\\1{,}\\2', text)
            except:
                print textTemplate
                print args
                raise
            try:
                if answerTemplate:
                    answer = answerTemplate.format(**args)
                    answer = re.sub('(\\d)\.(\\d)', '\\1{,}\\2', answer)
                else:
                    answer = None
            except:
                print answerTemplate
                print args
                raise
            yield problems.task.Task(
                text,
                answer=answer,
                solutionSpace=self.GetSolutionSpace(),
            )

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
        if self.Pupils.Letter:
            classLetter = u'{}«{}»'.format(self.Pupils.Grade, self.Pupils.Letter)
        else:
            classLetter = self.Pupils.Grade
        result = PAPER_TEMPLATE.format(
            date=self.Date.GetHumanText(),
            classLetter=classLetter,
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


def text(text_template):
    def decorator(cls):
        cls.TextTemplate = text_template
        return cls
    return decorator


def answer(answer_template):
    def decorator(cls):
        assert not hasattr(cls, 'AnswerTemplate')
        cls.AnswerTemplate = answer_template
        return cls
    return decorator


def answer_short(answer_template):
    def decorator(cls):
        assert not hasattr(cls, 'AnswerTemplate')
        templateLine = answer_template.replace(u'{ ', u'{{ ').replace(u' }', u' }}')
        template = u'${}$'.format(templateLine)
        cls.AnswerTemplate = template.replace('\n\n', '\n')
        return cls
    return decorator


def answer_align(answer_template):
    def decorator(cls):
        assert not hasattr(cls, 'AnswerTemplate')
        templateLines = []
        for line in answer_template:
            templateLines.append(line.replace(u'{ ', u'{{ ').replace(u' }', u' }}'))
        templateLine = u' \\\\\n'.join(templateLines).strip()
        template = u'\\begin{{align*}}\n' +  templateLine + u'\n\\end{{align*}}'
        cls.AnswerTemplate = template.replace('\n\n', '\n')
        return cls
    return decorator


def args(*args_list, **kws):
    assert args_list == () or (len(args_list) == 1 and (isinstance(args_list[0], dict) or args_list[0] is None)), '%r' % [args_list, kws]
    def decorator(cls):
        if args_list == ():
            if kws:
                cls.ArgsList = kws
            else:
                raise RuntimeError()
        else:
            if args_list[0] is None:
                if kws:
                    cls.ArgsList = kws
                else:
                    cls.ArgsList = args_list[0]
            else:
                cls.ArgsList = args_list[0]
                cls.ArgsList.update(kws)
        return cls
    return decorator
