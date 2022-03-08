import library.dnevnik.mesh
import library.datetools
import library.logging
import library.files

import locale

import logging
log = logging.getLogger(__name__)


class MarkSetter:
    def __init__(self, client=None, lesson_id=None, point_date=None, control_form_name=None, comment=None, grade=None):
        self._client = client
        self._point_date = point_date
        self._lesson = self._client.get_schedule_item_by_id(lesson_id)
        assert self._lesson, f'No lesson found by id {lesson_id}'
        self._control_form = self._client.get_control_forms(self._lesson._subject_id, grade)[control_form_name]
        self._comment = comment

    def Set(self, student_name=None, value=None):
        assert value in [2, 3, 4, 5]

        if value == 5:
            point_date = None
        else:
            point_date = self._point_date

        self._client.set_mark(
            schedule_lesson_id=self._lesson._id,
            student_id=self._client.get_student_by_name(student_name)._id,
            value=value,
            comment=self._comment,
            point_date=point_date,
            control_form=self._control_form,
        )


class MarksUpdater:
    def __init__(self, client=None):
        self._client = client
        self._marks_data = library.files.load_yaml_data('marks.yaml')

    def UpdateAll(self):
        # TODO: update grade
        grade = 11
        for group_id, class_data in self._marks_data.items():
            lesson_form = []
            for lesson_str in class_data['lessons']:
                lesson_id, control_form_name = lesson_str.split(' - ')
                lesson = self._client.get_schedule_item_by_id(int(lesson_id))
                control_form = self._client.get_control_forms(lesson._subject_id, grade, log_forms=False)[control_form_name]
                lesson_form.append((lesson, control_form))

            for student_name, marks_str in class_data['marks'].items():
                student = self._client.get_student_by_name(student_name)
                marks = marks_str.strip(',').split(',')
                assert len(marks) == len(lesson_form)
                for mark_str, (lesson, control_form) in zip(marks, lesson_form):
                    if mark_str == '-':
                        self._client.set_absent(
                            student_id=student._id,
                            lesson_id=lesson._id,
                        )
                    else:
                        mark = int(mark_str)
                        if mark == 1:
                            pass
                        elif mark in [2, 3, 4, 5]:
                            raise RuntimeError('TODO: Check if no mark was set')
                            self._client.set_mark(
                                schedule_lesson_id=lesson._id,
                                student_id=student._id,
                                value=mark,
                                comment=None,
                                point_date=None,
                                control_form=control_form,
                            )
                        else:
                            raise RuntimeError(f'Invalid mark {mark} for {student} at {lesson}')


