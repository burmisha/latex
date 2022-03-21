# see https://github.com/search?q=dnevnik.mos.ru&type=repositories
import attr
import collections
import datetime
import re
import requests
import json
import datetime
from typing import Optional

import logging
log = logging.getLogger(__name__)

from library.logging import colorize_json, cm, color
import library.secrets

Year = collections.namedtuple('Year', ['id', 'name', 'begin_date', 'end_date', 'calendar_id', 'current_year'])

BASE_URL = 'https://dnevnik.mos.ru'
MARKS_DATE_FMT = '%d.%m.%Y'
SCHEDULE_DATE_FMT = '%Y-%m-%d'
EDUCATION_LEVELS = {
    11: 3,
    10: 3,
    9: 2,
}
MARKS_LIMIT = 1000
VALID_MARKS = [2, 3, 4, 5]


class StudentsGroup:
    def __init__(self, data):
        self._id = data['id']
        self._name = data['name']
        self._student_ids = data['student_ids']
        self._subject_name = data['subject_name']
        self._class_unit_ids = data['class_unit_ids']
        self._subgroup_ids = data['subgroup_ids'] or []

        best_name = data['class_unit_name']
        if best_name is None:
            best_name = {
                # 'МЕТ.Физика Бурмистров 5ч. Тех': '10',
                'МЕТ. Физика 11АБ Техн': '11БА',
            }[self._name]
        self._best_name = f'{best_name} {self._subject_name}'

        self._raw_data = data

    def __str__(self):
        class_unit_id_str = ','.join(str(i) for i in self._class_unit_ids)
        return f'group {cm(self._best_name, color=color.Green)}'

    def __repr__(self):
        class_unit_id_str = ','.join(str(i) for i in self._class_unit_ids)
        return ' '.join([
            f'group {cm(self._best_name, color=color.Green)}',
            f'({self._id}, {len(self._student_ids)} students),',
            cm(f'{BASE_URL}/webteacher/study-process/grade-journals/{self._id}', color=color.Cyan),
            # cm(f'{BASE_URL}/manage/journal?group_id={self._id}&class_unit_id={class_unit_id_str}', color=color.Cyan),
        ])


class StudentProfile:
    def __init__(self, data):
        self._id = data['id']
        self._short_name = data['short_name']
        self._raw_data = data

    def __str__(self):
        return f'{cm(self._short_name, color=color.Cyan)}'

    def __repr__(self):
        return f'student {cm(self._short_name, color=color.Cyan)} ({self._id})'

    def matches(self, name: str) -> bool:
        return sorted(self._short_name.lower().split()) == sorted(name.lower().split())


class ScheduleItem:
    def __init__(self, data):
        self._id = data['id']
        self._date = data['date']
        self._iso_date_time = data['iso_date_time']
        self._schedule_id = data['schedule_id']
        self._group_id = data['group_id']
        self._subject_id = data['subject_id']
        self._timestamp = datetime.datetime.strptime(self._iso_date_time, '%Y-%m-%dT%H:%M:00.000')

        self._raw_data = data

    def set_group(self, group):
        self._group = group

    def get_link(self):
        return f'{BASE_URL}/conference/?scheduled_lesson_id={self._id}'

    @property
    def str_time(self):
        return self._timestamp.strftime('%d %B %Y, %A, %H:%M')

    def __lt__(self, other):
        return self._iso_date_time < other._iso_date_time

    def __str__(self):
        return f'lesson {cm(self.str_time, color=color.Yellow)} ({self._id}, {self._group})'

    def __repr__(self):
        return f'Schedule item {cm(self.str_time, color=color.Yellow)} ({self._id}) for {self._group!r}'


class Mark:
    def __init__(self, data):
        self._id = data['id']
        self._value = int(data['name'])
        assert self._value in VALID_MARKS

        self._student_id = data['student_profile_id']
        assert isinstance(self._student_id, int)

        self._lesson_id = data['schedule_lesson_id']
        assert isinstance(self._lesson_id, int)

        self._raw_data = data


    def __str__(self):
        return f'mark {cm(str(self._value), color=color.Red)}'

    def __repr__(self):
        return f'mark {cm(str(self._value), color=color.Red)} for {self._student_id} at {self._lesson_id}'


