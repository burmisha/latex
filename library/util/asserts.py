from library.logging import colorize_json, cm, color

import logging
log = logging.getLogger(__name__)


def assert_equals(name, expected, actual):
    if actual != expected:
        log.error(f'''Assertion error for {cm(name, color=color.Cyan)}:
\texpected:\t{cm(repr(expected), color=color.Red)}
\tactual:\t\t{cm(repr(actual), color=color.Green)}
''')
        raise AssertionError(f'{actual} != {expected}')
