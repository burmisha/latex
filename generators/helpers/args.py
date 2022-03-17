import itertools
import math

TOTAL_TIMES = {
    2: ('два', 'раза'),
    3: ('три', 'раза'),
    4: ('четыре', 'раза'),
    5: ('пять', 'раз'),
    6: ('шесть', 'раз'),
    7: ('семь', 'раз'),
    8: ('восемь', 'раз'),
    9: ('девять', 'раз'),
    10: ('десять', 'раз'),
    12: ('двенадцать', 'раз'),
    16: ('шестнадцать', 'раз'),
}

LV_SOLUTION_SPACE = 20

LV_TEXT = '''
    Установите каждой букве в соответствие ровно одну цифру и запишите ответ (только цифры, без других символов).

    {lv.Questions}.

    {lv.Options}.
'''


def permute(*options):
    return list(itertools.permutations(options))


class LV:
    def __init__(self, answers, mocks, answers_count=None, mocks_count=None):
        answers_count = answers_count or 0
        mocks_count = mocks_count or 0

        assert isinstance(answers, dict)
        assert isinstance(mocks, list)
        self.all_answers = set(mocks) | set(answers.values())
        assert len(self.all_answers) == len(answers) + len(mocks)

        self.answers = answers
        self.mocks = mocks
        self.answers_count = answers_count
        self.mocks_count = mocks_count

    def generate_letter_variants(self):
        # choose questions to be asked
        for questions in itertools.permutations(list(self.answers.items()), r=self.answers_count):
            question_texts = [question[0] for question in questions]
            proper_answers = list(enumerate(question[1] for question in questions))

            proper_answers_texts = set(proper_answer[1] for proper_answer in proper_answers)
            available_wrong_answers = [(None, answer) for answer in sorted(self.all_answers - proper_answers_texts)]

            # choose answers from wrong (both ok ones from other questions and mock ones)
            for wrong_answers in itertools.permutations(available_wrong_answers, self.mocks_count):
                # choose answers order
                for answers in itertools.permutations(proper_answers + list(wrong_answers)):
                    indexes = [None for i in range(self.answers_count)]
                    for index, answer in enumerate(answers):
                        if answer[0] is not None:
                            indexes[answer[0]] = index
                    yield list(zip(question_texts, indexes)), [answer[1] for answer in answers]

    def __len__(self):
        # choose questions to be asked
        choose_questions = math.perm(len(self.answers), self.answers_count)
        # choose answers from wrong (both ok ones from other questions and mock ones)
        answers_left = math.comb(len(self.answers) + len(self.mocks) - self.answers_count, self.mocks_count)
        # choose answers order
        answers_order = math.factorial(self.answers_count + self.mocks_count)

        return choose_questions * answers_left * answers_order


class LetterVariant:
    def __init__(self, questions, options):
        self.Answer = ''.join(f'{question[1] + 1}' for question in questions)
        self.Questions = ', '.join([
            f'{letter}) {question[0]}' for letter, question in zip('АБВГДЕЖЗ', questions)
        ])
        self.Options = ', '.join([
            f'{digit}) {option}' for digit, option in zip('123456789', options)
        ])


def test_generate_letter_variants():
    lv = LV(
        {'дважды два': 'четыре', 'трижды три': 'девять'},
        ['пять', 'шесть'],
        answers_count=1,
        mocks_count=1,
    )
    res = list(lv.generate_letter_variants())
    canonic = [
        ([('дважды два', 0),], ['четыре', 'девять']),
        ([('дважды два', 1),], ['девять', 'четыре']),
        ([('дважды два', 0),], ['четыре', 'пять']),
        ([('дважды два', 1),], ['пять', 'четыре']),
        ([('дважды два', 0),], ['четыре', 'шесть']),
        ([('дважды два', 1),], ['шесть', 'четыре']),
        ([('трижды три', 0),], ['девять', 'пять']),
        ([('трижды три', 1),], ['пять', 'девять']),
        ([('трижды три', 0),], ['девять', 'четыре']),
        ([('трижды три', 1),], ['четыре', 'девять']),
        ([('трижды три', 0),], ['девять', 'шесть']),
        ([('трижды три', 1),], ['шесть', 'девять']),
    ]
    assert res == canonic, f'Error:\n  expected:\t{canonic}\n  got:\t\t{res}'
    assert len(lv) == 12

    lv = LV(
        {'дважды два': 'четыре', 'трижды три': 'девять'},
        ['пять', 'шесть'],
        answers_count=1,
        mocks_count=0,
    )
    res = list(lv.generate_letter_variants())
    canonic = [
        ([('дважды два', 0),], ['четыре',]),
        ([('трижды три', 0),], ['девять',]),
    ]
    assert len(lv) == 2
    assert res == canonic, f'Error:\n  expected:\t{canonic}\n  got:\t\t{res}'


def test_letter_variant():
    letter_variant = LetterVariant(
        [('дважды два', 1),], ('шесть', 'четыре')
    )
    assert letter_variant.Answer == '2'
    assert letter_variant.Questions == 'А) дважды два'
    assert letter_variant.Options == '1) шесть, 2) четыре'


def letter_variants(*args, **kws):
    for questions, options in LV(*args, **kws).generate_letter_variants():
        yield LetterVariant(questions, options)


test_generate_letter_variants()

test_letter_variant()


def n_times(*ns):
    return [(n, TOTAL_TIMES[n][0] + ' ' + TOTAL_TIMES[n][1]) for n in ns]


def n_word(*ns):
    return [(n, TOTAL_TIMES[n][0]) for n in ns]


assert n_times(3, 5) == [(3, 'три раза'), (5, 'пять раз')]
