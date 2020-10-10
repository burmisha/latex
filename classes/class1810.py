# -*- coding: utf-8 -*-

import classes.paper as paper


# def style(columns=2, variants=2, pt=20):
#     columnsKey = {
#         2: 'twocolumns',
#     }[columns]
#     variants = '\\variant' * variants
#     return '\\{columns}{{{pt}pt}}{{{variants}}}{{{variants}}}'.format(
#         columns=columnsKey,
#         pt=pt,
#         variants=variants,
#     )


class Class1810(paper.PaperGenerator):
    def __call__(self):
        papers = {
            '2019-04-16': [
                ('gendenshteyn-10', ['21-13', '21-17', '21-27', '22-20', '22-31', '22-35']),
            ],
        }
        for date, tasks in papers.items():
            yield paper.Paper(date, tasks, classLetter='10', style=r'\twocolumns{40pt}{\twovariants{40pt}{\variant}}{\twovariants{20pt}{\variant}}')
