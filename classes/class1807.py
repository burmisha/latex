# -*- coding: utf-8 -*-

import paper


class Class1807(paper.PaperGenerator):
    def __call__(self):
        papers = {
            '2018-12-03': (ur'\variant\vspace{30pt}\variant', [
                ('gendenshteyn-7', [
                    '13-01', '13-02', '13-03', '13-04', '13-06',
                    '13-09', '13-16', '13-19', '13-21', '13-22',
                    '13-26', '13-33', '13-34', '13-38', '13-41',
                    '13-57', '13-61', '13-62'
                ]),
            ]),
            '2018-12-17': (ur'\twocolumns{40pt}{{\variant}}{{\variant}}', [
                ('gendenshteyn-7', [
                    '18-01', '18-02', '18-03', '18-04', '18-20',
                    '18-05', '18-06', '18-07', '18-08', '18-24',
                    '18-09', '18-10', '18-11', '18-15', '18-13', 
                ]),
            ]),
            '2019-01-25': (ur'\twocolumns{20pt}{\variant}{\variant}', [
                ('gendenshteyn-7', ['21-19', '21-20', '21-29', '21-39', '21-36', '21-34']),
                ('getaclass', ['297', '298', '306']),
            ]),
            '2019-01-28': (ur'\twocolumns{30pt}{\variant}{\variant}', [
                ('gendenshteyn-7', ['21-34']),
                ('getaclass', ['297', '298', '306']),
            ]),
            '2019-02-01': (ur'\twocolumns{20pt}{\variant}{\variant}', [
                ('getaclass', ['1576', '1577', '1578', '1579']),
                ('gendenshteyn-7', ['22-24', '22-25', '22-27', '22-28', '22-29-1', '22-29', '22-29-2']),
            ]),
        }
        for date, (style, tasks) in papers.iteritems():
            yield paper.Paper(date, tasks, classLetter='7', style=style)
