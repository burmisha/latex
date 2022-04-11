import library.dnevnik.mesh
import library.logging
import library.files

import locale
import datetime

import logging
log = logging.getLogger(__name__)


ABSENT_MARK = '-'
SKIP_MARKS = [0, 1]


class MarksUpdater:
    def __init__(self, *, client=None, marks_data=None):
        self._client = client
        self._marks_data = marks_data

    def UpdateAll(self):
        absences = []
        new_marks = []
        for group_id, class_data in self._marks_data.items():
            lesson_form = []
            grade = class_data['grade']
            for lesson_str in class_data['lessons']:
                lesson_id, control_form_name = lesson_str.split(' - ')
                lesson_id = int(lesson_id)

                if lesson_id in self._client._available_lessons_dict:
                    lesson = self._client.get_lesson_by_id(int(lesson_id))
                    control_form = self._client.get_control_forms(lesson._subject_id, grade, log_forms=False)[control_form_name]
                else:
                    lesson = None
                    control_form = None

                lesson_form.append((lesson, control_form))

            for student_name, marks_str in class_data['marks'].items():
                student = self._client.get_student_by_name(student_name)
                marks = marks_str.strip(',').split(',')
                assert len(marks) == len(lesson_form)
                for mark_str, (lesson, control_form) in zip(marks, lesson_form):
                    mark_str = mark_str.strip()
                    if not lesson:
                        continue

                    if mark_str == ABSENT_MARK:
                        absence = library.dnevnik.mesh.Absence(student_id=student.student_id, lesson_id=lesson.lesson_id)
                        absences.append(absence)
                    else:
                        mark = int(mark_str)
                        if mark in library.dnevnik.mesh.VALID_MARKS:
                            new_mark = library.dnevnik.mesh.NewMark(
                                lesson_id=lesson.lesson_id,
                                student_id=student.student_id,
                                value=mark,
                                comment=None,
                                point_date=None,
                                control_form=control_form,
                            )
                            new_marks.append(new_mark)
                        elif mark in SKIP_MARKS:
                            pass
                        else:
                            raise RuntimeError(f'Invalid mark {mark} for {student} at {lesson}')

        log.info(f'Got total of {len(absences)} absences')
        log.info(f'Got total of {len(new_marks)} new marks')

        for absence in absences:
            self._client.set_absent(absence)

        for new_mark in new_marks:
            self._client.set_mark(new_mark)


def get_dt(from_date_days: int, to_date_days: int):
    assert -15 <= from_date_days <= 15
    assert -15 <= to_date_days <= 15

    now = datetime.datetime.now()
    from_dt = now - datetime.timedelta(days=from_date_days)
    to_dt = now + datetime.timedelta(days=to_date_days)
    return from_dt, to_dt


def run(args):
    locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))

    from_dt, to_dt = get_dt(args.from_date, args.to_date)

    client = library.dnevnik.mesh.Client(
        username=library.secrets.token.get('dnevnik.mos.ru.username'),
        password=library.secrets.token.get('dnevnik.mos.ru.password'),
        from_dt=from_dt,
        to_dt=to_dt,
    )

    lessons = list(client.get_lessons())

    grades = sorted(library.dnevnik.mesh.EDUCATION_LEVELS.keys())
    for lesson in lessons:
        for grade in grades:
            client.get_control_forms(lesson._subject_id, grade, log_forms=True)

    for lesson in sorted(lessons):
        log.info(lesson)
        if args.log_links:
            log.info(f'  Link: {lesson.link}')

    if args.set_marks:
        for mark in client.get_all_marks():
            student = client.get_student_by_id(mark.student_id)
            lesson = client.get_lesson_by_id(mark.lesson_id)
            log.info(f'  {student} got {mark} at {lesson}')

        marks_updater = MarksUpdater(
            client=client,
            marks_data=library.files.load_yaml_data('marks.yaml'),
        )
        marks_updater.UpdateAll()
    else:
        log.info('Skip setting marks')

    if args.logout:
        client._logout()


def populate_parser(parser):
    parser.add_argument('-f', '--from-date', help='Search lessons from date (in days)', type=int, default=12)
    parser.add_argument('-t', '--to-date', help='Search lessons to date (in days)', type=int, default=2)
    parser.add_argument('-l', '--log-links', help='Log distant links', action='store_true')
    parser.add_argument('-m', '--set-marks', help='Set marks', action='store_true')
    parser.add_argument('--logout', help='Logout on all devices', action='store_true')
    parser.set_defaults(func=run)
