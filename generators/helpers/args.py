import itertools  

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
}


def permute(*options):
    return list(itertools.permutations(options))


def letter_variants(answers, mocks, answers_count=None, mocks_count=None):
    answers_count = answers_count or 0
    mocks_count = mocks_count or 0

    assert isinstance(answers, dict)
    assert isinstance(mocks, list)
    assert len(set(answers.values())) == len(answers)
    assert len(set(mocks)) == len(mocks)
    assert not (set(mocks) & set(answers.values()))
    all_texts = set(mocks) | set(answers.values())

    variants = list(itertools.permutations(answers.keys(), r=answers_count))
    for variant in variants:
        proper_texts = set(answers[question] for question in variant)
        for wrong_text in itertools.permutations(sorted(all_texts - proper_texts), r=mocks_count):
            available_texts = sorted(proper_texts | set(wrong_text))
            for options in itertools.permutations(available_texts):
                positions = [options.index(answers[question]) for question in variant]
                yield list(zip(variant, positions)), options


def test_letter_variants():
    assert list(letter_variants(
        {'дважды два': 'четыре', 'трижды три': 'девять'},
        ['пять', 'шесть'],
        answers_count=1,
        mocks_count=1,
    )) == [
        ([('дважды два', 1),], ('девять', 'четыре')),
        ([('дважды два', 0),], ('четыре', 'девять')),
        ([('дважды два', 1),], ('пять', 'четыре')),
        ([('дважды два', 0),], ('четыре', 'пять')),
        ([('дважды два', 0),], ('четыре', 'шесть')),
        ([('дважды два', 1),], ('шесть', 'четыре')),
        ([('трижды три', 0),], ('девять', 'пять')),
        ([('трижды три', 1),], ('пять', 'девять')),
        ([('трижды три', 0),], ('девять', 'четыре')),
        ([('трижды три', 1),], ('четыре', 'девять')),
        ([('трижды три', 0),], ('девять', 'шесть')),
        ([('трижды три', 1),], ('шесть', 'девять')),
    ]
    assert list(letter_variants(
        {'дважды два': 'четыре', 'трижды три': 'девять'},
        ['пять', 'шесть'],
        answers_count=1,
        mocks_count=0,
    )) == [
        ([('дважды два', 0),], ('четыре',)),
        ([('трижды три', 0),], ('девять',))
    ]

test_letter_variants()



def n_times(*ns):
    return [(n, TOTAL_TIMES[n][0] + ' ' + TOTAL_TIMES[n][1]) for n in ns]


def n_word(*ns):
    return [(n, TOTAL_TIMES[n][0]) for n in ns]


assert n_times(3, 5) == [(3, 'три раза'), (5, 'пять раз')]
