from fuzzywuzzy import process, fuzz

import collections
import re
import yaml

import library.location
import library.picker

import logging
log = logging.getLogger(__name__)

from library.logging import cm


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


class Pupils(object):
    SEARCH_MIN_THRESHOLD = 55
    SEARCH_DELTA_MULTIPLIER = 0.8

    def __init__(self, pupils_id=None, pupils=[], letter=None, grade=None, year=None):
        self._id = pupils_id
        self._pupils_list = pupils
        self._me = Pupil(name='Михаил', surname='Бурмистров')
        self.Letter = letter
        self.Grade = grade
        assert 2010 <= year < 2099
        self.Year = f'{year}-{year-2000+1}'
        assert isinstance(self.Grade, int)
        assert 6 <= self.Grade <= 11
        self.LatinLetter = {
            'А1': 'A1',
            'А': 'A',
            'Т': 'T',
            'Л': 'L',
            'М': 'M',
            'АБ': 'AB',
        }[self.Letter]
        self._name_lookup = dict([
            (f'{pupil.name} {pupil.surname}', pupil)
            for pupil in self.Iterate()
        ])

    def get_path(self, *args, archive=True):
        if archive:
            suffix = '- private'
        else:
            suffix = '- public'

        return library.location.udr(
            f'{self.Grade} класс',
            f'{self.Year} {self.Grade}{self.Letter} Физика {suffix}',
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


class NamesPicker:
    def __init__(self, pupils_file):
        with open(pupils_file) as f:
            config = yaml.safe_load(f)
        cfg = collections.defaultdict(list)
        for name, classes_names in config.items():
            if name.endswith(' - 2') or name.endswith(' - 3'):
                name = name[:-4]
            for class_name in classes_names:
                assert name not in cfg[class_name]
                cfg[class_name].append(name)

        self._key_picker = library.picker.KeyPicker(key=library.picker.letters_key)
        for pupils_id, names in cfg.items():
            pupils_list = []
            for fullName in names:
                name, surname = fullName.split(' ')
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
            self._key_picker.add(pupils_id, pupils)

    def get(self, key):
        return self._key_picker.get(key)


names_picker = NamesPicker(library.location.root('data', 'pupils.yaml'))


def get_class_from_string(value, addMyself=False, onlyMe=False):
    search_by_id = names_picker.get(value)
    if search_by_id:
        return search_by_id

    assert isinstance(value, str), f'Trying to search not by str: {value}'
    assert ' ' in value, f'No space in class name: {value}'

    parts = value.split()
    date_part, class_part = parts[0], parts[1]

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

    key = f'{year} {class_part}'
    pupils = names_picker.get(key)
    assert pupils

    log.debug(f'Got {pupils} (search by: {key!r})')
    return pupils
