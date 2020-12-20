import library.pupils
import library.location
import generators.variant

import collections
import datetime
import os
import re

import logging
log = logging.getLogger(__name__)

from library.logging import cm, color, log_list, one_line_pairs


class ProperAnswer:
    EN_TO_RU_MAPPING = {
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

    def __init__(self, answer, value=None):
        assert isinstance(value, (int, float)), f'Invalid value: {value}'
        assert isinstance(answer, (int, str))
        self._value = value
        self.__re = str(answer)

    def _format_re(self, canonic_re):
        result = str(canonic_re).strip()
        result = result.replace(' ', r'\s*')
        result = re.sub(r'([0-9][\.,][0-9])0+\b', r'\1', result)
        result = re.sub(r'([0-9])[,\.]([0-9])', r'\1[,\.]\2', result)
        assert not result.startswith(r'^[\s.;,]*')
        assert not result.endswith(r'[\s.;,]*$')
        result = f'^{result}$'
        return result

    def Printable(self):
        return str(self.__re)

    def Value(self):
        return self._value

    def _en_to_ru(self, value):
        res = str(value)
        for eng, rus in self.EN_TO_RU_MAPPING.items():
            res = res.replace(eng, rus)
        return res

    def IsOk(self, value):
        value = re.sub(r'([0-9][\.,][0-9])0+\b', r'\1', value)
        regexp = self._format_re(self.__re)
        if re.match(self._en_to_ru(regexp), self._en_to_ru(value)):
            return True

        return False


assert ProperAnswer('0.20', 1).IsOk('0.2')
# assert ProperAnswer('0.20', 1).__re == '0.20'
assert ProperAnswer('0.20', 1).IsOk('0,2')
assert ProperAnswer('20', 1).IsOk('20')
assert not ProperAnswer('20', 1).IsOk('200')
assert not ProperAnswer('200', 1).IsOk('20')
assert not ProperAnswer('0.20', 1).IsOk('0,21')
assert ProperAnswer('0.20', 1).IsOk('0,20')


class PupilAnswer:
    def __init__(self, value):
        self._value = value

    def Check(self, valid_answers_list):
        self._result_max = max(ans.Value() for ans in valid_answers_list)
        self._best_answer = list(ans for ans in valid_answers_list if ans.Value() == self._result_max)[0]
        matched_values = [ans.Value() for ans in valid_answers_list if ans.IsOk(self._value)]
        if not matched_values:
            self._result = 0
        else:
            self._result = matched_values[0]

        current_color = None
        best_color = None
        if self._result == self._result_max:
            current_color = color.Green
        else:
            if self._result > 0:
                current_color = color.Yellow
            else:
                current_color = color.Red

            if self._value and len(self._best_answer.Printable()) >= 2:
                best_color = color.Cyan

        self._color = current_color
        self._best_color = best_color


class PupilResult:
    def __init__(self, answers_count, row, marks):
        self._answers_count = answers_count
        self._result = []
        self._fields = {}
        self._marks = marks
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

    def SetPupil(self, pupil):
        self._pupil = pupil

    def GetResult(self):
        return sum(answer._result for answer in self._answers)

    def GetMaxResult(self):
        return sum(answer._result_max for answer in self._answers)

    def GetMark(self):
        mark = None
        result = self.GetResult()
        for index, value in enumerate(self._marks, 3):
            if value and result >= value:
                mark = index
        if any(self._marks) and not mark:
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
        self._csv_file = pupils.get_path(test_name + '.csv.zip', archive=True)
        self._marks = marks or [None, None, None]
        assert len(self._marks) == 3

        self._raw_answers = answers

        self._all_marks = collections.Counter()
        self._all_answers = [collections.Counter() for answer in self._raw_answers]
        self._all_results = collections.Counter()

    def _get_proper_answer_list(self, answer, pupil):
        if isinstance(answer, generators.variant.VariantTask):
            answer = answer.GetRandomTask(pupil).GetTestAnswer()

        if isinstance(answer, (str, int)):
            answer_dict = {
                str(answer): 1,
            }
        else:
            assert isinstance(answer, dict), f'got {answer}'
            for key, value in answer.items():
                assert isinstance(key, (str, int))
            answer_dict = answer

        return [
            ProperAnswer(key, value=value)
            for key, value in answer_dict.items()
        ]

    def GetPupilResult(self, row):
        pupil_result = PupilResult(len(self._raw_answers), row, self._marks)
        pupil = self._pupils.FindByName(pupil_result._original_name)
        pupil_result.SetPupil(pupil)

        for index, (pupil_answer, answer) in enumerate(zip(pupil_result._answers, self._raw_answers)):
            pupil_answer.Check(self._get_proper_answer_list(answer, pupil))
            self._all_answers[index][pupil_answer._value] += 1

        self._all_marks[pupil_result.GetMark()] += 1
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
                valid_answers_list = self._get_proper_answer_list(self._raw_answers[index], self._pupils._me)
                for answer_str, count in stats.most_common():
                    pupil_answer = PupilAnswer(answer_str)
                    pupil_answer.Check(valid_answers_list)
                    stats_line.append(f'{cm(answer_str, color=pupil_answer._color)}: {cm(count, color=color.Cyan)}')
                stats_line = ",  ".join(stats_line)
                log.info(f'Task {index + 1:>2}: {stats_line}.')

            log.info(f'Results: {one_line_pairs(sorted(self._all_results.items()))}')
            log.info(f'Marks: {one_line_pairs(sorted(self._all_marks.items()))}')
            not_found = set(p.GetFullName() for p in self._pupils.Iterate()) - found_pupils
            log.info(f'Not found:{log_list(sorted(not_found))}')
