import os
import time

import problems
import generators
import library
import tools

import logging
log = logging.getLogger(__name__)


PAPER_TEMPLATE = r'''
\newcommand\rootpath{{../../..}}
\input{{\rootpath/school-554/main}}
\begin{{document}}
{noanswers}
\input{{\rootpath/{filename}}}

\end{{document}}
'''


DEBUG_TEMPLATE = r'''
\newcommand\rootpath{{../../..}}
\input{{\rootpath/school-554/main}}
\begin{{document}}

{debug_tex}

\end{{document}}
'''


def get_dir_from_date(date, create_missing=False):
    first_start, second_year = date.GetStudyYearPair()
    dirname = os.path.join(
        'school-554',
        f'generated-{first_start}-{str(second_year)[2:]}',
        f'{date.Year}-{date.Month}',
    )
    if not os.path.isdir(dirname) and create_missing:
        log.info(f'Create missing {dirname}')
        os.mkdir(dirname)
    return dirname



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
            problems.gendenshteyn11.Gendenshteyn11_2(),
            problems.getaclass.GetAClass(),
            problems.savchenko.Savchenko(),
            problems.cheshev.Cheshev(),
        ]
        for tasksGenerator in tasksGenerators:
            log.info('Using %r for tasks in %r', tasksGenerator, tasksGenerator.GetBookName())
            problemsPath = library.location.root('problems', tasksGenerator.GetBookName())
            for task in sorted(tasksGenerator(), key=lambda task: task.GetFilename()):
                fileWriter.Write(problemsPath, task.GetFilename(), text=task.GetTex())
    else:
        log.warn('Skipping problems')

    if generateLists:
        papers_config = library.files.load_yaml_data('classes.yaml')
        for paper_id, data in papers_config.items():
            tasks = []
            for task_item in data['tasks']:
                book, tasks_line = task_item.split(':')
                tasks.append((book, [task.strip().replace('.', '-') for task in tasks_line.split(',')]))
            paper = library.template.paper.Paper(paper_id, tasks, style=data['style'])
            dirname = get_dir_from_date(paper.Date, create_missing=True)
            filename = os.path.join(dirname, paper.GetFilename())
            fileWriter.Write(f'{filename}-classwork.tex', text=paper.GetTex())
    else:
        log.warn('Skipping lists')

    if generateMultiple:
        for work in tools.variants.get_all_variants():
            tasks = work.get_tasks()
            if not tasks:
                continue

            date = work._date
            multiplePaper = generators.variant.MultiplePaper(date=date, pupils=work._pupils)
            dirname = get_dir_from_date(date, create_missing=True)
            filename = os.path.join(dirname, multiplePaper.GetFilename())

            text = multiplePaper.GetTex(variant_tasks=tasks, only_me=False)
            task = PAPER_TEMPLATE.format(noanswers='\n\\noanswers\n', filename=filename)
            answer = PAPER_TEMPLATE.format(noanswers='', filename=filename)
            debug_tex = DEBUG_TEMPLATE.format(debug_tex=multiplePaper.GetTex(variant_tasks=tasks, only_me=True))

            fileWriter.Write(f'{filename}.tex', text=text)
            fileWriter.Write(f'{filename}-task.tex', text=task)
            fileWriter.Write(f'{filename}-answer.tex', text=answer)
            fileWriter.Write(f'{filename}-debug.tex', text=debug_tex)

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
