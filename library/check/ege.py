from enum import Enum
from typing import Optional
import attr
import logging
log = logging.getLogger(__name__)

from library.util.asserts import assert_equals
from library.logging import cm, color

UNDERLINE = '_'  # prohibited in answers
SKIP = '-'


class Method(str, Enum):
    EXACT = 'exact'
    AB = 'ab'
    SET_2 = 'set_2'
    SET_3 = 'set_3'
    ASIS = 'asis'


TASKS_BY_METHOD = {
    Method.EXACT: [3, 4, 5, 9, 10, 11, 14, 15, 16, 20, 22, 23],
    Method.AB: [7, 8, 13, 18, 19, 21],
    Method.SET_2: [1, 6, 12, 17],
    Method.SET_3: [2],
    Method.ASIS: [24, 25, 26, 27, 28, 29, 30],
}

MethodByTaskNumber = {index: method for method, indices in TASKS_BY_METHOD.items() for index in indices}


@attr.s
class Result:
    value: int = attr.ib()
    max_value: int = attr.ib()
    answer: str = attr.ib()
    correct: str = attr.ib()
    colors_by_char: list = attr.ib()

    @property
    def colored_str(self) -> str:
        if not self.answer:
            return ''

        return ''.join(
            cm(char, char_color) for char, char_color in zip(self.answer, self.colors_by_char)
        )

    def str_fill(self, size: int) -> str:
        return ' ' * (size - len(self.answer))


def check_answer(number: int, correct: str, answer: str) -> Result:
    method = MethodByTaskNumber[number]
    if method == Method.EXACT:
        if answer == correct:
            return Result(1, 1, answer, correct, colors_by_char=[color.Green] * len(answer))
        else:
            return Result(0, 1, answer, correct, colors_by_char=[color.Red] * len(answer))

    elif method == Method.AB:
        assert len(correct) == 2
        assert len(answer) <= 2, f'{number} {correct} {answer}'
        answer_filled = answer + UNDERLINE * (len(correct) - len(answer))
        value = 0
        colors_by_char = []
        for correct_letter, letter in zip(correct, answer_filled):
            if correct_letter == letter:
                value += 1
                colors_by_char.append(color.Green)
            else:
                colors_by_char.append(color.Red)

        return Result(value, 2, answer, correct, colors_by_char=colors_by_char)

    elif method == Method.SET_2 or method == Method.SET_3:
        correct_set = set(correct)
        answer_set = set(answer)
        assert len(correct_set) == len(correct), f'Error on {number}: {correct}, {answer}'
        assert len(answer_set) == len(answer), f'Error on {number}: {correct}, {answer}'

        if method == Method.SET_3:
            if len(answer_set) > 3:
                return Result(0, 2, answer, correct, colors_by_char=[color.Red] * len(answer))

        new_answers = answer_set - correct_set
        missing_answers = correct_set - answer_set
        if len(new_answers) >= 2 or len(missing_answers) >= 2:
            return Result(0, 2, answer, correct, colors_by_char=[color.Red] * len(answer))
        elif not new_answers and not missing_answers:
            return Result(2, 2, answer, correct, colors_by_char=[color.Green] * len(answer))
        elif (len(new_answers) + len(missing_answers)) <= 2:
            return Result(1, 2, answer, correct, colors_by_char=[color.Yellow] * len(answer))
        else:
            return Result(0, 2, answer, correct, colors_by_char=[color.Red] * len(answer))

    elif method == Method.ASIS:
        max_value = int(correct)
        if not answer or answer == SKIP:
            return Result(0, max_value, answer, str(max_value), colors_by_char=[color.Red] * len(answer))
        int_answer = int(answer)
        if int_answer == max_value:
            return Result(int_answer, max_value, answer, correct, colors_by_char=[color.Green])
        elif int_answer in range(1, max_value):
            return Result(int_answer, max_value, answer, correct, colors_by_char=[color.Yellow] * len(answer))
        elif int_answer == 0:
            return Result(int_answer, max_value, answer, correct, colors_by_char=[color.Red] * len(answer))

        raise RuntimeError(f'Broken data for {method}: {correct} vs {answer}')

    raise RuntimeError(f'Unknown method: {method}')


def test_check_answer():
    rows = [
        (check_answer(1, '45', '345'), Result(1, 2, '345', '45', ['yellow', 'yellow', 'yellow'])),
        (check_answer(1, '45', '54'), Result(2, 2, '54', '45', ['green', 'green'])),
        (check_answer(1, '45', '5'), Result(1, 2, '5', '45', ['yellow'])),
        (check_answer(7, '31', '31'), Result(2, 2, '31', '31', ['green', 'green'])),
        (check_answer(24, '2', '1'), Result(1, 2, '1', '2', ['yellow'])),
        (check_answer(24, '2', '2'), Result(2, 2, '2', '2', ['green'])),
        (check_answer(24, '2', '-'), Result(0, 2, '-', '2', ['red'])),
        (check_answer(24, '2', '0'), Result(0, 2, '0', '2', ['red'])),
        (check_answer(2, '123', '723'), Result(1, 2, '723', '123', ['yellow', 'yellow', 'yellow'])),
        (check_answer(2, '123', '23'), Result(1, 2, '23', '123', ['yellow', 'yellow'])),
        (check_answer(2, '123', '423'), Result(1, 2, '423', '123', ['yellow', 'yellow', 'yellow'])),
        (check_answer(2, '123', '14'), Result(0, 2, '14', '123', ['red', 'red'])),
    ]
    for result, canonic in rows:
        assert_equals('Broken result', result, canonic)

test_check_answer()
