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

    random_tasks = [
        ('2019-04-16 10', ('electricity', ['ForceTask', 'ExchangeTask', 'FieldTaskGenerator', 'SumTask'])),
        ('2019-04-30 10', ('electricity', ['Potential728', 'Potential735', 'Potential737', 'Potential2335', 'Potential1621'])),
        ('2019-05-06 10', ('electricity', ['Rymkevich748', 'Rymkevich750', 'Rymkevich751', 'Rymkevich762', 'Cond1'])),
        ('2019-05-14 10', ('electricity', ['Rezistor1_v1', 'Rezistor2', 'Rezistor3', 'Rezistor4'])),
        ('2019-04-19 11',  ('quantum', ['Fotons', 'KernelCount', 'RadioFall', 'RadioFall2'])),
        ('2019-04-30 11',  ('quantum', ['Quantum1119', 'Quantum1120'])),
        ('2019-11-27 8',   ('termo', ['Ch_8_6', 'Ch_8_7', 'Ch_8_10', 'Ch_8_13', 'Ch_8_35'])),
        ('2019-11-25 9-А', ('mechanics', ['Ch_3_1', 'Ch_3_2', 'Ch_3_3', 'Ch_3_24', 'Ch_3_26'])),
        ('2019-12-17 9-А', ('koleb', ['Nu01', 'Nu02', 'Nu03', 'Nu04', 'Nu05'])),
        ('2019-12-24 9-А', ('waves', ['Waves00', 'Waves03', 'Waves04', 'Waves05'])),
        ('2020-04-22 9-А', ('vishnyakova', ['BK_53_01', 'BK_53_02', 'BK_53_03', 'BK_53_12'])),
        ('2020-01-20 9-Л', ('koleb', ['Nu01', 'Nu02', 'Nu03', 'Nu04', 'Nu05'])),
        ('2020-04-28 9-Л', ['optics.Gendenshteyn_11_11_18', 'vishnyakova.BK_52_01', 'vishnyakova.BK_52_02', 'vishnyakova.BK_52_07']),
        ('2019-09-11 11-Т', ('magnet', ['ConstMagnet0', 'ConstMagnet1', 'ConstMagnet2', 'ConstMagnet3'])),
        ('2019-11-13 11-Т', ('waves', ['Waves01', 'Ch1238', 'Ch1240', 'Waves02'])),
        ('2020-03-04 11-Т', ('optics', ['Gendenshteyn_11_11_18', 'Vishnyakova_example_11', 'Belolipetsky_5_196'])),
        ('2020-04-29 11-Т', [
            'sto.Equations', 'vishnyakova.BK_4_01', 'vishnyakova.BK_4_03', 'vishnyakova.BK_4_06',  # sto
            'vishnyakova.BK_52_01', 'vishnyakova.BK_52_02', 'vishnyakova.BK_52_07', 'quantum.Fotons',  # atomic-1
            'vishnyakova.BK_53_01', 'vishnyakova.BK_53_02', 'vishnyakova.BK_53_03', 'vishnyakova.BK_53_12',  # atomic-2
        ]),
        ('2019-09-30 11S', ('magnet', ['Chernoutsan11_01', 'Chernoutsan11_02', 'Chernoutsan11_5'])),
        ('2020-09-10 10', ('mechanics', ['Theory_1', 'Vectors_SumAndDiff', 'Chernoutsan_1_2', 'Vectors_SpeedSum'])),
        ('2020-09-10 9', ('mechanics', ['Theory_1_simple', 'Chernoutsan_1_2', 'Chernoutsan_1_2_1'])),
    ]
    if generateMultiple:
        for task_id, tasks_classes in random_tasks:
            pupils = library.pupils.get_class_from_string(task_id, addMyself=True, onlyMe=args.me)
            date = library.formatter.Date(task_id[:10])

            tasks = []
            if isinstance(tasks_classes, list):
                for task_cfg in tasks_classes:
                    task = generators
                    for part in task_cfg.split('.'):
                        task = getattr(task, part)
                    tasks.append(task)
            elif isinstance(tasks_classes, tuple):
                module = tasks_classes[0]
                for task_cfg in tasks_classes[1]:
                    tasks.append(getattr(getattr(generators, module), task_cfg))
            else:
                raise
            variants = generators.variant.Variants(pupils=pupils, date=date, tasks=[t() for t in tasks])
            multiplePaper = generators.variant.MultiplePaper(date=date, pupils=pupils)

            filename = multiplePaper.GetFilename()
            if fileWriter.NotMatches(filename):
                log.info('Skipping %s', filename)
                continue
            fileWriter.Write(
                'school-554',
                filename,
                text=multiplePaper.GetTex(variants=variants, withAnswers=args.answers),
            )

        if args.show_manual:
            fileWriter.ShowManual(extensions=['tex'])


def populate_parser(parser):
    parser.add_argument('--show-manual', '--sm', help='Show manual files', action='store_true')
    parser.add_argument('--filter', help='Process only files matchin filter')
    parser.add_argument('--me', help='Use only me mode', action='store_true')
    parser.add_argument('--answers', help='save answers', action='store_true')
    parser.set_defaults(func=run)
