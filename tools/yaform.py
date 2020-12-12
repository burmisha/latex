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


def add_pupil_lines(lines, pupil_name):
    blocks = []
    cur_block = []
    for line in lines:
        if re.match(f'^#+ .*$', line):
            if cur_block:
                blocks.append(cur_block)
            cur_block = [line]
        else:
            cur_block.append(line)
    if cur_block:
        blocks.append(cur_block)

    position = 0
    for block_index, block in enumerate(blocks):
        block_name = block[0].lstrip('#').strip()
        if block_name == pupil_name:
            return lines
        elif block_name < pupil_name:
            position += 1

    blocks = blocks[:position] + [[f'## {pupil_name}', '', '']] + blocks[position:]
    result = []
    for block in blocks:
        result.extend(block)
    return result


assert add_pupil_lines(['# A'], 'A') == ['# A']
assert add_pupil_lines(['# A', '## B'] , 'B') == ['# A', '## B']
assert add_pupil_lines(['# A', '## C'] , 'B') == ['# A', '## B', '', '', '## C']
assert add_pupil_lines(['# A', '## B'] , 'A') == ['# A', '## B']
assert add_pupil_lines(['# A', '## B'] , 'D') == ['# A', '## B', '## D', '', '']
assert add_pupil_lines(['# B', '### C'] , 'A') == ['## A', '', '', '# B', '### C']


class Description:
    def __init__(self, filename):
        self._filename = filename
        log.info(f'Description: {self._filename}')
        if not os.path.exists(self._filename):
            self._write_lines([])

    def _write_lines(self, lines):
        with open(self._filename, 'w') as f:
            for line in lines:
                f.write(line + '\n')

    def add_pupil(self, pupil_name):
        with open(self._filename, 'r') as f:
            lines = [line for line in f]

        new_lines = add_pupil_lines(lines, pupil_name)
        if new_lines != lines:
            self._write_lines(new_lines)


class AnswersJoiner:
    def __init__(self):
        self._task_map = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))
        self._headers = {
            'Cookie': library.secrets.token.get('yandex.ru.cookie'),
        }

    def add_answer(self, yf_answer):
        pupils = library.pupils.get_class_from_string(yf_answer.get_pupils_id())
        pupil = pupils.FindByName(yf_answer.get_pupil_name())
        pupils_dir = pupils.get_path(archive=True)
        work_id = yf_answer.get_work_id()
        pupil_name = pupil.GetFullName(surnameFirst=True)

        self._task_map[pupils_dir][work_id][pupil_name] += yf_answer.get_photos()

    def _download_to_file(self, link, filename):
        log.info(f'Downloading {link} into {filename}')
        response = requests.get(link, headers=self._headers)
        if response.ok:
            with open(filename, 'wb') as f:
                f.write(response.content)
        else:
            log.warn(f'Failed to download {link}')
            raise RuntimeError('Failed to download file from Yandex')

    def _get_download_cfg(self):
        for pupils_dir, works in self._task_map.items():
            for work_name, answers in works.items():
                description = Description(os.path.join(pupils_dir, f'{work_name}.md'))
                for pupil_name, links in answers.items():
                    for index, link in enumerate(links, 1):
                        link_basename = link.split('_', 1)[1]
                        file_name = os.path.join(
                            pupils_dir,
                            work_name,
                            f'{pupil_name} - {index:02d} - {link_basename}',
                        )
                        description.add_pupil(pupil_name)
                        yield link, file_name

    def Download(self):
        log.info('Downloading all files')
        for link, file_name in self._get_download_cfg():
            if not os.path.exists(file_name):
                os.makedirs(os.path.dirname(file_name), exist_ok=True)
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
        self._photos = row['Фотографии решений']
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

    def get_work_id(self):
        if self._work_name == 'Работа на уроке за сегодня':
            work_id = f'{self._create_time[:10]} Задание с урока'
        else:
            work_id = self._work_name
        return work_id

    def get_pupils_id(self):
        return f'{self._create_time[:10]} {self._group_name}'

    def get_pupil_name(self):
        return self._original_name

    def get_photos(self):
        photos = []
        for link in self._photos.split(', '):
            if link:
                link = link.replace('forms.yandex.ru/u/files?path=', 'forms.yandex.ru/u/files/?path=')
                assert link.split('.')[-1].lower() in ['pdf', 'jpeg', 'jpg', 'png']
                assert '_' in link
                assert re.match('[0-9a-zA-Z\.\-_а-яА-Я ]+', link.split('_', 1)[1])
                photos.append(link)
        return photos

    def __str__(self):
        return f'[{self._create_time}][{len(self._photos_list)} files] {self._work_name}: {self._original_name}'


def run(args):
    log.info('Forse JSON update at https://forms.yandex.ru/admin/5fd491a3dfc5aebea76233ef/answers')
    log.info('Delete old versions at https://disk.yandex.ru/client/disk/Yandex.Forms')

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
