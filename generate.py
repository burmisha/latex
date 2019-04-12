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
    generateProblems= False
    generateLists = False
    generateMultiple = False

    # generateProblems = True
    generateLists = True
    generateMultiple = True

    if generateProblems:
        tasksGenerators = [
            problems.gendenshteyn7.Gendenshteyn7(),
            problems.gendenshteyn8.Gendenshteyn8(),
            problems.getaclass.GetAClass(),
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
                log.info('Saving file %s', filename)
                with open(filename, 'w') as f:
                    f.write(task.GetTex().encode('utf-8'))
            allTasks = set(library.walkFiles(problemsPath, extensions=['tex']))
            manualTasks = sorted(allTasks - generatedTasks)
            if args.show_manual:
                log.info('Got %d manual tasks in %s', len(manualTasks), tasksGenerator.GetBookName())
                for manualTask in manualTasks:
                    log.info('  Manual task: %r', manualTask)

    if generateLists:
        papersGenerators = [
            classes.class1807.Class1807(),
        ]
        for papersGenerator in papersGenerators:
            for paper in papersGenerator():
                filename = os.path.join('school-554', paper.GetFilename())
                with open(filename, 'w') as f:
                    f.write(paper.GetTex().encode('utf-8'))

    if generateMultiple:
        pupils = [
            u'Гагик Аракелян',
            u'Ирен Аракелян',
            u'Сабина Асадуллаева',
            u'Вероника Битерякова',
            u'Юлия Буянова',
            u'Пелагея Вдовина',
            u'Леонид Викторов',
            u'Фёдор Гнутов',
            u'Илья Гримберг',
            u'Иван Гурьянов',
            u'Артём Денежкин',
            u'Виктор Жилин',
            u'Дмитрий Иванов',
            u'Олег Климов',
            u'Анна Ковалева',
            u'Глеб Ковылин',
            u'Даниил Космынин',
            u'Алина Леоничева',
            u'Ирина Лин',
            u'Олег Мальцев',
            u'Ислам Мунаев',
            u'Александр Наумов',
            u'Георгий Новиков',
            u'Егор Осипов',
            u'Руслан Перепелица',
            u'Михаил Перин',
            u'Егор Подуровский',
            u'Роман Прибылов',
            u'Александр Селехметьев',
            u'Алексей Тихонов',
            u'Алина Филиппова',
            u'Алина Яшина',
        ]
        fieldTaskGenerator = generators.electricity.FieldTaskGenerator()
        fieldTasks = []
        for charges in [['+q', '-q'], ['-q', '-q'], ['+Q', '+Q'], ['-Q', '+Q']]:
            for firstPoint in ['up', 'down']:
                for secondPoint in ['right', 'left']:
                    for letter in ['a', 'l', 'r', 'd']:
                        fieldTasks.append(fieldTaskGenerator(
                            charges=charges,
                            letter=letter,
                            points=[firstPoint, secondPoint],
                        ))

        sumTask = generators.electricity.SumTask()
        sumTasks = []
        for values, angles in [
            ((120, 50), (90, 180)),
            ((50, 120), (0, 90)),
            ((500, 500), (0, 120)),
            ((200, 200), (0, 60)),
            ((24, 7), (90, 180)),
            ((7, 24), (0, 90)),
            ((72, 72), (0, 120)),
            ((250, 250), (0, 60)),
            ((300, 400), (90, 180)),
            ((300, 400), (0, 90)),
        ]:
            for angleLetter in ['\\alpha', '\\varphi']:
                sumTasks.append(sumTask(
                    angleLetter=angleLetter,
                    values=values,
                    angles=angles
                ))
        sumTasks = sumTasks * 2

        variants = generators.electricity.Variants(pupils, 2704, zip(sumTasks, fieldTasks))
        multiplePaper = generators.electricity.MultiplePaper('2019-04-15', classLetter='10')
        filename = os.path.join('school-554', multiplePaper.GetFilename())
        tex = multiplePaper.GetTex(variants.Iterate())
        with open(filename, 'w') as f:
            f.write(tex.encode('utf-8'))




def CreateArgumentsParser():
    fmtClass = {'formatter_class': argparse.ArgumentDefaultsHelpFormatter}
    parser = argparse.ArgumentParser(description='Generate LaTeX-files', **fmtClass)

    loggingGroup = parser.add_argument_group('Logging arguments')
    defaultLogFormat = ' '.join([
        # '%(relativeCreated)d',
        '%(asctime)s.%(msecs)03d',
        '%(name)10s:%(lineno)-3d',
        '%(levelname)-7s',
        '%(message)s',
    ])
    loggingGroup.add_argument('--log-format', help='Logging format', default=defaultLogFormat)
    loggingGroup.add_argument('--log-separator', help='Logging string separator', choices=['space', 'tab'], default='space')
    loggingGroup.add_argument('--verbose', help='Enable debug logging', action='store_true')

    parser.add_argument('--show-manual', '--sm', help='Show manual files', action='store_true')
    parser.add_argument('--task-number', '--tn', help='Process only one task having number')

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
# 