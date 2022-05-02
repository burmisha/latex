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


@attr.s
class Result:
    value: int = attr.ib()
    max_value: int = attr.ib()
    answer: str = attr.ib()
    correct: str = attr.ib()
    colors_by_char: Optional[list] = attr.ib(default=None)

    @property
    def colored_str(self) -> str:
        if self.answer == self.correct:
            return cm(self.answer, color.Green)
        elif not self.answer:
            return ''
        elif self.value == 0:
            return cm(self.answer, color.Red)

        assert self.colors_by_char
        return ''.join(
            cm(char, char_color) for char, char_color in zip(self.answer, self.colors_by_char)
        )

    def str_fill(self, size: int) -> str:
        return ' ' * (size - len(self.answer))




MethodByTaskNumber = {
    1:  'set_2',
    2:  'set_3',
    3:  'exact',
    4:  'exact',
    5:  'exact',
    6:  'set_2',
    7:  'ab',
    8:  'ab',
    9:  'exact',
    10: 'exact',
    11: 'exact',
    12: 'set_2',
    13: 'ab',
    14: 'exact',
    15: 'exact',
    16: 'exact',
    17: 'set_2',
    18: 'ab',
    19: 'ab',
    20: 'exact',
    21: 'ab',
    22: 'exact',
    23: 'exact',
    24: 'asis',
    25: 'asis',
    26: 'asis',
    27: 'asis',
    28: 'asis',
    29: 'asis',
    30: 'asis',
}


def check_answer(number: int, correct: str, answer: str) -> Result:
    method = Method(MethodByTaskNumber[number])
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
        colors_by_char = [color.Red, color.Red] 
        if answer_filled[0] == correct[0]:
            value += 1
            colors_by_char[0] = color.Green
        if answer_filled[1] == correct[1]:
            value += 1
            colors_by_char[1] = color.Green
        return Result(value, 2, answer, correct, colors_by_char=colors_by_char)

    elif method == Method.SET_2 or method == Method.SET_3:
        correct_set = set(correct)
        answer_set = set(answer)
        assert len(correct_set) == len(correct)
        assert len(answer_set) == len(answer)

        if method == Method.SET_3:
            if len(answer_set) > 3:
                return Result(0, 2, answer, correct, colors_by_char=[color.Red] * len(answer))

        if correct_set == answer_set:
            return Result(2, 2, answer, correct, colors_by_char=[color.Green] * len(answer))
        elif answer_set.issubset(correct_set) and len(correct_set - answer_set) == 1:
            return Result(1, 2, answer, correct, colors_by_char=[color.Yellow] * len(answer))
        elif correct_set.issubset(answer_set) and len(answer_set - correct_set) == 1:
            return Result(1, 2, answer, correct, colors_by_char=[color.Yellow] * len(answer))
        else:
            return Result(0, 2, answer, correct, colors_by_char=[color.Red] * len(answer))

    elif method == Method.ASIS:
        max_value = int(correct)
        if not answer or answer == SKIP:
            return Result(0, max_value, answer, str(max_value), colors_by_char=[color.Red])
        int_answer = int(answer)
        if int_answer == max_value:
            return Result(int_answer, max_value, answer, correct)
        elif int_answer in range(1, max_value):
            return Result(int_answer, max_value, answer, correct, colors_by_char=[color.Yellow] * len(answer))
        elif int_answer == 0:
            return Result(int_answer, max_value, answer, correct)

        raise RuntimeError(f'Broken data for {method}: {correct} vs {answer}')

    raise RuntimeError(f'Unknown method: {method}')


def test_check_answer():
    rows = [
        (check_answer(1, '45', '345'), Result(1, 2, '345', '45', ['yellow', 'yellow', 'yellow'])),
        (check_answer(1, '45', '54'), Result(2, 2, '54', '45', ['green', 'green'])),
        (check_answer(1, '45', '5'), Result(1, 2, '5', '45', ['yellow'])),
        (check_answer(7, '31', '31'), Result(2, 2, '31', '31', ['green', 'green'])),
        (check_answer(24, '2', '1'), Result(1, 2, '1', '2', ['yellow'])),
        (check_answer(24, '2', '2'), Result(2, 2, '2', '2')),
        (check_answer(24, '2', '-'), Result(0, 2, '-', '2', colors_by_char=['red'])),
        (check_answer(24, '2', '0'), Result(0, 2, '0', '2')),
    ]
    for result, canonic in rows:
        assert_equals('Broken result', result, canonic)

test_check_answer()