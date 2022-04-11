# see https://github.com/search?q=dnevnik.mos.ru&type=repositories
# https://github.com/KonstantIMP/vega/blob/main/client/auth.py

import datetime
import datetime
from typing import Optional, List

import logging
log = logging.getLogger(__name__)

from library.logging import colorize_json, cm, color
import library.secrets
from library.dnevnik.client import AuthorizedClient, BASE_URL, ApiUrl
from library.dnevnik.models import (
    Year,
    Group,
    Student,
    Lesson,
    Mark,
    MarksCache,
    ControlForm,
    Absence,
    NewMark,
    VALID_MARKS,
)


MARKS_DATE_FMT = '%d.%m.%Y'
SCHEDULE_DATE_FMT = '%Y-%m-%d'
EDUCATION_LEVELS = {
    11: 3,
    10: 3,
    9: 2,
}
MARKS_LIMIT = 1000
CONTROL_FORMS_LIMIT = 100


class Client:
    def __init__(
        self,
        *,
        username=None,
        password=None,
        from_dt: datetime.datetime=None,
        to_dt: datetime.datetime=None,
    ):
        self.authorized_client = AuthorizedClient(username=username, password=password)
        self.teacher_id = self.authorized_client._profile_id

        self.from_dt = from_dt
        self.to_dt = to_dt

        self._current_year = None
        self._teacher_profile = None
        self._groups = None
        self._all_student_profiles = None
        self._available_lessons_dict = {}
        self._control_forms = {}

        self._marks_cache = MarksCache()
        self._loaded_marks = False

        from_date_str = library.datetools.formatTimestamp(self.from_dt, fmt='%F')
        to_date_str = library.datetools.formatTimestamp(self.to_dt, fmt='%F')

        log.info(f'Using dates {cm(from_date_str, color.Green)} ... {cm(to_date_str, color.Green)}')

    def get_current_year(self):
        if self._current_year is None:
            params = {'pid': self.teacher_id}
            rows = self.authorized_client.get(ApiUrl.ACADEMIC_YEARS, params)
            self._current_year = None
            for row in rows:
                year = Year(
                    year_id=row['id'],
                    name=row['name'],
                    begin_date=row['begin_date'],
                    end_date=row['end_date'],
                    calendar_id=row['calendar_id'],
                    current_year=row['current_year'],
                )
                if year.current_year:
                    assert not self._current_year
                    self._current_year = year
            assert self._current_year
            log.info(f'Set current year: {self._current_year}')

        return self._current_year

    def get_teacher_profile(self):
        if self._teacher_profile is None:
            params = {
                'academic_year_id': self.get_current_year().year_id,
                'pid': self.teacher_id,
                'with_assigned_groups': True
            }
            self._teacher_profile = self.authorized_client.get(ApiUrl.TEACHER_PROFILES.format(teacher_id=self.teacher_id), params)

        return self._teacher_profile

    def get_assigned_group_ids(self) -> List[int]:
        return self.get_teacher_profile()['assigned_group_ids']

    def get_groups(self):
        if self._groups is None:
            params = {
                'academic_year_id': self.get_current_year().year_id,
                'group_ids': ','.join(str(i) for i in self.get_assigned_group_ids()),
                'pid': self.teacher_id,
            }
            groups = self.authorized_client.get(ApiUrl.GROUPS, params)
            self._groups = [Group(item) for item in groups]
        return self._groups

    def get_group_by_id(self, group_id):
        for group in self.get_groups():
            if group.group_id == group_id:
                return group

        log.warn(f'No group with id {group_id}')
        return None

    def get_students(self):
        if self._all_student_profiles is None:
            self._all_student_profiles = {}
            for group in self.get_groups():
                params = {
                    'academic_year_id': self.get_current_year().year_id,
                    'class_unit_ids': ','.join(str(i) for i in group._class_unit_ids),
                    'group_ids': ','.join(str(i) for i in [group.group_id] + group._subgroup_ids),
                    'per_page': 1000,
                    'pid': self.teacher_id,
                    'with_archived_groups': True,
                    'with_deleted': True,
                    'with_final_marks': True,
                    'with_groups': True,
                    'with_home_based': True,
                    'with_lesson_info': True,
                    # 'with_parents': True,
                }
                rows = self.authorized_client.get(ApiUrl.STUDENT_PROFILES, params=params)
                log.info(f'Loaded {len(rows)} students for {group!r}')
                for row in rows:
                    student = Student(
                        student_id=int(row['id']),
                        short_name=row['short_name'],
                        group_ids=[int(group['id']) for group in row['groups']],
                        class_unit_id=int(row['class_unit']['id']),
                        raw_data=row,
                    )
                    self._all_student_profiles[student.student_id] = student
        return self._all_student_profiles

    def get_student_by_id(self, student_id: int) -> Student:
        assert isinstance(student_id, int)
        return self.get_students()[student_id]

    def get_student_by_name(self, student_name):
        matched = [
            student for student in self.get_students().values()
            if student.matches(student_name)
        ]
        if len(matched) != 1:
            raise RuntimeError(f'Not found students by name {student_name}: got {matched} matched')
        return matched[0]            

    def get_lesson_by_id(self, lesson_id: int) -> Lesson:
        assert isinstance(lesson_id, int)
        return self._available_lessons_dict[lesson_id]

    def set_absent(self, absence: Absence=None):
        student = self.get_student_by_id(absence.student_id)
        lesson = self.get_lesson_by_id(absence.lesson_id)

        request = {
            'absence_reason': None,
            'absence_reason_id': 2,
            'schedule_lesson_id': absence.lesson_id,
            'student_profile_id': absence.student_id,
        }
        result = self.authorized_client.post(ApiUrl.ATTENDANCES.format(teacher_id=self.teacher_id), json_data=request)

        if result.get('created_at'):
            log.info(f'Absense was set for {student} for {lesson}')
        elif result.get('code') == 403 and result.get('message') == 'Пропуск для выбранного ученика и урока уже существует':
            log.info(f'Absense has already been set for {student} for {lesson}')
        else:
            log.error(f'Unknown response: {colorize_json(result)}')
            raise RuntimeError('Unknown response')

    def get_lessons(self):
        request = {
            'academic_year_id': self.get_current_year().year_id,
            'from': library.datetools.formatTimestamp(self.from_dt, fmt=SCHEDULE_DATE_FMT),
            'to': library.datetools.formatTimestamp(self.to_dt, fmt=SCHEDULE_DATE_FMT),
            'original': True,
            'page': 1,
            'per_page': 100,
            'pid': self.teacher_id,
            'teacher_id': self.teacher_id,
            'with_group_class_subject_info': True,
        }
        rows = self.authorized_client.get(ApiUrl.SCHEDULE_ITEMS, request)
        for row in rows:
            lesson = Lesson(row)
            group = self.get_group_by_id(lesson.group_id)
            if group:
                lesson.set_group(group)
                self._available_lessons_dict[lesson.lesson_id] = lesson
                yield lesson
            else:
                log.warn(f'Skipping lesson for {cm(lesson.group_name, color=color.Red)} as no group found')

    def _get_marks_for_group(self, *, group: Group=None, limit: int=MARKS_LIMIT):
        from_date = library.datetools.formatTimestamp(self.from_dt, fmt=MARKS_DATE_FMT)
        to_date = library.datetools.formatTimestamp(self.to_dt, fmt=MARKS_DATE_FMT)
        log.info(f'Getting marks [{from_date}, {to_date}] for {group}')

        params = {
            'created_at_from': from_date,
            'created_at_to': to_date,
            'group_ids': ','.join(str(i) for i in [group.group_id] + group._subgroup_ids),
            'page': 1,
            'per_page': limit,
            'pid': self.teacher_id,
        }
        marks_items = self.authorized_client.get(ApiUrl.MARKS_GET, params=params)
        assert len(marks_items) < limit, f'Too many marks: reduce dates or increase limit: {limit}'

        for mark_item in marks_items:
            yield Mark(
                mark_id=mark_item['id'],
                value=int(mark_item['name']),
                student_id=int(mark_item['student_profile_id']),
                lesson_id=int(mark_item['schedule_lesson_id']),
                raw_data=mark_item,
            )

    def get_all_marks(self):
        marks = []
        for group in self.get_groups():
            for mark in self._get_marks_for_group(group=group):
                self._marks_cache.add(mark)
                marks.append(mark)

        self._loaded_marks = True
        return marks

    def validate_mark(self, new_mark: NewMark):
        lesson = self.get_lesson_by_id(new_mark.lesson_id)
        student = self.get_student_by_id(new_mark.student_id)

        ok = (lesson.group_id in student.group_ids) or (lesson.class_unit_id == student.class_unit_id)  
        if not ok:
            log.info(f'student: {colorize_json(student.raw_data)}')
            log.info(f'lesson: {colorize_json(lesson.raw_data)}')
            log.error(f'Failed on {student} at {lesson}')
            raise RuntimeError(f'Failed at student check')

    def set_mark(self, new_mark: NewMark):
        if not self._loaded_marks:
            raise RuntimeError('Marks were not loaded, setting new ones will cause duplicates')

        self.validate_mark(new_mark)
        lesson = self.get_lesson_by_id(new_mark.lesson_id)
        student = self.get_student_by_id(new_mark.student_id)

        log_message = f'Setting mark {cm(new_mark.value, color=color.Red)} for {student} at {lesson}'

        cached_mark = self._marks_cache.get(lesson_id=new_mark.lesson_id, student_id=new_mark.student_id)
        if cached_mark:
            if cached_mark.value == new_mark.value:
                log.info(f'{log_message}: already set')
                return
            if cached_mark.value < new_mark.value:
                self._update_mark(new_mark)
            else:
                log.error(f'{log_message}: changed mark, already have {new_mark.value}')
                raise RuntimeError('Seems to have broken mark')
        else:
            log.info(log_message)

        rounded_raw_data = new_mark.control_form.rounded_raw_data

        grade_system_id = int(rounded_raw_data['grade_system_id'])
        rounded_raw_data.update({
            'fromServer': False,
            'parentResource': None,
            'reqParams': None,
            'restangularCollection': False,
            'restangularized': True,
            'route': ApiUrl.CONTROL_FORMS,
            'selected': True,
        })

        request = {
          'comment': new_mark.comment,
          'controlForm': rounded_raw_data,
          'control_form_id': rounded_raw_data['id'],
          'grade_origins': [{'grade_origin': new_mark.value, 'grade_system_id': grade_system_id}],
          'grade_system_id': grade_system_id,
          'grade_system_name': rounded_raw_data['grade_system']['name'],
          'grade_system_type': rounded_raw_data['grade_system']['type'],
          'is_approve': False,
          'is_criterion': False,
          'is_exam': False,
          'is_point': new_mark.is_point,
          'pointDate': new_mark.point_date_strange,
          'point_date': new_mark.point_date_patched,
          'schedule_lesson_id': new_mark.lesson_id,
          'showComment': new_mark.show_comment,
          'student_profile_id': new_mark.student_id,
          'valuesByIds': {str(grade_system_id): new_mark.value},
          'weight': new_mark.control_form.weight,
        }
        response = self.authorized_client.post(ApiUrl.MARKS_POST.format(teacher_id=self.teacher_id), json_data=request)
        mark_id = response['id']
        if isinstance(mark_id, int) and mark_id > 0:
            log.info(f'Set mark ok: {mark_id}')
        else:
            raise RuntimeError('Could not set mark')

    def _update_mark(self, new_mark: NewMark):
        raise NotImplementedError(f'Could not update mark to {new_mark}')
        # https://dnevnik.mos.ru/core/api/marks/1188507628?pid=15033420

        self.validate_mark(new_mark)
        lesson = self.get_lesson_by_id(lesson_id)
        student = self.get_student_by_id(student_id)

        log_message = f'Updating mark {cm(value, color=color.Red)} for {student} at {lesson}'
        log.info(log_message)

        rounded_raw_data = new_mark.control_form.rounded_raw_data

        grade_system_id = int(rounded_raw_data['grade_system_id'])
        control_form_id = rounded_raw_data['id']
        rounded_raw_data.update({
            'fromServer': False,
            'parentResource': None,
            'reqParams': None,
            'restangularCollection': False,
            'restangularized': True,
            'route': ApiUrl.CONTROL_FORMS,
            'selected': True,
        })

        request = {
          'comment': comment,
          'controlForm': rounded_raw_data,
          'control_form_id': control_form_id,
          'grade_origins': [{ 'grade_origin': value, 'grade_system_id': grade_system_id}],
          'grade_system_id': grade_system_id,
          'grade_system_name': rounded_raw_data['grade_system']['name'],
          'grade_system_type': rounded_raw_data['grade_system']['type'],
          'is_approve': False,
          'is_criterion': False,
          'is_exam': False,
          'is_point': new_mark.is_point,
          'pointDate': new_mark.point_date_strange,
          'point_date': new_mark.point_date_patched,
          'schedule_lesson_id': new_mark.lesson_id,
          'showComment': new_mark.show_comment,
          'student_profile_id': student_id,
          'valuesByIds': {str(grade_system_id): value},
          'weight': new_mark.control_form.weight,

          # some additional fields
          'id': mark_id,
          'name': str(value),
        }

        response = self.authorized_client.put(
            ApiUrl.MARKS_PUT.format(mark_id=mark_id, teacher_id=self.teacher_id),
            json_data=request,
        )
        assert response['id'] == mark_id
        assert int(response['name']) == value

    def delete_mark(self):
        # curl 'https://dnevnik.mos.ru/core/api/marks/1188480155?pid=15033420' -X DELETE
        pass

    def get_control_forms(self, subject_id, grade, log_forms: bool) -> dict:
        education_level_id = EDUCATION_LEVELS[grade]
        key = (grade, subject_id)
        if self._control_forms.get(key) is None:
            log.info(f'Loading available control forms for grade {grade} subject {subject_id}')
            params = {
                'academic_year_id': self.get_current_year().year_id,
                'education_level_id': education_level_id,
                'page': 1,
                'per_page': CONTROL_FORMS_LIMIT,
                'pid': self.teacher_id,
                'subject_id': subject_id,
                'with_grade_system': True,
            }
            data = self.authorized_client.get(ApiUrl.CONTROL_FORMS, params)

            control_forms = {}
            for item in data:
                if item['deleted_at']:
                    continue
                control_form = ControlForm(item)
                control_forms[control_form.name] = control_form
                if log_forms:
                    log.info(f'  {control_form}')

            assert 1 <= len(control_forms) < CONTROL_FORMS_LIMIT
            self._control_forms[key] = control_forms
            log.info(f'Loaded {len(control_forms)} active control forms for grade {grade} subject {subject_id}')
        return self._control_forms[key]


# curl 'https://dnevnik.mos.ru/core/api/lesson_comments?pid=15033420'  --data-raw $'{"schedule_lesson_id":221224612,"student_id":2890790,"comment":"\u041e","teacher_id":15033420,"subject_id":56}'