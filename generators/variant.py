# -*- coding: utf-8 -*-

import collections
import hashlib
import re

from generators.helpers import UnitValue, Consts
from generators.helpers.vars import Vars

import library
import problems

import logging
log = logging.getLogger(__name__)


PAPER_TEMPLATE = r'''
\setdate{{{date}}}
\setclass{{{classLetter}}}

{text}
'''.strip()


def escape_tex(template):
    replacements = [
        ('{', '{{'),
        ('}', '}}'),
        (' * ', ' \\cdot '),
    ]
    tmpl = str(template)
    for src, dst in replacements:
        tmpl = tmpl.replace(src, dst)
    return tmpl


class LaTeXFormatter:
    def __init__(self, args=None):
        if args is None:
            args = {}
        assert isinstance(args, dict)
        self._args = args
        self._args['Consts'] = Consts
        self._keys = set(self._args.keys())

    def __substitute(self, line, replace_comma):
        assert isinstance(line, str)
        result = escape_tex(line)
        subs = {}
        for key in self._keys:
            for regexp in [
                '',
                '[\.\w]*\[[\\.\\:\\|\\*\\w\]]*',
                '([\.\w\]\[])*\\:[\\.\\:\\|\\*\\w]*',
            ]:
                regexp = '{{(' + key + regexp + ')}}'
                result, n = re.subn(regexp, r'{\1}', result)
                subs[key] = subs.get(key, 0) + n

        try:
            result = result.format(**(self._args))
        except Exception as e:
            log.error(f'Error {e} while formatting line with {len(self._args)} args:\n{line}\n\n{result}')
            for k, v in self._args.items():
                log.error(f'  arg {k}: {type(v)}')
            log.error(f'Subs: {subs}')
            raise

        # dirty hacks for tikz
        if replace_comma and ('node' not in line) and ('draw' not in line):
            result = re.sub('(\\d)\.(\\d)', '\\1{,}\\2', result)


        subs = [
            (r'\+ +-', '-'),
            (r'(\S) +}', r'\1 }'),
            ('{ +', '{ '),
        ]
        for src, dst in subs:
            result = re.sub(src, dst, result)
        return result

    def format(self, value, replace_comma=True):
        if value is None:
            return None
        elif isinstance(value, str):
            return self.__substitute(value, replace_comma)
        elif isinstance(value, dict):
            return {
                self.__substitute(k, replace_comma): v
                for k, v in value.items()
            }
        else:
            raise RuntimeError(f'LaTeXFormatter does not support {type(value)}: {value}')


def test_replace_comma():
    assert LaTeXFormatter().format('0.2', replace_comma=False) == '0.2'
    assert LaTeXFormatter().format('0.2', replace_comma=True) == r'0{,}2'
    assert LaTeXFormatter().format('node 0.2', replace_comma=True) == r'node 0.2'

test_replace_comma()

def test_substitute():
    for args, value, result in [
        ({}, '{}', '{}'),
        ({}, '{    }', '{ }'),
        (dict(a=2), {'{a}': 3}, {'2': 3}),
        (dict(a='0.20'), {'{a}': 0.3}, {'0{,}20': 0.3}),
        (dict(a=2), '{a}', '2'),
        (dict(a=2), '{a}', '2'),
        (dict(a=2), '{ab}[asd]', '{ab}[asd]'),
        (dict(a=[2, 3]), '{a[1]}', '3'),
        (dict(a=2), '{b}', '{b}'),
        (dict(a=2), '{b:.1d|as}', '{b:.1d|as}'),
        (dict(a=2, b=3), '{a}{b}', '23'),
        (dict(a=2, b=3), '{{a}}{b}', '{2}3'),
        (dict(a=2, b=3), '{ {a} }{b}', '{ 2 }3'),
        (dict(a=UnitValue('1 м')), '{a:V}', r'1\,\text{м}'),
        (dict(a=UnitValue('1 м')), '{a:V|sqr}', r'\sqr{1\,\text{м}}'),
        ({}, '{Consts.c:Letter}', r'c'),
        ({}, '{Consts.p_atm:Task:e}', r'$p_{\text{aтм}} = 100\,\text{кПа}$'),
        ({}, '{ {Consts.c:Letter} }', r'{ c }'),
        (dict(a=1), '{Consts.c:Letter}', r'c'),
        (dict(a=1), '\\begin{qq}', r'\begin{qq}'),
        (dict(a=1), '\\begin{qq*}', r'\begin{qq*}'),
        ({}, '\\begin{align*}F &= \sqrt{ F_a^2 + F_b^2 }\\end{align*}', r'\begin{align*}F &= \sqrt{ F_a^2 + F_b^2 }\end{align*}'),
    ]:
        res = LaTeXFormatter(args).format(value)
        assert res == result, f'''
  Expected: {result}
  Got: {res}
    value: {value}
    args: {args}
'''


test_substitute()


