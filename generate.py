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


def runLucky(args):
    library.lucky.getLucky(grade=args.grade, count=args.count)


def runTripod(args):
    fileWriter = library.files.FileWriter()    
    tripodFormat = args.format
    getText, extension = {
        'tex': (lambda r: r.GetTex(), 'tex'),
        'txt': (lambda r: r.GetText(), 'txt'),
    }[tripodFormat]
    for className, report in library.tripod.getTripodReports():
        fileWriter.Write(os.path.join('school-554', 'tripod'), className + '-tripod.%s' % extension, text=getText(report))


def runDownload(args):
    for downloader in [
        # library.download.MathusPhys(),
        library.download.ZnakKachestava(),
    ]:
        downloader.Download(os.path.join(args.root, downloader.GetDirname()))



def runGenerate(args):
    fileWriter = library.files.FileWriter(args.filter)

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
            problems.cheshev.Cheshev(),
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
            classes.class1911.Class1911(),
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
                '2019-05-06': [
                    generators.electricity.Rymkevich748(),
                    generators.electricity.Rymkevich750(),
                    generators.electricity.Rymkevich751(),
                    generators.electricity.Rymkevich762(),
                    generators.electricity.Cond1(),
                ],
                '2019-05-14': [
                    generators.electricity.Rezistor1(),
                    generators.electricity.Rezistor2(),
                    generators.electricity.Rezistor3(),
                    generators.electricity.Rezistor4(),
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
            'class-2019-8': {
                '2019-11-27': [
                    generators.termo.Ch_8_6(),
                    generators.termo.Ch_8_7(),
                    generators.termo.Ch_8_10(),
                    generators.termo.Ch_8_13(),
                    generators.termo.Ch_8_35(),
                ],
            },
            'class-2019-9': {
                '2019-11-25': [
                    generators.mechanics.Ch_3_1(),
                    generators.mechanics.Ch_3_2(),
                    generators.mechanics.Ch_3_3(),
                    generators.mechanics.Ch_3_24(),
                    generators.mechanics.Ch_3_26(),
                ],
                '2019-12-17': [
                    generators.koleb.Nu01(),
                    generators.koleb.Nu02(),
                    generators.koleb.Nu03(),
                    generators.koleb.Nu04(),
                    generators.koleb.Nu05(),
                ],
                '2019-12-24': [
                    generators.waves.Waves00(),
                    generators.waves.Waves03(),
                    generators.waves.Waves04(),
                    generators.waves.Waves05(),
                ],
            },
            'class-2019-9L': {
                '2020-01-20': [
                    generators.koleb.Nu01(),
                    generators.koleb.Nu02(),
                    generators.koleb.Nu03(),
                    generators.koleb.Nu04(),
                    generators.koleb.Nu05(),
                ],
            },
            'class-2019-11': {
                '2019-09-11': [
                    generators.magnet.ConstMagnet0(),
                    generators.magnet.ConstMagnet1(),
                    generators.magnet.ConstMagnet2(),
                    generators.magnet.ConstMagnet3(),
                ],
                '2019-11-13': [
                    generators.waves.Waves01(),
                    generators.waves.Ch1238(),
                    generators.waves.Ch1240(),
                    generators.waves.Waves02(),
                ],
            },
            'class-2019-11S': {
                '2019-09-30': [
                    generators.magnet.Chernoutsan11_01(),
                    generators.magnet.Chernoutsan11_02(),
                    generators.magnet.Chernoutsan11_5(),
                ],
            },
        }
        for className, dateTasks in classRandomTasks.iteritems():
            pupils = library.pupils.getPupils(className, addMyself=True, onlyMe=args.me)
            pupilsList = list(pupils.Iterate())
            for date, taskGenerators in dateTasks.iteritems():
                multiplePaper = generators.variant.MultiplePaper(date, classLetter=pupils.Grade)
                if fileWriter.NotMatches(multiplePaper.GetFilename()):
                    continue
                tasksLists = [taskGenerator.Shuffle(seed, minCount=len(pupilsList)) for taskGenerator in taskGenerators]
                variants = generators.variant.Variants(pupilsList, zip(*tasksLists))
                fileWriter.Write(
                    'school-554',
                    multiplePaper.GetFilename(),
                    text=multiplePaper.GetTex(variants.Iterate(), withAnswers=args.answers),
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

    subparsers = parser.add_subparsers()

    generateParser = subparsers.add_parser('generate', help='Generate all papers')
    generateParser.add_argument('--show-manual', '--sm', help='Show manual files', action='store_true')
    generateParser.add_argument('--filter', help='Process only files matchin filter')
    generateParser.add_argument('--me', help='Use only me mode', action='store_true')
    generateParser.add_argument('--answers', help='save answers', action='store_true')
    generateParser.set_defaults(func=runGenerate)

    luckyParser = subparsers.add_parser('lucky', help='Find lucky pupils')
    luckyParser.add_argument('-g', '--grade', help='Grade', type=int, choices=[8, 9])
    luckyParser.add_argument('-c', '--count', help='Count', type=int)
    luckyParser.set_defaults(func=runLucky)

    tripodParser = subparsers.add_parser('tripod', help='Generate tripod results')
    tripodParser.add_argument('--format', help='Format', choices=['tex', 'txt'])
    tripodParser.set_defaults(func=runTripod)

    downloadParser = subparsers.add_parser('download', help='Download extra files')
    downloadParser.add_argument('--root', help='Location to save', default=u'/Users/burmisha/Yandex.Disk.localized/УДР/Общие материалы физиков УДР')
    downloadParser.set_defaults(func=runDownload)

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
