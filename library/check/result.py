import datetime
from library.check.pupil_answer import PupilAnswer
from library.check.proper_answer import ProperAnswer

from library.logging import cm, color, log_list, one_line_pairs


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
