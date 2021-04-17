import library.pupils
import library.formatter
import library.picker

from library.gform.node import Choice, Text, TextTask, text_task, abv_choices


import generators

import logging
log = logging.getLogger(__name__)

ms2_re = r'( ?м/[cс]\^?2| м/\([cс]\^?2\))?'


def follow_dots(key, base):
    assert isinstance(key, str)
    b = base
    for part in key.split('.'):
        b = getattr(b, part)
    return b


def pick_classes(base, config):
    if isinstance(config, dict):
        for key, value in config.items():
            for c in pick_classes(follow_dots(key, base), value):
                yield c
    elif isinstance(config, list):
        for cfg in config:
            for c in pick_classes(base, cfg):
                yield c
    elif isinstance(config, str):
        yield follow_dots(config, base)
    else:
        raise RuntimeError(f'Invalid config: {config}')


class Work:
    FORCED_NOT_DISTANT = ['2020-12-24 9']
    def __init__(self, task_id=None, classes=None, human=None, thresholds=None, up_to=None, image=None, questions=None):
        self._task_id = task_id
        self._tasks_classes = pick_classes(generators, classes) if classes else None
        self._pupils = library.pupils.get_class_from_string(task_id)
        self._date = library.formatter.Date(task_id[:10])

        self._human_name = human
        self._thresholds = thresholds

        self._up_to = up_to
        self._image = image
        self._questions = questions

    def is_distant_task(self):
        if self._task_id in self.FORCED_NOT_DISTANT:
            return False
        elif '2020-11-20' <= self._task_id <= '2021-01-01':  # use test version on distant
            return True
        else:
            return False

    def get_tasks(self):
        tasks = [task(pupils=self._pupils, date=self._date) for task in self._tasks_classes]
        if self.is_distant_task():  # use test version on distant
            for task in tasks:
                task.PreferTestVersion()
                task.SolutionSpace = 0
                assert hasattr(task, 'AnswerTestTemplate')
        return tasks


class SimpleTextWork:
    def __init__(self, human=None, thresholds=None, up_to=None, image=None, questions=None, answers=None):
        self._human_name = human
        self._thresholds = thresholds

        self._up_to = up_to
        self._image = image
        self._questions = questions
        self._answers = answers


