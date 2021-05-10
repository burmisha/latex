import fractions

import logging
log = logging.getLogger(__name__)


class Fraction:
    def __init__(self, base_value=1, numerator=None, denominator=None):
        assert base_value == 1 or base_value == 0
        if base_value == 0:
            assert numerator is None
            assert denominator is None
            self._fraction = fractions.Fraction(numerator=base_value, denominator=1)
        else:
            numer = numerator or 1
            denom = denominator or 1
            self._fraction = fractions.Fraction(numerator=numer, denominator=denom)

    @staticmethod
    def from_fraction(fraction):
        assert isinstance(fraction, fractions.Fraction)
        return Fraction(
            numerator=fraction.numerator,
            denominator=fraction.denominator,
        )

    def __mul__(self, other):
        if isinstance(other, Fraction):
            return Fraction.from_fraction(self._fraction * other._fraction)
        else:
            return Fraction.from_fraction(self._fraction * other)

    def __add__(self, other):
        if isinstance(other, Fraction):
            return Fraction.from_fraction(self._fraction + other._fraction)
        else:
            return Fraction.from_fraction(self._fraction + other)

    def __sub__(self, other):
        if isinstance(other, Fraction):
            return Fraction.from_fraction(self._fraction - other._fraction)
        else:
            return Fraction.from_fraction(self._fraction - other)

    def __truediv__(self, other):
        if isinstance(other, Fraction):
            return Fraction.from_fraction(self._fraction / other._fraction)
        else:
            return Fraction.from_fraction(self._fraction / other)

    def __float__(self):
        return float(self._fraction)

    def _escape_int(self, value):
        assert isinstance(value, int)
        if len(f'{value}') == 1:
            return f'{value}'
        else:
            return f'{{{value}}}'

    def __format__(self, fmt):
        try:
            fmt_parts = fmt.replace(':', '|').split('|')
            if len(fmt_parts) == 1:
                main_format = fmt_parts[0]
                if main_format == 'LaTeX':
                    if self._fraction < 0:
                        prefix = '-'
                        num = - self._fraction.numerator
                    else:
                        prefix = ''
                        num = self._fraction.numerator
                    if self._fraction.denominator == 1:
                        return prefix + str(num)
                    else:
                        nom = self._escape_int(int(num))
                        denom = self._escape_int(int(self._fraction.denominator))
                        return f'{prefix}\\frac{nom}{denom}'
                elif main_format == 'Basic':
                    if self._fraction.denominator == 1:
                        return str(self._fraction.numerator)
                    else:
                        return f'{int(self._fraction.numerator)}/{int(self._fraction.denominator)}'
                else:
                    raise RuntimeError(f'Unknown main format: {main_format!r} from {fmt!r}')
            else:
                raise RuntimeError()
        except Exception:
            log.error(f'Error in __format__ for {fmt} and {self._fraction}')
            raise

    def __str__(self):
        return f'fraction: {self._fraction.numerator} / {self._fraction.denominator}'


def test_fraction():
    for template, frac, result in [
        ('{f:LaTeX}', Fraction(), '1'),
        ('{f:LaTeX}', Fraction(0), '0'),
        ('{f:LaTeX}', Fraction(1), '1'),
        ('{f:LaTeX}', Fraction(1) * (-2), '-2'),
        ('{f:LaTeX}', Fraction(1) * 2, '2'),
        ('{f:LaTeX}', Fraction(1) * 2 / 2, '1'),
        ('{f:LaTeX}', Fraction(1) * 2 / 2, '1'),
        ('{f:LaTeX}', Fraction(1) * 2 / 4, '\\frac12'),
        ('{f:LaTeX}', Fraction(1) * 19 / 20, '\\frac{19}{20}'),
        ('{f:LaTeX}', Fraction(1) * (-19) / 20, '-\\frac{19}{20}'),
        ('{f:LaTeX}', Fraction() / (2 * 3) * (-1) + 1, '\\frac56'),
        ('{f:Basic}', Fraction() / (2 * 3) * (-1) + 1, '5/6'),
        ('{f:Basic}', Fraction() / (2 * 3) * (-12), '-2'),
    ]:
        res = template.format(f=frac)
        assert res == result, f'Expected {result}, got {res}'

    alpha = 3
    A_bonus_cycle = Fraction() * (alpha - 1) ** 2 / 2
    assert f'{A_bonus_cycle:LaTeX}'
    A_bonus_plus = Fraction() * (11 * alpha + 3) * (5 * alpha - 3) / (16 * 8)
    assert f'{A_bonus_plus:LaTeX}'
    U_bonus_plus = (Fraction() * 15 * (alpha + 1) ** 2 / 64 - alpha) * 3 / 2
    assert f'{U_bonus_plus:LaTeX}'
    U_bonus_12 = Fraction() * (alpha - 1) / 1 * 3 / 2
    assert f'{U_bonus_12:LaTeX}'
    eta_bonus = Fraction() * A_bonus_cycle / (U_bonus_plus + A_bonus_plus + U_bonus_12)
    assert f'{eta_bonus:LaTeX}'

    a = Fraction()
    assert int(float(a)) == 1
    b = a * 200
    assert int(float(a)) == 1


test_fraction()
