# -*- coding: utf-8 -*-

import collections
import hashlib
import itertools
import re

import generators.value as value

import library
import problems

import logging
log = logging.getLogger(__name__)


PAPER_TEMPLATE = r'''
\input{{main}}
\narrow
\begin{{document}}
{noanswers}

\setdate{{{date}}}
\setclass{{{classLetter}}}

{text}

\end{{document}}
'''.strip()


class LaTeXFormatter:
    def __init__(self, args):
        self._args = args

    def __substitute(self, line, replace_comma):
        assert isinstance(line, str)
        result = line.format(**(self._args))
        if replace_comma:
            result = re.sub('(\\d)\.(\\d)', '\\1{,}\\2', result)
        result = re.sub(r'\+ +-', '-', result)
        return result

    def format(self, value, replace_comma=True):
        try:
            if value is None:
                return None
            elif isinstance(value, str):
                return self.__substitute(value, replace_comma=replace_comma)
            elif isinstance(value, dict):
                return dict(
                    (self.__substitute(k, replace_comma=replace_comma), v)
                    for k, v in value.items()
                )
            else:
                raise RuntimeError(f'LaTeXFormatter does not support {value}')
        except:
            log.error(f'Cannot format template for {type(value)}')
            log.error(f'Template: {value}')
            log.error(f'Args: {self._args}')
            raise


assert LaTeXFormatter({}).format('0.2', replace_comma=False) == '0.2'
assert LaTeXFormatter({}).format('0.2', replace_comma=True) == r'0{,}2'
assert LaTeXFormatter({'a': '0.20'}).format({'{a}': 0.3}, replace_comma=False) == {'0.20': 0.3}


def check_unit_value(v):
    if isinstance(v, str) and (('=' in v and len(v) >= 3) or re.match(r'-?\d.* \w', v, re.UNICODE)):
        return value.UnitValue(v)
    else:
        return v


assert isinstance(check_unit_value('2 суток'), value.UnitValue)
assert isinstance(check_unit_value('2 см'), value.UnitValue)
assert isinstance(check_unit_value('2 Дж'), value.UnitValue)
assert isinstance(check_unit_value('-2 Дж'), value.UnitValue)
assert isinstance(check_unit_value('1.6 м'), value.UnitValue)


def form_args(kwargs):
    keys = []
    values = []
    assert isinstance(kwargs, collections.OrderedDict), kwargs
    for key, value in kwargs.items():
        value = list(value)
        if any(isinstance(v, tuple) or isinstance(v, list) for v in value):
            for v in value:
                assert isinstance(v, tuple) or isinstance(v, list)
            if isinstance(key, str) and '__' in key:
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


def test_form_args():
    od = collections.OrderedDict()
    od['a'] = [1, 2]
    od['b'] = [7, 8]
    assert list(form_args(od)) == [
        {'a': 1, 'b': 7},
        {'a': 1, 'b': 8},
        {'a': 2, 'b': 7},
        {'a': 2, 'b': 8},
    ]

    od = collections.OrderedDict()
    od['b'] = [7, 8]
    od['a'] = [1, 2]
    assert list(form_args(od)) == [
        {'a': 1, 'b': 7},
        {'a': 2, 'b': 7},
        {'a': 1, 'b': 8},
        {'a': 2, 'b': 8},
    ]

    od = collections.OrderedDict()
    od['a'] = [1, 2]
    od['b__c'] = [(7, 77), (8, 88), (9, 99)]
    assert list(form_args(od)) == [
        {'a': 1, 'b': 7, 'c': 77},
        {'a': 1, 'b': 8, 'c': 88},
        {'a': 1, 'b': 9, 'c': 99},
        {'a': 2, 'b': 7, 'c': 77},
        {'a': 2, 'b': 8, 'c': 88},
        {'a': 2, 'b': 9, 'c': 99},
    ]

    od = collections.OrderedDict()
    od['b__c'] = [(7, 77), (8, 88), (9, 99)]
    od['a'] = [1, 2]
    assert list(form_args(od)) == [
        {'a': 1, 'b': 7, 'c': 77},
        {'a': 2, 'b': 7, 'c': 77},
        {'a': 1, 'b': 8, 'c': 88},
        {'a': 2, 'b': 8, 'c': 88},
        {'a': 1, 'b': 9, 'c': 99},
        {'a': 2, 'b': 9, 'c': 99},
    ]

