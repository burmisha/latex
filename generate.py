#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import random
import time

import problems
import classes
import generators
import library

log = logging.getLogger('generate')


def getLucky(lucky):
    count = None
    if ':' in lucky:
        className, count = lucky.split(':')
        count = int(count)
    else:
        className = lucky
    className = 'class-2018-{}'.format(className)
    pupils = list(library.pupils.getPupils(className).Iterate())
    random.seed(int(time.time()))
    random.shuffle(pupils)
    if count:
        pupils = pupils[:count]
    for pupil in pupils:
        log.info('New lucky person:  %s', pupil)
    return None


def generate(args):
    if args.lucky:
        return getLucky(args.lucky)

    generateProblems= False
    generateLists = False
    generateMultiple = False

    generateProblems = True
    generateLists = True
    generateMultiple = True

    if generateProblems:
        tasksGenerators = [
            problems.gendenshteyn7.Gendenshteyn7(),
            problems.gendenshteyn8.Gendenshteyn8(),
            problems.gendenshteyn10.Gendenshteyn10(),
            problems.getaclass.GetAClass(),
            problems.savchenko.Savchenko(),
        ]
        taskNumber = args.task_number
        for tasksGenerator in tasksGenerators:
            log.info('Using %r for tasks in %r', tasksGenerator, tasksGenerator.GetBookName())
            generatedTasks = set()
            problemsPath = os.path.join('problems', tasksGenerator.GetBookName())
            for task in sorted(tasksGenerator(), key=lambda task: task.GetFilename()):
                if taskNumber and taskNumber not in task.GetFilename():
                    continue
                filename = os.path.join(problemsPath, task.GetFilename())
                generatedTasks.add(filename)
                library.files.writeFile('', filename, task.GetTex())
            allTasks = set(library.files.walkFiles(problemsPath, extensions=['tex']))
            manualTasks = sorted(allTasks - generatedTasks)
            if args.show_manual:
                log.info('Got %d manual tasks in %s', len(manualTasks), tasksGenerator.GetBookName())
                for manualTask in manualTasks:
                    log.info('  Manual task: %r', manualTask)

    if generateLists:
        papersGenerators = [
            classes.class1807.Class1807(),
            classes.class1810.Class1810(),
        ]
        for papersGenerator in papersGenerators:
            for paper in papersGenerator():
                library.files.writeFile('school-554', paper.GetFilename(), paper.GetTex())

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
            for date, tasks in dateTasks.iteritems():
                pupilsNames = list(library.pupils.getPupils(className, addMyself=True, onlyMe=False).Iterate())
                pupilsCount = len(pupilsNames)
                tasksResults = []
                for task in tasks:
                    tasksList = task.Shuffle(seed)
                    tasksResult = list(tasksList)
                    while len(tasksResult) <= pupilsCount:
                        tasksResult += tasksList
                    tasksResults.append(tasksResult)
                variants = generators.variant.Variants(pupilsNames, zip(*tasksResults))
                multiplePaper = generators.variant.MultiplePaper(date, classLetter=classLetter)
                library.files.writeFile(
                    'school-554',
                    multiplePaper.GetFilename(),
                    multiplePaper.GetTex(variants.Iterate(), withAnswers=False),
                )


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
    parser.add_argument('--task-number', '--tn', help='Process only one task having number')

    parser.add_argument('--lucky', help='Get lucky people')

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
