
def to_plain_list(config, prefix='', sep='.'):
    if isinstance(config, dict):
        new_prefix = f'{prefix}{sep}' if prefix else ''
        for key, value in config.items():
            for result in to_plain_list(value, prefix=f'{new_prefix}{key}', sep=sep):
                yield result
    elif isinstance(config, list):
        for value in config:
            for result in to_plain_list(value, prefix=prefix, sep=sep):
                yield result
    elif isinstance(config, str):
        if prefix:
            yield f'{prefix}{sep}{config}'
        else:
            yield f'{config}'
    else:
        raise RuntimeError(f'Invalid config: {config}')


def test_to_plain_list():
    data = [
        ({}, []),
        ([], []),
        ('a', ['a']),
        (['a'], ['a']),
        (['a', 'b'], ['a', 'b']),
        ({'a': 'b'}, ['a.b']),
        (['a', {'b': 'c'}], ['a', 'b.c']),
        (['a', {'b': ['c', 'd']}], ['a', 'b.c', 'b.d']),
    ]
    for config, result in data:
        res = list(to_plain_list(config))
        assert res == result, f'got {res} != expected {result}'


test_to_plain_list()


def follow_dots(base, key, sep='.'):
    assert isinstance(key, str)
    b = base
    for part in key.split(sep):
        b = getattr(b, part)
    return b
