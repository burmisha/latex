import csv
import re
import datetime
import collections

import library.pupils

from library.logging import colorize_json, cm, color, log_list

import logging
log = logging.getLogger(__name__)

NAME_MAPPING = {
    'Barbara Egiazaryan': 'Варвара Егиазарян',
    'lesha alimpiev': 'Алексей Алимпиев',
}
AVAILABLE_PUPILS_KEYS = ('2020 10', '2020 9')
MATCHED_THRESHOLD = 0.8
SURNAME_FIRST = True


class ParticipantAction:
    JOINED = 0
    LEFT = 1

    def __init__(self, raw_name=None, action_name=None, time_label=None):
        raw_name = re.sub(r' *\(.*\)', '', raw_name).strip()
        raw_name = NAME_MAPPING.get(raw_name, raw_name)
        self._raw_name = raw_name
        self._name = None
        self._type = {
            'Присоединился': self.JOINED,
            'Присоединились раньше': self.JOINED,
            'Ушел': self.LEFT,
        }[action_name]
        self._time = datetime.datetime.strptime(time_label, '%d.%m.%Y, %H:%M:%S')

    def set_name(self, pupils):
        self._name = pupils.FindByName(self._raw_name).GetFullName(surnameFirst=SURNAME_FIRST)

    def __str__(self):
        action_color, action_name = {self.JOINED: (color.Green, 'joined'), self.LEFT: (color.Red, 'left')}[self._type]
        return f'{cm(self._name or self._raw_name, color=color.Cyan)} {cm(action_name, color=action_color)} on {self._time}'

    def __lt__(self, other):
        if self._name is None:
            assert other._name is None
            self_name = self._raw_name
            other_name = other._raw_name
        else:
            assert other._name is not None
            self_name = self._name
            other_name = other._name

        if self_name < other_name:
            return True
        elif self_name == other_name:
            if self._time < other._time:
                return True
            elif self._time == other._time:
                if self._type < other._type:
                    return True

        return False


class MSTeamsVisitors:
    def __init__(self, filename):
        self._filename = filename
        self._actions = list(self._load())
        for action in self._actions:
            log.info(action)
        first_action_time = min(action._time for action in self._actions)
        active_raw_name = set(action._raw_name for action in self._actions)
        log.info(f'First action was on {cm(first_action_time, color=color.Yellow)}')
        matched_rates = {}
        for pupils_key in AVAILABLE_PUPILS_KEYS:
            pupils = library.pupils.get_class_from_string(pupils_key)
            matched_count = sum(pupils.FindByName(raw_name, use_raw_if_missing=False) is not None for raw_name in active_raw_name)
            matched_rates[pupils_key] = matched_count / len(active_raw_name)
        log.info(f'Matched rates: {colorize_json(matched_rates)}')
        ok_keys = [key for key, value in matched_rates.items() if value > MATCHED_THRESHOLD]
        assert len(ok_keys) == 1
        self._pupils = library.pupils.get_class_from_string(ok_keys[0])

        for action in self._actions:
            action.set_name(self._pupils)
        # self._actions = sorted(self._actions)

        all_pupils = collections.defaultdict(list)
        for action in self._actions:
            all_pupils[action._name].append(action)

        missing_names = []
        for pupil in self._pupils.Iterate():
            full_name = pupil.GetFullName(surnameFirst=SURNAME_FIRST)
            if full_name in all_pupils:
                log.info(f'Visitor {full_name}:{log_list(all_pupils[full_name])}')
            else:
                missing_names.append(full_name)
        log.info(f'Absent pupils:{log_list(missing_names)}')



    def _load(self):
        log.info(f'Loading {cm(self._filename, color=color.Yellow)}')
        with open(self._filename, 'r', encoding='utf-16le') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                yield ParticipantAction(
                    raw_name=row['\ufeffПолное имя'],
                    action_name=row['Действие пользователя'],
                    time_label=row['Метка времени'],
                )
