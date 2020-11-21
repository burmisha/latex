import os
import time

import problems
import classes
import generators
import library
import tools

import logging
log = logging.getLogger(__name__)


def run(args):
    fileWriter = library.files.FileWriter(args.filter)

    generateProblems = True
    generateLists = True
    generateMultiple = True

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

    if generateMultiple:
        for pupils, date, variants in classes.variants.get_all(only_me=args.me):
            multiplePaper = generators.variant.MultiplePaper(date=date, pupils=pupils)
            text = multiplePaper.GetTex(variants=variants, withAnswers=args.answers)
            fileWriter.Write('school-554', multiplePaper.GetFilename(), text=text)

        if args.show_manual:
            fileWriter.ShowManual(extensions=['tex'])


def populate_parser(parser):
    parser.add_argument('--show-manual', '--sm', help='Show manual files', action='store_true')
    parser.add_argument('--filter', help='Process only files matchin filter')
    parser.add_argument('--me', help='Use only me mode', action='store_true')
    parser.add_argument('--answers', help='save answers', action='store_true')
    parser.set_defaults(func=run)