def check_unit_value(value):
    if isinstance(value, str):
        if value.count('=') == 1 and len(value) >= 3:
            return UnitValue(value)
        elif re.match(r'-?\d.* \w', value, re.UNICODE):
            return UnitValue(value)

    return value


assert isinstance(check_unit_value('2 суток'), UnitValue)
assert isinstance(check_unit_value('2 см'), UnitValue)
assert isinstance(check_unit_value('2 Дж'), UnitValue)
assert isinstance(check_unit_value('-2 Дж'), UnitValue)
assert isinstance(check_unit_value('1.6 м'), UnitValue)


class VariantTask:
    def __init__(self, pupils, date):
        self.__Stats = collections.defaultdict(int)
        self._pupils = pupils
        self._date = date
        self._expanded_args_list = None
        self._variants_count = None
        self._prefer_test_version = False

    def validate(self):
        pass

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
        results = [
            getattr(self, attr) for attr in ['AnswerTemplate', 'AnswerTex'] if hasattr(self, attr)
        ]
        if results:
            return '\n\n'.join(results)
        else:
            return None

    def GetAnswerTestTemplate(self):
        if hasattr(self, 'AnswerTestTemplate'):
            return self.AnswerTestTemplate
        else:
            return None

    def _get_args_from_index(self, index):
        res = self._vars.form_one(index)

        try:
            for k, v in res.items():
                res[k] = check_unit_value(v)
            res['Consts'] = Consts
            for k, v in self.GetUpdate(**res).items():
                res[k] = check_unit_value(v)
        except:
            log.error(f'Cannot enrich {type(self)}, args: {res}')
            raise

        return res

    def GetTasksCount(self):
        return self._vars.total_count()

    def GetRandomTask(self, pupil):
        if self._vars is None:
            args = ''
        else:
            args = '__'.join(sorted(self._vars._original_keys))
        hash_md5 = hashlib.md5()
        hash_md5.update((self._get_random_str(pupil) + args).encode('utf-8'))
        randomHash = hash_md5.hexdigest()[8:16]  # use only part of hash
        randomIndex = int(randomHash, 16) % self.GetTasksCount()
        self.__Stats[randomIndex] += 1
        args = self._get_args_from_index(randomIndex)

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
        # TODO: very slow on large tasks
        # if set(self.__Stats.values()) - {0, 1}:
        #     stats = ''.join(str(self.__Stats.get(index, '_')) for index in range(self.GetTasksCount()))  # TODO: support tasks with 10 on more
        # else:
        stats = ''
        log.info(
            '%s: total of %d tasks, used %d: |%s|',
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


class MultiplePaper:
    def __init__(self, date=None, pupils=None):
        self.Date = date  # only for date in header and filename
        self.Pupils = pupils

    def GetTex(self, variant_tasks=None, withAnswers=False, only_me=False):
        paper_tex = []
        for pupil in self.Pupils.Iterate(only_me=only_me):
            pupil_tex = [
                f'\\addpersonalvariant{{{pupil.name} {pupil.surname}}}'
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

    def GetFilename(self):
        filename = f'{self.Date.GetFilenameText()}-{self.Pupils.Grade}'
        if self.Pupils.LatinLetter:
            filename += self.Pupils.LatinLetter
        log.debug(f'Got filename {filename}')
        return filename


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
        cls.TextTemplate = template_str
        return cls
    return decorator


def text_test(template_str):
    def decorator(cls):
        assert not hasattr(cls, 'TextTestTemplate')
        cls.TextTestTemplate = template_str
        return cls
    return decorator


def answer(template_str):
    def decorator(cls):
        assert not hasattr(cls, 'AnswerTemplate')
        cls.AnswerTemplate = template_str
        return cls
    return decorator


def answer_short(template_str):
    def decorator(cls):
        assert not hasattr(cls, 'AnswerTemplate')
        cls.AnswerTemplate = f'${template_str}$'
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
            if '&' not in line:
                line = '&' + line
            lines.append(line)
        template = '\\begin{align*}\n' + ' \\\\\n'.join(lines) + '\n\\end{align*}'
        cls.AnswerTemplate = template.replace('\n\n', '\n')
        return cls
    return decorator


def answer_tex(text):
    def decorator(cls):
        assert not hasattr(cls, 'AnswerTex')
        cls.AnswerTex = text
        return cls
    return decorator


def no_args(cls):
    assert not hasattr(cls, '_vars')
    cls._vars = Vars()
    cls._vars._flatten()  # only one variant
    return cls


def arg(**kws):
    def decorator(cls):
        assert len(kws) == 1, f'Expected only one arg for {cls}, got {kws}'

        if not hasattr(cls, '_vars'):
            cls._vars = Vars()
        assert isinstance(cls._vars, Vars), f'Invalid _vars for {cls}: {cls._vars}'

        for key, value in kws.items():
            if isinstance(value, tuple):
                assert len(value) == 2
                assert '{}' in value[0], f'No {{}} in {value}'
                options = [value[0].format(option) for option in value[1]]
            else:
                options = value
            cls._vars.add(key, options)

        return cls

    return decorator
