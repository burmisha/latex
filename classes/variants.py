import library.pupils
import library.formatter
import library.picker

import generators

import logging
log = logging.getLogger(__name__)


def pick_classes(base, config):
    if isinstance(config, dict):
        for key, value in config.items():
            log.info(f'Picking {key}, {value} from {config}')
            b = base
            for part in key.split('.'):
                b = getattr(b, part)
            log.info(f'Picking {key}, {value} from {b}')
            for c in pick_classes(b, value):
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


FORCED_NOT_DISTANT = ['2020-12-24 9']


def is_distant_task(task_id):
    if task_id in FORCED_NOT_DISTANT:
        return False
    elif '2020-11-20' <= task_id <= '2021-01-01':  # use test version on distant
        return True
    else:
        return False


def get_all_variants():
    random_tasks = [
        ('2019-04-16 10', {'electricity.kulon_field': ['ForceTask', 'ExchangeTask', 'FieldTaskGenerator', 'SumTask']}),
        ('2019-04-30 10', {'electricity.potential': ['Potential728', 'Potential735', 'Potential737', 'Potential2335', 'Potential1621']}),
        ('2019-05-06 10', {'electricity.cond': ['Rymkevich748', 'Rymkevich750', 'Rymkevich751', 'Rymkevich762', 'Cond1']}),
        ('2019-05-14 10', {'electricity.om': ['Rezistor1_v1', 'Rezistor2', 'Rezistor3', 'Rezistor4']}),
        ('2019-04-19 11', {'quantum': ['Fotons', 'KernelCount', 'RadioFall', 'RadioFall2']}),
        ('2019-04-30 11', {'quantum': ['Quantum1119', 'Quantum1120']}),
        ('2019-11-27 8', {'termodynamics.termo': ['Ch_8_6', 'Ch_8_7', 'Ch_8_10', 'Ch_8_13', 'Ch_8_35']}),
        ('2019-11-25 9А', {'mechanics.zsi_zse': ['Ch_3_1', 'Ch_3_2', 'Ch_3_3', 'Ch_3_24', 'Ch_3_26']}),
        ('2019-12-17 9А', {'mechanics.koleb': ['Nu01', 'Nu02', 'Nu03', 'Nu04', 'Nu05']}),
        ('2019-12-24 9А', {'mechanics.waves': ['Waves00', 'Waves03', 'Waves04', 'Waves05']}),
        ('2020-04-22 9А', {'vishnyakova': ['BK_53_01', 'BK_53_02', 'BK_53_03', 'BK_53_12']}),
        ('2020-01-20 9Л', {'mechanics.koleb': ['Nu01', 'Nu02', 'Nu03', 'Nu04', 'Nu05']}),
        ('2020-04-28 9Л', ['optics.Gendenshteyn_11_11_18', {'vishnyakova': ['BK_52_01', 'BK_52_02', 'BK_52_07']}]),
        ('2019-09-11 11Т', {'magnet': ['ConstMagnet0', 'ConstMagnet1', 'ConstMagnet2', 'ConstMagnet3']}),
        ('2019-11-13 11Т', {'mechanics.waves': ['Waves01', 'Ch1238', 'Ch1240', 'Waves02']}),
        ('2020-03-04 11Т', {'optics': ['Gendenshteyn_11_11_18', 'Vishnyakova_example_11', 'Belolipetsky_5_196']}),
        ('2020-04-29 11Т', [
            'sto.Equations', {'vishnyakova': ['BK_4_01', 'BK_4_03', 'BK_4_06']},  # sto
            {'vishnyakova': ['BK_52_01', 'BK_52_02', 'BK_52_07']}, 'quantum.Fotons',  # atomic-1
            {'vishnyakova': ['BK_53_01', 'BK_53_02', 'BK_53_03', 'BK_53_12']},  # atomic-2
        ]),
        ('2019-09-30 11S', {'magnet': ['Chernoutsan11_01', 'Chernoutsan11_02', 'Chernoutsan11_5']}),
        ('2020-09-10 10', {'mechanics.kinematics': ['Theory_1', 'Vectors_SumAndDiff', 'Chernoutsan_1_2', 'Vectors_SpeedSum']}),
        ('2020-09-10 9', {'mechanics.kinematics': ['Theory_1_simple', 'Chernoutsan_1_2', 'Chernoutsan_1_2_1']}),
        ('2020-11-26 10', {'mechanics.zsi_zse': ['Ch_3_1', 'Ch_3_2', 'Ch_3_3', 'Ch_3_6', 'Ch_3_26', 'Vishnyakova_1_4_6', 'Ch_4_2', 'Ch_4_29', 'Ch_4_45', 'Vishnyakova_1_4_12']}),
        ('2020-12-11 10', {'mechanics.gidro': ['Ch_6_3', 'Ch_6_8', 'Ch_6_10', 'Ch_6_16', 'Ch_6_20']}),
        ('2020-12-24 9', {'mechanics.koleb': ['Nu01', 'Nu02', 'Nu03', 'Nu04', 'Nu05']}),
        ('2021-01-21 9', {'mechanics.koleb': ['Nu01', 'Nu02', 'Nu03', 'Nu04', 'Nu05']}),
        ('2021-01-22 10', {'termodynamics.mkt': [
            'Basic01', 
            'Basic02', 'Basic03', 'Basic04', 
            'Basic05', 'CountNu', 'CountMass', 'CountParticles'
        ]}),
        ('2021-01-29 10', {'termodynamics.mkt': [
            # 'Celsuis',
            'Basic06', 'Basic07', 'Basic08', 'Basic09', 'Basic10', 'Basic11',
        ]}),
        ('2021-03-02 10', {'termodynamics.mkt': [
            'Basic12', 'Basic13', 'GraphPV_1', 'GraphPV_2', 'ZFTSH_10_2_9_kv', 'ZFTSH_10_2_2_kv', 'Polytrope',
        ]}),
        ('2021-03-04 10', {'termodynamics.termo': [
            'YesNo', 'P_from_V_and_U', 'A_on_P_const', 'DeltaU_on_P_const', 'DeltaU_from_DeltaT', 'Q_from_DeltaU', 'Q_from_DeltaU_and_A',
        ]}),
        ('2021-03-05 10', [
            {'termodynamics.mkt': ['Basic12', 'GraphPV_2', 'ZFTSH_10_2_9_kv', 'ZFTSH_10_2_2_kv', 'Polytrope']},
        ]),
        ('2021-03-11 10', {'termodynamics.termo': [
            'Definitions01', 'V_from_P_and_U', 'A_on_P_const', 'A_from_DeltaT', 'DeltaU_on_P_const', 'DeltaU_from_DeltaT', 'Q_from_DeltaU', 'Q_from_DeltaU_and_A',
        ]}),
        ('2021-03-12 10', [
            'termodynamics.cycle.Rectangle', 'termodynamics.termo.DeltaQ_from_states', 'termodynamics.termo.Definitions02',
        ]),
        ('2021-03-16 9', {'electricity.cond': ['Rymkevich748', 'Rymkevich750', 'Rymkevich751', 'Rymkevich762', 'Definitions01', 'Definitions02']}),
        ('2021-03-18 10', ['termodynamics.cycle.Rectangle_T', 'termodynamics.mkt.GraphPV_1', 'termodynamics.termo.YesNo']),
        ('2021-03-23 10', ['termodynamics.cycle.TriangleUp_T', 'termodynamics.vapor.GetPhi', 'termodynamics.mkt.Basic12', 'termodynamics.termo.Definitions02']),
        ('2021-03-23 9', {'quantum': ['Fotons', 'ColorNameFromLambda', 'E_from_nu',  'E_from_lambda', 'T_Nu_from_lambda', 'Deduce01']}),
        # ('2021-03-30 10', {'termodynamics.termo': ['CycleTriangleUp']}),
        ('2021-03-25 10', {'electricity.kulon_field': ['ForceTask', 'ExchangeTask', 'FieldTaskGenerator', 'SumTask']}),
        ('2021-03-26 10', {'termodynamics.vapor': ['GetNFromPhi', 'GetPFromPhi', 'GetPFromM', 'Vapor01']}),
        ('2021-03-30 9', ['optics.Gendenshteyn_11_11_18', 'c_9_5_em_waves.Definitions01', 'c_9_5_em_waves.Deduce01']),
    ]
    for task_id, tasks_classes in random_tasks:
        pupils = library.pupils.get_class_from_string(task_id)
        date = library.formatter.Date(task_id[:10])

        tasks_classes = pick_classes(generators, tasks_classes)

        tasks = [task(pupils=pupils, date=date) for task in tasks_classes]
        if is_distant_task(task_id):  # use test version on distant
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
