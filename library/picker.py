from library.logging import log_list, cm, color

import logging
log = logging.getLogger(__name__)


def letters_key(key):
    assert isinstance(key, str), f'Key is not str, but {type(key)}: {key}'
    return ''.join(l for l in key if l.isalpha() or l.isdigit()).lower()


class KeyPicker:
    def __init__(self, key=lambda x: x):
        self._options = {}
        self._keys = {}
        self._make_key = key

    def add(self, key, value):
        if not value:
            raise RuntimeError(f'Cannot save empty value: {value}')
        new_key = self._make_key(key)
        if new_key in self._keys:
            raise RuntimeError(f'Already got similar key for {key!r}: {self._keys[new_key]!r}')
        self._options[new_key] = value
        self._keys[new_key] = key

    def _get_matched_keys(self, flt):
        flt_key = self._make_key(flt) if flt else None
        result = sorted([key for key in self._options if not flt or flt_key in key])
        if len(result) > 1:
            if result.count(flt_key) == 1:
                return flt_key, [flt_key]
        return flt_key, result

    def get(self, flt=None):
        assert flt is None or isinstance(flt, str)
        flt_key, matched_keys = self._get_matched_keys(flt)
        if len(matched_keys) > 1:
            keys = [self._keys[key] for key in matched_keys]
            keys = log_list(sorted(keys))
            log.warning(f'Too many matches for filter {flt!r}:{keys}')
            return None
        elif len(matched_keys) == 1:
            key = matched_keys[0]
            log.debug(f"Found '{cm(self._keys[key], color=color.Cyan)}' (as '{key}' for '{flt_key}')")
            return self._options[key]
        else:
            log.debug(f'No search results for {flt}')
            return None

    def __str__(self):
        keys = log_list(sorted(self._keys.values()))
        return 'Available keys:{keys}'

    def all(self, flt=None):
        flt_key, matched_keys = self._get_matched_keys(flt)
        for key in matched_keys:
            yield self._options[key]