def get_simple_variants():
    email = lambda desc: Text(f'Электронная почта {desc}'.strip())

    works = [
        SimpleTextWork(
            human='2020.10.22 10АБ - Тест по динамике - 1',
            up_to='8:50',
            questions=Choice(['Верно', 'Неверно', 'Недостаточно данных в условии']) * 4 + text_task * 6 + Text('Сколько задач на уроке сегодня было понятно?'),
            answers=['Неверно', 'Верно', 'Верно', 'Неверно', '([Кк]илограмм.?|кг)', '([Нн]ьютон.?|Н)', f'1.6{ms2_re}', f'16{ms2_re}', f'2{ms2_re}', '6( Н)?'],
            thresholds=[5, 7, 9],
        ),
        SimpleTextWork(
            human='2020.10.22 9М - Тест по динамике - 1',
            up_to='10:50',
            questions=abv_choices * 10 + Text('Сколько задач на уроке сегодня было понятно?'),
            answers=list('ББВВААВААБ'),
            thresholds=[5, 7, 9],
        ),
        SimpleTextWork(
            human='2020.10.27 10АБ - Тест по динамике - 2',
            up_to='10:05', 
            image='incredibles',
            questions=text_task * 7,
            answers=[13, 17, 120, 20, 2, 40, 15],
            thresholds=[3, 4, 5],
        ),
        SimpleTextWork(
            human='2020.10.27 9М - Тест по динамике - 2', 
            up_to='10:50',
            image='incredibles',
            questions=abv_choices * 8 + text_task * 4,
            answers=list('АВАВАББВ') + ['1.5', '24', '5', '50'],
            thresholds=[4, 6, 8],
        ),
        SimpleTextWork(
            human='2020.10.29 10АБ - Тест по динамике - 3',
            up_to='12:05',
            image='insideout',
            questions=abv_choices * 6 + text_task * 11,
            answers=list('ВВАВАБ') + ['400', '1000000', r'0.02( м)?', '500( Н/м)?', r'0.02', r'0.102(75)?', r'0.14', '160', '2[kк].*', '4[kк].*', r'.*\b400\b.*\b75\b.*'], 
            thresholds=[10, 13, 15],
        ),
        SimpleTextWork(
            human='2020.10.30 10АБ - Тест по динамике - 4',
            up_to='10:05',
            image='minions',
            questions=abv_choices * 9 + text_task * 3,
            answers=list('АБАВАВААБ') + [{'25600( к[мл])?': 2, '32000( к[мл])?': 1}, {'6400( км)?': 2}, {'8': 2}],
            thresholds=[6, 8, 10],
        ),
        SimpleTextWork(
            human='2020.11.03 10АБ - Тест по динамике - 5',
            up_to='9:05', 
            image='insideout', 
            questions=email('(только для 10«Б», 10«А» уже присылал)') + abv_choices * 2 + text_task * 5,
            answers=['А', 'В', 12, 240, '0.05', '100 Н?', 5],
            thresholds=[4, 5, 6],
        ),
        SimpleTextWork(
            human='2020.11.03 9М - Тест по динамике - 3',
            up_to='11:05',
            image='insideout', 
            questions=email('') + abv_choices * 10,
            answers=list('БАВАБАБВАВ'),
            thresholds=[5, 7, 9],
        ),
        SimpleTextWork(
            human='2020.11.05 9М - Тест по динамике - 4',
            up_to='10:05',
            image='incredibles',
            questions=abv_choices * 10,
            answers=list('ВБВБААВББА'),
            thresholds=[5, 7, 9],
        ),
        SimpleTextWork(
            human='2020.11.06 10АБ - Тест по динамике - 6',
            up_to='10:05',
            image='up',
            questions=text_task * 8,
            answers=[5, {'-?5': 1, '6.73': 1}, '-?3.(2[67]|3|23|256)', 0, 80, 120, 18, 5],
            thresholds=[3, 5, 7],
        ),
        SimpleTextWork(
            human='2020.11.12 9М - Динамика - 6',
            up_to='10:15', 
            image='zootopia',
            questions=abv_choices * 5 + text_task * 4,
            answers=list('АББВВ') + ['(0.5|1/2)', 2, 120, 2],
            thresholds=[3, 5, 7],
        ),
        SimpleTextWork(
            human='2020.11.13 10АБ - Законы сохранения - 1',
            up_to='10:05', 
            image='zootopia',
            questions=email('(если не присылали на прошлой неделе)') + abv_choices * 6 + text_task * 4,
            answers=list('АБАБВА') + [{8000: 2}, {'12.6': 2}, {10: 2}, {5: 2}],
            thresholds=[4, 8, 11],
        ),
        SimpleTextWork(
            human='2020.11.19 9М - Законы сохранения - 1',
            up_to='10:05', 
            image='up',
            questions=abv_choices * 6 + text_task * 4,
            answers=list('АБАБВА') + [{'2( кг\*м/с)?': 2}, {'2( м/c)?': 2}, {'3( м/с)?': 2}, {'0.1( м/c)?': 2, '1/10': 2}],
            thresholds=[6, 8, 10],
        ),
        SimpleTextWork(
            human='2020.12.04 10АБ - Статика и гидростатика - 1',
            up_to='12:05',
            image='ratatouille',
            questions=text_task * 7 + Text('Ссылка на гифку') + Text('Какой вопрос добавить в опрос?'),
            answers=[{'1/56': 2, 56: 2}, {15: 2, 12: 1}, {8: 2}, {100: 2}, {75: 2, 225: 1}, {5: 2}, {60: 2}],
            thresholds=[6, 8, 10],
        ),
        SimpleTextWork(
            human='2020.12.08 9М - Колебания и волны - 1',
            up_to='11:05', 
            image='ratatouille',
            questions=abv_choices * 8,
            answers=list('ВВАВБАВБ'),
            thresholds=[5, 6, 7],
        ),
        SimpleTextWork(
            human='2020.12.10 9М - Колебания и волны - 2',
            up_to='11:05',
            image='incredibles',
            questions=abv_choices * 8,
            answers=list('ВБВВ') + [{'Б': 1, 'В': 1}] + list('АВА'),
            thresholds=[5, 6, 7],
        ),
        SimpleTextWork(
            human='2020.12.17 9М - Колебания и волны - 3',
            up_to='11:05', 
            image='keanureeves',
            questions=abv_choices * 10,
            answers=list('АВБАВБ') + [{'А': 0, 'Б': 0}] + list('ВАБ'),
            thresholds=[6, 7, 8],
        ),
        SimpleTextWork(
            human='2020.12.22 9М - Колебания и волны - 4',
            up_to='11:05', 
            image='zootopia',
            questions=abv_choices * 10,
        ),
    ]
    for work in works:
        yield work


