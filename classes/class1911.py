# -*- coding: utf-8 -*-

import paper



class Class1911(paper.PaperGenerator):
    def __call__(self):
        papers = {
            '2019-01-22': [
                ('cheshev', ['5-01', '5-02', '5-03', '5-04']),
            ],
        }
        for date, tasks in papers.iteritems():
            yield paper.Paper(date, tasks, classLetter='11', style=ur'\twovariants{60pt}{\variant}')