test_form_args()


class VariantTask(object):
    def __init__(self, pupils, date):
        self.__Stats = collections.defaultdict(int)
        self._pupils = pupils
        self._date = date
        self._expanded_args_list = None
        self._prefer_test_version = False

    def PreferTestVersion(self):
        self._prefer_test_version = True

    def GetUpdate(self, **kws):
        return {}

    def GetSolutionSpace(self):
        if hasattr(self, 'SolutionSpace'):
            return self.SolutionSpace
        else:
            return problems.task.DEFAULT_SOLUTION_SPACE

    def GetTextTemplate(self):
        if self._prefer_test_version and hasattr(self, 'TextTestTemplate'):
            return self.TextTestTemplate
        if hasattr(self, 'TextTemplate'):
            return self.TextTemplate
        else:
            raise RuntimeError(f'No text for task {type(self)}')

    def GetAnswerTemplate(self):
        if hasattr(self, 'AnswerTemplate'):
            return self.AnswerTemplate
        else:
            return None

    def GetAnswerTestTemplate(self):
        if hasattr(self, 'AnswerTestTemplate'):
            return self.AnswerTestTemplate
        else:
            return None

    def _get_expanded_args_list(self):
        try:
            if self._expanded_args_list is None:
                self._expanded_args_list = []
                if self.ArgsList is None:  # only one variant
                    args = collections.OrderedDict()
                else:
                    args = self.ArgsList

                for res in form_args(args):
                    try:
                        for k, v in res.items():
                            res[k] = check_unit_value(v)
                        res['Consts'] = value.Consts
                        for k, v in self.GetUpdate(**res).items():
                            res[k] = check_unit_value(v)
                    except:
                        log.error(f'Cannot enrich {type(self)}')
                        raise
                    self._expanded_args_list.append(res)
        except:
            log.error(f'Could not _get_expanded_args_list for {type(self)}')
            raise

        return self._expanded_args_list

    def GetTasksCount(self):
        return len(self._get_expanded_args_list())

    def GetRandomTask(self, pupil):
        if self.ArgsList is None:
            args = ''
        else:
            args = '__'.join(sorted(self.ArgsList.keys()))
        hash_md5 = hashlib.md5()
        hash_md5.update((self._get_random_str(pupil) + args).encode('utf-8'))
        randomHash = hash_md5.hexdigest()[8:16] # use only part of hash
        randomIndex = int(randomHash, 16) % self.GetTasksCount()
        self.__Stats[randomIndex] += 1
        args = self._get_expanded_args_list()[randomIndex]
        laTeXFormatter = LaTeXFormatter(args)

        textTemplate = self.GetTextTemplate()
        answerTemplate = self.GetAnswerTemplate()
        answer_test_template = self.GetAnswerTestTemplate()

        return problems.task.Task(
            laTeXFormatter.format(textTemplate),
            answer=laTeXFormatter.format(answerTemplate),
            test_answer=laTeXFormatter.format(answer_test_template, replace_comma=False),
            solutionSpace=self.GetSolutionSpace(),
        )

    def CheckStats(self):
        stats = ''.join(str(self.__Stats.get(index, '_')) for index in range(self.GetTasksCount()))  # TODO: support tasks with 10 on more
        log.info(
            '%s: total of %d tasks, used %d: %r',
            type(self).__name__,
            self.GetTasksCount(),
            len(self.__Stats),
            stats,
        )

    def _get_random_str(self, pupil):
        return '_'.join([
            pupil.GetRandomSeedPart(),
            self._date.GetFilenameText(),
            self._pupils.GetRandomSeedPart()
        ])


