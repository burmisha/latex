import datetime
import re
import attr
from typing import Optional, Any, List
from library.dnevnik.client import BASE_URL
from library.logging import cm, color
import json

VALID_MARKS = [2, 3, 4, 5]


@attr.s
class Year:
    id: int = attr.ib()
    name: str = attr.ib()
    begin_date: str = attr.ib()
    end_date: str = attr.ib()
    calendar_id: int = attr.ib()
    current_year: bool = attr.ib()


class Group:
    def __init__(self, data):
        self.group_id = data['id']
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
            f'({self.group_id}, {len(self._student_ids)} students),',
            cm(f'{BASE_URL}/webteacher/study-process/grade-journals/{self.group_id}', color=color.Cyan),
            # cm(f'{BASE_URL}/manage/journal?group_id={self.group_id}&class_unit_id={class_unit_id_str}', color=color.Cyan),
        ])


@attr.s
class Student:
    student_id: int = attr.ib()
    short_name: int = attr.ib()
    raw_data: Any = attr.ib()
    group_ids: List[int] = attr.ib()
    class_unit_id: int = attr.ib()

    def __str__(self):
        return f'{cm(self.short_name, color=color.Cyan)}'

    def __repr__(self):
        return f'student {cm(self.short_name, color=color.Cyan)} ({self.student_id})'

    def matches(self, name: str) -> bool:
        return sorted(self.short_name.lower().split()) == sorted(name.lower().split())


class Lesson:
    def __init__(self, data):
        self.lesson_id = data['id']
        self._date = data['date']
        self._iso_date_time = data['iso_date_time']
        self._schedule_id = data['schedule_id']
        self.group_id = data['group_id']
        self._subject_id = data['subject_id']
        self._timestamp = datetime.datetime.strptime(self._iso_date_time, '%Y-%m-%dT%H:%M:00.000')

        self.class_unit_id = data['class_unit_id']
        self.group_name = data['group_name']
        self.raw_data = data

    def set_group(self, group):
        self._group = group

    def get_link(self):
        return f'{BASE_URL}/conference/?scheduled_lesson_id={self.lesson_id}'

    @property
    def str_time(self):
        return self._timestamp.strftime('%d %B %Y, %A, %H:%M')

    def __lt__(self, other):
        return self._iso_date_time < other._iso_date_time

    def __str__(self):
        return f'lesson {cm(self.str_time, color=color.Yellow)} ({self.lesson_id}, {self._group})'

    def __repr__(self):
        return f'Schedule item {cm(self.str_time, color=color.Yellow)} ({self.lesson_id}) for {self._group!r}'


@attr.s
class Mark:
    mark_id: int = attr.ib()
    value: str = attr.ib()
    student_id: int = attr.ib()
    lesson_id: int = attr.ib()
    raw_data: Any = attr.ib()

    @value.validator
    def is_valid(self, attribute, mark_value):
        if mark_value not in VALID_MARKS:
            raise ValueError(f'Mark value {mark_value} is invalid')

    def __str__(self):
        return f'mark {cm(str(self.value), color=color.Red)}'

    def __repr__(self):
        return f'mark {cm(str(self.value), color=color.Red)} for {self.student_id} at {self.lesson_id}'


class MarksCache:
    def __init__(self):
        self._marks = dict()

    def add(self, mark: Mark):
        assert isinstance(mark.lesson_id, int)
        assert isinstance(mark.student_id, int)
        key = (mark.lesson_id, mark.student_id)
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
