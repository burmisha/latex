# see https://github.com/search?q=dnevnik.mos.ru&type=repositories`
import requests
import collections
import re
import datetime

import logging
log = logging.getLogger(__name__)

from library.logging import colorize_json, cm
import library.secrets

import locale
locale.setlocale(locale.LC_ALL, ('RU','UTF8'))

Year = collections.namedtuple('Year', ['id', 'name', 'begin_date', 'end_date', 'calendar_id', 'current_year'])


class StudentsGroup:
    def __init__(self, data):
        self._id = data['id']
        self._name = data['name']
        self._student_ids = data['student_ids']
        self._subject_name = data['subject_name']
        self._class_unit_ids = data['class_unit_ids']
        self._subgroup_ids = data['subgroup_ids'] or []
        self._raw_data = data

    def __str__(self):
        class_unit_id_str = ','.join(str(i) for i in self._class_unit_ids)
        return ' '.join([
            f'group {cm(self._name, color="green")} ({self._id}) of {len(self._student_ids)} students, see',
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

    def __str__(self):
        return f'Schedule item {self._id} on {self._timestamp.strftime("%d %B %Y, %A, %H:%M")} for {self._group}'


class Client:
    def __init__(self):
        self._profile_id = 15033420
        self._auth_token = library.secrets.token.dnevnik_mos_ru
        self._base_url = 'https://dnevnik.mos.ru'
        self._current_year = None
        self._teacher_profile = None
        self._groups = None
        self._all_student_profiles = None
        self._available_lessons_dict = {}

    def get_teacher_id(self):
        return self._profile_id

    def _get_headers(self):
        return {
            'Auth-Token': self._auth_token,
            'Profile-Id': str(self._profile_id),
            'Content-Type': 'application/json;charset=utf-8',
        }

    def post(self, url, json_data):
        assert url.startswith('/'), f'url doesn\'t start with /: {url}' 
        full_url = f'{self._base_url}{url}'
        try:
            response = requests.post(full_url, json=json_data, headers=self._get_headers())
            response = response.json()
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
            response = response.json()
            log.debug(f'Response from {url}: {response}')
            if isinstance(response, dict) and response.get('code') == 400:
                raise RuntimeError(f'Got {colorize_json(response)}')
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
                log.info(f'Loaded {len(student_profiles_data)} student profiles for {group._id}')
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
                log.warn(f'Skipping schedule item for {cm(schedule_item._raw_data["group_name"], color="red")}')
        return schedule_items
