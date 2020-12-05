# see https://github.com/search?q=dnevnik.mos.ru&type=repositories
import collections
import datetime
import re
import requests

import logging
log = logging.getLogger(__name__)

from library.logging import colorize_json, cm
import library.secrets

import locale
locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))

Year = collections.namedtuple('Year', ['id', 'name', 'begin_date', 'end_date', 'calendar_id', 'current_year'])


BASE_URL = 'https://dnevnik.mos.ru'

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
            assert self._name == 'МЕТ.Физика Бурмистров 5ч. Тех'
            best_name = '10'
        self._best_name = best_name + " " + self._subject_name

        self._raw_data = data

    def __str__(self):
        class_unit_id_str = ','.join(str(i) for i in self._class_unit_ids)
        return ' '.join([
            f'group {cm(self._best_name, color="green")}',
            f'({self._id}, {len(self._student_ids)} students),',
            cm(f'https://dnevnik.mos.ru/manage/journal?group_id={self._id}&class_unit_id={class_unit_id_str}', color="cyan"),
        ])


class StudentProfile:
    def __init__(self, data):
        self._id = data['id']
        self._short_name = data['short_name']
        self._raw_data = data

    def __str__(self):
        return f'student {self._short_name} ({self._id})'


class ScheduleItem:
    def __init__(self, data):
        self._id = data['id']
        self._date = data['date']  
        self._iso_date_time = data['iso_date_time']  
        self._schedule_id = data['schedule_id']  
        self._group_id = data['group_id']  
        self._timestamp = datetime.datetime.strptime(self._iso_date_time, '%Y-%m-%dT%H:%M:00.000')

        self._raw_data = data

    def set_group(self, group):
        self._group = group

    def log_link(self):
        log.info(f'Link: {BASE_URL}/conference/?scheduled_lesson_id={self._id}')

    def __str__(self):
        return f'Schedule item {cm(self._timestamp.strftime("%d %B %Y, %A, %H:%M"), color="yellow")} ({self._id}) for {self._group}'


class Mark:
    def __init__(self, data):
        self._id = data['id']
        self._name = data['name']
        self._student_profile_id = data['student_profile_id']
        self._schedule_lesson_id = data['schedule_lesson_id']
        assert self._name in ['2', '3', '4', '5']
        self._raw_data = data


