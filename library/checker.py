import library.pupils
import library.location

import Levenshtein

import collections
import datetime
import os
import re

import logging
log = logging.getLogger(__name__)

import library.logging
cm = library.logging.ColorMessage()


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
            parts += [
                ' '.join(parts),
                ' '.join(parts[::-1]),
            ]
            for part in parts:
                counter[part] += 1
                self._unique_names[part] = name

        for part, count in sorted(counter.items()):
            if count != 1:
                log.debug(f'{part} has {count} duplicates, will not use')
                del self._unique_names[part]
            else:
                log.debug(f'Using {part} → {self._unique_names[part]}')

        self._found_names = collections.Counter()

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

        name = list(best_matches)[0]
        self._found_names[name] += 1
        return name

    def NotFound(self):
        return sorted(set(self._names) - set(self._found_names))


class ProperAnswer:
    def __init__(self, canonicRe, value=1):
        assert isinstance(canonicRe, (str, int)), f'Invalid re: {canonicRe}'
        assert isinstance(value, int), f'Invalid value: {value}'
        canonicRe = str(canonicRe).strip()
        canonicRe = canonicRe.replace(' ', r'\s*')
        re.sub(r'([0-9])[,\.]([0-9])', r'\1[,\.]\2', canonicRe)
        assert not canonicRe.startswith(r'^[\s.;,]*')
        assert not canonicRe.endswith(r'[\s.;,]*$')
        self._value = value
        self._canonic_re = f'^{canonicRe}$'
        self._printable = str(canonicRe)
        # use russian instead of english
        self._eng_rus_mapping = {
            'A': 'А', 'a': 'а',
            'B': 'В',
            'C': 'С', 'c': 'с',
            'E': 'Е', 'e': 'е',
            'H': 'Н',
            'K': 'К',
            'M': 'М',
            'O': 'O', 'o': 'о',
            'P': 'Р', 'p': 'р',
            'T': 'Т',
            'X': 'Х', 'x': 'х',
        }

    def Printable(self):
        return self._printable

    def Value(self):
        return int(self._value)

    def _simplify(self, value):
        res = str(value)
        for eng, rus in self._eng_rus_mapping.items():
            res = res.replace(eng, rus)
        return res

    def IsOk(self, value=None):
        if re.match(self._simplify(self._canonic_re), self._simplify(value)):
            return True

        return False


class Answer:
    def __init__(self, value):
        self._value = value

    def Check(self, proper_answers):
        self._result_max = max(ans.Value() for ans in proper_answers)
        self._best_answer = list(ans for ans in proper_answers if ans.Value() == self._result_max)[0]
        self._result = max([ans.Value() for ans in proper_answers if ans.IsOk(self._value)] + [0])

        color = None
        best_color = None
        if self._result == self._result_max:
            color = library.logging.color.Green
        else:
            if self._result > 0:
                color = library.logging.color.Yellow
            else:
                color = library.logging.color.Red

            if self._value and len(self._best_answer.Printable()) >= 2:
                best_color = library.logging.color.Cyan

        self._color = color
        self._best_color = best_color



