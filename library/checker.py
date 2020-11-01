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


class PupilResult:
    def __init__(self, name, answers_count):
        self._name = name
        self._result = []
        self._answers_count = answers_count

        self._answers = ['' for _ in range(answers_count)]
        self._best_answers = ['' for _ in range(answers_count)]

        self._values = [0 for _ in range(answers_count)]
        self._max_values = [0 for _ in range(answers_count)]

        self._fields = {}

    def ParseRow(self, row):
        self._timestamp = datetime.datetime.strptime(row['Timestamp'], '%Y/%m/%d %H:%M:%S %p GMT+3')
        for key, value in row.items():
            value = value.strip()
            if value:
                if key.startswith('Задание '):
                    index = int(key.split(' ')[1]) - 1
                    assert 0 <= index < self._answers_count
                    self._answers[index] = value
                else:
                    if key not in ('Фамилия Имя', 'Timestamp'):
                        self._fields[key] = value

    def GetResult(self):
        return sum(self._values)

    def CheckAnswer(self, index, proper):
        answer = self._answers[index]
        max_value = max(ans.Value() for ans in proper)
        best_answer = list(ans for ans in proper if ans.Value() == max_value)[0]
        value = max([ans.Value() for ans in proper if ans.IsOk(answer)] + [0])

        self._best_answers[index] = best_answer
        self._values[index] = value

        return answer

    def ToStr(self, original_name=None, mark=None):
        task_line = []
        answers_line = []
        best_line = []
        max_result = 0
        for index, (answer, best_answer) in enumerate(zip(self._answers, self._best_answers)):
            best_printable = best_answer.Printable()
            value = self._values[index]
            max_value = best_answer.Value()
            max_result += max_value

            best_color = None
            if value == max_value:
                color = 'green'
            else:
                if value > 0:
                    color = 'yellow'
                else:
                    color = 'red'

                if answer and len(best_printable) >= 2:
                    best_color = 'cyan'

            width = (max(len(answer), len(best_printable)) + 1) // 4 + 1
            fmt = '{:<%d}' % (width * 4)
            answers_line.append(cm(fmt.format(answer), color))
            best_line.append(cm(fmt.format(best_printable), best_color))
            task_line.append(fmt.format(index + 1))

        answers_line = ''.join(answers_line)
        best_line = ''.join(best_line)
        task_line = ''.join(task_line)

        message = f'''
[{self._timestamp}] {cm(self._name, bold=True)} ({original_name}): {cm(self._result, bold=True)} / {max_result} → {cm(mark, bold=True)}
    Task:\t{task_line}
    Form:\t{best_line}
    Answer:\t{answers_line}
'''

        if self._fields:
            for key, value in sorted(self._fields.items()):
                message += f'    {key[:10]}...:\t{cm(value, bold=True)}\n'

        return message

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

    def ParseRow(self, row, pupil_filter):
        candidate_name = row['Фамилия Имя']
        name = self._name_lookup.Find(candidate_name)

        if pupil_filter and (not name or pupil_filter.lower() not in name.lower()):
            return

        pupil_result = PupilResult(name, len(self._proper_answers))
        pupil_result.ParseRow(row)

        for index, proper_answers in enumerate(self._proper_answers):
            answer = pupil_result.CheckAnswer(index, proper_answers)
            if answer:
                self._all_answers[index][answer] += 1

        mark = self._get_mark(pupil_result.GetResult())

        message = pupil_result.ToStr(original_name=candidate_name, mark=mark)
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
