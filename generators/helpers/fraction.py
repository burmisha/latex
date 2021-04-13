import fractions

import logging
log = logging.getLogger(__name__)


class Fraction:
    def __init__(self, base_value=1):
        assert base_value == 1 or base_value == 0
        self._fraction = fractions.Fraction(numerator=base_value, denominator=1)

    def __mul__(self, other):
        if isinstance(other, Fraction):
            self._fraction = self._fraction * other._fraction
        else:
            self._fraction = self._fraction * other
        return self

    def __add__(self, other):
        if isinstance(other, Fraction):
            self._fraction = self._fraction + other._fraction
        else:
            self._fraction = self._fraction + other
        return self

    def __sub__(self, other):
        if isinstance(other, Fraction):
            self._fraction = self._fraction - other._fraction
        else:
            self._fraction = self._fraction - other
        return self

    def __truediv__(self, other):
        if isinstance(other, Fraction):
            self._fraction = self._fraction / other._fraction
        else:
            self._fraction = self._fraction / other
        return self

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
                    if self._fraction.denominator == 1:
                        return str(self._fraction.numerator)
                    else:
                        nom = self._escape_int(int(self._fraction.numerator))
                        denom = self._escape_int(int(self._fraction.denominator))
                        return f'\\frac{nom}{denom}'
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
        ('{f:LaTeX}', Fraction(1) * (-19) / 20, '\\frac{-19}{20}'),
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


test_fraction()
