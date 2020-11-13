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
            problems.gendenshteyn11.Gendenshteyn11(),
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
            '2018-10': {
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
                    generators.electricity.Rezistor1_v1(),
                    generators.electricity.Rezistor2(),
                    generators.electricity.Rezistor3(),
                    generators.electricity.Rezistor4(),
                ],
            },
            '2018-11': {
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
            '2019-8': {
                '2019-11-27': [
                    generators.termo.Ch_8_6(),
                    generators.termo.Ch_8_7(),
                    generators.termo.Ch_8_10(),
                    generators.termo.Ch_8_13(),
                    generators.termo.Ch_8_35(),
                ],
            },
            '2019-9-А': {
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
                '2020-04-22': [
                    generators.vishnyakova.BK_53_01(),
                    generators.vishnyakova.BK_53_02(),
                    generators.vishnyakova.BK_53_03(),
                    generators.vishnyakova.BK_53_12(),
                ],
            },
            '2019-9-Л': {
                '2020-01-20': [
                    generators.koleb.Nu01(),
                    generators.koleb.Nu02(),
                    generators.koleb.Nu03(),
                    generators.koleb.Nu04(),
                    generators.koleb.Nu05(),
                ],
                '2020-04-28': [
                    generators.optics.Gendenshteyn_11_11_18(),
                    generators.vishnyakova.BK_52_01(),
                    generators.vishnyakova.BK_52_02(),
                    generators.vishnyakova.BK_52_07(),
                ],
            },
            '2019-11-Т': {
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
                '2020-03-04': [
                    generators.optics.Gendenshteyn_11_11_18(),
                    generators.optics.Vishnyakova_example_11(),
                    generators.optics.Belolipetsky_5_196(),
                ],
                '2020-04-29': [
                    # sto
                    generators.sto.Equations(),
                    generators.vishnyakova.BK_4_01(),
                    generators.vishnyakova.BK_4_03(),
                    generators.vishnyakova.BK_4_06(),
                    # atomic-1
                    generators.vishnyakova.BK_52_01(),
                    generators.vishnyakova.BK_52_02(),
                    generators.vishnyakova.BK_52_07(),
                    generators.quantum.Fotons(),
                    # atomic-2
                    generators.vishnyakova.BK_53_01(),
                    generators.vishnyakova.BK_53_02(),
                    generators.vishnyakova.BK_53_03(),
                    generators.vishnyakova.BK_53_12(),

                ],
            },
            '2019-11S': {
                '2019-09-30': [
                    generators.magnet.Chernoutsan11_01(),
                    generators.magnet.Chernoutsan11_02(),
                    generators.magnet.Chernoutsan11_5(),
                ],
            },
            '2020-10': {
                '2020-09-10': [
                    generators.mechanics.Theory_1(),
                    generators.mechanics.Vectors_SumAndDiff(),
                    generators.mechanics.Chernoutsan_1_2(),
                    generators.mechanics.Vectors_SpeedSum(),
                ],
            },
            '2020-9': {
                '2020-09-10': [
                    generators.mechanics.Theory_1_simple(),
                    generators.mechanics.Chernoutsan_1_2(),
                    generators.mechanics.Chernoutsan_1_2_1(),
                ],
            },
        }
        for className, dateTasks in classRandomTasks.items():
            pupils = library.pupils.getPupils(className, addMyself=True, onlyMe=args.me)
            for date, variantTasks in dateTasks.items():
                multiplePaper = generators.variant.MultiplePaper(date, pupils=pupils)
                filename = multiplePaper.GetFilename()
                if fileWriter.NotMatches(filename):
                    log.info('Skipping %s', filename)
                    continue
                fileWriter.Write(
                    'school-554',
                    filename,
                    text=multiplePaper.GetTex(
                        variants=generators.variant.Variants(variantTasks, date=date, pupils=pupils),
                        withAnswers=args.answers,
                    ),
                )

        if args.show_manual:
            fileWriter.ShowManual(extensions=['tex'])


def populate_parser(parser):
    parser.add_argument('--show-manual', '--sm', help='Show manual files', action='store_true')
    parser.add_argument('--filter', help='Process only files matchin filter')
    parser.add_argument('--me', help='Use only me mode', action='store_true')
    parser.add_argument('--answers', help='save answers', action='store_true')
    parser.set_defaults(func=run)
