import library.dnevnik.mesh
import library.logging
import library.files

import locale
import datetime

import logging
log = logging.getLogger(__name__)


class MarksUpdater:
    def __init__(self, *, client=None, marks_cache=None):
        self._client = client
        self._marks_cache = marks_cache
        self._marks_data = library.files.load_yaml_data('marks.yaml')

    def UpdateAll(self):
        for group_id, class_data in self._marks_data.items():
            lesson_form = []
            grade = class_data['grade']
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
                            cached_mark = self._marks_cache.get(lesson_id=lesson._id, student_id=student._id)
                            if cached_mark is None:
                                self._client.set_mark(
                                    schedule_lesson_id=lesson._id,
                                    student_id=student._id,
                                    value=mark,
                                    comment=None,
                                    point_date=None,
                                    control_form=control_form,
                                )
                            else:
                                log.info(f'{cached_mark} for {student} at {lesson} already set')
                        else:
                            raise RuntimeError(f'Invalid mark {mark} for {student} at {lesson}')


def get_dt(from_date_days, to_date_days):
    assert -15 <= from_date_days <= 15
    assert -15 <= to_date_days <= 15

    now = datetime.datetime.now()
    from_dt = now - datetime.timedelta(days=from_date_days)
    to_dt = now + datetime.timedelta(days=to_date_days)
    return from_dt, to_dt


def run(args):
    locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))

    class_filter = args.class_filter
    group_filter = args.group_filter

    from_dt, to_dt = get_dt(args.from_date, args.to_date)

    client = library.dnevnik.mesh.Client(
        username=args.username,
        password=library.secrets.token.get('dnevnik.mos.ru.password'),
        from_dt=from_dt,
        to_dt=to_dt,
    )

    schedule_items = client.get_schedule_items()

    grades = sorted(library.dnevnik.mesh.EDUCATION_LEVELS.keys())
    for lesson in schedule_items:
        for grade in grades:
            client.get_control_forms(lesson._subject_id, grade, log_forms=True)

    for schedule_item in sorted(schedule_items):
        if class_filter and class_filter not in schedule_item._group._best_name:
            continue
        if group_filter and schedule_item._group._id != group_filter:
            continue

        log.info(schedule_item)
        if args.log_links:
            log.info(f'  Link: {schedule_item.get_link()}')

    for _, student in client.get_student_profiles().items():
        log.debug(student)

    marks_cache = library.dnevnik.mesh.MarksCache(from_dt=from_dt, to_dt=to_dt)
    for group in client.get_groups():
        for mark in client.get_marks(group=group):
            marks_cache.add(mark)
            student = client.get_student_by_id(mark._student_id)
            lesson = client.get_schedule_item_by_id(mark._lesson_id)
            log.info(f'  {student} got {mark} at {lesson}')
    marks_cache.freeze()

    if args.set_marks:
        marks_updater = MarksUpdater(client=client, marks_cache=marks_cache)
        marks_updater.UpdateAll()
    else:
        log.info('Skip setting marks')

    return

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
    parser.add_argument('-f', '--from-date', help='Search lessons from date (in days)', type=int, default=12)
    parser.add_argument('-t', '--to-date', help='Search lessons to date (in days)', type=int, default=2)
    parser.add_argument('-c', '--class-filter', help='Class filter')
    parser.add_argument('-g', '--group-filter', help='Group filter (by id)', type=int)
    parser.add_argument('--username', help='Username to login', default='burmistrovmo')
    parser.add_argument('-l', '--log-links', help='Log distant links', action='store_true')
    parser.add_argument('-m', '--set-marks', help='Set marks', action='store_true')
    parser.add_argument('--logout', help='Logout on all devices', action='store_true')
    parser.set_defaults(func=run)
