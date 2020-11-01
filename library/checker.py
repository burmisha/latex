import library.pupils

import Levenshtein

import re
import os
import zipfile
import csv
from io import StringIO
import collections

import logging
log = logging.getLogger(__name__)


class NameLookup:
    def __init__(self, names):
        assert names
        for name in names:
            assert name
        self._names = names
        self._unique_names = {}

        counter = collections.Counter()
        for name in self._names:
            parts = sorted(self._split(name))
            parts.append(' '.join(parts))
            for part in parts:
                counter[part] += 1
                self._unique_names[part] = name

        for part, count in sorted(counter.items()):
            if count != 1:
                log.info(f'{part} has {count} duplicates')
                del self._unique_names[part]


    def _split(self, line):
        parts = re.split(r'\s|-|,|;|\.', line)
        return [p.strip() for p in parts if len(p) >= 2]
    

    def _distance(self, name_1, name_2):
        name_1_strip = name_1.strip().lower()
        name_2_strip = name_2.strip().lower()
        assert len(name_1_strip) >= 2
        assert len(name_2_strip) >= 2
        distance = Levenshtein.distance(name_1_strip, name_2_strip)
        return distance

    def Find(self, candidate_name):
        best_matches = set()
        best_match_distance = None
        for part in sorted(self._split(candidate_name)):
            for key, name in sorted(self._unique_names.items()):
                distance = self._distance(part, key)
                if best_match_distance is None or distance < best_match_distance:
                    best_matches = set([name])
                    best_match_distance = distance
                elif distance == best_match_distance:
                    best_matches.add(name)

        if best_match_distance is None or best_match_distance >= 2 or len(best_matches) != 1:
            log.warn(f'Could not find name for {candidate_name}: best matches are {best_matches} is bad ({best_match_distance})')
            return None

        return list(best_matches)[0]


class ProperAnswer:
    def __init__(self, canonicRe=None):
        assert not canonicRe.startswith('^')
        assert not canonicRe.endswith('$')
        self._canonic_re = '^{canonicRe}$'

    def IsOk(self, value=None):
        if re.match(self._canonic_re, value):
            return True

        return False


class Checker:
    def __init__(self, csv_file, answers):
        self._csv_file = csv_file

        basename = os.path.basename(self._csv_file)
        class_str = basename.split()[1]
        class_key = 'class-2020-' + ''.join(i for i in class_str if i.isdigit())
        pupils = library.pupils.getPupils(class_key, addMyself=True)
        names = [pupil.GetFullName(surnameFirst=True) for pupil in pupils.Iterate()]
        name_lookup = NameLookup(names)

        answers_count = len(answers)

        assert self._csv_file.endswith('.zip')
        with zipfile.ZipFile(self._csv_file, 'r') as zfile:
            for file in zfile.namelist():
                log.info(f'Got {file!r}')
                data = StringIO(zfile.read(file).decode('utf8'))
                reader = csv.DictReader(data)
                for row in reader:
                    timestamp = row['Timestamp']
                    candidate_name = row['Фамилия Имя']
                    name = name_lookup.Find(candidate_name)
                    candidate_answers = [None for _ in range(answers_count)]
                    additional_fields = {}
                    for key, value in row.items():
                        if key.startswith('Задание '):
                            index = int(key.split(' ')[1]) - 1
                            assert 0 <= index < answers_count
                            candidate_answers[index] = value
                        else:
                            value = value.strip()
                            if value:
                                additional_fields[key] = value
                    log_indices = '\t'.join(str(index) for index in range(1, answers_count + 1))
                    log_answer = '\t'.join(str(answer) for answer in answers)
                    log_candidate_answer = '\t'.join(str(answer) for answer in candidate_answers)
                    log.info(f'''
{candidate_name} → {name}
Index:\t\t{log_indices}
Proper:\t\t{log_answer}
Candidate:\t{log_candidate_answer}
''')

        self._answers = answers

    def Check(self):
        pass
