# see https://github.com/search?q=dnevnik.mos.ru&type=repositories
import attr
import datetime
import re
import requests
import json
import datetime
from typing import Optional, List

import logging
log = logging.getLogger(__name__)

from library.logging import colorize_json, cm, color
import library.secrets


@attr.s
class Year:
    id: int = attr.ib()
    name: str = attr.ib()
    begin_date: str = attr.ib()
    end_date: str = attr.ib()
    calendar_id: int = attr.ib()
    current_year: bool = attr.ib()


BASE_URL = 'https://dnevnik.mos.ru'
MARKS_DATE_FMT = '%d.%m.%Y'
SCHEDULE_DATE_FMT = '%Y-%m-%d'
EDUCATION_LEVELS = {
    11: 3,
    10: 3,
    9: 2,
}
MARKS_LIMIT = 1000
CONTROL_FORMS_LIMIT = 100
VALID_MARKS = [2, 3, 4, 5]


class ApiUrl:
    GROUPS = '/jersey/api/groups'
    SCHEDULE_ITEMS = '/jersey/api/schedule_items'
    ACADEMIC_YEARS = '/core/api/academic_years'
    TEACHER_PROFILES = '/core/api/teacher_profiles/{teacher_id}'
    STUDENT_PROFILES = '/core/api/student_profiles'
    ATTENDANCES = '/core/api/attendances?pid={teacher_id}'
    MARKS_GET = '/core/api/marks'
    MARKS_POST = '/core/api/marks?pid={teacher_id}'
    MARKS_PUT = '/core/api/marks/{mark_id}?pid={teacher_id}'
    CONTROL_FORMS = '/core/api/control_forms'

    LMS_LOGIN = '/lms/api/sessions'
    LMS_LOGOUT = '/lms/api/sessions?authentication_token={auth_token}'


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
        self.group_ids = [group['id'] for group in data['groups']]
        self.class_unit_id = data['class_unit']['id']

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
        self.group_id = data['group_id']
        self._subject_id = data['subject_id']
        self._timestamp = datetime.datetime.strptime(self._iso_date_time, '%Y-%m-%dT%H:%M:00.000')

        self.class_unit_id = data['class_unit_id']
        self.group_name = data['group_name']
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
        self.name = data['name']
        self.weight = data['weight']

        self._raw_data = data

        control_form_str = json.dumps(data)
        control_form_str = control_form_str.replace('.0', '')
        self.rounded_raw_data = json.loads(control_form_str)

    def __str__(self):
        return f'active control form [{cm(self.weight, color=color.Green)}] {cm(self.name, color=color.Yellow)}'


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

    @value.validator
    def is_valid(self, attribute, mark_value):
        if mark_value not in VALID_MARKS:
            raise ValueError(f'Mark value {mark_value} is invalid')

    @property
    def is_point(self):
        return self.point_date is not None

    @property
    def point_date_patched(self) -> Optional[str]:
        if self.point_date is None:
            return None

        assert re.match(r'202\d\-\d\d-\d\d', self.point_date)
        return '.'.join([self.point_date[8:], self.point_date[5:7], self.point_date[:4]])

    @property
    def point_date_strange(self) -> Optional[str]:
        if self.point_date is None:
            return library.datetools.NowDelta().After(fmt='%FT%T.000Z', hours=20)

        assert re.match(r'202\d\-\d\d\-\d\d', point_date)
        return f'{new_mark.point_date}T04:12:35.678Z'

    @property
    def show_comment(self) -> bool:
        return self.comment is not None


