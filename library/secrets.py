import os
import json

import logging
log = logging.getLogger(__name__)

import library.logging
cm = library.logging.ColorMessage()


class Token:
    def __init__(self, file):
        
        if os.path.exists(file):
            with open(file) as f:
                data = json.load(f)
            log.warn(f'Loaded secrets from: {cm(file, color="green")}')
        else:
            data = {}
            log.warn(f'Could not load secrets from missing file: {cm(file, bg="red")}')
        self._load(data)

    def _load(self, tokens_dict):
        self.dnevnik_mos_ru_password = tokens_dict.get('dnevnik.mos.ru.password')  # get manually from browser


token = Token(os.path.join(os.path.dirname(__file__), '..', 'secrets.json'))
