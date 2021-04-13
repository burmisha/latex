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



def n_times(*ns):
    return [(n, TOTAL_TIMES[n][0] + ' ' + TOTAL_TIMES[n][1]) for n in ns]


def n_word(*ns):
    return [(n, TOTAL_TIMES[n][0]) for n in ns]


assert n_times(3, 5) == [(3, 'три раза'), (5, 'пять раз')]
