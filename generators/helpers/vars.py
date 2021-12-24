import itertools
import re

import logging
log = logging.getLogger(__name__)


class Vars:
    def __init__(self):
        self._keys = []
        self._original_keys = []
        self._values = []
        self._fixed = False
        self._used_keys = set()

    def _flatten(self):
        if self._fixed:
            return

        self._fixed = True
        for index in range(len(self._keys)):
            # TODO: use lazy getter for large lists
            self._values[index] = list(self._values[index])
            values = self._values[index]
            key = self._keys[index]
            if '__' in key:
                key = tuple(key_part.strip() for key_part in key.split('__'))
                for key_part in key:
                    assert key_part not in self._used_keys, f'Already used key {key_part}'
                    self._used_keys.add(key_part)
                tuple_length = len(key)
                for value in values:
                    assert isinstance(value, tuple)
                    assert len(value) == tuple_length, f'value: {value} has not length {tuple_length}'
                self._keys[index] = key
            else:
                assert key not in self._used_keys, f'Already used key {key}'
                self._used_keys.add(key)
                for value in values:
                    assert not isinstance(value, tuple)

        self._denoms = [1 for v in self._values]
        for i in range(len(self._values) - 2, -1, -1):
            self._denoms[i] = self._denoms[i + 1] * len(self._values[i + 1])

    def add(self, key, values):
        assert not self._fixed
        assert isinstance(key, str), f'key {key} is not str'
        assert values, f'No values for {key}'

        str_re = re.compile(r'^(-?\d+(\.\d+)?/)+-?\d+(\.\d+)?$')
        if isinstance(values, tuple):
            assert len(values) == 2
            assert '{}' in values[0], f'No {{}} in {values}'
            values = [values[0].format(option) for option in values[1]]
        elif isinstance(values, str):
            if any(s.isdigit() for s in values):
                parts = values.split()
                for index, part in enumerate(parts):
                    if '/' in part and str_re.match(part):
                        split_values = part.split('/')
                        assert all(float(i) for i in split_values), f'part: '
                        prefix = ' '.join(parts[:index])
                        suffix = ' '.join(parts[index + 1:])
                        values = [f'{prefix} {v} {suffix}' for v in split_values]
                        break
            else:
                values = values.split('/')

        self._original_keys.append(key)
        self._keys.append(key)
        self._values.append(values)

    @property
    def random_str(self):
        return '__'.join(sorted(self._original_keys))

    def total_count(self):
        self._flatten()
        try:
            r = 1
            for vs in self._values:
                r *= len(vs)
        except:
            log.error(f'{self._keys}, {self._values}')
            raise
        return r

    def form_all(self):
        self._flatten()
        for row in itertools.product(*self._values):
            result = {}
            for key, value in zip(self._keys, row):
                if isinstance(key, tuple):
                    result.update(dict(zip(key, value)))
                else:
                    result[key] = value
            yield result

    def form_one(self, index):
        self._flatten()

        result = {}
        new_index = int(index)
        for key, value, denom in zip(self._keys, self._values, self._denoms):
            vs = value[new_index // denom]
            new_index %= denom

            if isinstance(key, tuple):
                result.update(dict(zip(key, vs)))
            else:
                result[key] = vs

        return result


def test_vars():
    vars = Vars()
    vars.add('a', [1, 2])
    vars.add('b', [7, 8])
    assert list(vars.form_all()) == [
        {'a': 1, 'b': 7},
        {'a': 1, 'b': 8},
        {'a': 2, 'b': 7},
        {'a': 2, 'b': 8},
    ]
    assert vars.form_one(1) == {'a': 1, 'b': 8}
    assert vars.form_one(2) == {'a': 2, 'b': 7}

    vars = Vars()
    vars.add('b', [7, 8])
    vars.add('a', [1, 2])
    assert list(vars.form_all()) == [
        {'a': 1, 'b': 7},
        {'a': 2, 'b': 7},
        {'a': 1, 'b': 8},
        {'a': 2, 'b': 8},
    ]

    vars = Vars()
    vars.add('a', [1, 2])
    vars.add('b__c', [(7, 77), (8, 88), (9, 99)])
    assert list(vars.form_all()) == [
        {'a': 1, 'b': 7, 'c': 77},
        {'a': 1, 'b': 8, 'c': 88},
        {'a': 1, 'b': 9, 'c': 99},
        {'a': 2, 'b': 7, 'c': 77},
        {'a': 2, 'b': 8, 'c': 88},
        {'a': 2, 'b': 9, 'c': 99},
    ]
    assert vars.form_one(2) == {'a': 1, 'b': 9, 'c': 99}
    assert vars.form_one(3) == {'a': 2, 'b': 7, 'c': 77}

    vars = Vars()
    vars.add('b__c', [(7, 77), (8, 88), (9, 99)])
    vars.add('a', [1, 2])
    assert list(vars.form_all()) == [
        {'a': 1, 'b': 7, 'c': 77},
        {'a': 2, 'b': 7, 'c': 77},
        {'a': 1, 'b': 8, 'c': 88},
        {'a': 2, 'b': 8, 'c': 88},
        {'a': 1, 'b': 9, 'c': 99},
        {'a': 2, 'b': 9, 'c': 99},
    ]
    assert vars.form_one(2) == {'a': 1, 'b': 8, 'c': 88}
    assert vars.form_one(3) == {'a': 2, 'b': 8, 'c': 88}

    vars = Vars()
    assert list(vars.form_all()) == [{}]
    assert vars.form_one(0) == {}

    vars = Vars()
    vars.add('a', 'a_{ыфвфыв} = 4/5.0/8/-3 Дж / с')
    assert list(vars.form_all()) == [
        {'a': 'a_{ыфвфыв} = 4 Дж / с'},
        {'a': 'a_{ыфвфыв} = 5.0 Дж / с'},
        {'a': 'a_{ыфвфыв} = 8 Дж / с'},
        {'a': 'a_{ыфвфыв} = -3 Дж / с'},
    ]
    assert vars.form_one(0) == {'a': 'a_{ыфвфыв} = 4 Дж / с'}

    vars = Vars()
    vars.add('a', 'й/ц/у')
    assert list(vars.form_all()) == [
        {'a': 'й'},
        {'a': 'ц'},
        {'a': 'у'},
    ]
    assert vars.form_one(0) == {'a': 'й'}

test_vars()