class PupilResult:
    def __init__(self, name, answers_count):
        self._name = name
        self._result = []
        self._answers_count = answers_count

        self._fields = {}

    def ParseRow(self, row):
        self._timestamp = datetime.datetime.strptime(row['Timestamp'], '%Y/%m/%d %I:%M:%S %p GMT+3')
        self._original_name = row['Фамилия Имя']

        self._answers = [None for _ in range(self._answers_count)]
        for key, value in row.items():
            value = value.strip()
            if key.startswith('Задание '):
                index = int(key.split(' ')[1]) - 1
                assert 0 <= index < self._answers_count
                self._answers[index] = Answer(value)
            else:
                if value and key not in ('Фамилия Имя', 'Timestamp'):
                    self._fields[key] = value

    def GetResult(self):
        return sum(answer._result for answer in self._answers)

    def GetMaxResult(self):
        return sum(answer._result_max for answer in self._answers)

    def CheckAnswer(self, index, proper):
        answer = self._answers[index]
        answer.Check(proper)
        return answer._value

    def SetMark(self, marks):
        mark = None
        result = self.GetResult()
        for index, value in enumerate(marks, 3):
            if value and result >= value:
                mark = index
        if any(marks) and not mark:
            mark = 2
        self._mark = mark
        return mark

    def __str__(self):
        task_line = []
        answers_line = []
        best_line = []
        for index, answer in enumerate(self._answers):
            best_printable = answer._best_answer.Printable()
            result = answer._result
            result_max = answer._best_answer.Value()

            width = (max(len(answer._value), len(best_printable)) + 1) // 4 + 1
            fmt = '{:<%d}' % (width * 4)
            answers_line.append(cm(fmt.format(answer._value), answer._color))
            best_line.append(cm(fmt.format(best_printable), answer._best_color))
            task_line.append(fmt.format(index + 1))

        answers_line = ''.join(answers_line)
        best_line = ''.join(best_line)
        task_line = ''.join(task_line)

        message = f'''
[{self._timestamp}] {cm(self._name, bold=True)} ({self._original_name}): {cm(self.GetResult(), bold=True)} / {self.GetMaxResult()} → {cm(self._mark, bold=True)}
    Задание:\t{task_line}
    Верные:\t{best_line}
    Прислано:\t{answers_line}
'''

        if self._fields:
            for key, value in sorted(self._fields.items()):
                message += f'    {key[:12]}…: {cm(value, bold=True)}\n'

        return message


class Checker:
    def __init__(self, test_name, answers, marks=None):
        pupils = library.pupils.get_class_from_string(test_name)
        csv_file = library.location.udr(
            f'{pupils.Grade} класс',
            f'{pupils.Year} {pupils.Grade}{pupils.Letter} Физика - Архив',
            test_name + '.csv.zip',
        )

        self._csv_file = csv_file
        if not marks:
            marks = [None, None, None]
        self._marks = marks
        assert len(self._marks) == 3

        self._proper_answers = []
        for answer in answers:
            answer_variants = []
            if isinstance(answer, ProperAnswer):
                answer_variants = [answer]
            elif isinstance(answer, dict):
                for key, value in answer.items():
                    answer_variants.append(ProperAnswer(key, value=value))
            else:
                answer_variants = [ProperAnswer(answer)]
            self._proper_answers.append(answer_variants)

        names = [pupil.GetFullName(surnameFirst=True) for pupil in pupils.Iterate()]
        self._name_lookup = NameLookup(names)
        self._all_marks = collections.Counter()
        self._all_answers = [collections.Counter() for answer in self._proper_answers]
        self._all_results = collections.Counter()

    def ParseRow(self, row, pupil_filter):
        name = self._name_lookup.Find(row['Фамилия Имя'])
        if pupil_filter and (not name or pupil_filter.lower() not in name.lower()):
            return None

        pupil_result = PupilResult(name, len(self._proper_answers))
        pupil_result.ParseRow(row)
        for index, proper_answers in enumerate(self._proper_answers):
            answer = pupil_result.CheckAnswer(index, proper_answers)
            if answer:
                self._all_answers[index][answer] += 1

        mark = pupil_result.SetMark(self._marks)
        self._all_marks[mark] += 1
        self._all_results[pupil_result.GetResult()] += 1

        log.info(str(pupil_result).lstrip('\n'))
        return pupil_result

    def Check(self, pupil_filter):
        zipped_csv = library.files.ZippedCsv(self._csv_file)
        for row in zipped_csv.ReadDicts():
            yield self.ParseRow(row, pupil_filter)

        for index, stats in enumerate(self._all_answers):
            stats_line = []
            for answer_str, count in stats.most_common():
                answer = Answer(answer_str)
                answer.Check(self._proper_answers[index])
                stats_line.append(f'{cm(answer_str, color=answer._color)}: {cm(count, color=library.logging.color.Cyan)}')
            stats_line = ",  ".join(stats_line)
            log.info(f'Task {index + 1:>2}: {stats_line}.')

        log.info(f'Results: {", ".join("%s: %d" % (k, v) for k, v in sorted(self._all_results.items()))}')
        log.info(f'Marks: {", ".join("%s: %d" % (k, v) for k, v in sorted(self._all_marks.items()))}')
        if not pupil_filter:
            log.info(f'Not found:{library.logging.log_list(self._name_lookup.NotFound())}')
