import itertools

import logging
log = logging.getLogger(__name__)


class Vars:
    def __init__(self):
        self._keys = []
        self._original_keys = []
        self._values = []
        self._fixed = False

    def _flatten(self):
        if self._fixed:
            return

        self._fixed = True
        for index, (key, values) in enumerate(zip(self._keys, self._values)):
            assert isinstance(key, str), f'key {key} is not str'
            # TODO: lazy getter for large lists
            self._values[index] = list(values)
            values = self._values[index]
            if any(isinstance(v, tuple) for v in values):
                assert all(isinstance(v, tuple) for v in values)
                key = tuple(part.strip() for part in key.split('__'))
                assert all(len(v) == len(key) for v in values)
                self._keys[index] = key

            assert isinstance(self._values[index], list)

        # TODO: check all parts of key
        # assert key not in self._keys, f'Already used key {key}: {self._keys}'

        self._denoms = [1 for v in self._values]
        for i in range(len(self._values) - 2, -1, -1):
            self._denoms[i] = self._denoms[i + 1] * len(self._values[i + 1])


    def add(self, key, values):
        if isinstance(values, tuple):
            assert len(values) == 2
            assert '{}' in values[0], f'No {{}} in {values}'
            values = [values[0].format(option) for option in values[1]]

        try:
            assert not self._fixed
            self._original_keys.append(key)
            self._keys.append(key)
            self._values.append(values)
        except:
            log.error(f'Failed to add {key} and {vs}')
            raise

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


test_vars()
