#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import os

import problems
import classes
import generators
import library

log = logging.getLogger('generate')


def generate(args):
    if args.lucky:
        return library.lucky.getLucky(args.lucky)

    fileWriter = library.files.FileWriter(args.filter)
    if args.tripod:
        for className, report in library.tripod.getTripodReports():
            fileWriter.Write(os.path.join('school-554', 'tripod'), className + '-tripod.tex', text=report.GetText())
            # print reports
        return

    generateProblems= False
    generateLists = False
    generateMultiple = False

    generateProblems = True
    generateLists = True
    generateMultiple = True

    fileWriter = library.files.FileWriter(args.filter)

    if generateProblems:
        tasksGenerators = [
            problems.gendenshteyn7.Gendenshteyn7(),
            problems.gendenshteyn8.Gendenshteyn8(),
            problems.gendenshteyn10.Gendenshteyn10(),
            problems.getaclass.GetAClass(),
            problems.savchenko.Savchenko(),
        ]
        for tasksGenerator in tasksGenerators:
            log.info('Using %r for tasks in %r', tasksGenerator, tasksGenerator.GetBookName())
            problemsPath = os.path.join('problems', tasksGenerator.GetBookName())
            for task in sorted(tasksGenerator(), key=lambda task: task.GetFilename()):
                if fileWriter.NotMatches(task.GetFilename()):
                    continue
                fileWriter.Write(problemsPath, task.GetFilename(), text=task.GetTex())

    if generateLists:
        papersGenerators = [
            classes.class1807.Class1807(),
            classes.class1808.Class1808(),
            classes.class1810.Class1810(),
        ]
        for papersGenerator in papersGenerators:
            for paper in papersGenerator():
                if fileWriter.NotMatches(paper.GetFilename()):
                    continue
                fileWriter.Write('school-554', paper.GetFilename(), text=paper.GetTex())

    if generateMultiple:
        seed = 2704

        classRandomTasks = {
            'class-2018-10': {
                '2019-04-16': [
                    generators.electricity.ForceTask(),
                    generators.electricity.ExchangeTask(),
                    generators.electricity.FieldTaskGenerator(),
                    generators.electricity.SumTask(),
                ],
                '2019-04-30': [
                    generators.electricity.Potential728(),
                    generators.electricity.Potential735(),
                    generators.electricity.Potential737(),
                    generators.electricity.Potential2335(),
                    generators.electricity.Potential1621(),
                ],
            },
            'class-2018-11': {
                '2019-04-19': [
                    generators.quantum.Fotons(),
                    generators.quantum.KernelCount(),
                    generators.quantum.RadioFall(),
                    generators.quantum.RadioFall2(),
                ],
                '2019-04-30': [
                    generators.quantum.Quantum1119(),
                    generators.quantum.Quantum1120(),
                ],
            },
        }
        for className, dateTasks in classRandomTasks.iteritems():
            classLetter = className.split('-')[-1]
            pupilsNames = list(library.pupils.getPupils(className, addMyself=True, onlyMe=False).Iterate())
            for date, taskGenerators in dateTasks.iteritems():
                multiplePaper = generators.variant.MultiplePaper(date, classLetter=classLetter)
                if fileWriter.NotMatches(multiplePaper.GetFilename()):
                    continue
                tasksLists = [taskGenerator.Shuffle(seed, minCount=len(pupilsNames)) for taskGenerator in taskGenerators]
                variants = generators.variant.Variants(pupilsNames, zip(*tasksLists))
                fileWriter.Write(
                    'school-554',
                    multiplePaper.GetFilename(),
                    text=multiplePaper.GetTex(variants.Iterate(), withAnswers=False),
                )

        if args.show_manual:
            fileWriter.ShowManual(extensions=['tex'])


def CreateArgumentsParser():
    fmtClass = {'formatter_class': argparse.ArgumentDefaultsHelpFormatter}
    parser = argparse.ArgumentParser(description='Generate LaTeX-files', **fmtClass)

    loggingGroup = parser.add_argument_group('Logging arguments')
    defaultLogFormat = ' '.join([
        # '%(relativeCreated)d',
        '%(asctime)s.%(msecs)03d',
        # '%(name)15s:%(lineno)-4d',
        '%(levelname)-7s',
        '%(message)s',
    ])
    loggingGroup.add_argument('--log-format', help='Logging format', default=defaultLogFormat)
    loggingGroup.add_argument('--log-separator', help='Logging string separator', choices=['space', 'tab'], default='space')
    loggingGroup.add_argument('-v', '--verbose', help='Enable debug logging', action='store_true')

    parser.add_argument('--show-manual', '--sm', help='Show manual files', action='store_true')
    parser.add_argument('--filter', help='Process only files matchin filter')

    parser.add_argument('-l', '--lucky', help='Get lucky people')
    parser.add_argument('-t', '--tripod', help='Print tripod results', action='store_true')

    parser.set_defaults(func=generate)

    return parser


def main():
    parser = CreateArgumentsParser()
    args = parser.parse_args()

    logFormat = args.log_format.replace('\t', ' ')
    logFormat = logFormat.replace(' ', {'space': ' ', 'tab': '\t'}[args.log_separator])
    logLevel = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=logLevel, format=logFormat, datefmt='%H:%M:%S')

    log.info('Start')
    args.func(args)
    log.info('Finish')


if __name__ == '__main__':
    main()
