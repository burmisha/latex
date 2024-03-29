from library.util.asserts import assert_equals

from decimal import Decimal, ROUND_DOWN
import math


def _strip_prefix(line):
    return line.replace('-', '').replace('.', '').lstrip('0')


def _leading_one(line: str) -> bool:
    stripped = _strip_prefix(line)
    return bool(stripped and stripped[0] == '1')


def format_with_precision(value, precision):
    assert isinstance(value, (int, float, Decimal)), f'Value {value} has unsupported type {type(value)}'
    assert isinstance(precision, int), f'Precision must be int, got {precision!r}'
    assert 1 <= precision <= 10, f'Invalid precision {precision} for {value}'

    if not isinstance(value, float) and (int(value) == value):
        return str(int(value))

    str_value = str(abs(value))
    abs_decimal = Decimal(str_value)

    log10 = math.floor(abs_decimal.log10()) - precision + 1
    if _leading_one(str_value):
        log10 -= 1
    mult = Decimal(10) ** log10
    new_value = Decimal(int(abs_decimal / mult + Decimal('0.5'))) * mult

    result = str(new_value)
    if 'E-' in result:
        line, exp = result.split('E-')
        result = '0.' + '0' * (int(exp) - 1) + line.replace('.', '')

    if value < 0:
        result = '-' + result
    return result


def test_format_with_precision():
    for value, precision, result in [
        (1, 1, '1'),
        (1.0, 1, '1.0'),
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
        (2.00, 3, '2.00'),
        (12, 1, '12'),
        (12, 2, '12'),
        (20, 2, '20'),
        (20, 1, '20'),
        (2.99, 2, '3.0'),
        (29.9, 2, '30'),
        (299., 2, '300'),
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
        res = format_with_precision(value, precision)
        assert_equals(f'value {value}, precision {precision}', result, res)


test_format_with_precision()


def get_precision(line):
    precisionStr = _strip_prefix(line)
    if not precisionStr:
        assert line in ['0', '0.0', '0.00'], f'Could not get precision from {line!r}'
        return 1

    precision = len(precisionStr)
    if _leading_one(precisionStr) and precision >= 2:
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
        ('0.00020', 2),
        ('20', 2),
        ('200', 3),
        ('192', 2),
        ('1', 1),
        ('2', 1),
        ('0', 1),
        ('0.0', 1),
        ('0.00', 1),
    ]
    for line, precision in data:
        result = get_precision(line)
        assert_equals(f'line {line!r}', precision, result)


test_get_precision()


def get_delta(decimal_value: Decimal, precision: int):
    abs_decimal = abs(decimal_value)
    str_value = str(abs_decimal)

    log10 = math.floor(abs_decimal.log10()) - precision + 1
    if _leading_one(str_value):
        log10 -= 1
    return Decimal(10) ** log10


def test_get_delta():
    data = [
        (Decimal('2.2'), 3, Decimal('0.01')),
        (Decimal('2.2'), 2, Decimal('0.1')),
        (Decimal('2.2'), 1, Decimal('1')),
        (Decimal('0.002'), 3, Decimal('0.00001')),
        (Decimal('0.002'), 2, Decimal('0.0001')),
        (Decimal('0.002'), 1, Decimal('0.001')),
        (Decimal('2000'), 3, Decimal('10')),
        (Decimal('2000'), 2, Decimal('100')),
        (Decimal('2000'), 1, Decimal('1000')),
    ]
    for decimal_value, precision, delta in data:
        result = get_delta(decimal_value, precision)
        assert_equals(f'line {decimal_value!r}, precision: {precision}', delta, result)

    assert math.floor(- (Decimal(1) / Decimal(67)).log10() + 1) == 2, - (Decimal(1) / Decimal(67)).log10() + 1


test_get_delta()
