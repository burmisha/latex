# -*- coding: utf-8 -*-

import problems
import variant

import itertools

import logging
log = logging.getLogger(__name__)


class Equations(variant.VariantTask):
    def __call__(self, **kws):
        text = u'''
            Для частицы, движущейся с релятивистской скоростью, 
            выразите ${x}$ и ${y}$ через $m$, ${a}$ и ${b}$, где
            $E_\\text{{кин}}$~--- кинетическая энергия частицы,
            $E_0$~--- её энергия покоя,
            а $p, v, m$~--- её импульс, скорость и масса.
        '''.format(**kws)
        return problems.task.Task(text, solutionSpace=200)

    def GetArgs(self):
        return {
            ('x', 'y', 'a', 'b'): itertools.permutations([
                u'E_\\text{кин}',
                u'E_0',
                u'p',
                u'v',
            ], 4),
        }
