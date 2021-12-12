# -*- coding: utf-8 -*-

import collections
import hashlib
import re

from generators.helpers import UnitValue, Consts, letter_variants
from generators.helpers.vars import Vars
from generators.helpers.fraction import Fraction, FractionFormatter

import library
import problems
from library.logging import cm, color

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
        self._args = {}
        for key, value in args.items():
            if isinstance(value, Fraction):
                self._args[key] = FractionFormatter(value)
            else:
                self._args[key] = value
        self._args['Consts'] = Consts
        self._keys = set(self._args.keys())

    def __substitute(self, line, replace_comma):
        assert isinstance(line, str)
        result = escape_tex(line)
        subs = {}
        for key in self._keys:
            for regexp in [
                '',
                '\.\w+',
                '[\.\w]*\[[\\.\\:\\|\\*\\w\]]*',
                '([\.\w\]\[])*\\:[\\.\\:\\|\\*\\w]*',
            ]:
                regexp = '{{(' + key + regexp + ')}}'
                result, n = re.subn(regexp, r'{\1}', result)
                subs[key] = subs.get(key, 0) + n

        try:
            result = result.format(**(self._args))
        except Exception as e:
            log.error(f'''Error {cm(e, color=color.Red)} while formatting line with {len(self._args)} args
Line:
{line}

Substitutions:
{subs}

Preprocessed result:
{result}
''')
            for k, v in self._args.items():
                log.error(f'  arg {cm(k, color=color.Blue)}: {cm(type(v), color=color.Green)} is {cm(v, color=color.Red)}')
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

lv = list(letter_variants(
    {'дважды два': 'четыре', 'трижды три': 'девять'},
    ['пять', 'шесть'],
    answers_count=1,
    mocks_count=1,
))[0]

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
        (dict(a=UnitValue('1 м')), '{a:V}', '1\\,\\text{м}'),
        (dict(a=UnitValue('1 м')), '{a:V|sqr}', '\\sqr{1\\,\\text{м}}'),
        ({}, '{Consts.c:Letter}', r'c'),
        ({}, '{Consts.p_atm:Task:e}', r'$p_{\text{aтм}} = 100\,\text{кПа}$'),
        ({}, '{ {Consts.c:Letter} }', r'{ c }'),
        (dict(a=1), '{Consts.c:Letter}', r'c'),
        (dict(a=1), '\\begin{qq}', '\\begin{qq}'),
        (dict(a=1), '\\begin{qq*}', '\\begin{qq*}'),
        ({}, '\\begin{align*}F &= \\sqrt{ F_a^2 + F_b^2 }\\end{align*}', r'\begin{align*}F &= \sqrt{ F_a^2 + F_b^2 }\end{align*}'),
        (dict(lv=lv), '{lv.Questions}', 'А) дважды два'),
    ]:
        res = LaTeXFormatter(args).format(value)
        assert res == result, f'''
  Expected: {result}
  Got: {res}
    value: {value}
    args: {args}
'''


test_substitute()


