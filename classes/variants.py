import library.pupils
import library.formatter
import library.picker
import library.check

from library.gform.node import Choice, Text, TextTask, text_task, abv_choices
from library.gform.generator import Generator

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

    def __init__(
        self,
        task_id=None,
        classes=None,
        thresholds=None,
        up_to=None,
        image=None,
        questions=None,
        answers=None,
    ):
        self._task_id = task_id
        self._tasks_classes = list(pick_classes(generators, classes)) if classes else None
        self._pupils = library.pupils.get_class_from_string(task_id)
        self._date = library.formatter.Date(task_id.split()[0])

        self._thresholds = thresholds

        self._up_to = up_to
        self._image = image
        self._questions = questions
        self._answers = answers

        if self.has_gform:
            assert self.get_human_name(), f'No human_name for task {self._task_id}'
            assert self._questions, f'No questions for task {self._task_id}'
            assert self._up_to, f'No up_to for task {self._task_id}'
            if self._questions and self._tasks_classes:
                q_count = sum(1 for q in self._questions if isinstance(q, (Choice, TextTask)))
                assert q_count == len(self._tasks_classes), f'Broken answers count for {self._task_id}: {q_count} vs {len(self._tasks_classes)}, {self._tasks_classes}'

    def _is_distant_task(self):
        if self._task_id in self.FORCED_NOT_DISTANT:
            return False
        elif '2020-11-20' <= self._task_id <= '2021-01-01':  # use test version on distant
            return True
        else:
            return False

    def get_tasks(self):
        if not self._tasks_classes:
            return None

        tasks = [task(pupils=self._pupils, date=self._date) for task in self._tasks_classes]
        if self._is_distant_task():  # use test version on distant
            for task in tasks:
                task.PreferTestVersion()
                task.SolutionSpace = 0
                assert hasattr(task, 'AnswerTestTemplate')
        for task in tasks:
            task.validate()
        return tasks

    def get_human_name(self):
        res = ' '.join(
            [
                f'{self._date:dots}',
                f'{self._pupils.Grade}{self._pupils.Letter}',
            ] + self._task_id.split()[2:]
        )
        return res

    def get_checker(self):
        if self._up_to is None:
            return None
        elif self._tasks_classes:
            answers = self.get_tasks()
        elif self._answers:
            answers = self._answers
        else:
            return None

        checker = library.check.checker.Checker(
            self.get_human_name(),
            answers,
            self._thresholds
        )
        return checker

    @property
    def has_gform(self):
        return self._up_to is not None

    def get_gform(self):
        if not self.has_gform:
            return None
        form_generator = Generator(title=self.get_human_name(), questions=self._questions)
        return form_generator.Generate(up_to=self._up_to, image=self._image)


