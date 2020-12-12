import os
import json

import logging
log = logging.getLogger(__name__)

from library.logging import cm


class Token:
    def __init__(self, file):
        if os.path.exists(file):
            with open(file) as f:
                data = json.load(f)
            log.warn(f'Loaded secrets from {cm(file, color="green")}')
        else:
            data = {}
            log.warn(f'Could not load secrets from missing file: {cm(file, bg="red")}')
        self._load(data)

    def _load(self, tokens_dict):
        self._tokens_dict = tokens_dict
        self.dnevnik_mos_ru_password = tokens_dict.get('dnevnik.mos.ru.password')  # get manually from browser

    def get(self, key):
        token = self._tokens_dict.get(key)
        if not token:
            raise RuntimeError(f'No token for {key}')
        token_length = len(token)
        if token_length < 20:
            token_mock = ': ' + '*' * token_length
        else:
            token_mock = f' of length {cm(token_length, color="green")}'
        log.info(f'Using token {cm(key, color="green")}{token_mock}')
        return token


token = Token(os.path.join(os.path.dirname(__file__), '..', 'secrets.json'))
