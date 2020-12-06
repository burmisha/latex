from library.logging import log_list, cm

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

    def get_original_key(self, flt):
        matched_keys = sorted([key for key in self._keys if not flt or self._make_key(flt) in key])
        assert len(matched_keys) == 1
        return self._keys[matched_keys[0]]

    def _get_matched_keys(self, flt):
        flt_key = self._make_key(flt) if flt else None
        return flt_key, sorted([key for key in self._options if not flt or flt_key in key])

    def get(self, flt=None):
        flt_key, matched_keys = self._get_matched_keys(flt)
        if len(matched_keys) > 1:
            keys = [self._keys[key] for key in matched_keys]
            keys = log_list(sorted(keys))
            log.warning(f'Too many matches for {flt}:{keys}')
        elif len(matched_keys) == 1:
            key = matched_keys[0]
            log.info(f"Found '{cm(self._keys[key], color='cyan')}' (as '{key}' for '{flt_key}')")
            return self._options[key]
        else:
            keys = log_list(sorted(self._keys.values()))
            log.warning(f'No search results for {flt}\nAvailable ones:{keys}')

        return None

    def all(self, flt=None):
        flt_key, matched_keys = self._get_matched_keys(flt)
        for key in matched_keys:
            yield self._options[key]
