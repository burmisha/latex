import os
import time

import problems
import classes
import generators
import library
import tools

import logging
log = logging.getLogger(__name__)


PAPER_TEMPLATE = r'''
\newcommand\rootpath{{../..}}
\input{{\rootpath/school-554/main}}
\begin{{document}}
{noanswers}
\input{{\rootpath/{filename}}}

\end{{document}}
'''


def run(args):
    fileWriter = library.files.FileWriter(args.filter)

    generateProblems = args.problems
    generateLists = args.lists
    generateMultiple = args.multiple

    if generateProblems:
        tasksGenerators = [
            problems.gendenshteyn7.Gendenshteyn7(),
            problems.gendenshteyn8.Gendenshteyn8(),
            problems.gendenshteyn10.Gendenshteyn10(),
            problems.gendenshteyn11.Gendenshteyn11(),
            problems.getaclass.GetAClass(),
            problems.savchenko.Savchenko(),
            problems.cheshev.Cheshev(),
        ]
        for tasksGenerator in tasksGenerators:
            log.info('Using %r for tasks in %r', tasksGenerator, tasksGenerator.GetBookName())
            problemsPath = os.path.join('problems', tasksGenerator.GetBookName())
            for task in sorted(tasksGenerator(), key=lambda task: task.GetFilename()):
                fileWriter.Write(problemsPath, task.GetFilename(), text=task.GetTex())
    else:
        log.warn('Skipping problems')

    if generateLists:
        papersGenerators = [
            classes.class1807.Class1807(),
            classes.class1808.Class1808(),
            classes.class1810.Class1810(),
            classes.class1911.Class1911(),
        ]
        for papersGenerator in papersGenerators:
            for paper in papersGenerator():
                fileWriter.Write('school-554', paper.GetFilename(), text=paper.GetTex())
    else:
        log.warn('Skipping lists')

    if generateMultiple:
        for work in classes.variants.get_all_variants():
            tasks = work.get_tasks()
            if not tasks:
                continue

            date = work._date
            multiplePaper = generators.variant.MultiplePaper(date=date, pupils=work._pupils)
            study_year_pair = date.GetStudyYearPair()
            filename = os.path.join(
                'school-554',
                f'generated-{str(study_year_pair[0])}-{str(study_year_pair[1])[2:]}',
                multiplePaper.GetFilename(),
            )

            text = multiplePaper.GetTex(variant_tasks=tasks)
            task = PAPER_TEMPLATE.format(noanswers='\n\\noanswers\n', filename=filename)
            answer = PAPER_TEMPLATE.format(noanswers='', filename=filename)

            fileWriter.Write(f'{filename}.tex', text=text)
            fileWriter.Write(f'{filename}-task.tex', text=task)
            fileWriter.Write(f'{filename}-answer.tex', text=answer)

        if args.show_manual:
            fileWriter.ShowManual(extensions=['tex'])
    else:
        log.warn('Skipping multiple')


def populate_parser(parser):
    parser.add_argument('--show-manual', '--sm', help='Show manual files', action='store_true')
    parser.add_argument('--filter', help='Process only files matching filter')
    parser.add_argument('-p', '--problems', help='Generate problems', action='store_true')
    parser.add_argument('-l', '--lists', help='Generate list', action='store_true')
    parser.add_argument('-m', '--multiple', help='Generate multiple', action='store_true')
    parser.set_defaults(func=run)