def test_fraction():
    for template, frac, result in [
        ('{f:LaTeX}', Fraction(), '0'),
        ('{f:LaTeX}', Fraction(0), '0'),
        ('{f:LaTeX}', Fraction(1), '1'),
        ('{f:LaTeX}', Fraction(1) * (-2), '-2'),
        ('{f:LaTeX}', Fraction(1) * 2, '2'),
        ('{f:LaTeX}', Fraction(1) * 2 / 2, '1'),
        ('{f:LaTeX}', Fraction(1) * 2 / 2, '1'),
        ('{f:LaTeX}', Fraction(1) * 2 / 4, '\\frac12'),
        ('{f:LaTeX}', Fraction(1) * 19 / 20, '\\frac{19}{20}'),
        ('{f:LaTeX}', Fraction(1) * (-19) / 20, '-\\frac{19}{20}'),
        ('{f:LaTeX}', Fraction(1) / (2 * 3) * (-1) + 1, '\\frac56'),
        ('{f:Basic}', Fraction(1) / (2 * 3) * (-1) + 1, '5/6'),
        ('{f:Basic}', Fraction(1) / (2 * 3) * (-12), '-2'),
    ]:
        res = LaTeXFormatter({'f': frac}).format(template)
        assert res == result, f'Expected {result}, got {res} for {frac}'

    # alpha = 3
    # A_bonus_cycle = Fraction() * (alpha - 1) ** 2 / 2
    # assert f'{A_bonus_cycle:LaTeX}'
    # A_bonus_plus = Fraction() * (11 * alpha + 3) * (5 * alpha - 3) / (16 * 8)
    # assert f'{A_bonus_plus:LaTeX}'
    # U_bonus_plus = (Fraction() * 15 * (alpha + 1) ** 2 / 64 - alpha) * 3 / 2
    # assert f'{U_bonus_plus:LaTeX}'
    # U_bonus_12 = Fraction() * (alpha - 1) / 1 * 3 / 2
    # assert f'{U_bonus_12:LaTeX}'
    # eta_bonus = Fraction() * A_bonus_cycle / (U_bonus_plus + A_bonus_plus + U_bonus_12)
    # assert f'{eta_bonus:LaTeX}'

    # a = Fraction(1)
    # assert int(float(a)) == 1
    # b = a * 200
    # assert int(float(a)) == 1


test_fraction()


def check_unit_value(value):
    try:
        if isinstance(value, UnitValue):
            return value

        if isinstance(value, str):
            if value.count('=') == 1 and len(value) >= 3:
                after_eq = value.split('=')[1].strip()
                if ('sqrt' not in after_eq) and ('frac' not in after_eq) and not after_eq.isalpha():
                    return UnitValue(value)
            elif re.match(r' ?-?\d.* \w', value, re.UNICODE):
                return UnitValue(value)
    except ValueError:
        log.debug(f'Failed to check_unit_value for {cm(value, color=color.Red)}')

    return value


def test_check_unit_value():
    data = [
        ('2 суток', True),
        ('2 см', True),
        ('2 Дж', True),
        ('-2 Дж', True),
        ('1.6 м', True),
        ('2 * A \\frac{1}{\\sqrt 2} = A\\sqrt{2}', False),
        ('2 * A / 2 = A', False),
        ('A', False),
    ]
    for row, is_uv in data:
        result = isinstance(check_unit_value(row), UnitValue)
        assert result is is_uv


test_check_unit_value()


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
            for k, v in self.GetUpdate(**res).items():
                res[k] = check_unit_value(v)
        except:
            log.error(f'Cannot enrich {cm(type(self), color=color.Green)} with args')
            for k, v in res.items():
                log.error(f'  {cm(k, color=color.Cyan)} of type {cm(type(v), color=color.Cyan)}: {v!r}')

            raise

        return res

    def GetTasksCount(self):
        result = self._vars.total_count()
        assert result, f'No tasks for {self}'
        return result

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
            classLetter=self.Pupils.get_class_letter(),
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
        assert '\t' not in template_str
        cls.TextTemplate = template_str
        return cls
    return decorator


def text_test(template_str):
    def decorator(cls):
        assert not hasattr(cls, 'TextTestTemplate')
        assert '\t' not in template_str
        cls.TextTestTemplate = template_str
        return cls
    return decorator


def answer(template_str):
    def decorator(cls):
        assert not hasattr(cls, 'AnswerTemplate')
        assert '\t' not in template_str
        cls.AnswerTemplate = template_str
        return cls
    return decorator


def answer_short(template_str):
    def decorator(cls):
        assert not hasattr(cls, 'AnswerTemplate')
        assert '\t' not in template_str
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
        assert '\t' not in template
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

        if hasattr(cls, '_vars'):
            assert isinstance(cls._vars, Vars), f'Invalid _vars for {cls}: {cls._vars}'
        else:
            cls._vars = Vars()

        for key, value in kws.items():
            cls._vars.add(key, value)

        return cls

    return decorator
