import library.pupils
import library.formatter
import library.picker

import generators

import logging
log = logging.getLogger(__name__)


def pick_classes(base, config):
    if isinstance(config, dict):
        for key, value in config.items():
            for c in pick_classes(getattr(base, key), value):
                yield c
    elif isinstance(config, list):
        for cfg in config:
            for c in pick_classes(base, cfg):
                yield c
    elif isinstance(config, str):
        c = base
        for part in config.split('.'):
            c = getattr(c, part)
        yield c
    else:
        raise RuntimeError(f'Invalid config: {config}')


def get_all_variants(only_me=False):
    random_tasks = [
        ('2019-04-16 10', {'electricity': ['ForceTask', 'ExchangeTask', 'FieldTaskGenerator', 'SumTask']}),
        ('2019-04-30 10', {'electricity': ['Potential728', 'Potential735', 'Potential737', 'Potential2335', 'Potential1621']}),
        ('2019-05-06 10', {'electricity': ['Rymkevich748', 'Rymkevich750', 'Rymkevich751', 'Rymkevich762', 'Cond1']}),
        ('2019-05-14 10', {'electricity': ['Rezistor1_v1', 'Rezistor2', 'Rezistor3', 'Rezistor4']}),
        ('2019-04-19 11', {'quantum': ['Fotons', 'KernelCount', 'RadioFall', 'RadioFall2']}),
        ('2019-04-30 11', {'quantum': ['Quantum1119', 'Quantum1120']}),
        ('2019-11-27 8', {'termo': ['Ch_8_6', 'Ch_8_7', 'Ch_8_10', 'Ch_8_13', 'Ch_8_35']}),
        ('2019-11-25 9А', {'zsi_zse': ['Ch_3_1', 'Ch_3_2', 'Ch_3_3', 'Ch_3_24', 'Ch_3_26']}),
        ('2019-12-17 9А', {'koleb': ['Nu01', 'Nu02', 'Nu03', 'Nu04', 'Nu05']}),
        ('2019-12-24 9А', {'waves': ['Waves00', 'Waves03', 'Waves04', 'Waves05']}),
        ('2020-04-22 9А', {'vishnyakova': ['BK_53_01', 'BK_53_02', 'BK_53_03', 'BK_53_12']}),
        ('2020-01-20 9Л', {'koleb': ['Nu01', 'Nu02', 'Nu03', 'Nu04', 'Nu05']}),
        ('2020-04-28 9Л', ['optics.Gendenshteyn_11_11_18', {'vishnyakova': ['BK_52_01', 'BK_52_02', 'BK_52_07']}]),
        ('2019-09-11 11Т', {'magnet': ['ConstMagnet0', 'ConstMagnet1', 'ConstMagnet2', 'ConstMagnet3']}),
        ('2019-11-13 11Т', {'waves': ['Waves01', 'Ch1238', 'Ch1240', 'Waves02']}),
        ('2020-03-04 11Т', {'optics': ['Gendenshteyn_11_11_18', 'Vishnyakova_example_11', 'Belolipetsky_5_196']}),
        ('2020-04-29 11Т', [
            'sto.Equations', {'vishnyakova': ['BK_4_01', 'BK_4_03', 'BK_4_06']},  # sto
            {'vishnyakova': ['BK_52_01', 'BK_52_02', 'BK_52_07']}, 'quantum.Fotons',  # atomic-1
            {'vishnyakova': ['BK_53_01', 'BK_53_02', 'BK_53_03', 'BK_53_12']},  # atomic-2
        ]),
        ('2019-09-30 11S', {'magnet': ['Chernoutsan11_01', 'Chernoutsan11_02', 'Chernoutsan11_5']}),
        ('2020-09-10 10', {'kinematics': ['Theory_1', 'Vectors_SumAndDiff', 'Chernoutsan_1_2', 'Vectors_SpeedSum']}),
        ('2020-09-10 9', {'kinematics': ['Theory_1_simple', 'Chernoutsan_1_2', 'Chernoutsan_1_2_1']}),
        ('2020-11-26 10', {'zsi_zse': ['Ch_3_1', 'Ch_3_2', 'Ch_3_3', 'Ch_3_6', 'Ch_3_26', 'Vishnyakova_1_4_6', 'Ch_4_2', 'Ch_4_29', 'Ch_4_45', 'Vishnyakova_1_4_12']}),
        ('2020-12-11 10', {'gidro': ['Ch_6_3', 'Ch_6_8', 'Ch_6_10', 'Ch_6_16', 'Ch_6_20']}),
    ]
    for task_id, tasks_classes in random_tasks:
        pupils = library.pupils.get_class_from_string(task_id, addMyself=True, onlyMe=only_me)
        date = library.formatter.Date(task_id[:10])

        tasks_classes = pick_classes(generators, tasks_classes)

        tasks = [task(pupils=pupils, date=date) for task in tasks_classes]
        if '2020-11-20' <= task_id <= '2021-07-01':  # use test version on distant
            for task in tasks:
                task.PreferTestVersion()
                task.SolutionSpace = 0
                assert hasattr(task, 'AnswerTestTemplate')

        yield pupils, date, tasks


def get_variant(key):
    key_picker = library.picker.KeyPicker(key=library.picker.letters_key)
    for pupils, date, tasks in get_all_variants():
        key_picker.add(f'{date.GetFilenameText()} {pupils.Grade}', tasks)

    return key_picker.get(key)
