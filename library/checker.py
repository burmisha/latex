import library.pupils
import library.logging

import Levenshtein

import datetime
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
                log.debug(f'{part} has {count} duplicates, will not use')
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
            log.warn(cm(f'Could not find name for {candidate_name}: best matches are {best_matches} is bad ({best_match_distance})', bg='red'))
            return None

        return list(best_matches)[0]


class ProperAnswer:
    def __init__(self, canonicRe=None, value=1):
        canonicRe = canonicRe.strip()
        canonicRe.replace(' ', '\s*')
        assert not canonicRe.startswith('^[\s.;,]*')
        assert not canonicRe.endswith('[\s.;,]*$')
        self._value = value
        self._canonic_re = f'^{canonicRe}$'
        self._printable = str(canonicRe)

    def Printable(self):
        return self._printable

    def Value(self):
        return int(self._value)

    def IsOk(self, value=None):
        if re.match(self._canonic_re, value):
            return True

        return False

cm = library.logging.ColorMessage()


class Checker:
    def __init__(self, csv_file, answers, marks=None):
        self._csv_file = csv_file
        if not marks:
            marks = [None, None, None]
        self._marks = marks
        assert len(self._marks) == 3
        self._proper_answers = []
        for answer in answers:
            if isinstance(answer, str):
                self._proper_answers.append([ProperAnswer(answer)])
            elif isinstance(answer, list):
                self._proper_answers.append(answer)
            else:
                raise RuntimeError(f'Answer {answer} is not supported yet')

        assert self._csv_file.endswith('.csv.zip')
        assert os.path.exists(self._csv_file)
        assert os.path.isfile(self._csv_file)

        basename = os.path.basename(self._csv_file)
        class_str = basename.split()[1]
        class_key = 'class-2020-' + ''.join(i for i in class_str if i.isdigit())
        pupils = library.pupils.getPupils(class_key, addMyself=True)
        names = [pupil.GetFullName(surnameFirst=True) for pupil in pupils.Iterate()]
        self._name_lookup = NameLookup(names)
        self._all_marks = collections.Counter()
        self._all_answers = [collections.Counter() for answer in self._proper_answers]

    def _get_mark(self, result):
        mark = None
        for index, value in enumerate(self._marks,  3):
            if result >= value:
                mark = index
        if any(self._marks) and not mark:
            mark = 2
        self._all_marks[mark] += 1
        return mark

    def _get_canidates(self, row):
        answers_count = len(self._proper_answers)
        candidate_answers = ['' for _ in self._proper_answers]
        additional_fields = {}
        for key, value in row.items():
            value = value.strip()
            if value:
                if key.startswith('Задание '):
                    index = int(key.split(' ')[1]) - 1
                    assert 0 <= index < answers_count
                    candidate_answers[index] = value
                else:
                    if key not in ('Фамилия Имя', 'Timestamp'):
                        additional_fields[key] = value
        return candidate_answers, additional_fields

    def ParseRow(self, row, pupil_filter):
        timestamp = datetime.datetime.strptime(row['Timestamp'], '%Y/%m/%d %H:%M:%S %p GMT+3')
        candidate_name = row['Фамилия Имя']
        name = self._name_lookup.Find(candidate_name)

        if pupil_filter and (not name or pupil_filter.lower() not in name.lower()):
            return

        candidate_answers, additional_fields =self._get_canidates(row)

        log_proper_answers = []
        log_candidate_answers = []
        log_indices = []
        result = 0
        max_result = 0
        for index, (candidate, proper_answers) in enumerate(zip(candidate_answers, self._proper_answers), 1):
            proper_color = None
            max_value = max(ans.Value() for ans in proper_answers)
            max_result += max_value
            best_answer = list(ans for ans in proper_answers if ans.Value() == max_value)[0]
            value = max([answer.Value() for answer in proper_answers if answer.IsOk(candidate)] + [0])

            best_printable = best_answer.Printable()
            result += value
            if value == max_value:
                color = 'green'
            else:
                if value == 0:
                    color = 'red'
                else:
                    color = 'yellow'
                if candidate and len(best_printable) >= 2:
                    proper_color = 'cyan'

            if candidate:
                self._all_answers[index - 1][candidate] += 1

            width = (((max(len(candidate), len(best_printable)) + 1) / 4) + 1)
            fmt = '{:<%d}' % (width * 4)
            log_candidate_answers.append(cm(fmt.format(candidate), color))
            log_proper_answers.append(cm(fmt.format(best_printable), proper_color))
            log_indices.append(fmt.format(str(index)))

        log_candidate_answers = ''.join(log_candidate_answers)
        log_proper_answers = ''.join(log_proper_answers)
        log_indices = ''.join(log_indices)

        mark = self._get_mark(result)
        message = f'''
[{timestamp}] {cm(name, bold=True)} ({candidate_name}): {cm(result, bold=True)} / {max_result} → {cm(mark, bold=True)}
    Task:\t{log_indices}
    Answer:\t{log_proper_answers}
    Form:\t{log_candidate_answers}
'''
        if additional_fields:
            for key, value in sorted(additional_fields.items()):
                message += f'    {key[:10]}...:\t{cm(value, bold=True)}\n'

        log.info(message.lstrip('\n'))
        return name, mark

    def Check(self, pupil_filter):
        results = []
        with zipfile.ZipFile(self._csv_file, 'r') as zfile:
            for file in zfile.namelist():
                log.info(f'Got {file!r}')
                data = StringIO(zfile.read(file).decode('utf8'))
                reader = csv.DictReader(data)
                for row in reader:
                    results.append(self.ParseRow(row, pupil_filter))

        for index, stats in enumerate(self._all_answers, 1):
            log.info(f'Task {index}: {stats.most_common()}')

        log.info(f'Marks: {sorted(self._all_marks.items())}')


        return results
