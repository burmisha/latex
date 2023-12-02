from fuzzywuzzy import process, fuzz

import collections
import datetime
import re

import library.files
import library.location
import library.picker

from typing import Optional

import logging
log = logging.getLogger(__name__)

from library.logging import cm, color


class Pupil(object):
    def __init__(self, name=None, surname=None):
        self._name = name
        self._surname = surname
        self._mesh_name = None

    @property
    def name(self):
        return self._name

    @property
    def surname(self):
        return self._surname

    def set_mesh_name(self, mesh_name):
        self._mesh_name = mesh_name

    def get_paper_name(self):
        return f'{self._name} {self._surname}'

    def get_mesh_name(self):
        if self._mesh_name is None:
            return f'{self._surname} {self._name}'
        else:
            return self._mesh_name

    def GetFullName(self, surnameFirst=False):
        if surnameFirst:
            parts = [self._surname, self._name]
        else:
            parts = [self._name, self._surname]
        return ' '.join(part for part in parts if part)

    def GetRandomSeedPart(self):
        return f'{self._name} {self._surname}'

    def __str__(self):
        return f'{self._name} {self._surname}'

    def __lt__(self, other):
        if self._surname < other._surname:
            return True
        elif self._surname == other._surname and self._name < other._name:
            return True
        else:
            return False

class IndexType:
    ALPHA = 'alpha'
    DIGIT = 'digit'


class Pupils(object):
    SEARCH_MIN_THRESHOLD = 54
    SEARCH_DELTA_MULTIPLIER = 0.85

    def __init__(self, pupils_id=None, pupils=[], letter=None, grade=None, year=None):
        assert isinstance(grade, int)
        assert 6 <= grade <= 11
        assert 2010 <= year < 2099

        self._id = pupils_id
        self._pupils_list = pupils
        self._me = Pupil(name='Михаил', surname='Бурмистров')
        self.Letter = letter
        self.Grade = grade
        self.Year = f'{year}-{year-2000+1}'
        self.start_year = year
        try:
            int(self.Letter)
            self.LatinLetter = f'-{self.Letter}'
            self._index_type = IndexType.DIGIT
        except ValueError:
            self.LatinLetter = {
                'А1': 'A1',
                'А': 'A',
                'Б': 'B',
                'В': 'V',
                'Г': 'G',
                'Т': 'T',
                'Л': 'L',
                'М': 'M',
                'АБ': 'AB',
                'БА': 'BA',
            }[self.Letter]
            self._index_type = IndexType.ALPHA
        except Exception:
            raise
        self._name_lookup = dict([
            (f'{pupil.name} {pupil.surname}', pupil)
            for pupil in self.Iterate()
        ])

    def get_path(self, *args, archive=True):
        if archive:
            suffix = ' - private'
        else:
            suffix = ''

        grade_suffix = {
            IndexType.DIGIT: f'-{self.Letter}',
            IndexType.ALPHA: self.Letter,
        }[self._index_type]
        return library.location.udr(
            f'{self.Grade} класс',
            f'{self.Year} {self.Grade}{grade_suffix} Физика{suffix}',
            *args,
        )

    def Iterate(self, only_me=False):
        yield self._me
        if not only_me:
            for pupil in self._pupils_list:
                yield pupil

    def FindByName(self, name, use_raw_if_missing=True):
        best_keys = process.extract(name, self._name_lookup.keys(), limit=2, scorer=fuzz.token_sort_ratio)
        assert 1 <= len(best_keys) <= 2
        best_key = None

        if best_keys[0][1] >= self.SEARCH_MIN_THRESHOLD:
            if len(best_keys) == 1:
                best_key = best_keys[0][0]
            elif len(best_keys) == 2 and best_keys[1][1] < self.SEARCH_DELTA_MULTIPLIER * best_keys[0][1]:
                best_key = best_keys[0][0]

        pupil = None
        if best_key:
            pupil = self._name_lookup[best_key]
        elif use_raw_if_missing:
            if ' ' in name:
                new_name, new_surname = name.split(' ', 1)
            else:
                new_name, new_surname = name, ''
            pupil = Pupil(name=new_name, surname=new_surname)
            log.warn(f'Could not find pupil by name {name!r} in {self._id}, candidates are {best_keys}, using {pupil}')
        else:
            log.error(f'Could not find pupil by name {name!r} in {self._id}, candidates are {best_keys}')
            raise RuntimeError(f'Could not find pupil {name}')
        log.debug(f'Search pupil by name {name!r} in {self._id}: {best_keys} → {pupil}')
        return pupil

    def GetRandomSeedPart(self):
        return '{}-{}'.format(self.Grade, self.Letter)

    def __str__(self):
        return f'{len(self._pupils_list)} pupils from {self._id}'

    def get_class_letter(self):
        if self.Letter:
            return '{}«{}»'.format(self.Grade, self.Letter)
        else:
            return self.Grade

    @property
    def is_active(self) -> bool:
        today = datetime.datetime.now().strftime('%F')
        return get_study_year(today) == self.start_year