def get_all_variants():
    works = [
        Work(
            task_id='2019-04-16 10',
            classes={'electricity.kulon_field': ['ForceTask', 'ExchangeTask', 'FieldTaskGenerator', 'SumTask']}
        ),
        Work(
            task_id='2019-04-30 10',
            classes={'electricity.potential': ['A_from_Q_E_l', 'E_from_U_l', 'Potential737', 'v_from_Ev_m', 'Phi_from_static_e']}
        ),
        Work(
            task_id='2019-05-06 10',
            classes={'electricity.cond': ['C_from_U_Q', 'Q_is_possible', 'C_ratio', 'W_from_Q_C', 'Cond1']}
        ),
        Work(
            task_id='2019-05-14 10',
            classes={'electricity.om': ['Rezistor1_v1', 'Rezistor2', 'Rezistor3', 'Rezistor4']}
        ),
        Work(
            task_id='2019-04-19 11',
            classes={'atomic.quantum': ['Fotons', 'KernelCount', 'RadioFall', 'RadioFall2']}
        ),
        Work(
            task_id='2019-04-30 11',
            classes={'atomic.quantum': ['Quantum1119', 'Quantum1120']}
        ),
        Work(
            task_id='2019-11-27 8',
            classes={'termodynamics.termo': ['Ch_8_6', 'Ch_8_7', 'Ch_8_10', 'Ch_8_13', 'Ch_8_35']}
        ),
        Work(
            task_id='2019-11-25 9А',
            classes={'mechanics.zsi_zse': ['Ch_3_1', 'Ch_3_2', 'Ch_3_3', 'Ch_3_24', 'Ch_3_26']}
        ),
        Work(
            task_id='2019-12-17 9А',
            classes={'mechanics.koleb': ['Nu01', 'Nu02', 'Nu03', 'Nu04', 'Nu05']}
        ),
        Work(
            task_id='2019-12-24 9А',
            classes={'mechanics.waves': ['Waves00', 'Waves03', 'Waves04', 'Waves05']}
        ),
        Work(
            task_id='2020-04-22 9А',
            classes={'atomic.radioactive': ['BK_53_01', 'BK_53_02', 'BK_53_03', 'BK_53_12']}
        ),
        Work(
            task_id='2020-01-20 9Л',
            classes={'mechanics.koleb': ['Nu01', 'Nu02', 'Nu03', 'Nu04', 'Nu05']}
        ),
        Work(
            task_id='2020-04-28 9Л',
            classes=['atomic.em_waves.Gendenshteyn_11_11_18', 'atomic.em_waves.Lambda_from_E', 'atomic.em_waves.Lambda_from_E_2', 'atomic.em_waves.H_levels']),
        Work(
            task_id='2019-09-11 11Т',
            classes={'electricity.magnet': ['ConstMagnet0', 'ConstMagnet1', 'ConstMagnet2', 'ConstMagnet3']}
        ),
        Work(
            task_id='2019-11-13 11Т',
            classes={'mechanics.waves': ['Waves01', 'Ch1238', 'Ch1240', 'Waves02']},
        ),
        Work(
            task_id='2020-03-04 11Т',
            classes=[
                'atomic.em_waves.Gendenshteyn_11_11_18',
                {'optics.wave': ['Vishnyakova_example_11', 'Belolipetsky_5_196']}
            ]
        ),
        Work(
            task_id='2020-04-29 11Т',
            classes={'atomic': [
                {'sto': ['Equations', 'E_ratio_from_v_ratio', 'E_P_from_v_ratio', 'beta_from_l_reduction']},
                {'em_waves': ['Lambda_from_E', 'Lambda_from_E_2', 'H_levels']}, 'quantum.Fotons',  # atomic-1
                {'radioactive': ['BK_53_01', 'BK_53_02', 'BK_53_03', 'BK_53_12']},  # atomic-2
            ]}
        ),
        Work(
            task_id='2019-09-30 11S',
            classes={'electricity.magnet': ['Chernoutsan11_01', 'Chernoutsan11_02', 'Chernoutsan11_5']}
        ),
        Work(
            task_id='2020-09-10 10',
            classes={'mechanics.kinematics': ['Theory_1', 'Vectors_SumAndDiff', 'Chernoutsan_1_2', 'Vectors_SpeedSum']}
        ),
        Work(
            task_id='2020-09-10 9',
            classes={'mechanics.kinematics': ['Theory_1_simple', 'Chernoutsan_1_2', 'Chernoutsan_1_2_1']}
        ),
        Work(
            task_id='2020-11-26 10',
            classes={'mechanics.zsi_zse': ['Ch_3_1', 'Ch_3_2', 'Ch_3_3', 'Ch_3_6', 'Ch_3_26', 'Vishnyakova_1_4_6', 'Ch_4_2', 'Ch_4_29', 'Ch_4_45', 'Vishnyakova_1_4_12']},
            human='2020.11.26 10АБ - Законы сохранения - 2',
            thresholds=[4, 6, 8],
            up_to='12:05',
            image='incredibles',
            questions=text_task * 10,
        ),
        Work(
            task_id='2020-12-11 10',
            classes={'mechanics.gidro': ['Ch_6_3', 'Ch_6_8', 'Ch_6_10', 'Ch_6_16', 'Ch_6_20']},
            human='2020.12.11 10АБ - Статика и гидростатика - 2',
            thresholds=[1.5, 2.5, 3.5],
            up_to='11:05',
            image='minions',
            questions=text_task * 5,
        ),
        Work(
            task_id='2020-12-24 9',
            classes={'mechanics.koleb': ['Nu01', 'Nu02', 'Nu03', 'Nu04', 'Nu05']}
        ),
        Work(
            task_id='2021-01-21 9',
            classes={'mechanics.koleb': ['Nu01', 'Nu02', 'Nu03', 'Nu04', 'Nu05']}
        ),
        Work(
            task_id='2021-01-22 10',
            classes={'termodynamics.mkt': [
                'Basic01',
                'Basic02', 'Basic03', 'Basic04',
                'Basic05', 'CountNu', 'CountMass', 'CountParticles'
            ]
        }),
        Work(
            task_id='2021-01-29 10',
            classes={'termodynamics.mkt': [
                # 'Celsuis',
                'Basic06', 'Basic07', 'Basic08', 'Basic09', 'Basic10', 'Basic11',
            ]}
        ),
        Work(
            task_id='2021-03-02 10',
            classes={'termodynamics.mkt': [
                'Basic12', 'Basic13', 'GraphPV_1', 'GraphPV_2', 'ZFTSH_10_2_9_kv', 'ZFTSH_10_2_2_kv', 'Polytrope',
            ]}
        ),
        Work(
            task_id='2021-03-04 10',
            classes={'termodynamics.termo': [
                'YesNo', 'P_from_V_and_U', 'A_on_P_const', 'DeltaU_on_P_const', 'DeltaU_from_DeltaT', 'Q_from_DeltaU', 'Q_from_DeltaU_and_A',
            ],
        }),
        Work(
            task_id='2021-03-05 10',
            classes=[{'termodynamics.mkt': ['Basic12', 'GraphPV_2', 'ZFTSH_10_2_9_kv', 'ZFTSH_10_2_2_kv', 'Polytrope']}],
        ),
        Work(
            task_id='2021-03-11 10',
            classes={'termodynamics.termo': [
                'Definitions01', 'V_from_P_and_U', 'A_on_P_const', 'A_from_DeltaT', 'DeltaU_on_P_const', 'DeltaU_from_DeltaT', 'Q_from_DeltaU', 'Q_from_DeltaU_and_A',
            ]},
        ),
        Work(
            task_id='2021-03-12 10',
            classes=['termodynamics.cycle.Rectangle', 'termodynamics.termo.DeltaQ_from_states', 'termodynamics.termo.Definitions02',
        ]),
        Work(
            task_id='2021-03-16 9',
            classes={'electricity.cond': ['C_from_U_Q', 'Q_is_possible', 'C_ratio', 'W_from_Q_C', 'Definitions01', 'Definitions02']}
        ),
        Work(
            task_id='2021-03-18 10',
            classes=['termodynamics.cycle.Rectangle_T', 'termodynamics.mkt.GraphPV_1', 'termodynamics.termo.YesNo']),
        Work(
            task_id='2021-03-20 10',
            classes=['termodynamics.cycle.TriangleUp_T', 'termodynamics.cycle.TriangleUp']),
        Work(
            task_id='2021-03-23 10',
            classes=['termodynamics.cycle.TriangleUp_T', 'termodynamics.vapor.GetPhi', 'termodynamics.mkt.Basic12', 'termodynamics.termo.Definitions02']),
        Work(
            task_id='2021-03-23 9',
            classes={'atomic.quantum': ['Fotons', 'ColorNameFromLambda', 'E_from_nu',  'E_from_lambda', 'T_Nu_from_lambda', 'Deduce01']}
        ),
        Work(
            task_id='2021-03-25 10',
            classes={'electricity.kulon_field': ['ForceTask', 'ExchangeTask', 'FieldTaskGenerator', 'SumTask']}
        ),
        Work(
            task_id='2021-03-26 10',
            classes={'termodynamics.vapor': ['GetNFromPhi', 'GetPFromPhi', 'GetPFromM', 'Vapor01']},
        ),
        Work(
            task_id='2021-03-30 10',
            classes={'electricity': [
                'kulon_field.ExchangeTask', 'kulon_field.FieldTaskGenerator',
                'potential.E_from_U_l', 'potential.A_from_Q_E_l',
                'kulon_field.Definitions01',
            ]}
        ),
        Work(
            task_id='2021-03-30 9',
            classes={'atomic.em_waves': ['Gendenshteyn_11_11_18', 'Definitions01', 'Deduce01', 'Sound_to_value', 'Prefix']}
        ),
        Work(
            task_id='2021-04-01 9',
            classes={'atomic.em_waves': ['Lambda_from_E', 'Lambda_from_E_2', 'H_levels']}
        ),
        Work(
            task_id='2021-04-02 10',
            classes={'electricity.potential': ['Phi_from_static_e', 'A_from_motion', 'E_phi_graphs', 'Definitions01']}
        ),
        Work(
            task_id='2021-04-15 10',
            classes={'electricity.cond': ['Definitions03', 'Definitions04', 'Q_is_possible', 'Q_from_DeltaU_C', 'C_from_U_Q', 'C_ratio', 'W_from_Q_C']},
            human='2021.04.15 10АБ - Электростатика - 1',
            thresholds=[2, 4, 6],
            up_to='9:02',
            image='zootopia',
            questions=text_task * 7
        ),
        Work(
            task_id='2021-04-16 9',
            classes={'atomic.radioactive': ['Definitions01', 'Definitions02', 'Definitions03', 'Definitions04', 'Definitions05', 'Definitions06', 'Definitions07']},
            human='2021.04.16 9М - Строение атома - 1',
            thresholds=[4, 5, 6],
            questions=text_task * 7,
            up_to='11:02',
            image='zootopia',
        ),
    ]
    for work in works:
        yield work


def get_variant(key):
    key_picker = library.picker.KeyPicker(key=library.picker.letters_key)
    for work in get_all_variants():
        if work._tasks_classes:
            key_picker.add(f'{work._date.GetFilenameText()} {work._pupils.Grade}', work.get_tasks())

    return key_picker.get(key)
