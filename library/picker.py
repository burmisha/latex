import library.logging

import logging
log = logging.getLogger(__name__)


class KeyPicker:
    def __init__(self, key=lambda x: x):
        self._options = {}
        self._keys = {}
        self._make_key = key

    def add(self, key, value):
        new_key = self._make_key(key)
        if new_key in self._keys:
            raise RuntimeError(f'Already got similar key for {key!r}: {self._keys[new_key]!r}')
        self._options[new_key] = value
        self._keys[new_key] = key

    def get(self, flt=None):
        matched_keys = sorted([key for key in self._options if not flt or self._make_key(flt) in key])
        
        if len(matched_keys) > 1:
            keys = [self._keys[key] for key in matched_keys]
            keys = library.logging.log_list(sorted(keys))
            log.warning(f'Too many matches for {flt}:{keys}')
        elif len(matched_keys) == 1:
            key = matched_keys[0]
            log.info(f'Found {self._keys[key]}')
            return self._options[key]
        else:
            keys = library.logging.log_list(sorted(self._keys.values()))
            log.warning(f'No search results for {flt}\nAvailable ones:{keys}')

        return None