class NamesPicker:
    def __init__(self, pupils_file):
        config = library.files.load_yaml_data(pupils_file)
        cfg = collections.defaultdict(list)
        for row in config:
            parts = [part.strip() for part in row.split(',')]
            name = parts[0]
            for class_name in parts[1:]:
                assert name not in cfg[class_name]
                cfg[class_name].append(name)

        self._key_picker = library.picker.KeyPicker(key=library.picker.letters_key)
        for pupils_id, names in cfg.items():
            pupils_list = []
            for fullName in names:
                name, surname = fullName.split(' ', 1)
                pupils_list.append(Pupil(name=name, surname=surname))

            start_year, class_id, letter = pupils_id.split('-')
            grade = int(''.join(s for s in class_id if s.isdigit()))
            pupils = Pupils(
                pupils_id=pupils_id,
                pupils=pupils_list,
                letter=letter,
                grade=grade,
                year=int(start_year),
            )
            log.info(f'Adding class for key {cm(pupils_id, color=color.Green)}')
            self._key_picker.add(pupils_id, pupils)

    def get(self, key):
        return self._key_picker.get(key)


names_picker = NamesPicker('pupils.yaml')


def get_study_year(date_part: str) -> int:
    year = int(date_part[:4])
    if re.match(r'20\d\d[\.-]\d{2}[\.-]\d{2}', date_part):
        if int(date_part[5:7]) <= 8:  # Aug
            year -= 1
    elif f'{year}' == date_part:
        pass
    elif f'{year}-{year+1}' == date_part:
        pass
    elif f'{year}-' + f'{year+1}'[2:] == date_part:
        pass
    else:
        raise RuntimeError(f'Could not guess class from {value}: {date_part} {class_part} {year}')
    return year


assert get_study_year('2020-09-01') == 2020
assert get_study_year('2021-09-01') == 2021
assert get_study_year('2021-08-31') == 2020
assert get_study_year('2021') == 2021
assert get_study_year('2021-22') == 2021
assert get_study_year('2021-2022') == 2021


def get_class_from_string(value, addMyself=False, onlyMe=False) -> Optional[Pupils]:
    assert isinstance(value, str), f'Trying to search not by str: {value!r}'

    search_by_id = names_picker.get(value)
    if search_by_id:
        return search_by_id

    value = value.split('.', 1)[0]
    matches = re.match(r'^(20\d{2}-\d{2}-\d{2})-(\d+)\b', value)
    if matches:
        study_year = get_study_year(matches.group(1))
        class_part = matches.group(2)
        key = f'{study_year} {class_part}'
    elif ' ' in value:
        parts = value.split()
        date_part, class_part = parts[0], parts[1]
        study_year = get_study_year(date_part)

        if (len(parts)) >= 3 and (len(parts[2]) <= 2):
            key = f'{study_year} {class_part} {parts[2]}'
        else:
            key = f'{study_year} {class_part}'
    else:
        raise ValueError(f'Invalid value to search class: {value!r}')

    pupils = names_picker.get(key)
    if not pupils:
        log.info(f'Could not find pupils by key {value!r}: got key {key!r}')
        return None

    log.debug(f'Got {pupils} (search by: {key!r})')
    return pupils


assert get_class_from_string('2019 11Т')
assert get_class_from_string('2020 9М Физика')
assert get_class_from_string('2022-01-31 11 БА')
assert get_class_from_string('2022-01-31 11БА')
assert get_class_from_string('2022-01-31 11 Б')
assert get_class_from_string('2022-01-31 11Б')
assert get_class_from_string('2021-04-30 10')._id == '2020-10-АБ'
assert get_class_from_string('2021-04-30 10.docx')._id == '2020-10-АБ'
assert get_class_from_string('2021-04-30 10 класс.docx')._id == '2020-10-АБ'
assert get_class_from_string('2021-06-30 10 - занятие.docx')._id == '2020-10-АБ'
assert get_class_from_string('2021-06-30-10')._id == '2020-10-АБ'
assert get_class_from_string('2021-06-30-10 - занятие')._id == '2020-10-АБ'
assert get_class_from_string('2022-09-01 10-0')._id == '2022-10-0'
assert get_class_from_string('2022-23 10-0')._id == '2022-10-0'
assert get_class_from_string('2022-09-01 10-0').get_path().endswith('/10 класс/2022-23 10-0 Физика - private')
assert get_class_from_string('2022-01-31 11Б').Year == '2021-22'
assert get_class_from_string('2022-09-01 10-0').Year == '2022-23'
assert get_class_from_string('2022-01-31 11Б').is_active is False
assert get_class_from_string('2022-09-01 10-0').is_active is False
assert get_class_from_string('2020-9-М').is_active is False
