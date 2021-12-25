from library.util.asserts import assert_equals

import logging
log = logging.getLogger(__name__)

from decimal import Decimal


def precisionFmt2(value, precision):
    assert isinstance(value, (int, float, Decimal)), f'Value {value} has type {type(value)}'
    assert isinstance(precision, int), f'Got precision {precision} for {value}'
    assert 1 <= precision <= 10, f'Got precision {precision} for {value}'

    if int(value) == value:
        return str(int(value))

    abs_value = float(abs(value))

    shift = 0
    lower = 10 ** (precision - 1)
    upper = 10 ** precision
    while not (lower <= abs_value < upper):
        if abs_value < lower:
            abs_value *= 10
            shift += 1
        else:
            abs_value /= 10
            shift -= 1

    leading_one = False
    if str(abs_value).startswith('1'):
        precision += 1
        abs_value *= 10
        shift += 1
        leading_one = True

    int_value = int(abs_value + 0.5)
    result = str(int_value)

    more_zeros = 0
    if len(result) < precision:
        more_zeros = precision - len(result)
        if more_zeros and leading_one:
            more_zeros -= 1
    result += '0' * more_zeros

    if shift < 0:
        result += '0' * (-shift)
    elif shift > 0:
        if len(result) >= shift + 1:
            result = result[:-shift] + '.' + result[-shift:]
        else:
            result = '0.' + '0' * (shift - len(result)) + result

    if value < 0:
        result = '-' + result
    return result


def test_precisionFmt2():
    for value, precision, result in [
        (1, 1, '1'),
        (1.0, 1, '1'),
        (Decimal(1), 1, '1'),
        (1.7, 1, '1.7'),
        (0.091, 2, '0.091'),
        (0.095, 2, '0.095'),
        (0.0949, 2, '0.095'),
        (-0.0949, 2, '-0.095'),
        (0.99, 2, '0.99'),
        (0.99, 1, '1.0'),
        (1.99, 2, '1.99'),
        (1.99, 3, '1.990'),
        (19.9, 2, '19.9'),
        (19.9, 1, '20'),
        (12, 1, '12'),
        (12, 2, '12'),
        (20, 2, '20'),
        (20, 1, '20'),
        (2.99, 2, '3.0'),
        (29.9, 2, '30'),
        (299., 2, '299'),
        (299, 2, '299'),
        (1 + 1. / 30, 2, '1.03'),
        (1 + 1. / 300, 2, '1.00'),
        (1 + 1. / 300, 3, '1.003'),
        (1. / 3, 2, '0.33'),
        (4. / 3, 2, '1.33'),
        (7. / 3, 2, '2.3'),
        (7. / 3, 3, '2.33'),
        (700. / 3, 3, '233'),
        (700. / 3, 3, '233'),
        (7000. / 3, 3, '2330'),
        (7000. / 3, 2, '2300'),
        (7000. / 3, 1, '2000'),
        (8000. / 3, 1, '3000'),
        (7000. / 3, 4, '2333'),
        (7000. / 3, 5, '2333.3'),
        (1000. / 3, 5, '333.33'),
        (100. / 3, 5, '33.333'),
        (10. / 3, 5, '3.3333'),
        (0.1 / 3, 5, '0.033333'),
        (0.01 / 3, 5, '0.0033333'),
        (0.001 / 3, 5, '0.00033333'),
        (0.0049594, 5, '0.0049594'),
        (0.0049594, 4, '0.004959'),
        (0.0049595, 4, '0.004960'),
        (0.0049594, 3, '0.00496'),
        (0.0049594, 2, '0.0050'),
        (0.0049594, 1, '0.005'),
        (3 / 10 ** 7, 2, '0.00000030'),
        (3 / 10 ** 7, 1, '0.0000003'),
        (3 * 10 ** 7, 1, '30000000'),
        (3 * 10 ** 7, 2, '30000000'),
    ]:
        res = precisionFmt2(value, precision)
        assert_equals(f'value {value}, precision {precision}', result, res)


test_precisionFmt2()


def get_precision(line):
    precisionStr = line.replace('-', '').replace('.', '').lstrip('0')
    if not precisionStr:
        assert line in ['0', '0.0', '0.00'], f'Could not get precision from {line!r}'
        precisionStr = '0'

    precision = len(precisionStr)
    if precisionStr[0] == '1' and precision >= 2:
        precision -= 1

    assert precision >= 1, f'Got invalid precision {precision} from {line!r}'

    return precision


def test_get_precision():
    data = [
        ('-2.0', 2),
        ('2.0', 2),
        ('2.00', 3),
        ('0.0020', 2),
        ('0.00200', 3),
        ('20', 2),
        ('200', 3),
        ('192', 2),
        ('0', 1),
        ('0.0', 1),
        ('0.00', 1),
    ]
    for line, precision in data:
        result = get_precision(line)
        assert result == precision, f'Expected {precision},  got {result} for {line}'


test_get_precision()

