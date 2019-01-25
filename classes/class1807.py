# -*- coding: utf-8 -*-

import paper


class Class1807(paper.PaperGenerator):
    def __call__(self):
        papers = {
            '2019-01-25': [
                ('gendenshteyn-7', ['21-19', '21-20', '21-29', '21-39', '21-36', '21-34']),
                ('getaclass', ['297', '298', '306']),
            ],
        }
        for date, tasks in papers.iteritems():
            yield paper.Paper(date, tasks, classLetter='7')