class Client:
    def __init__(self, username=None, password=None):
        self._base_url = BASE_URL
        self._login(username=username, password=password)

        self._current_year = None
        self._teacher_profile = None
        self._groups = None
        self._all_student_profiles = None
        self._available_lessons_dict = {}

    def _login(self, username, password):
        response = requests.post(
            f'{self._base_url}/lms/api/sessions',
            headers=self._get_headers(add_personal=False),
            json={'login': username, 'password_plain': password,
        }).json()
        self._profile_id = response['profiles'][0]['id']
        self._auth_token = response['authentication_token']
        log.info(f'Got profile_id {self._profile_id} and auth_token {self._auth_token} for {username}')

    def _logout(self):
        response = requests.delete(
            f'{self._base_url}/lms/api/sessions?authentication_token={self._auth_token}',
            headers=self._get_headers(add_personal=False)
        ).json()
        log.info(f'Got on login: {response}')
        assert response == {'status': 'ok', 'http_status_code': 200}

    def get_teacher_id(self):
        return self._profile_id

    def _get_headers(self, add_personal=True):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=utf-8',
            'Origin': 'https://dnevnik.mos.ru',
            'Referer': 'https://dnevnik.mos.ru/',
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
            log.error('Error on POST to {full_url} with {json_data}')
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
            academic_years = self.get('/core/api/academic_years', {'pid': self.get_teacher_id()})
            academic_years = [Year(**item) for item in academic_years]
            current_years = [year for year in academic_years if year.current_year]
            assert len(current_years) == 1
            log.info(f'Current year: {current_years[0]}')
            self._current_year = current_years[0]

        return self._current_year

    def get_teacher_profile(self):
        if self._teacher_profile is None:
            self._teacher_profile = self.get(f'/core/api/teacher_profiles/{self.get_teacher_id()}', {
                'academic_year_id': self.get_current_year().id,
                'pid': self.get_teacher_id(),
                'with_assigned_groups': True
            })

        return self._teacher_profile

    def get_groups(self):
        assigned_group_ids = ','.join(str(i) for i in sorted(self.get_teacher_profile()['assigned_group_ids']))
        if self._groups is None:
            groups = self.get('/jersey/api/groups', {
                'academic_year_id': self.get_current_year().id,
                'group_ids': assigned_group_ids,
                'pid': self.get_teacher_id(),
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
                    'pid': self.get_teacher_id(),
                    'with_archived_groups': True,
                    'with_deleted': True,
                    'with_final_marks': True,
                    'with_groups': True,
                    'with_home_based': True,
                    'with_lesson_info': True,
                    # 'with_parents': True,
                })
                log.info(f'Loaded {len(student_profiles_data)} students for {group}')
                assert len(student_profiles_data) == len(group._student_ids)
                for item in student_profiles_data:
                    student_profile = StudentProfile(item)
                    self._all_student_profiles[student_profile._id] = student_profile
        return self._all_student_profiles

    def get_student_by_id(self, student_id):
        student_profile = self.get_student_profiles().get(student_id)
        if not student_profile:
            log.warn(f'No student item with id {student_id}')
        return student_profile

    def get_schedule_item_by_id(self, schedule_item_id):
        schedule_item = self._available_lessons_dict.get(schedule_item_id)
        if not schedule_item:
            log.warn(f'No schedule item with id {schedule_item_id}')
        return schedule_item

    def set_absent(self, student_id=None, lesson_id=None):
        student = self.get_student_by_id(student_id)
        assert student is not None
        schedule_lesson = self.get_schedule_item_by_id(lesson_id)
        assert schedule_lesson is not None

        result = self.post(f'/core/api/attendances?pid={self.get_teacher_id()}', {
            'absence_reason': None,
            'absence_reason_id': 2,
            'schedule_lesson_id': lesson_id,
            'student_profile_id': student_id,
        })
        if result.get('created_at'):
            log.info(f'Absense was set for {student} for {schedule_lesson}')
        elif result.get('code') == 403 and result.get('message') == 'Пропуск для выбранного ученика и урока уже существует':
            log.info(f'Absense has already been set for {student} for {schedule_lesson}')
        else:
            log.error(f'Unknown response: {colorize_json(result)}')
            raise RuntimeError('Unknown response')

    def get_schedule_items(self, from_date=None, to_date=None):
        log.info(f'get_schedule_items from {from_date} to {to_date}')
        assert re.match(r'20\d\d-\d{2}-\d{2}', from_date), f'Invalid from_date format: {from_date}'
        assert re.match(r'20\d\d-\d{2}-\d{2}', to_date), f'Invalid to_date format: {to_date}'
        schedule_items_raw = self.get('/jersey/api/schedule_items', {
            'academic_year_id': self.get_current_year().id, 
            'from': from_date,
            'to': to_date,
            'original': True,
            'page': 1,
            'per_page': 100,
            'pid': self.get_teacher_id(),
            'teacher_id': self.get_teacher_id(),
            'with_group_class_subject_info': True,
            # 'with_lesson_info': True,  # no need
            # 'with_rooms_info': True,  # no need
        })
        schedule_items = []

        for item in schedule_items_raw:
            schedule_item = ScheduleItem(item)
            group = self.get_group_by_id(schedule_item._group_id)
            if group is not None:
                schedule_item.set_group(group)
                schedule_items.append(schedule_item)
                self._available_lessons_dict[schedule_item._id] = schedule_item
            else:
                log.warn(f'Skipping schedule item for {cm(schedule_item._raw_data["group_name"], color="red")} as no group found')
        return schedule_items

    def get_marks(self, from_date=None, to_date=None, group=None):
        log.info(f'Getting marks [{from_date}, {to_date}] for {group}')
        assert re.match(r'\d{2}.\d{2}.20\d{2}', from_date), f'Invalid from_date format: {from_date}'
        assert re.match(r'\d{2}.\d{2}.20\d{2}', to_date), f'Invalid to_date format: {to_date}'
        marks_items = self.get('/core/api/marks', params={
            'created_at_from': from_date,
            'created_at_to': to_date,
            'group_ids': ','.join(str(i) for i in [group._id] + group._subgroup_ids),
            'page': 1,
            'per_page': 1000,
            'pid': self.get_teacher_id(),
        })
        assert len(marks_items) < 1000, 'Too many marks: reduce dates or increase limit'
        marks = [Mark(item) for item in marks_items]
        marks.sort(key=lambda x: (x._schedule_lesson_id, x._student_profile_id))
        return marks
