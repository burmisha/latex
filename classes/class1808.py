import paper


class Class1808(paper.PaperGenerator):
    def __call__(self):
        papers = {
            '2018-12-14': (ur'\threecolumns{30pt}{\variant}{\variant}{\variant}', [
                ('gendenshteyn-8', [
                	'10-01', '10-02', '10-03', '10-04', '10-05',
                	'10-06', '10-07', '10-08', '10-09', '10-10',
                	'10-11', '10-12', '10-13',
                ]),
            ]),
        }
        for date, (style, tasks) in papers.iteritems():
            yield paper.Paper(date, tasks, classLetter='8', style=style)
