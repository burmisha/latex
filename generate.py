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

    # generateProblems = True
    # generateLists = True
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

        tasks = zip(
            generators.electricity.ForceTask().Shuffle(seed),
            generators.electricity.ExchangeTask().Shuffle(seed),
            generators.electricity.FieldTaskGenerator().Shuffle(seed),
            generators.electricity.SumTask().Shuffle(seed) * 2,
        )
        pupilsNames = list(library.pupils.getPupils('class-2018-10', addMyself=True, onlyMe=False).Iterate())
        variants = generators.variant.Variants(pupilsNames, tasks)
        multiplePaper = generators.variant.MultiplePaper('2019-04-16', classLetter='10')
        library.files.writeFile('school-554', multiplePaper.GetFilename(), multiplePaper.GetTex(variants.Iterate()))

        tasks = zip(
            generators.electricity.Potential728().Shuffle(seed),
            generators.electricity.Potential735().Shuffle(seed),
            generators.electricity.Potential737().Shuffle(seed),
            generators.electricity.Potential2335().Shuffle(seed) * 4,
            generators.electricity.Potential1621().Shuffle(seed),
        )
        pupilsNames = list(library.pupils.getPupils('class-2018-10', addMyself=True, onlyMe=False).Iterate())
        variants = generators.variant.Variants(pupilsNames, tasks)
        multiplePaper = generators.variant.MultiplePaper('2019-04-30', classLetter='10')
        library.files.writeFile('school-554', multiplePaper.GetFilename(), multiplePaper.GetTex(variants.Iterate()))

        tasks = zip(
            generators.quantum.Fotons().Shuffle(seed),
            generators.quantum.KernelCount().Shuffle(seed) * 5,
            generators.quantum.RadioFall().Shuffle(seed) * 10,
            generators.quantum.RadioFall2().Shuffle(seed) * 10,
        )
        pupilsNames = list(library.pupils.getPupils('class-2018-11', addMyself=True, onlyMe=False).Iterate())
        variants = generators.variant.Variants(pupilsNames, tasks)
        multiplePaper = generators.variant.MultiplePaper('2019-04-19', classLetter='11')
        library.files.writeFile('school-554', multiplePaper.GetFilename(), multiplePaper.GetTex(variants.Iterate()))

        tasks = zip(
            generators.quantum.Quantum1119().Shuffle(seed) * 2,
            generators.quantum.Quantum1120().Shuffle(seed),
        )
        pupilsNames = list(library.pupils.getPupils('class-2018-11', addMyself=True, onlyMe=False).Iterate())
        variants = generators.variant.Variants(pupilsNames, tasks)
        multiplePaper = generators.variant.MultiplePaper('2019-04-30', classLetter='11')
        library.files.writeFile('school-554', multiplePaper.GetFilename(), multiplePaper.GetTex(variants.Iterate()))


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
