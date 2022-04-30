import datetime
import re
import attr
from typing import Optional, List
from library.dnevnik.client import BASE_URL
from library.logging import cm, color
import json

VALID_MARKS = [2, 3, 4, 5]


@attr.s
class Year:
    year_id: int = attr.ib()
    name: str = attr.ib()
    begin_date: str = attr.ib()
    end_date: str = attr.ib()
    calendar_id: int = attr.ib()
    current_year: bool = attr.ib()


@attr.s
class Group:
    """
        Группа — это учебная группа в духе «10 класс — Алгебра».
        Класс — это класс в духе «10А класс».
        Таким образом, одному классу соответствует много групп (по всем предметам).
        Но и в одной группе могут оказаться ученики разных классов (мета-группы).
    """
    group_id: int = attr.ib()
    name: str = attr.ib()
    student_ids: List[int] = attr.ib()
    subject_name: str = attr.ib()
    class_unit_ids: List[int] = attr.ib()
    subgroup_ids: List[int] = attr.ib()
    raw_data: dict = attr.ib()

    @property
    def best_name(self) -> str:
        name = self.raw_data['class_unit_name']
        if name is None:
            name = {
                # 'МЕТ.Физика Бурмистров 5ч. Тех': '10',
                'МЕТ. Физика 11АБ Техн': '11БА',
            }[self.name]
        return f'{name} {self.subject_name}'

    @property
    def class_unit_id_str(self):
        return ','.join(str(i) for i in self.class_unit_ids)

    @property
    def all_groups_ids(self) -> str:
        return ','.join(str(i) for i in [self.group_id] + self.subgroup_ids)

    def __str__(self):
        return f'group {cm(self.best_name, color=color.Green)}'

    def __repr__(self):
        return ' '.join([
            f'group {cm(self.best_name, color=color.Green)}',
            f'({self.group_id}, {len(self.student_ids)} students),',
            cm(f'{BASE_URL}/webteacher/study-process/grade-journals/{self.group_id}', color=color.Cyan),
            # cm(f'{BASE_URL}/manage/journal?group_id={self.group_id}&class_unit_id={self.class_unit_id_str}', color=color.Cyan),
        ])


@attr.s
class Student:
    student_id: int = attr.ib()
    short_name: int = attr.ib()
    raw_data: dict = attr.ib()
    group_ids: List[int] = attr.ib()
    class_unit_id: int = attr.ib()

    def __str__(self):
        return f'{cm(self.short_name, color=color.Cyan)}'

    def __repr__(self):
        return f'student {cm(self.short_name, color=color.Cyan)} ({self.student_id})'

    def matches(self, name: str) -> bool:
        return sorted(self.short_name.lower().split()) == sorted(name.lower().split())


@attr.s
class Lesson:
    lesson_id: int = attr.ib()
    group_id: int = attr.ib()
    subject_id: int = attr.ib()
    class_unit_id: Optional[int] = attr.ib()
    iso_date_time: str = attr.ib()
    raw_data: dict = attr.ib()

    @property
    def link(self):
        return f'{BASE_URL}/conference/?scheduled_lesson_id={self.lesson_id}'

    @property
    def dt(self):
        return datetime.datetime.strptime(self.iso_date_time, '%Y-%m-%dT%H:%M:00.000')

    @property
    def human_time(self):
        return self.dt.strftime('%d %B %Y, %A, %H:%M')

    def __str__(self):
        return f'lesson {cm(self.human_time, color=color.Yellow)} ({self.lesson_id})'


@attr.s
class Mark:
    mark_id: int = attr.ib()
    value: str = attr.ib()
    student_id: int = attr.ib()
    lesson_id: int = attr.ib()
    raw_data: dict = attr.ib()

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


@attr.s
class ControlForm:
    name: str = attr.ib()
    weight: int = attr.ib()
    raw_data: dict = attr.ib()

    @raw_data.validator
    def is_valid(self, attribute, value):
        if value['deleted_at']:
            raise ValueError(f'ControlForm is deleted')

    @property
    def rounded_raw_data(self):
        control_form_str = json.dumps(self.data)
        control_form_str = control_form_str.replace('.0', '')
        return json.loads(control_form_str)

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