def get_all_variants():
    email = lambda desc: Text(f'Электронная почта {desc}'.strip())

    works = [
        Work(
            task_id='2019-04-16 10',
            classes={'electricity.kulon_field': ['ForceTask', 'ExchangeTask', 'FieldTaskGenerator', 'SumTask']},
        ),
        Work(
            task_id='2019-04-19 11',
            classes={'atomic': ['quantum.Fotons', 'nuclear.KernelCount', 'nuclear.RadioFall', 'quantum.RadioFall2']},
        ),
        Work(
            task_id='2019-04-30 10',
            classes={'electricity.potential': ['A_from_Q_E_l', 'E_from_U_l', 'Potential737', 'v_from_Ev_m', 'Phi_from_static_e']},
        ),
        Work(
            task_id='2019-04-30 11',
            classes={'atomic.quantum': ['Quantum1119', 'Quantum1120']},
        ),
        Work(
            task_id='2019-05-06 10',
            classes={'electricity.cond': ['C_from_U_Q', 'Q_is_possible', 'C_ratio', 'W_from_Q_C', 'Cond_posled']},
        ),
        Work(
            task_id='2019-05-14 10',
            classes={'electricity': [
                'om.P_from_R_U',
                'om.P_from_R_I',
                'full_circuit.Om_eta_full',
                'full_circuit.r_eta_from_Rs',
                'kirchgoff.Kirchgof_double',
            ]},
        ),
        Work(
            task_id='2019-09-11 11Т',
            classes={'magnet.magnet': ['ConstMagnet0', 'ConstMagnet1', 'ConstMagnet2', 'ConstMagnet3']},
        ),
        Work(
            task_id='2019-09-30 11S',
            classes={'magnet.ampere': ['Chernoutsan11_01', 'Chernoutsan11_02', 'Chernoutsan11_5']},
        ),
        Work(
            task_id='2019-11-13 11Т',
            classes={'mechanics.waves': ['Waves01', 'Ch1238', 'Ch1240', 'Waves02']},
        ),
        Work(
            task_id='2019-11-25 9А',
            classes={'mechanics.zsi_zse': ['Ch_3_1', 'Ch_3_2', 'Ch_3_3', 'Ch_3_24', 'Ch_3_26']},
        ),
        Work(
            task_id='2019-11-27 8',
            classes={'termodynamics.termo': ['Ch_8_6', 'Ch_8_7', 'Ch_8_10', 'Ch_8_13', 'Ch_8_35']},
        ),
        Work(
            task_id='2019-12-17 9А',
            classes={'mechanics.koleb': ['Nu01', 'Nu02', 'Nu03', 'Nu04', 'Nu05']},
        ),
        Work(
            task_id='2019-12-24 9А',
            classes={'mechanics.waves': ['Waves00', 'Waves03', 'Waves04', 'Waves05']},
        ),
        Work(
            task_id='2020-01-20 9Л',
            classes={'mechanics.koleb': ['Nu01', 'Nu02', 'Nu03', 'Nu04', 'Nu05']},
        ),
        Work(
            task_id='2020-03-04 11Т',
            classes=['atomic.em_waves.Gendenshteyn_11_11_18', {'optics.wave': ['Vishnyakova_example_11', 'Belolipetsky_5_196']}]
        ),
        Work(
            task_id='2020-04-22 9А',
            classes={'atomic.radioactive': ['BK_53_01', 'BK_53_02', 'BK_53_03', 'BK_53_12']},
        ),
        Work(
            task_id='2020-04-28 9Л',
            classes={'atomic': ['em_waves.Gendenshteyn_11_11_18', 'em_waves.Lambda_from_E', 'em_waves.Lambda_from_E_2', 'em_waves.H_levels']},
        ),
        Work(
            task_id='2020-04-29 11Т',
            classes={'atomic': [
                {'sto': ['Equations', 'E_ratio_from_v_ratio', 'E_P_from_v_ratio', 'beta_from_l_reduction']},
                {'em_waves': ['Lambda_from_E', 'Lambda_from_E_2', 'H_levels']}, 'quantum.Fotons',
                {'radioactive': ['BK_53_01', 'BK_53_02', 'BK_53_03', 'BK_53_12']}
            ]},
        ),
        Work(
            task_id='2020-09-10 10',
            classes={'mechanics.kinematics': ['Theory_1', 'Vectors_SumAndDiff', 'Chernoutsan_1_2', 'Vectors_SpeedSum']},
        ),
        Work(
            task_id='2020-09-10 9',
            classes={'mechanics.kinematics': ['Theory_1_simple', 'Chernoutsan_1_2', 'Chernoutsan_1_2_1']},
        ),
        Work(
            task_id='2020-10-22 10АБ - Тест по динамике - 1',
            up_to='8:50',
            questions=Choice(['Верно', 'Неверно', 'Недостаточно данных в условии']) * 4 + text_task * 6 + Text('Сколько задач на уроке сегодня было понятно?'),
            answers=['Неверно', 'Верно', 'Верно', 'Неверно', '([Кк]илограмм.?|кг)', '([Нн]ьютон.?|Н)', f'1.6{ms2_re}', f'16{ms2_re}', f'2{ms2_re}', '6( Н)?'],
            thresholds=[5, 7, 9],
        ),
        Work(
            task_id='2020-10-22 9М - Тест по динамике - 1',
            up_to='10:50',
            questions=abv_choices * 10 + Text('Сколько задач на уроке сегодня было понятно?'),
            answers=list('ББВВААВААБ'),
            thresholds=[5, 7, 9],
        ),
        Work(
            task_id='2020-10-27 10АБ - Тест по динамике - 2',
            up_to='10:05',
            image='incredibles',
            questions=text_task * 7,
            answers=[13, 17, 120, 20, 2, 40, 15],
            thresholds=[3, 4, 5],
        ),
        Work(
            task_id='2020-10-27 9М - Тест по динамике - 2',
            up_to='10:50',
            image='incredibles',
            questions=abv_choices * 8 + text_task * 4,
            answers=list('АВАВАББВ') + ['1.5', '24', '5', '50'],
            thresholds=[4, 6, 8],
        ),
        Work(
            task_id='2020-10-29 10АБ - Тест по динамике - 3',
            up_to='12:05',
            image='insideout',
            questions=abv_choices * 6 + text_task * 11,
            answers=list('ВВАВАБ') + ['400', '1000000', r'0.02( м)?', '500( Н/м)?', r'0.02', r'0.102(75)?', r'0.14', '160', '2[kк].*', '4[kк].*', r'.*\b400\b.*\b75\b.*'],
            thresholds=[10, 13, 15],
        ),
        Work(
            task_id='2020-10-30 10АБ - Тест по динамике - 4',
            up_to='10:05',
            image='minions',
            questions=abv_choices * 9 + text_task * 3,
            answers=list('АБАВАВААБ') + [{'25600( к[мл])?': 2, '32000( к[мл])?': 1}, {'6400( км)?': 2}, {'8': 2}],
            thresholds=[6, 8, 10],
        ),
        Work(
            task_id='2020-11-03 10АБ - Тест по динамике - 5',
            up_to='9:05',
            image='insideout',
            questions=email('(только для 10«Б», 10«А» уже присылал)') + abv_choices * 2 + text_task * 5,
            answers=['А', 'В', 12, 240, '0.05', '100 Н?', 5],
            thresholds=[4, 5, 6],
        ),
        Work(
            task_id='2020-11-03 9М - Тест по динамике - 3',
            up_to='11:05',
            image='insideout',
            questions=email('') + abv_choices * 10,
            answers=list('БАВАБАБВАВ'),
            thresholds=[5, 7, 9],
        ),
        Work(
            task_id='2020-11-05 9М - Тест по динамике - 4',
            up_to='10:05',
            image='incredibles',
            questions=abv_choices * 10,
            answers=list('ВБВБААВББА'),
            thresholds=[5, 7, 9],
        ),
        Work(
            task_id='2020-11-06 10АБ - Тест по динамике - 6',
            up_to='10:05',
            image='up',
            questions=text_task * 8,
            answers=[5, {'-?5': 1, '6.73': 1}, '-?3.(2[67]|3|23|256)', 0, 80, 120, 18, 5],
            thresholds=[3, 5, 7],
        ),
        Work(
            task_id='2020-11-12 9М - Динамика - 6',
            up_to='10:15',
            image='zootopia',
            questions=abv_choices * 5 + text_task * 4,
            answers=list('АББВВ') + ['(0.5|1/2)', 2, 120, 2],
            thresholds=[3, 5, 7],
        ),
        Work(
            task_id='2020-11-13 10АБ - Законы сохранения - 1',
            up_to='10:05',
            image='zootopia',
            questions=email('(если не присылали на прошлой неделе)') + abv_choices * 6 + text_task * 4,
            answers=list('АБАБВА') + [{8000: 2}, {'12.6': 2}, {10: 2}, {5: 2}],
            thresholds=[4, 8, 11],
        ),
        Work(
            task_id='2020-11-19 9М - Законы сохранения - 1',
            up_to='10:05',
            image='up',
            questions=abv_choices * 6 + text_task * 4,
            answers=list('АБАБВА') + [{'2( кг\*м/с)?': 2}, {'2( м/c)?': 2}, {'3( м/с)?': 2}, {'0.1( м/c)?': 2, '1/10': 2}],
            thresholds=[6, 8, 10],
        ),
        Work(
            task_id='2020-11-26 10 - Законы сохранения - 2',
            classes={'mechanics.zsi_zse': ['Ch_3_1', 'Ch_3_2', 'Ch_3_3', 'Ch_3_6', 'Ch_3_26', 'Vishnyakova_1_4_6', 'Ch_4_2', 'Ch_4_29', 'Ch_4_45', 'Vishnyakova_1_4_12']},
            thresholds=[4, 6, 8],
            up_to='12:05',
            image='incredibles',
            questions=text_task * 10,
        ),
        Work(
            task_id='2020-12-04 10АБ - Статика и гидростатика - 1',
            up_to='12:05',
            image='ratatouille',
            questions=text_task * 7 + Text('Ссылка на гифку') + Text('Какой вопрос добавить в опрос?'),
            answers=[{'1/56': 2, 56: 2}, {15: 2, 12: 1}, {8: 2}, {100: 2}, {75: 2, 225: 1}, {5: 2}, {60: 2}],
            thresholds=[6, 8, 10],
        ),
        Work(
            task_id='2020-12-08 9М - Колебания и волны - 1',
            up_to='11:05',
            image='ratatouille',
            questions=abv_choices * 8,
            answers=list('ВВАВБАВБ'),
            thresholds=[5, 6, 7],
        ),
        Work(
            task_id='2020-12-10 9М - Колебания и волны - 2',
            up_to='11:05',
            image='incredibles',
            questions=abv_choices * 8,
            answers=list('ВБВВ') + [{'Б': 1, 'В': 1}] + list('АВА'),
            thresholds=[5, 6, 7],
        ),
        Work(
            task_id='2020-12-11 10 - Статика и гидростатика - 2',
            classes={'mechanics.gidro': ['Ch_6_3', 'Ch_6_8', 'Ch_6_10', 'Ch_6_16', 'Ch_6_20']},
            thresholds=[1.5, 2.5, 3.5],
            up_to='11:05',
            image='minions',
            questions=text_task * 5,
        ),
        Work(
            task_id='2020-12-17 9М - Колебания и волны - 3',
            up_to='11:05',
            image='keanureeves',
            questions=abv_choices * 10,
            answers=list('АВБАВБ') + [{'А': 0, 'Б': 0}] + list('ВАБ'),
            thresholds=[6, 7, 8],
        ),
        Work(
            task_id='2020-12-22 9М - Колебания и волны - 4',
            up_to='11:05',
            image='zootopia',
            questions=abv_choices * 10,
        ),
        Work(
            task_id='2020-12-24 9',
            classes={'mechanics.koleb': ['Nu01', 'Nu02', 'Nu03', 'Nu04', 'Nu05']},
        ),
        Work(
            task_id='2021-01-21 9',
            classes={'mechanics.koleb': ['Nu01', 'Nu02', 'Nu03', 'Nu04', 'Nu05']},
        ),
        Work(
            task_id='2021-01-22 10',
            classes={'termodynamics.mkt': [ 'Basic01', 'Basic02', 'Basic03', 'Basic04', 'Basic05', 'CountNu', 'CountMass', 'CountParticles' ]},
        ),
        Work(
            task_id='2021-01-29 10',
            classes={'termodynamics.mkt': ['Basic06', 'Basic07', 'Basic08', 'Basic09', 'Basic10', 'Basic11',]},
        ),
        Work(
            task_id='2021-03-02 10',
            classes={'termodynamics.mkt': ['Basic12', 'Basic13', 'GraphPV_1', 'GraphPV_2', 'ZFTSH_10_2_9_kv', 'ZFTSH_10_2_2_kv', 'Polytrope',]},
        ),
        Work(
            task_id='2021-03-04 10',
            classes={'termodynamics.termo': ['YesNo', 'P_from_V_and_U', 'A_on_P_const', 'DeltaU_on_P_const', 'DeltaU_from_DeltaT', 'Q_from_DeltaU', 'Q_from_DeltaU_and_A',],},
        ),
        Work(
            task_id='2021-03-05 10',
            classes=[{'termodynamics.mkt': ['Basic12', 'GraphPV_2', 'ZFTSH_10_2_9_kv', 'ZFTSH_10_2_2_kv', 'Polytrope']}],
        ),
        Work(
            task_id='2021-03-11 10',
            classes={'termodynamics.termo': ['Definitions01', 'V_from_P_and_U', 'A_on_P_const', 'A_from_DeltaT', 'DeltaU_on_P_const', 'DeltaU_from_DeltaT', 'Q_from_DeltaU', 'Q_from_DeltaU_and_A',]},
        ),
        Work(
            task_id='2021-03-12 10',
            classes={'termodynamics': ['cycle.Rectangle', 'termo.DeltaQ_from_states', 'termo.Definitions02']},
        ),
        Work(
            task_id='2021-03-16 9',
            classes={'electricity.cond': ['C_from_U_Q', 'Q_is_possible', 'C_ratio', 'W_from_Q_C', 'Definitions01', 'Definitions02']},
        ),
        Work(
            task_id='2021-03-18 10',
            classes={'termodynamics': ['cycle.Rectangle_T', 'mkt.GraphPV_1', 'termo.YesNo']},
        ),
        Work(
            task_id='2021-03-20 10',
            classes={'termodynamics.cycle': ['TriangleUp_T', 'TriangleUp']},
        ),
        Work(
            task_id='2021-03-23 10',
            classes={'termodynamics': ['cycle.TriangleUp_T', 'vapor.GetPhi', 'mkt.Basic12', 'termo.Definitions02']},
        ),
        Work(
            task_id='2021-03-23 9',
            classes={'atomic.quantum': ['Fotons', 'ColorNameFromLambda', 'E_from_nu',  'E_from_lambda', 'T_Nu_from_lambda', 'Deduce01']},
        ),
        Work(
            task_id='2021-03-25 10',
            classes={'electricity.kulon_field': ['ForceTask', 'ExchangeTask', 'FieldTaskGenerator', 'SumTask']},
        ),
        Work(
            task_id='2021-03-26 10',
            classes={'termodynamics.vapor': ['GetNFromPhi', 'GetPFromPhi', 'GetPFromM', 'Vapor01']},
        ),
        Work(
            task_id='2021-03-30 10',
            classes={'electricity': ['kulon_field.ExchangeTask', 'kulon_field.FieldTaskGenerator', 'potential.E_from_U_l', 'potential.A_from_Q_E_l', 'kulon_field.Definitions01']},
        ),
        Work(
            task_id='2021-03-30 9',
            classes={'atomic.em_waves': ['Gendenshteyn_11_11_18', 'Definitions01', 'Deduce01', 'Sound_to_value', 'Prefix']},
        ),
        Work(
            task_id='2021-04-01 9',
            classes={'atomic.em_waves': ['Lambda_from_E', 'Lambda_from_E_2', 'H_levels']},
        ),
        Work(
            task_id='2021-04-02 10',
            classes={'electricity.potential': ['Phi_from_static_e', 'A_from_motion', 'E_phi_graphs', 'Definitions01']},
        ),
        # Work(
        #     task_id='2021-04-15 10 - Электростатика - 1',
        #     classes={'electricity.cond': ['Definitions03', 'Definitions04', 'Q_is_possible', 'Q_from_DeltaU_C', 'C_from_U_Q', 'C_ratio', 'W_from_Q_C']},
        #     thresholds=[3, 4, 6],
        #     up_to='9:02',
        #     image='zootopia',
        #     questions=text_task * 7,
        # ),
        # Work(
        #     task_id='2021-04-16 9 - Строение атома - 1',
        #     classes={'atomic.radioactive': ['Definitions01', 'Definitions02', 'Definitions03', 'Definitions04', 'Definitions05', 'Definitions06', 'Definitions07']},
        #     thresholds=[4, 5, 6],
        #     questions=text_task * 7,
        #     up_to='11:02',
        #     image='zootopia',
        # ),
        # Work(
        #     task_id='2021-04-23 10 - Постоянный ток - 1',
        #     classes={'electricity.om': ['Definitions01', 'Definitions02', 'Definitions03', 'Definitions04', 'I_from_U_R', 'r_from_R_N', 'U_from_R1_R2_I', 'I_ratio', 'R_best_from_R_N']},
        #     thresholds=[4, 6, 8],
        #     questions=text_task * 9,
        #     up_to='9:05',
        #     image='ratatouille',
        # ),
        # Work(
        #     task_id='2021-04-23 9 - Строение атома - 2',
        #     classes={'atomic.nuclear': ['AtomCount01', 'AtomCount02', 'AtomCount03', 'AtomCount04', 'AtomCount05', 'AtomCount06', 'AtomCount07', 'AtomCount08', 'AtomCount09', 'AtomCount10', 'AtomCount11', 'AtomCount12','AtomCount01_Text', 'AtomCount02_Text', 'AtomCount03_Text', 'AtomCount04_Text', 'AtomCount05_Text', 'AtomCount06_Text', 'AtomCount07_Text', 'AtomCount08_Text', 'AtomCount09_Text', 'AtomCount10_Text', 'AtomCount11_Text', 'AtomCount12_Text',]},
        #     thresholds=[12, 16, 20],
        #     questions=text_task * 24,
        #     up_to='11:02',
        #     image='ratatouille',
        # ),
        Work(
            task_id='2021-04-30 10',
            classes={
                'electricity.om': ['Definitions05', 'Definitions06', 'P_from_R_U', 'P_from_R_I'],
                'electricity.full_circuit': ['Om_eta_full', 'r_eta_from_Rs'],
            },
        ),
        Work(
            task_id='2021-04-30 9',
            classes={'atomic': ['nuclear.KernelCount', 'nuclear.RadioFall', 'radioactive.BK_53_12', 'radioactive.Delta_m_from_m', 'em_waves.H_levels']},
        ),
        Work(
            task_id='2021-04-31 10',
            classes={'electricity': ['om.Definitions07', 'om.Definitions08', 'kirchgoff.Kirchgof_double']},
        ),
        Work(
            task_id='2021-05-12 10',
            classes={'electricity': ['om.Circuit_four', 'om.Circuit_six', 'kirchgoff.Kirchgof_double_2']},
        ),
        Work(
            task_id='2021-05-13 10',
            classes={'electricity': ['full_circuit.Update_external_R', 'kirchgoff.Kirchgof_triple']},
        ),
        Work(
            task_id='2021-05-14 10',
            classes={'electricity': ['om.Compare_power', 'full_circuit.Short_i', 'kirchgoff.Kirchgof_plain']},
        ),
        Work(
            task_id='2021-05-13 9',
            classes={'atomic.radioactive': ['BK_53_01', 'BK_53_02', 'BK_53_03', 'BK_53_12']},
        ),
        Work(
            task_id='2021-05-18 10',
            classes=[
                # 'mechanics.kinematics.AvgSpeed_electron',
                'mechanics.kinematics.A_plus_V',
                'mechanics.kinematics.V_and_S_from_g_and_t',
                'mechanics.kinematics.All_from_l_and_n',
                'mechanics.kinematics.Stones_into_river',
                'mechanics.dynamics.Many_blocks',
                'mechanics.dynamics.Two_blocks_on_block',
                'mechanics.dynamics.F_tren',
                'mechanics.gidro.Rho_from_n',
                'mechanics.statics.Sterzhen',
                'mechanics.zsi_zse.Ch_4_45',
                'mechanics.zsi_zse.Ch_4_2',
                'mechanics.zsi_zse.Ek_ratio_Ep',
                'termodynamics.mkt.Air_rho',
                'termodynamics.mkt.ZFTSH_10_2_9_kv',
                'termodynamics.termo.Q_from_DeltaU',
                'electricity.cond.Cond_posled',
                'electricity.kulon_field.F_from_many_q',
                'electricity.om.P_ratio',
            ],
        ),
        Work(
            task_id='2021-09-07 11БА',
            classes={'magnet.magnet': ['ConstMagnet0', 'ConstMagnet01', 'ConstMagnet02', 'ConstMagnet1', 'ConstMagnet2']},
        ),
        Work(
            task_id='2021-09-08 11Б',
            classes={'magnet.magnet': ['ConstMagnet0', 'ConstMagnet01', 'ConstMagnet02', 'ConstMagnet1', 'ConstMagnet2']},
        ),
        Work(
            task_id='2021-09-14 11БА',
            classes={'magnet': ['magnet.Force10', 'magnet.Force11', 'magnet.Force12', 'lorentz.Force13', 'lorentz.Force14', 'lorentz.Force15']},
        ),
        Work(
            task_id='2021-09-15 11БА',
            classes={'magnet': ['ampere.Chernoutsan11_5', 'ampere.Chernoutsan11_02', 'lorentz.BaseR', 'lorentz.Force16', 'lorentz.Force18']},
        ),
        Work(
            task_id='2021-09-16 11Б',
            classes={'magnet': ['magnet.Force10', 'magnet.Force11', 'magnet.Force12', 'ampere.Chernoutsan11_02', 'lorentz.BaseR', 'lorentz.Force17']},
        ),
        # Work(
        #     task_id='2021-09-22 11БА - ЭМИ - 1',
        #     classes={'magnet.emi': ['Definitions01', 'Definitions02', 'Find_F_easy', 'Action1', 'Action2', 'Find_E_easy', 'Find_F_hard', 'Find_I_hard']},
        #     thresholds=[3, 5, 7],
        #     up_to='10:00',
        #     image='zootopia',
        #     questions=text_task * 8,
        # ),
        # Work(
        #     task_id='2021-09-23 11Б - ЭМИ - 1',
        #     classes={'magnet.emi': ['Definitions01', 'Definitions02', 'Find_F_easy', 'Action1', 'Action2', 'Find_E_easy', 'Find_F_hard']},
        #     thresholds=[2, 4, 5],
        #     up_to='11:00',
        #     image='ratatouille',
        #     questions=text_task * 7,
        # ),
        Work(
            task_id='2021-09-28 11БА - ЭМИ - 2',
            classes={'magnet': ['emi.Definitions03', 'induction.Definitions01', 'induction.Definitions02', 'induction.Definitions03', 'induction.Find_E_easy', 'induction.Find_Phi_1']},
            thresholds=[3, 4, 5],
            up_to='10:00',
            image='zootopia',
            questions=text_task * 6,
        ),
        Work(
            task_id='2021-09-30 11БА - ЭМИ - 3',
            classes={'magnet.induction': ['W_from_L_or_Phi', 'L_W_ratio', 'L_from_BIRn', 'E_rotation', 'F_speed']},
        ),
        Work(
            task_id='2021-09-30 11Б - ЭМИ - 2',
            classes={'magnet': ['emi.Definitions03', 'induction.Definitions01', 'induction.Definitions02', 'induction.Definitions03', 'induction.Find_E_easy', 'induction.Find_Phi_1', 'induction.W_from_L_or_Phi', 'induction.L_W_ratio']},
        ),
        Work(
            task_id='2021-10-05 11БА - ЭМИ - 4',
            classes={'magnet.induction': ['L_from_b', 'a_from_n', 'q_from_B_a_b_r', 'W_kirchgof', 'B_angle_hard']},
        ),
        Work(
            task_id='2021-10-07 11БА - МК - 1',
            classes={'mechanics.koleb': ['Definitions01', 'Definitions02', 'Definitions03', 'Nu02', 'Nu03', 'Nu04', 'Nu05', 'S_from_func']},
        ),
        Work(
            task_id='2021-10-07 11Б - МК - 1',
            classes={'mechanics.koleb': ['Definitions01', 'Definitions02', 'Nu02', 'Nu03', 'Nu04', 'S_from_func']},
        ),
    ]
    return works
