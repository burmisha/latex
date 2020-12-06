import library.pupils
import library.location
import generators.variant

import collections
import datetime
import os
import re

import logging
log = logging.getLogger(__name__)

from library.logging import cm, color, log_list


class ProperAnswer:
    ENG_RUS_MAPPING = {
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

    def __init__(self, answer, value=1):
        assert isinstance(value, int), f'Invalid value: {value}'
        self._value = value

        if isinstance(answer, (str, int)):
            self._is_re = True
            self._printable = str(answer)
            self._canonic_re = self._format_re(answer)
        elif isinstance(answer, generators.variant.VariantTask):
            self._is_re = False
            self._variant_task = answer
        else:
            raise RuntimeError(f'Invalid proper answer: {answer}')

    def _format_re(self, canonic_re):
        canonic_re = str(canonic_re).strip()
        canonic_re = canonic_re.replace(' ', r'\s*')
        re.sub(r'([0-9])[,\.]([0-9])', r'\1[,\.]\2', canonic_re)
        assert not canonic_re.startswith(r'^[\s.;,]*')
        assert not canonic_re.endswith(r'[\s.;,]*$')
        canonic_re = f'^{canonic_re}$'
        return canonic_re

    def Printable(self, pupil):
        if self._is_re:
            return self._printable
        else:
            return self._variant_task.GetRandomTask(pupil).GetTestAnswer()

    def Value(self):
        return self._value

    def _duplicates_to_rus(self, value):
        res = str(value)
        for eng, rus in self.ENG_RUS_MAPPING.items():
            res = res.replace(eng, rus)
        return res

    def IsOk(self, pupil_answer, pupil):
        if self._is_re:
            if re.match(self._duplicates_to_rus(self._canonic_re), self._duplicates_to_rus(pupil_answer._value)):
                return True
        else:
            personal_answer = self._variant_task.GetRandomTask(pupil).GetTestAnswer()
            answer_re = self._format_re(personal_answer)
            if re.match(self._duplicates_to_rus(answer_re), self._duplicates_to_rus(pupil_answer._value)):
                return True

        return False


class PupilAnswer:
    def __init__(self, value):
        self._value = value

    def Check(self, proper_answers, pupil):
        self._result_max = max(ans.Value() for ans in proper_answers)
        self._best_answer = list(ans for ans in proper_answers if ans.Value() == self._result_max)[0]
        self._result = max([ans.Value() for ans in proper_answers if ans.IsOk(self, pupil)] + [0])

        current_color = None
        best_color = None
        if self._result == self._result_max:
            current_color = color.Green
        else:
            if self._result > 0:
                current_color = color.Yellow
            else:
                current_color = color.Red

            if self._value and len(self._best_answer.Printable(pupil)) >= 2:
                best_color = color.Cyan

        self._color = current_color
        self._best_color = best_color


class PupilResult:
    def __init__(self, answers_count, row):
        self._answers_count = answers_count
        self._result = []
        self._fields = {}
        self._parse_row(row)

    def _parse_row(self, row):
        self._original_name = row['Фамилия Имя']
        self._timestamp = datetime.datetime.strptime(row['Timestamp'], '%Y/%m/%d %I:%M:%S %p GMT+3')
        del row['Фамилия Имя']
        del row['Timestamp']

        self._answers = [None for _ in range(self._answers_count)]
        for key, value in row.items():
            value = value.strip()
            if key.startswith('Задание '):
                index = int(key.split(' ')[1]) - 1
                assert 0 <= index < self._answers_count
                self._answers[index] = PupilAnswer(value)
            elif value:
                self._fields[key] = value

    def SetPupil(self, pupils):
        self._pupil = pupils.FindByName(self._original_name)

    def GetResult(self):
        return sum(answer._result for answer in self._answers)

    def GetMaxResult(self):
        return sum(answer._result_max for answer in self._answers)

    def CheckAnswer(self, index, proper):
        answer = self._answers[index]
        answer.Check(proper, self._pupil)
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
            best_printable = answer._best_answer.Printable(self._pupil)
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
[{self._timestamp}] {cm(self._pupil.GetFullName(surnameFirst=True), bold=True)} ({self._original_name}): {cm(self.GetResult(), bold=True)} / {self.GetMaxResult()} → {cm(self._mark, bold=True)}
    Задание:\t{task_line}
    Верные:\t{best_line}
    Прислано:\t{answers_line}
'''

        if self._fields:
            for key, value in sorted(self._fields.items()):
                message += f'    {key[:12]}…: {cm(value, bold=True)}\n'

        return message.lstrip('\n')


class Checker:
    def __init__(self, test_name, answers, marks=None):
        pupils = library.pupils.get_class_from_string(test_name, addMyself=True)
        self._pupils = pupils

        self._csv_file = library.location.udr(
            f'{pupils.Grade} класс',
            f'{pupils.Year} {pupils.Grade}{pupils.Letter} Физика - Архив',
            test_name + '.csv.zip',
        )
        self._marks = marks or [None, None, None]
        assert len(self._marks) == 3

        self._proper_answers_lists = []
        for answer in answers:
            if isinstance(answer, ProperAnswer):
                answer_variants = [answer]
            elif isinstance(answer, dict):
                answer_variants = [ProperAnswer(key, value=value) for key, value in answer.items()]
            else:
                answer_variants = [ProperAnswer(answer)]
            self._proper_answers_lists.append(answer_variants)

        self._all_marks = collections.Counter()
        self._all_answers = [collections.Counter() for answer in self._proper_answers_lists]
        self._all_results = collections.Counter()

    def GetPupilResult(self, row):
        pupil_result = PupilResult(len(self._proper_answers_lists), row)
        pupil_result.SetPupil(self._pupils)

        for index, answers in enumerate(self._proper_answers_lists):
            answer = pupil_result.CheckAnswer(index, answers)
            if answer:
                self._all_answers[index][answer] += 1

        mark = pupil_result.SetMark(self._marks)
        self._all_marks[mark] += 1
        self._all_results[pupil_result.GetResult()] += 1

        return pupil_result

    def Check(self, pupil_filter):
        zipped_csv = library.files.ZippedCsv(self._csv_file)
        found_pupils = set()
        for row in zipped_csv.ReadDicts():
            pupil_result = self.GetPupilResult(row)

            pupil_name = pupil_result._pupil.GetFullName()
            found_pupils.add(pupil_name)

            if pupil_filter and (not pupil_name or pupil_filter.lower() not in pupil_name.lower()):
                continue

            log.info(pupil_result)
            yield pupil_result

        if not pupil_filter:
            for index, stats in enumerate(self._all_answers):
                stats_line = []
                for answer_str, count in stats.most_common():
                    pupil_answer = PupilAnswer(answer_str)
                    pupil_answer.Check(self._proper_answers_lists[index], self._pupils._me)
                    stats_line.append(f'{cm(answer_str, color=pupil_answer._color)}: {cm(count, color=color.Cyan)}')
                stats_line = ",  ".join(stats_line)
                log.info(f'Task {index + 1:>2}: {stats_line}.')

            log.info(f'Results: {", ".join("%s: %d" % (k, v) for k, v in sorted(self._all_results.items()))}')
            log.info(f'Marks: {", ".join("%s: %d" % (k, v) for k, v in sorted(self._all_marks.items()))}')
            not_found = set(p.GetFullName() for p in self._pupils.Iterate()) - found_pupils
            log.info(f'Not found:{log_list(sorted(not_found))}')
