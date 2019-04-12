# -*- coding: utf-8 -*-

import paper


class Class1807(paper.PaperGenerator):
    def __call__(self):
        papers = {
            '2019-01-25': [
                ('gendenshteyn-7', ['21-19', '21-20', '21-29', '21-39', '21-36', '21-34']),
                ('getaclass', ['297', '298', '306']),
            ],
            '2019-01-28': [
                ('gendenshteyn-7', ['21-34']),
                ('getaclass', ['297', '298', '306']),
                # ur'\twocolumns{30pt}{\variant}{\variant}'
            ],
            '2019-02-01': [
                ('getaclass', ['1576', '1577', '1578', '1579']),
                ('gendenshteyn-7', ['22-24', '22-25', '22-27', '22-28', '22-29-1', '22-29', '22-29-2']),
            ],
        }
        for date, tasks in papers.iteritems():
            yield paper.Paper(date, tasks, classLetter='7', style=ur'\twocolumns{20pt}{\variant}{\variant}')
