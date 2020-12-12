import library.files
import library.location
import library.logging
import library.pupils
import library.secrets

import collections
import json
import os
import re

import requests

import logging
log = logging.getLogger(__name__)


class AnswersJoiner:
    GROUP_CONFIG = {
        '2020-9-М': library.location.udr('9 класс', '2020-21 9М Физика - Архив'),
        '2020-10-АБ': library.location.udr('10 класс', '2020-21 10АБ Физика - Архив'),
    }

    def __init__(self):
        self._task_map = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))
        self._headers = {
            'Cookie': library.secrets.token.get('yandex.ru.cookie'),
        }

    def add_answer(self, yf_answer):
        pupils = library.pupils.get_class_from_string(
            f'{yf_answer._create_time[:10]} {yf_answer._group_name}',
            addMyself=True,
        )
        pupil = pupils.FindByName(yf_answer._original_name)

        pupils_id = pupils._id

        if yf_answer._work_name == 'Работа на уроке за сегодня':
            work_id = f'{yf_answer._update_time[:10]} Задание с урока'
        else:
            work_id = yf_answer._work_name

        pupil_name = pupil.GetFullName(surnameFirst=True)

        self._task_map[pupils_id][work_id][pupil_name] += yf_answer._photos_list

    def _download_to_file(self, link, filename):
        log.info(f'Downloading {link} into {filename}')
        response = requests.get(link, headers=self._headers)
        if response.ok:
            with open(filename, 'wb') as f:
                f.write(response.content)
        else:
            log.warn(f'Failed to download {link}')
            raise RuntimeError('Failed to download file from Yandex')

    def Download(self):
        log.info('Downloading all files')
        for pupils_id, works in self._task_map.items():
            for work_name, answers in works.items():
                for pupil_name, links in answers.items():
                    for index, link in enumerate(links, 1):
                        link_basename = link.split('_', 1)[1]
                        dir_name = os.path.join(
                            self.GROUP_CONFIG[pupils_id],
                            work_name
                        )
                        file_name = os.path.join(
                            dir_name,
                            f'{pupil_name} - {index:02d} - {link_basename}',
                        )
                        os.makedirs(dir_name, exist_ok=True)
                        if not os.path.exists(file_name):
                            self._download_to_file(link, file_name)
                        else:
                            log.debug('File already exists')

        log.info('Downloaded all files')


class YFAnswer:
    def __init__(self, row):
        self._original_name = row['Фамилия и имя']
        self._id = row['ID']
        self._create_time = row['Время создания']
        self._update_time = row['Время изменения']
        self._group_name = row['Выберите группу']
        photos = []
        for link in row['Фотографии решений'].split(', '):
            if link:
                link = link.replace('forms.yandex.ru/u/files?path=', 'forms.yandex.ru/u/files/?path=')
                assert link.split('.')[-1].lower() in ['pdf', 'jpeg', 'jpg', 'png']
                assert '_' in link
                assert re.match('[0-9a-zA-Z\.\-_а-яА-Я ]+', link.split('_', 1)[1])
                photos.append(link)
        self._photos_list = photos
        self._work_name = row['Что загружаем?']

    def __str__(self):
        return f'[{self._create_time}][{len(self._photos_list)} files] {self._work_name}: {self._original_name}'


def run(args):
    log.info('Delete old versions at https://disk.yandex.ru/client/disk/Yandex.Forms')
    log.info('Forse JSON update at https://forms.yandex.ru/admin/5fd491a3dfc5aebea76233ef/answers')

    answer_location = library.location.ya_disk('Yandex.Forms')
    candidates = library.files.walkFiles(answer_location, regexp=r'.*202021 Физика 554.*\.json')
    yandex_form_file = sorted(candidates)[-1]
    log.info(f'Using {yandex_form_file} as having largest filename')

    with open(yandex_form_file) as f:
        yandex_form_raw = json.load(f)

    answers_joiner = AnswersJoiner()
    answers = [YFAnswer(dict(row)) for row in yandex_form_raw]
    answers.sort(key=lambda x: x._create_time)
    for answer in answers:
        answers_joiner.add_answer(answer)
    answers_joiner.Download()


def populate_parser(parser):
    parser.set_defaults(func=run)
