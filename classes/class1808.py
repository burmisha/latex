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
            '2018-12-21': (ur'\threecolumns{18pt}{\variant}{\variant}{\variant}', [
                ('gendenshteyn-8', [
                    '11-10', '11-15', '11-15-my', '11-20', '11-21',
                    '11-23', '11-24', '11-25', '11-26', '11-27',
                ]),
            ]),
            '2019-01-11': (ur'\twocolumns{30pt}{\variant \\ \variant}{\variant \\ \variant}', [
                ('gendenshteyn-8', [
                    '12-00-my-1', '12-00-my-2', '12-00-my-3', '12-04', '12-08',
                    '12-10', '12-00-my-4', '12-00-my-5', '12-00-my-6',
                ]),
            ]),
            '2019-01-15': (ur'\twocolumns{30pt}{\threevariants{20pt}{\variant}}{\threevariants{20pt}{\variant}}', [
                ('gendenshteyn-8', [
                    '12-00-my-4', '12-00-my-5', '12-00-my-6', '12-00-my-7'
                ]),
            ]),
        }
        for date, (style, tasks) in papers.iteritems():
            yield paper.Paper(date, tasks, classLetter='8', style=style)