def get_class_letter(pupils):
    if pupils.Letter:
        return '{}«{}»'.format(pupils.Grade, pupils.Letter)
    else:
        return pupils.Grade


class MultiplePaper(object):
    def __init__(self, date=None, pupils=None):
        self.Date = date  # only for date in header and filename
        self.Pupils = pupils

    def GetTex(self, variant_tasks=None, withAnswers=False):
        paper_tex = []
        for pupil in self.Pupils.Iterate():
            pupil_tex = [
                f'\\addpersonalvariant{{{pupil.GetFullName()}}}'
            ]
            for index, variant_task in enumerate(variant_tasks, 1):
                task = variant_task.GetRandomTask(pupil)
                task_tex = task.GetTex(index=index, add_solution_space=index != len(variant_tasks))
                pupil_tex += ['', task_tex]
            paper_tex.append('\n'.join(pupil_tex))

        for variant_task in variant_tasks:
            variant_task.CheckStats()

        paper_tex = '\n\n\\variantsplitter\n\n'.join(paper_tex)

        result = PAPER_TEMPLATE.format(
            date=self.Date.GetHumanText(),
            classLetter=get_class_letter(self.Pupils),
            text=paper_tex,
            noanswers='' if withAnswers else '\\noanswers',
        )
        return result

    def GetFilename(self, name='task'):
        filename = f'{self.Date.GetFilenameText()}-{self.Pupils.Grade}'
        if self.Pupils.LatinLetter:
            filename += self.Pupils.LatinLetter
        if name:
            filename += '-' + name
        filename += '.tex'
        log.debug(f'Got filename {filename}')
        return filename


def escape_tex(template):
    return template.replace('{\n', '{{\n').replace('\n}', '\n}}').replace('{ ', '{{ ').replace(' }', ' }}')


def solution_space(space):
    def decorator(cls):
        assert not hasattr(cls, 'SolutionSpace')
        assert isinstance(space, int)
        cls.SolutionSpace = space
        return cls
    return decorator


def text(template_str):
    def decorator(cls):
        assert not hasattr(cls, 'TextTemplate')
        cls.TextTemplate = escape_tex(template_str)
        return cls
    return decorator


def text_test(template_str):
    def decorator(cls):
        assert not hasattr(cls, 'TextTestTemplate')
        cls.TextTestTemplate = escape_tex(template_str)
        return cls
    return decorator


def answer(template_str):
    def decorator(cls):
        assert not hasattr(cls, 'AnswerTemplate')
        cls.AnswerTemplate = escape_tex(template_str)
        return cls
    return decorator


def answer_short(template_str):
    def decorator(cls):
        assert not hasattr(cls, 'AnswerTemplate')
        cls.AnswerTemplate = '${}$'.format(escape_tex(template_str))
        return cls
    return decorator


def answer_test(template):
    def decorator(cls):
        assert not hasattr(cls, 'AnswerTestTemplate')
        cls.AnswerTestTemplate = template
        return cls
    return decorator


def answer_align(template_lines):
    def decorator(cls):
        assert not hasattr(cls, 'AnswerTemplate')
        lines = []
        for line in template_lines:
            assert '&' in line
            lines.append(escape_tex(line))
        template = '\\begin{{align*}}\n' + ' \\\\\n'.join(lines) + '\n\\end{{align*}}'
        cls.AnswerTemplate = template.replace('\n\n', '\n')
        return cls
    return decorator


def no_args(cls):
    assert not hasattr(cls, 'ArgsList')
    cls.ArgsList = None
    return cls


def arg(**kws):
    def decorator(cls):
        assert len(kws) == 1, f'Invalid arg for {cls}: {kws}'
        if hasattr(cls, 'ArgsList'):
            assert isinstance(cls.ArgsList, collections.OrderedDict), f'Invalid ArgsList for {cls}: {cls.ArgsList}'
        else:
            cls.ArgsList = collections.OrderedDict()
        for key, value in kws.items():
            assert key not in cls.ArgsList, f'Already used key in ArgsList: {key}'
            cls.ArgsList[key] = value
        return cls

    return decorator