def run(args):
    locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))

    class_filter = args.class_filter
    group_filter = args.group_filter

    from_date_days = args.from_date
    to_date_days = args.to_date
    assert -15 <= from_date_days <= 15
    assert -15 <= to_date_days <= 15

    now_delta = library.datetools.NowDelta(default_fmt='%Y-%m-%d')
    from_date = now_delta.Before(days=from_date_days)
    to_date = now_delta.After(days=to_date_days)

    # for data in [
    #     # '{"schedule_lesson_id":220536675,"student_profile_id":5575224,"control_form_id":4789098,"is_exam":false,"grade_system_id":3839912,"grade_system_type":"five","grade_system_name":"\u0448\u043a\u0430\u043b\u0430 \u043e\u0446\u0435\u043d\u0438\u0432\u0430\u043d\u0438\u044f 1597410492","weight":1,"comment":"\u0417\u0430\u0434\u0430\u0447\u0438 \u043d\u0430\u0438\u0437\u0443\u0441\u0442\u044c \u043f\u043e \u0434\u0438\u043d\u0430\u043c\u0438\u043a\u0435","point_date":"29.12.2020","pointDate":"2020-12-28T21:54:11.000Z","is_point":true,"grade_origins":[{"grade_system_id":3839912,"grade_origin":4}],"valuesByIds":{"3839912":4},"is_criterion":false,"is_approve":false,"controlForm":{"subject_id":3626,"name":"\u0414\u043e\u043c\u0430\u0448\u043d\u044f\u044f \u0440\u0430\u0431\u043e\u0442\u0430","short_name":"","education_level_id":3,"origin_control_form_id":null,"school_id":1098,"id":4789098,"is_exam":false,"grade_system_id":3839912,"grade_system":{"id":3839912,"nmax":6,"name":"\u0448\u043a\u0430\u043b\u0430 \u043e\u0446\u0435\u043d\u0438\u0432\u0430\u043d\u0438\u044f 1597410492","type":"five","defaults":[{"nmax":6,"inversion":false,"hundred":[{"range":{"from":81,"to":100}},{"range":{"from":61,"to":80}},{"range":{"from":31,"to":60}},{"range":{"from":21,"to":30}},{"range":{"from":11,"to":20}},{"range":{"from":0,"to":10}}],"names":["\u041e\u0446\u0435\u043d\u043a\u0430 5","\u041e\u0446\u0435\u043d\u043a\u0430 4","\u041e\u0446\u0435\u043d\u043a\u0430 3","\u041e\u0446\u0435\u043d\u043a\u0430 2","\u041e\u0446\u0435\u043d\u043a\u0430 1","\u041e\u0446\u0435\u043d\u043a\u0430 0"],"n":[{"range":{"from":81,"to":100}},{"range":{"from":61,"to":80}},{"range":{"from":31,"to":60}},{"range":{"from":21,"to":30}},{"range":{"from":11,"to":20}},{"range":{"from":0,"to":10}}],"five":[{"mark":5},{"mark":4},{"mark":3},{"mark":2},{"mark":1},{"mark":0}]}]},"weight":1,"deleted_at":null,"type":null,"route":"/core/api/control_forms","reqParams":null,"restangularized":true,"fromServer":false,"parentResource":null,"restangularCollection":false,"selected":true},"showComment":true}',
    #     # '{"schedule_lesson_id":220536675,"student_profile_id":2890384,"control_form_id":4789098,"is_exam":false,"grade_system_id":3839912,"grade_system_type":"five","grade_system_name":"шкала оценивания 1597410492","weight":1,"comment":null,"point_date":"29.12.2020","pointDate":"2020-12-28T22:24:06.000Z","is_point":true,"grade_origins":[{"grade_system_id":3839912,"grade_origin":3}],"valuesByIds":{"3839912":3},"is_criterion":false,"is_approve":false,"controlForm":{"subject_id":3626,"name":"Домашняя работа","short_name":"","education_level_id":3,"origin_control_form_id":null,"school_id":1098,"id":4789098,"is_exam":false,"grade_system_id":3839912,"grade_system":{"id":3839912,"nmax":6,"name":"шкала оценивания 1597410492","type":"five","defaults":[{"nmax":6,"inversion":false,"hundred":[{"range":{"from":81,"to":100}},{"range":{"from":61,"to":80}},{"range":{"from":31,"to":60}},{"range":{"from":21,"to":30}},{"range":{"from":11,"to":20}},{"range":{"from":0,"to":10}}],"names":["Оценка 5","Оценка 4","Оценка 3","Оценка 2","Оценка 1","Оценка 0"],"n":[{"range":{"from":81,"to":100}},{"range":{"from":61,"to":80}},{"range":{"from":31,"to":60}},{"range":{"from":21,"to":30}},{"range":{"from":11,"to":20}},{"range":{"from":0,"to":10}}],"five":[{"mark":5},{"mark":4},{"mark":3},{"mark":2},{"mark":1},{"mark":0}]}]},"weight":1,"deleted_at":null,"type":null,"route":"/core/api/control_forms","reqParams":null,"restangularized":true,"fromServer":false,"parentResource":null,"restangularCollection":false,"selected":true}}',
    #     # '{"schedule_lesson_id":220536675,"student_profile_id":12925712,"control_form_id":4789098,"is_exam":false,"grade_system_id":3839912,"grade_system_type":"five","grade_system_name":"шкала оценивания 1597410492","weight":1,"comment":"Динамика - Задачи наизусть","point_date":null,"pointDate":"2020-12-14T22:35:25.539Z","is_point":false,"grade_origins":[{"grade_system_id":3839912,"grade_origin":5}],"valuesByIds":{"3839912":5},"is_criterion":false,"is_approve":false,"controlForm":{"subject_id":3626,"name":"Домашняя работа","short_name":"","education_level_id":3,"origin_control_form_id":null,"school_id":1098,"id":4789098,"is_exam":false,"grade_system_id":3839912,"grade_system":{"id":3839912,"nmax":6,"name":"шкала оценивания 1597410492","type":"five","defaults":[{"nmax":6,"inversion":false,"hundred":[{"range":{"from":81,"to":100}},{"range":{"from":61,"to":80}},{"range":{"from":31,"to":60}},{"range":{"from":21,"to":30}},{"range":{"from":11,"to":20}},{"range":{"from":0,"to":10}}],"names":["Оценка 5","Оценка 4","Оценка 3","Оценка 2","Оценка 1","Оценка 0"],"n":[{"range":{"from":81,"to":100}},{"range":{"from":61,"to":80}},{"range":{"from":31,"to":60}},{"range":{"from":21,"to":30}},{"range":{"from":11,"to":20}},{"range":{"from":0,"to":10}}],"five":[{"mark":5},{"mark":4},{"mark":3},{"mark":2},{"mark":1},{"mark":0}]}]},"weight":1,"deleted_at":null,"type":null,"route":"/core/api/control_forms","reqParams":null,"restangularized":true,"fromServer":false,"parentResource":null,"restangularCollection":false,"selected":true},"showComment":true}',
    #     '{"schedule_lesson_id":220536671,"student_profile_id":2892328,"control_form_id":4614283,"is_exam":false,"grade_system_id":3660295,"grade_system_type":"five","grade_system_name":"5-\u0431\u0430\u043b\u043b\u044c\u043d\u0430\u044f \u0448\u043a\u0430\u043b\u0430","weight":1,"comment":"\u0414\u0438\u043d\u0430\u043c\u0438\u043a\u0430 - \u0417\u0430\u0434\u0430\u0447\u0438 \u043d\u0430\u0438\u0437\u0443\u0441\u0442\u044c","point_date":null,"pointDate":"2020-12-15T21:15:27.493Z","is_point":false,"grade_origins":[{"grade_system_id":3660295,"grade_origin":3}],"valuesByIds":{"3660295":3},"is_criterion":false,"is_approve":false,"controlForm":{"subject_id":56,"name":"\u0426\u0438\u0444\u0440\u043e\u0432\u043e\u0435 \u0434\u043e\u043c\u0430\u0448\u043d\u0435\u0435 \u0437\u0430\u0434\u0430\u043d\u0438\u0435","short_name":"\u0426\u0414\u0417","education_level_id":3,"origin_control_form_id":null,"school_id":1098,"id":4614283,"is_exam":false,"grade_system_id":3660295,"grade_system":{"id":3660295,"nmax":6,"name":"5-\u0431\u0430\u043b\u043b\u044c\u043d\u0430\u044f \u0448\u043a\u0430\u043b\u0430","type":"five","defaults":[{"nmax":6,"inversion":false,"hundred":[{"range":{"from":0,"to":10}},{"range":{"from":11,"to":20}},{"range":{"from":21,"to":30}},{"range":{"from":31,"to":60}},{"range":{"from":61,"to":80}},{"range":{"from":81,"to":100}}],"names":["\u041e\u0446\u0435\u043d\u043a\u0430 0","\u041e\u0446\u0435\u043d\u043a\u0430 1","\u041e\u0446\u0435\u043d\u043a\u0430 2","\u041e\u0446\u0435\u043d\u043a\u0430 3","\u041e\u0446\u0435\u043d\u043a\u0430 4","\u041e\u0446\u0435\u043d\u043a\u0430 5"],"n":[{"range":{"from":0,"to":10}},{"range":{"from":11,"to":20}},{"range":{"from":21,"to":30}},{"range":{"from":31,"to":60}},{"range":{"from":61,"to":80}},{"range":{"from":81,"to":100}}],"five":[{"mark":0},{"mark":1},{"mark":2},{"mark":3},{"mark":4},{"mark":5}]}]},"weight":1,"deleted_at":null,"type":"digital_training","route":"/core/api/control_forms","reqParams":null,"restangularized":true,"fromServer":false,"parentResource":null,"restangularCollection":false,"selected":true},"showComment":true}',
    #     # '{"created_at":"14.12.2020 00:55","id":1186382356,"student_profile_id":5575224,"weight":1,"teacher_id":15033420,"name":"4","comment":"Задачи наизусть по динамике","control_form_id":4789098,"deleted_by":null,"grade_id":22324525,"schedule_lesson_id":220536675,"is_exam":false,"group_id":5396206,"date":"08.12.2020","is_point":true,"point_date":"29.12.2020","subject_id":3626,"grade_system_id":3839912,"grade_system_type":"five","values":[{"grade_system_id":3839912,"name":"шкала оценивания 1597410492","nmax":6.0,"grade_system_type":"five","grade":{"origin":"4","five":4.0,"hundred":80.0}}]}',
    #     # '{"schedule_lesson_id":220571202,"student_profile_id":3068575,"control_form_id":186166,"is_exam":false,"grade_system_id":92978,"grade_system_type":"five","grade_system_name":"\u0448\u043a\u0430\u043b\u0430 \u043e\u0446\u0435\u043d\u0438\u0432\u0430\u043d\u0438\u044f 1474746446-590","weight":1,"comment":"\u041a\u043e\u043b\u0435\u0431\u0430\u043d\u0438\u044f \u0438 \u0432\u043e\u043b\u043d\u044b - \u0442\u0435\u0441\u0442 3","point_date":null,"pointDate":"2020-12-22T14:26:30.673Z","is_point":false,"grade_origins":[{"grade_system_id":92978,"grade_origin":5}],"valuesByIds":{"92978":5},"is_criterion":false,"is_approve":false,"controlForm":{"subject_id":3626,"name":"\u0420\u0435\u0448\u0435\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447","short_name":"","education_level_id":2,"origin_control_form_id":null,"school_id":1098,"id":186166,"is_exam":false,"grade_system_id":92978,"grade_system":{"id":92978,"nmax":6,"name":"\u0448\u043a\u0430\u043b\u0430 \u043e\u0446\u0435\u043d\u0438\u0432\u0430\u043d\u0438\u044f 1474746446-590","type":"five","defaults":[{"nmax":6,"inversion":false,"hundred":[{"range":{"from":81,"to":100}},{"range":{"from":61,"to":80}},{"range":{"from":31,"to":60}},{"range":{"from":21,"to":30}},{"range":{"from":11,"to":20}},{"range":{"from":0,"to":10}}],"names":["\u041e\u0446\u0435\u043d\u043a\u0430 5","\u041e\u0446\u0435\u043d\u043a\u0430 4","\u041e\u0446\u0435\u043d\u043a\u0430 3","\u041e\u0446\u0435\u043d\u043a\u0430 2","\u041e\u0446\u0435\u043d\u043a\u0430 1","\u041e\u0446\u0435\u043d\u043a\u0430 0"],"n":[{"range":{"from":81,"to":100}},{"range":{"from":61,"to":80}},{"range":{"from":31,"to":60}},{"range":{"from":21,"to":30}},{"range":{"from":11,"to":20}},{"range":{"from":0,"to":10}}],"five":[{"mark":5},{"mark":4},{"mark":3},{"mark":2},{"mark":1},{"mark":0}]}]},"weight":1,"deleted_at":null,"type":null,"route":"/core/api/control_forms","reqParams":null,"restangularized":true,"fromServer":false,"parentResource":null,"restangularCollection":false,"selected":true},"showComment":true}',
    #     '{"created_at":"15.12.2020 01:30","id":1188507628,"student_profile_id":2892307,"weight":1,"teacher_id":15033420,"name":"2","comment":"\u0414\u0438\u043d\u0430\u043c\u0438\u043a\u0430 - \u0417\u0430\u0434\u0430\u0447\u0438 \u043d\u0430\u0438\u0437\u0443\u0441\u0442\u044c","control_form_id":4614283,"deleted_by":null,"grade_id":21251381,"schedule_lesson_id":220536671,"is_exam":false,"group_id":5472791,"date":"08.12.2020","is_point":false,"point_date":null,"subject_id":56,"grade_system_id":3660295,"grade_system_type":"five","values":[{"grade_system_id":3660295,"name":"5-\u0431\u0430\u043b\u043b\u044c\u043d\u0430\u044f \u0448\u043a\u0430\u043b\u0430","nmax":6,"grade_system_type":"five","grade":{"origin":4,"five":2,"hundred":30}}],"is_point_active":true,"is_criterion":false,"pointDate":"2020-12-28T21:00:00.000Z","hasComment":true,"showComment":false,"previousControlFormId":4614283,"controlForm":{"subject_id":56,"name":"\u0426\u0438\u0444\u0440\u043e\u0432\u043e\u0435 \u0434\u043e\u043c\u0430\u0448\u043d\u0435\u0435 \u0437\u0430\u0434\u0430\u043d\u0438\u0435","short_name":"\u0426\u0414\u0417","education_level_id":3,"origin_control_form_id":null,"school_id":1098,"id":4614283,"is_exam":false,"grade_system_id":3660295,"grade_system":{"id":3660295,"nmax":6,"name":"5-\u0431\u0430\u043b\u043b\u044c\u043d\u0430\u044f \u0448\u043a\u0430\u043b\u0430","type":"five","defaults":[{"nmax":6,"inversion":false,"hundred":[{"range":{"from":0,"to":10}},{"range":{"from":11,"to":20}},{"range":{"from":21,"to":30}},{"range":{"from":31,"to":60}},{"range":{"from":61,"to":80}},{"range":{"from":81,"to":100}}],"names":["\u041e\u0446\u0435\u043d\u043a\u0430 0","\u041e\u0446\u0435\u043d\u043a\u0430 1","\u041e\u0446\u0435\u043d\u043a\u0430 2","\u041e\u0446\u0435\u043d\u043a\u0430 3","\u041e\u0446\u0435\u043d\u043a\u0430 4","\u041e\u0446\u0435\u043d\u043a\u0430 5"],"n":[{"range":{"from":0,"to":10}},{"range":{"from":11,"to":20}},{"range":{"from":21,"to":30}},{"range":{"from":31,"to":60}},{"range":{"from":61,"to":80}},{"range":{"from":81,"to":100}}],"five":[{"mark":0},{"mark":1},{"mark":2},{"mark":3},{"mark":4},{"mark":5}]}]},"weight":1,"deleted_at":null,"type":"digital_training","route":"/core/api/control_forms","reqParams":null,"restangularized":true,"fromServer":false,"parentResource":null,"restangularCollection":false,"selected":true},"grade_origins":[{"grade_system_id":3660295,"grade_origin":4}],"valuesByIds":{"3660295":4},"originalMarkData":{"control_form_id":4614283,"is_exam":false,"grade_system_type":"five","grade_system_id":3660295,"weight":1,"valuesByIds":{"3660295":2}}}',  # update mark
    # ]:
    #     import json
    #     log.info(f'Got\n{library.logging.colorize_json(json.loads(data))}')
    # return

    client = library.dnevnik.mesh.Client(
        username=args.username,
        password=library.secrets.token.get('dnevnik.mos.ru.password'),
    )

    schedule_items = client.get_schedule_items(from_date=from_date, to_date=to_date)

    for lesson in schedule_items:
        for grade in [9, 10, 11]:
            client.get_control_forms(lesson._subject_id, grade, log_forms=True)

    marks_updater = MarksUpdater(client)
    marks_updater.UpdateAll()

    return

    for schedule_item in sorted(schedule_items):
        if class_filter and class_filter not in schedule_item._group._best_name:
            continue
        if group_filter and schedule_item._group._id != group_filter:
            continue

        log.info(schedule_item)
        if args.log_links:
            log.info(f'  Link: {schedule_item.get_link()}')

        if schedule_item._id in args.set_all_absent:
            for student_id in schedule_item._group._student_ids:
                client.set_absent(student_id=student_id, lesson_id=schedule_item._id)

    for _, student in client.get_student_profiles().items():
        log.debug(student)

    marks_now_date = library.datetools.NowDelta(default_fmt='%d.%m.%Y')
    marks_from_date = marks_now_date.Before(days=from_date_days)
    marks_to_date = marks_now_date.After(days=to_date_days)
    for group in client.get_groups():
        for mark in client.get_marks(from_date=marks_from_date, to_date=marks_to_date, group=client.get_group_by_id(group._id)):
            student = client.get_student_by_id(mark._student_profile_id)
            lesson = client.get_schedule_item_by_id(mark._schedule_lesson_id)
            log.info(f'  {student} got {mark} at {lesson}')

    marks_cfg = [
        # (10, 220536675, '2020-12-29', 'Домашняя работа', 'Динамика - Задачи наизусть', [
        #     ('Ан Ирина', 2),
        #     ('Андрианова Софья', 4),  # 4 / 6
        #     ('Артемчук Владимир', 4),  # 3 / 6
        #     ('Белянкина Софья', 2),
        #     ('Егиазарян Варвара', 3),  # 2 / 6
        #     ('Емелин Владислав', 2),
        #     ('Жичин Артём', 2),
        #     ('Кошман Дарья', 5),
        #     ('Кузьмичёва Анна', 2),
        #     ('Куприянова Алёна', 2),
        #     ('Ламанова Анастасия', 2),
        #     ('Легонькова Виктория', 3),  # 2 / 6
        #     ('Мартынов Семён', 2),
        #     ('Минаева Варвара', 5),  # 5 / 6
        #     ('Никитин Леонид', 5),  # 6 / 6
        #     ('Полетаев Тимофей', 3),  # 2 / 6
        #     ('Рожков Андрей', 5),  # 5 / 6
        #     ('Таржиманова Рената', 5),  # 6 / 6
        #     ('Трофимов Арсений', 2),
        #     ('Щербаков Андрей', 4),  # 4 / 6
        #     ('Ярошевский Михаил', 2),
        # ]),
        (10, 220536894, None, 'Проверочная работа', 'Гидростатика по индивидуальным вариантам', [
            ('Андрианова Софья', 4),
            ('Артемчук Владимир', 3),
            ('Белянкина Софья', 4),
            ('Егиазарян Варвара', 3),
            ('Жичин Артём', 3),
            ('Козлов Константин', 2),
            ('Кошман Дарья', 3),
            ('Куприянова Алёна', 4),
            ('Легонькова Виктория', 3),
            ('Минаева Варвара', 3),
            ('Никитин Леонид', 4),
            ('Полетаев Тимофей', 3),
            ('Полканова Алина', 2),
            ('Пономарев Сергей', 3),
            ('Рожков Андрей', 4),
            ('Соколов Дмитрий', 4),
            ('Таржиманова Рената', 3),
            ('Трофимов Арсений', 2),
            ('Щербаков Андрей', 5),
        ]),
        # (10, 220536671, '2020-12-29', 'Цифровое домашнее задание', 'Динамика - Задачи наизусть', [
        #     ('Алимпиев Алексей', 2),  # 0 / 6
        #     ('Васин Евгений', 2),  # 0 / 6
        #     ('Говоров Герман', 2),  # 0 / 6
        #     ('Журавлёва София', 2),  # 0 / 6
        #     ('Козлов Константин', 2),  # 0 / 6
        #     ('Кравченко Наталья', 2),  # 0 / 6
        #     ('Малышев Сергей', 2),  # 0 / 6
        #     ('Полканова Алина', 2),  # 0 / 6
        #     ('Пономарев Сергей', 3),  # 1 / 6
        #     ('Свистушкин Егор', 2),  # 0 / 6
        #     ('Соколов Дмитрий', 2),  # 0 / 6
        # ]),
        # (9, 220571202, None, 'Решение задач', 'Колебания и волны - тест 3', [
        #     ('Гончарова Наталья', 5),
        #     ('Касымов Файёзбек', 5),
        #     ('Козинец Александр', 5),
        #     ('Лоткова ПОЛИНА', 5),
        #     ('Медведева Екатерина', 5),
        #     ('Мельник Константин', 5),
        #     ('Небоваренков Степан', 5),
        #     ('Неретин Матвей', 5),
        #     ('Никонова Мария', 5),
        #     ('Палаткин Даниил', 5),
        #     ('Пикун Станислав', 5),
        #     ('Севрюгин Кирилл', 5),
        #     ('Стратонников Илья', 5),
        #     ('Шустов Иван', 5),
        # ]),
    ]
    if args.set_marks:
        for grade, lesson_id, point_date, control_form_name, comment, marks in marks_cfg:
            mark_setter = MarkSetter(client=client, lesson_id=lesson_id, point_date=point_date, control_form_name=control_form_name, comment=comment, grade=grade)
            for student_name, value in marks:
                mark_setter.Set(student_name=student_name, value=value)

    for res in [
        # client.get('/acl/api/users', {
        #     'ids': 14650300
        # }),
        # client.get('/jersey/api/lesson_replacements', {
        #     'academic_year_id': current_year.id,
        #     'begin_date': '2020/11/30',
        #     'end_date': '2020/12/06',
        #     'pid': client.get_teacher_id(),
        #     'teacher_id': client.get_teacher_id()
        # }),
        # client.get('/core/api/homeworks', {
        #     'academic_year_id': current_year.id,
        #     'begin_date': '30.11.2020',
        #     'end_date': '06.12.2020',
        #     'group_ids': '5404115,5472791,5396206,5351031,5351036',
        #     'pid': client.get_teacher_id(),
        #     'with_entries': True
        # }),
    ]:
        log.info(f'Got\n{library.logging.colorize_json(res)}')

    if args.logout:
        client._logout()
    else:
        log.info('Skipping logout as it will require login on all devices')


def populate_parser(parser):
    parser.add_argument('-a', '--set-all-absent', help='Set all absent for schedult item', type=int, action='append', default=[])
    parser.add_argument('-f', '--from-date', help='Search lessons from date (in days)', type=int, default=5)
    parser.add_argument('-t', '--to-date', help='Search lessons to date (in days)', type=int, default=2)
    parser.add_argument('-c', '--class-filter', help='Class filter')
    parser.add_argument('-g', '--group-filter', help='Group filter (by id)', type=int)
    parser.add_argument('--username', help='Username to login', default='burmistrovmo')
    parser.add_argument('-l', '--log-links', help='Log distant links', action='store_true')
    parser.add_argument('-m', '--set-marks', help='Set marks', action='store_true')
    parser.add_argument('--logout', help='Logout an all devices', action='store_true')
    parser.set_defaults(func=run)
