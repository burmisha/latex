import os
import json

import logging
log = logging.getLogger(__name__)

from library.logging import cm


class Token:
    def __init__(self, file):
        self._file = file
        self._tokens_dict = None

    def _load(self):
        file = self._file
        if os.path.exists(file):
            with open(file) as f:
                data = json.load(f)
            log.warn(f'Loaded secrets from {cm(file, color="red")}')
        else:
            data = {}
            log.warn(f'Could not load secrets from missing file: {cm(file, bg="red")}')

        return data

    def get(self, key):
        if self._tokens_dict is None:
            self._tokens_dict = self._load()

        token = self._tokens_dict.get(key)
        if not token:
            raise RuntimeError(f'No token for {key}')
        token_length = len(token)
        if token_length < 40:
            token_mock = ': ' + '*' * token_length
        else:
            token_mock = f' of length {cm(token_length, color="green")}'
        log.info(f'Using token {cm(key, color="green")}{token_mock}')
        return token


token = Token(os.path.join(os.path.dirname(__file__), '..', 'secrets.json'))
