from fractions import Fraction

import logging
log = logging.getLogger(__name__)


class FractionFormatter:
    def __init__(self, fraction):
        self._fraction = fraction

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