class AuthorizedClient:
    def __init__(self, *, username: str=None, password: str=None):    
        self._base_url = BASE_URL
        self._login(username=username, password=password)

    def _login(self, username, password):
        log.info('Trying to log in...')
        response = requests.post(
            self.get_full_url(ApiUrl.LMS_LOGIN),
            headers=self._get_headers(add_personal=False),
            json={'login': username, 'password_plain': password}
        ).json()
        self._profile_id = response['profiles'][0]['id']
        self._auth_token = response['authentication_token']
        log.info(f'Got profile_id {self._profile_id} and auth_token of len {len(self._auth_token)} for {username} at login')

    def _logout(self):
        raise RuntimeError('Logout is disabled as it will require login on all devices')

        response = requests.delete(
            self.get_full_url(ApiUrl.LMS_LOGOUT.format(authentication_token=self._auth_token)),
            headers=self._get_headers(add_personal=False)
        ).json()
        if response == {'status': 'ok', 'http_status_code': 200}:
            log.info(f'Logged out')
        else:
            log.error(f'Got during log out: {response}')
            raise RuntimeError('Could not logout')

    def headers(self, add_personal=True):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=utf-8',
            'Origin': self._base_url,
            'Referer': f'{self._base_url}/',
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

        if isinstance(data, dict):
            if data.get('code') == 400:
                raise RuntimeError(f'Got 400: {colorize_json(data)}')
            if data.get('message') == 'Предыдущая сессия работы в ЭЖД завершена. Войдите в ЭЖД заново':
                raise RuntimeError(f'Token is invalid')

        return data

    def get_full_url(self, path):
        assert path.startswith('/'), f'path must start with /, got: {path!r}'
        return f'{self._base_url}{path}'

    def post(self, url: str, json_data: dict):
        full_url = self.get_full_url(url)
        try:
            response = requests.post(full_url, json=json_data, headers=self.headers())
            return self._check_response(response)
        except:
            log.error(f'Error on POST to {full_url} with {colorize_json(json_data)}')
            raise

    def put(self, url: str, json_data: dict):
        full_url = self.get_full_url(url)
        try:
            response = requests.put(full_url, json=json_data, headers=self.headers())
            return self._check_response(response)
        except:
            log.error(f'Error on PUT to {full_url} with {colorize_json(json_data)}')
            raise

    def get(self, url: str, params: dict):
        full_url = self.get_full_url(url)

        str_params = {}
        for key, value in params.items():
            str_params[key] = str(value)

        try:
            response = requests.get(full_url, params=str_params, headers=self.headers())
            return self._check_response(response)
        except:
            log.error(f'Error on GET to {full_url} with str params {colorize_json(str_params)}')
            raise


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
            academic_years = self.authorized_client.get(ApiUrl.ACADEMIC_YEARS, params)
            self._current_year = None
            for item in academic_years:
                year = Year(**item)
                if year.current_year:
                    assert not self._current_year
                    self._current_year = year
            assert self._current_year
            log.info(f'Set current year: {self._current_year}')

        return self._current_year

    def get_teacher_profile(self):
        if self._teacher_profile is None:
            params = {
                'academic_year_id': self.get_current_year().id,
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
                'academic_year_id': self.get_current_year().id,
                'group_ids': ','.join(str(i) for i in self.get_assigned_group_ids()),
                'pid': self.teacher_id,
            }
            groups = self.authorized_client.get(ApiUrl.GROUPS, params)
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
                params = {
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
                }
                student_profiles_data = self.authorized_client.get(ApiUrl.STUDENT_PROFILES, params=params)
                log.info(f'Loaded {len(student_profiles_data)} students for {group!r}')
                for item in student_profiles_data:
                    student_profile = StudentProfile(item)
                    self._all_student_profiles[student_profile._id] = student_profile
        return self._all_student_profiles

    def get_student_by_id(self, student_id: int) -> StudentProfile:
        assert isinstance(student_id, int)
        return self.get_student_profiles()[student_id]

    def get_student_by_name(self, student_name):
        matched = [
            student_profile for student_profile in self.get_student_profiles().values()
            if student_profile.matches(student_name)
        ]
        if len(matched) != 1:
            raise RuntimeError(f'Not found students by name {student_name}: got {matched} matched')
        return matched[0]            

    def get_schedule_item_by_id(self, schedule_item_id: int) -> ScheduleItem:
        assert isinstance(schedule_item_id, int)
        return self._available_lessons_dict[schedule_item_id]

    def set_absent(self, absence: Absence=None):
        student = self.get_student_by_id(absence.student_id)
        schedule_lesson = self.get_schedule_item_by_id(absence.lesson_id)

        request = {
            'absence_reason': None,
            'absence_reason_id': 2,
            'schedule_lesson_id': absence.lesson_id,
            'student_profile_id': absence.student_id,
        }
        result = self.authorized_client.post(ApiUrl.ATTENDANCES.format(teacher_id=self.teacher_id), json_data=request)

        if result.get('created_at'):
            log.info(f'Absense was set for {student} for {schedule_lesson}')
        elif result.get('code') == 403 and result.get('message') == 'Пропуск для выбранного ученика и урока уже существует':
            log.info(f'Absense has already been set for {student} for {schedule_lesson}')
        else:
            log.error(f'Unknown response: {colorize_json(result)}')
            raise RuntimeError('Unknown response')

    def get_schedule_items(self):
        request = {
            'academic_year_id': self.get_current_year().id,
            'from': library.datetools.formatTimestamp(self.from_dt, fmt=SCHEDULE_DATE_FMT),
            'to': library.datetools.formatTimestamp(self.to_dt, fmt=SCHEDULE_DATE_FMT),
            'original': True,
            'page': 1,
            'per_page': 100,
            'pid': self.teacher_id,
            'teacher_id': self.teacher_id,
            'with_group_class_subject_info': True,
        }
        schedule_items_raw = self.authorized_client.get(ApiUrl.SCHEDULE_ITEMS, request)
        for item in schedule_items_raw:
            schedule_item = ScheduleItem(item)
            group = self.get_group_by_id(schedule_item.group_id)
            if group:
                schedule_item.set_group(group)
                self._available_lessons_dict[schedule_item._id] = schedule_item
                yield schedule_item
            else:
                log.warn(f'Skipping schedule item for {cm(schedule_item.group_name, color=color.Red)} as no group found')

    def _get_marks_for_group(self, *, group: StudentsGroup=None, limit: int=MARKS_LIMIT):
        from_date = library.datetools.formatTimestamp(self.from_dt, fmt=MARKS_DATE_FMT)
        to_date = library.datetools.formatTimestamp(self.to_dt, fmt=MARKS_DATE_FMT)
        log.info(f'Getting marks [{from_date}, {to_date}] for {group}')

        params = {
            'created_at_from': from_date,
            'created_at_to': to_date,
            'group_ids': ','.join(str(i) for i in [group._id] + group._subgroup_ids),
            'page': 1,
            'per_page': limit,
            'pid': self.teacher_id,
        }
        marks_items = self.authorized_client.get(ApiUrl.MARKS_GET, params=params)
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

    def validate_mark(self, new_mark: NewMark):
        lesson = self.get_schedule_item_by_id(new_mark.lesson_id)
        student = self.get_student_by_id(new_mark.student_id)

        ok = (lesson.group_id in student.group_ids) or (lesson.class_unit_id == student.class_unit_id)  
        if not ok:
            log.info(f'student: {colorize_json(student._raw_data)}')
            log.info(f'lesson: {colorize_json(lesson._raw_data)}')
            log.error(f'Failed on {student} at {lesson}')
            raise RuntimeError(f'Failed at student check')

    def set_mark(self, new_mark: NewMark):
        if not self._loaded_marks:
            raise RuntimeError('Marks were not loaded, setting new ones will cause duplicates')

        self.validate_mark(new_mark)
        lesson = self.get_schedule_item_by_id(new_mark.lesson_id)
        student = self.get_student_by_id(new_mark.student_id)

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
        lesson = self.get_schedule_item_by_id(schedule_lesson_id)
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
          'schedule_lesson_id': schedule_lesson_id,
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
                'academic_year_id': self.get_current_year().id,
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