class MarksCache:
    def __init__(self):
        self._marks = dict()

    def add(self, mark: Mark):
        assert isinstance(mark._lesson_id, int)
        assert isinstance(mark._student_id, int)
        key = (mark._lesson_id, mark._student_id)
        assert key not in self._marks
        self._marks[key] = mark

    def get(self, *, lesson_id: int=None, student_id: int=None):
        assert isinstance(lesson_id, int)
        assert isinstance(student_id, int)
        key = (lesson_id, student_id)
        mark = self._marks.get(key)
        return mark


class ControlForm:
    def __init__(self, data):
        assert not data['deleted_at']
        self._raw_data = data

    def get_name(self):
        return self._raw_data['name']

    def __str__(self):
        weight = self._raw_data['weight']
        name = self._raw_data['name']
        return f'active control form [{weight}] {cm(name, color=color.Yellow)}'


@attr.s
class Absence:
    student_id: int = attr.ib()
    lesson_id: int = attr.ib()


@attr.s
class NewMark:
    lesson_id: int = attr.ib()
    student_id: int = attr.ib()
    value: int = attr.ib()
    comment: Optional[str] = attr.ib()
    point_date: Optional[str] = attr.ib()
    control_form: ControlForm = attr.ib()


class Client:
    def __init__(
        self,
        *,
        username=None,
        password=None,
        from_dt: datetime.datetime=None,
        to_dt: datetime.datetime=None,
    ):
        self._base_url = BASE_URL
        self._login(username=username, password=password)

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

    def _login(self, username, password):
        log.info('Trying to log in...')
        response = requests.post(
            f'{self._base_url}/lms/api/sessions',
            headers=self._get_headers(add_personal=False),
            json={'login': username, 'password_plain': password,
        }).json()
        self._profile_id = response['profiles'][0]['id']
        self._auth_token = response['authentication_token']
        log.info(f'Got profile_id {self._profile_id} and auth_token {self._auth_token} for {username} at login')

    def _logout(self):
        response = requests.delete(
            f'{self._base_url}/lms/api/sessions?authentication_token={self._auth_token}',
            headers=self._get_headers(add_personal=False)
        ).json()
        if response == {'status': 'ok', 'http_status_code': 200}:
            log.debug(f'Logged out')
        else:
            log.error(f'Got during log out: {response}')
            raise RuntimeError('Could not logout')

    @property
    def teacher_id(self):
        return self._profile_id

    def _get_headers(self, add_personal=True):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=utf-8',
            'Origin': BASE_URL,
            'Referer': f'{BASE_URL}/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:83.0) Gecko/20100101 Firefox/83.0',
        }
        if add_personal:
            headers.update({
                'Auth-Token': self._auth_token,
                'Profile-Id': str(self._profile_id),
            })
        return headers

    def _check_response(self, response):
        try:
            data = response.json()
        except:
            log.error(f'Could not load json from {response.text}')
            raise

        if isinstance(data, dict) and data.get('code') == 400:
            raise RuntimeError(f'Got {colorize_json(data)}')
        if isinstance(data, dict) and data.get('message') == 'Предыдущая сессия работы в ЭЖД завершена. Войдите в ЭЖД заново':
            raise RuntimeError(f'Token is invalid')

        return data

    def post(self, url, json_data):
        assert url.startswith('/'), f'url doesn\'t start with /: {url}'
        full_url = f'{self._base_url}{url}'
        try:
            response = requests.post(full_url, json=json_data, headers=self._get_headers())
            response = self._check_response(response)
            log.debug(f'Response from {url}: {response}')
            return response
        except:
            log.error(f'Error on POST to {full_url} with {colorize_json(json_data)}')
            raise

    def put(self, url, json_data):
        assert url.startswith('/'), f'url doesn\'t start with /: {url}'
        full_url = f'{self._base_url}{url}'
        try:
            response = requests.put(full_url, json=json_data, headers=self._get_headers())
            response = self._check_response(response)
            log.debug(f'Response from {url}: {response}')
            return response
        except:
            log.error(f'Error on PUT to {full_url} with {colorize_json(json_data)}')
            raise

    def get(self, url, params):
        assert url.startswith('/'), f'url doesn\'t start with /: {url}'
        str_params = {}
        for key, value in params.items():
            str_params[key] = str(value)

        full_url = f'{self._base_url}{url}'
        try:
            response = requests.get(full_url, params=str_params, headers=self._get_headers())
            response = self._check_response(response)
            log.debug(f'Response from {url}: {response}')
            return response
        except:
            log.error(f'Error on GET to {full_url} with {params}')
            raise

    def get_current_year(self):
        if self._current_year is None:
            academic_years = self.get('/core/api/academic_years', {'pid': self.teacher_id})
            academic_years = [Year(**item) for item in academic_years]
            current_years = [year for year in academic_years if year.current_year]
            assert len(current_years) == 1
            log.info(f'Current year: {current_years[0]}')
            self._current_year = current_years[0]

        return self._current_year

    def get_teacher_profile(self):
        if self._teacher_profile is None:
            self._teacher_profile = self.get(f'/core/api/teacher_profiles/{self.teacher_id}', {
                'academic_year_id': self.get_current_year().id,
                'pid': self.teacher_id,
                'with_assigned_groups': True
            })

        return self._teacher_profile

    def get_groups(self):
        assigned_group_ids = ','.join(str(i) for i in sorted(self.get_teacher_profile()['assigned_group_ids']))
        if self._groups is None:
            groups = self.get('/jersey/api/groups', {
                'academic_year_id': self.get_current_year().id,
                'group_ids': assigned_group_ids,
                'pid': self.teacher_id,
            })
            self._groups = [StudentsGroup(item) for item in groups]
        return self._groups

    def get_group_by_id(self, group_id):
        for group in self.get_groups():
            if group._id == group_id:
                return group

        log.warn(f'No group with id {group_id}')
        return None

    def get_student_profiles(self):
        if self._all_student_profiles is None:
            self._all_student_profiles = {}
            for group in self.get_groups():
                student_profiles_data = self.get('/core/api/student_profiles', params={
                    'academic_year_id': self.get_current_year().id,
                    'class_unit_ids': ','.join(str(i) for i in group._class_unit_ids),
                    'group_ids': ','.join(str(i) for i in [group._id] + group._subgroup_ids),
                    'per_page': 1000,
                    'pid': self.teacher_id,
                    'with_archived_groups': True,
                    'with_deleted': True,
                    'with_final_marks': True,
                    'with_groups': True,
                    'with_home_based': True,
                    'with_lesson_info': True,
                    # 'with_parents': True,
                })
                log.info(f'Loaded {len(student_profiles_data)} students for {group!r}')
                for item in student_profiles_data:
                    student_profile = StudentProfile(item)
                    self._all_student_profiles[student_profile._id] = student_profile
        return self._all_student_profiles

    def get_student_by_id(self, student_id: int) -> StudentProfile:
        assert isinstance(student_id, int)
        return self.get_student_profiles()[student_id]

    def get_student_by_name(self, student_name):
        matched = [student_profile for student_profile in self.get_student_profiles().values() if student_profile.matches(student_name)]
        if len(matched) == 1:
            return matched[0]
        else:
            raise RuntimeError(f'Not found students by name {student_name}: got {matched}')

    def get_schedule_item_by_id(self, schedule_item_id: int) -> ScheduleItem:
        assert isinstance(schedule_item_id, int)
        return self._available_lessons_dict[schedule_item_id]

    def set_absent(self, absence: Absence=None):
        student = self.get_student_by_id(absence.student_id)
        schedule_lesson = self.get_schedule_item_by_id(absence.lesson_id)

        result = self.post(f'/core/api/attendances?pid={self.teacher_id}', {
            'absence_reason': None,
            'absence_reason_id': 2,
            'schedule_lesson_id': absence.lesson_id,
            'student_profile_id': absence.student_id,
        })

        if result.get('created_at'):
            log.info(f'Absense was set for {student} for {schedule_lesson}')
        elif result.get('code') == 403 and result.get('message') == 'Пропуск для выбранного ученика и урока уже существует':
            log.info(f'Absense has already been set for {student} for {schedule_lesson}')
        else:
            log.error(f'Unknown response: {colorize_json(result)}')
            raise RuntimeError('Unknown response')

    def get_schedule_items(self):
        from_date = library.datetools.formatTimestamp(self.from_dt, fmt=SCHEDULE_DATE_FMT)
        to_date = library.datetools.formatTimestamp(self.to_dt, fmt=SCHEDULE_DATE_FMT)
        log.info(f'get_schedule_items from {from_date} to {to_date}')

        schedule_items_raw = self.get('/jersey/api/schedule_items', {
            'academic_year_id': self.get_current_year().id,
            'from': from_date,
            'to': to_date,
            'original': True,
            'page': 1,
            'per_page': 100,
            'pid': self.teacher_id,
            'teacher_id': self.teacher_id,
            'with_group_class_subject_info': True,
            # 'with_lesson_info': True,  # no need
            # 'with_rooms_info': True,  # no need
        })
        for item in schedule_items_raw:
            schedule_item = ScheduleItem(item)
            group = self.get_group_by_id(schedule_item._group_id)
            if group:
                schedule_item.set_group(group)
                self._available_lessons_dict[schedule_item._id] = schedule_item
                yield schedule_item
            else:
                group_name = schedule_item._raw_data['group_name']
                log.warn(f'Skipping schedule item for {cm(group_name, color=color.Red)} as no group found')

    def _get_marks_for_group(
        self,
        *,
        group: StudentsGroup=None,
        limit: int=MARKS_LIMIT,
    ):
        from_date = library.datetools.formatTimestamp(self.from_dt, fmt=MARKS_DATE_FMT)
        to_date = library.datetools.formatTimestamp(self.to_dt, fmt=MARKS_DATE_FMT)
        log.info(f'Getting marks [{from_date}, {to_date}] for {group}')

        marks_items = self.get('/core/api/marks', params={
            'created_at_from': from_date,
            'created_at_to': to_date,
            'group_ids': ','.join(str(i) for i in [group._id] + group._subgroup_ids),
            'page': 1,
            'per_page': limit,
            'pid': self.teacher_id,
        })
        assert len(marks_items) < limit, f'Too many marks: reduce dates or increase limit: {limit}'

        for mark_item in marks_items:
            yield Mark(mark_item)

    def get_all_marks(self):
        marks = []
        for group in self.get_groups():
            for mark in self._get_marks_for_group(group=group):
                self._marks_cache.add(mark)
                marks.append(mark)

        self._loaded_marks = True
        return marks

    def set_mark(self, new_mark: NewMark):
        assert self._loaded_marks, 'Marks were not loaded, setting new ones will cause duplicates'

        lesson = self.get_schedule_item_by_id(new_mark.lesson_id)
        student = self.get_student_by_id(new_mark.student_id)

        try:
            student_group_ids = [group['id'] for group in student._raw_data['groups']]
            assert (lesson._raw_data['group_id'] in student_group_ids) or (student._raw_data['class_unit']['id'] == lesson._raw_data['class_unit_id'])
        except:
            log.info(colorize_json(student._raw_data))
            log.info(colorize_json(lesson._raw_data))
            log.error(f'Failed on {student} at {lesson}')
            raise RuntimeError(f'Failed at student check')

        log_message = f'Setting mark {cm(new_mark.value, color=color.Red)} for {student} at {lesson}'

        cached_mark = self._marks_cache.get(lesson_id=new_mark.lesson_id, student_id=new_mark.student_id)

        if cached_mark:
            if cached_mark._value == new_mark.value:
                log.info(f'{log_message}: already set')
                return
            if cached_mark._value < new_mark.value:
                self._update_mark(new_mark)
            else:
                log.error(f'{log_message}: changed mark, already have {new_mark.value}')
                raise RuntimeError('Seems to have broken mark')
        else:
            log.info(log_message)

        show_comment = (new_mark.comment is not None)

        if new_mark.point_date is None:
            is_point = False
            point_date_patched = None
            point_date_strange = library.datetools.NowDelta().After(fmt='%FT%T.000Z', hours=20)
        else:
            assert isinstance(new_mark.point_date, str)
            assert re.match(r'202\d\-\d\d-\d\d', point_date)
            is_point = True
            point_date_patched = '.'.join([new_mark.point_date[8:], new_mark.point_date[5:7], new_mark.point_date[:4], ])
            point_date_strange = f'{new_mark.point_date}T04:12:35.678Z'
            assert re.match(r'\d\d\.\d\d.202\d', point_date_patched)

        assert new_mark.value in VALID_MARKS, f'{value!r} is not valid mark'

        # TODO: round all floats better
        control_form_str = json.dumps(new_mark.control_form._raw_data)
        control_form_str = control_form_str.replace('.0', '')
        control_form_data = json.loads(control_form_str)

        grade_system_id = int(control_form_data['grade_system_id'])
        grade_system_name = control_form_data['grade_system']['name']
        grade_system_type = control_form_data['grade_system']['type']
        # subject_id = control_form_data['subject_id']  # unused
        # school_id = control_form_data['school_id']  # unused
        control_form_id = control_form_data['id']
        weight = control_form_data['weight']
        control_form_data.update({
            'fromServer': False,
            'parentResource': None,
            'reqParams': None,
            'restangularCollection': False,
            'restangularized': True,
            'route': '/core/api/control_forms',
            'selected': True,
        })

        data = {
          'comment': new_mark.comment,
          'controlForm': control_form_data,
          'control_form_id': control_form_id,
          'grade_origins': [{ 'grade_origin': new_mark.value, 'grade_system_id': grade_system_id}],
          'grade_system_id': grade_system_id,
          'grade_system_name': grade_system_name,
          'grade_system_type': grade_system_type,
          'is_approve': False,
          'is_criterion': False,
          'is_exam': False,
          'is_point': is_point,
          'pointDate': point_date_strange,
          'point_date': point_date_patched,
          'schedule_lesson_id': new_mark.lesson_id,
          'showComment': show_comment,
          'student_profile_id': new_mark.student_id,
          'valuesByIds': {str(grade_system_id): new_mark.value},
          'weight': weight,
        }
        response = self.post(f'/core/api/marks?pid={self.teacher_id}', json_data=data)
        mark_id = response['id']
        if isinstance(mark_id, int) and mark_id > 0:
            log.info(f'Set mark ok: {mark_id}')
        else:
            raise RuntimeError('Could not set mark')

    def _update_mark(self, new_mark: NewMark):
        raise NotImplementedError(f'Could not update mark to {new_mark}')
        # https://dnevnik.mos.ru/core/api/marks/1188507628?pid=15033420
        assert isinstance(control_form, ControlForm)

        lesson = self.get_schedule_item_by_id(schedule_lesson_id)
        assert lesson

        student = self.get_student_by_id(student_id)
        assert student

        try:
            student_group_ids = [group['id'] for group in student._raw_data['groups']]
            assert (lesson._raw_data['group_id'] in student_group_ids) or (student._raw_data['class_unit']['id'] == lesson._raw_data['class_unit_id'])
        except:
            log.info(colorize_json(student._raw_data))
            log.info(colorize_json(lesson._raw_data))
            log.error(f'Failed on {student} at {lesson}')
            raise RuntimeError(f'Failed at student check')

        log_message = f'Updating mark {cm(value, color=color.Red)} for {student} at {lesson}'
        log.info(log_message)

        if comment is None:
            show_comment = False
        else:
            assert isinstance(comment, str)
            show_comment = True

        if point_date is None:
            is_point = False
            point_date_patched = None
            point_date_strange = library.datetools.NowDelta().After(fmt='%FT%T.000Z', hours=20)
        else:
            assert isinstance(point_date, str)
            assert re.match(r'202\d\-\d\d-\d\d', point_date)
            is_point = True
            point_date_patched = '.'.join([point_date[8:], point_date[5:7], point_date[:4], ])
            point_date_strange = f'{point_date}T04:12:35.678Z'
            assert re.match(r'\d\d\.\d\d.202\d', point_date_patched)

        assert value in [2, 3, 4, 5]

        # TODO: round all floats better
        control_form_str = json.dumps(control_form._raw_data)
        control_form_str = control_form_str.replace('.0', '')
        control_form_data = json.loads(control_form_str)

        grade_system_id = int(control_form_data['grade_system_id'])
        grade_system_name = control_form_data['grade_system']['name']
        grade_system_type = control_form_data['grade_system']['type']
        # subject_id = control_form_data['subject_id']  # unused
        # school_id = control_form_data['school_id']  # unused
        control_form_id = control_form_data['id']
        weight = control_form_data['weight']
        control_form_data.update({
            'fromServer': False,
            'parentResource': None,
            'reqParams': None,
            'restangularCollection': False,
            'restangularized': True,
            'route': '/core/api/control_forms',
            'selected': True,
        })

        data = {
          'comment': comment,
          'controlForm': control_form_data,
          'control_form_id': control_form_id,
          'grade_origins': [{ 'grade_origin': value, 'grade_system_id': grade_system_id}],
          'grade_system_id': grade_system_id,
          'grade_system_name': grade_system_name,
          'grade_system_type': grade_system_type,
          'is_approve': False,
          'is_criterion': False,
          'is_exam': False,
          'is_point': is_point,
          'pointDate': point_date_strange,
          'point_date': point_date_patched,
          'schedule_lesson_id': schedule_lesson_id,
          'showComment': show_comment,
          'student_profile_id': student_id,
          'valuesByIds': {str(grade_system_id): value},
          'weight': weight,

          # some additional fields
          'id': mark_id,
          'name': str(value),
        }

        response = self.put(f'/core/api/marks/{mark_id}?pid={self.teacher_id}', json_data=data)
        assert response['id'] == mark_id
        assert int(response['name']) == value

    def delete_mark(self):
        # curl 'https://dnevnik.mos.ru/core/api/marks/1188480155?pid=15033420' -X DELETE
        pass

    def get_control_forms(self, subject_id, grade, log_forms: bool):
        education_level_id = EDUCATION_LEVELS[grade]
        key = (grade, subject_id)
        if self._control_forms.get(key) is None:
            log.info(f'Loading available control forms for grade {grade} subject {subject_id}')
            data = self.get('/core/api/control_forms', {
                'academic_year_id': self.get_current_year().id,
                'education_level_id': education_level_id,
                'page': 1,
                'per_page': 100,
                'pid': self.teacher_id,
                'subject_id': subject_id,
                'with_grade_system': True,
            })
            assert 1 <= len(data) < 100
            control_forms = [ControlForm(item) for item in data if not item['deleted_at']]
            assert control_forms
            self._control_forms[key] = {}
            for control_form in control_forms:
                self._control_forms[key][control_form.get_name()] = control_form
                if log_forms:
                    log.info(f'  {control_form}')
            log.info(f'Loaded {len(self._control_forms[key])} active control forms for grade {grade} subject {subject_id}')
        return self._control_forms[key]


# curl 'https://dnevnik.mos.ru/core/api/lesson_comments?pid=15033420'  --data-raw $'{"schedule_lesson_id":221224612,"student_id":2890790,"comment":"\u041e","teacher_id":15033420,"subject_id":56}'