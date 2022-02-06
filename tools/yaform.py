import library.files
import library.location
import library.logging
import library.pupils
import library.secrets
from library.logging import colorize_json, cm, color

import collections
import json
import os
import re
import time
import shutil

import requests

import logging
log = logging.getLogger(__name__)

EXTENSIONS = ['pdf', 'jpeg', 'jpg', 'png', 'docx', 'doc']

TODAY_WORK = 'Задание с урока'


class Description:
    def __init__(self, filename):
        self._filename = filename
        self._blocks = {}
        log.info(f'Description: {self._filename}')
        if not os.path.exists(self._filename):
            self.save()

        with open(self._filename, 'r') as f:
            block = []
            for line in f:
                if re.match(f'^#+ .*$', line):
                    self._add_block(block)
                    block = []
                block.append(line.strip())
            self._add_block(block)

    def _add_block(self, block):
        log.debug(f'Adding block {block} to {self._blocks}')
        if block:
            block_name = block[0].lstrip('#').strip()
            if not block_name:
                return None
            if block_name in self._blocks:
                return None
            self._blocks[block_name] = block
            return block_name
        else:
            return None

    def add_pupil(self, pupil_name):
        if pupil_name:
            self._add_block([f'## {pupil_name}', ''])

    def save(self):
        with open(self._filename, 'w') as f:
            for pupil_name in sorted(self._blocks):
                for line in self._blocks[pupil_name]:
                    f.write(line + '\n')


class AnswersJoiner:
    def __init__(self, form_id: str):
        self._form_id = form_id
        self._task_map = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))
        ya_cookie = library.secrets.token.get('ru.yandex.cookie')
        self._headers = {
            # 'Cookie': ya_cookie,
        }
        self._csrf_headers = {
            # 'Cookie': ya_cookie,
            # 'csrf-token': library.secrets.token.get('ru.yandex.token.csrf'),
        }
        self._known_files = self._get_known_files()

    def _get_known_files(self):
        files = {}
        files_dir = library.location.ya_disk('Yandex.Forms', self._form_id, 'Files')
        for file in library.files.walkFiles(files_dir):
            files[os.path.basename(file)] = os.path.join(files_dir, file)
        return files

    def add_answer(self, yf_answer):
        pupils = library.pupils.get_class_from_string(yf_answer.get_pupils_id())
        pupil = pupils.FindByName(yf_answer.get_pupil_name())
        pupils_dir = pupils.get_path(archive=True)
        work_id = yf_answer.get_work_id()
        pupil_name = pupil.GetFullName(surnameFirst=True)
        if not pupils_dir:
            log.warn(f'{cm("Skipping", color=color.Red)} {yf_answer} as got no pupils_dir')
        elif not work_id:
            log.warn(f'{cm("Skipping", color=color.Red)} {yf_answer} as got no work_id')
        elif not pupil_name:
            log.warn(f'{cm("Skipping", color=color.Red)} {yf_answer} as got no pupil_name')
        elif TODAY_WORK not in work_id and not work_id.startswith(str(pupils.Grade)):
            log.warn(f'{cm("Skipping", color=color.Red)} {yf_answer} as got broken work id')
        else:
            self._task_map[pupils_dir][work_id][pupil_name] += yf_answer.get_photos()

    def _download_to_file(self, link, filename):
        basename = link.split('/')[-1]
        if basename in self._known_files:
            ready_file = self._known_files[basename]
            shutil.copy(ready_file, filename)
            log.info(f'Copied into {ready_file} to {filename}')
            return

        log.info(f'Downloading {link} into {filename}')
        response = requests.get(link, headers=self._headers)
        if response.ok:
            with open(filename, 'wb') as f:
                f.write(response.content)
        else:
            log.warn(f'Failed to download {link}: {response.status_code}')
            raise RuntimeError('Failed to download file from Yandex')

    def _get_download_cfg(self):
        for pupils_dir, works in self._task_map.items():
            for work_name, answers in works.items():
                description = Description(os.path.join(pupils_dir, f'{work_name}.md'))
                for pupil_name, links in answers.items():
                    for index, link in enumerate(links, 1):
                        link_basename = link.split('_', 1)[1]
                        dir_name = os.path.join(pupils_dir, work_name)
                        file_name = f'{pupil_name} - {index:02d} - {link_basename}'
                        yield dir_name, pupil_name, link, file_name
                    description.add_pupil(pupil_name)
                description.save()

    def _already_downloaded(self, file_name):
        if os.path.exists(file_name):
            return True

        dir_name = os.path.dirname(file_name)
        base_name = os.path.basename(file_name)
        existing_files = list(library.files.walkFiles(dir_name, regexp=base_name))
        if existing_files:
            assert len(existing_files) == 1
            log.debug(f'{file_name} was downloaded to {existing_files[0]}')
            return True
        else:
            return False

    def _get_best_dir(self, dir_name, pupil_name):
        existing_files = list(library.files.walkFiles(dir_name, regexp=f'{pupil_name}.*'))
        if existing_files:
            dir_names = list(set(os.path.dirname(existing_file) for existing_file in existing_files))
            if len(dir_names) == 1:
                return dir_names[0]

        return dir_name

    def Download(self):
        log.info('Downloading all files')
        count, existing = 0, 0
        for dir_name, pupil_name, link, file_name in self._get_download_cfg():
            best_dir = self._get_best_dir(dir_name, pupil_name)
            full_name = os.path.join(best_dir, file_name)
            if not self._already_downloaded(full_name):
                if not os.path.isdir(best_dir):
                    log.info(f'Creating {best_dir}')
                    os.makedirs(best_dir, exist_ok=True)
                self._download_to_file(link, full_name)
                count += 1
            else:
                log.debug(f'File {file_name} for {pupil_name} already exists')
                existing += 1

        log.info(f'Downloaded {count} files and got {existing} existing ones')

    def sync_with_yadisk(self, form_id=None):
        data = {
            'method': 'POST',
            'path[name]': 'profile-survey-answers:export',
            'path[params][id]': form_id,
            'data': json.dumps({
                'export_columns': {
                    'answer_fields': 'id,date_created,date_updated',
                    'orders': True,
                    'questions': '5685839,5685855,5685930,5685860,5685887',
                    'user_fields': '',
                },
                'export_format':'json',
                'export_archived_answers': True,
                'upload': 'disk',
            }),
            'query[survey]': form_id,
        }
        response = requests.post('https://forms.yandex.ru/admin/_api', headers=self._csrf_headers, data=data)
        if response.ok:
            task_id = response.json()['task_id']
            log.info(f'Got task id {task_id}')
        else:
            log.error(f'Error at {response.url} and {colorize_json(data)}: {response.content}')
            raise RuntimeError(f'Failed to start sync task: {response}')


class YFAnswer:
    def __init__(self, row):
        self._original_name = row['Фамилия и имя']
        self._id = row['ID']
        self._create_time = row['Время создания']
        self._update_time = row['Время изменения']
        self._group_name = row['Выберите группу']
        self._photos = row['Фотографии решений']
        self._work_name = row['Что загружаем?']
        self._raw_data = row

    def __lt__(self, other):
        return self._create_time < other._create_time

    def get_work_id(self):
        if self._work_name == 'Работа на уроке за сегодня':
            work_id = f'{self._create_time[:10]} {TODAY_WORK}'
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
                try:
                    link = link.replace('forms.yandex.ru/u/files?path=', 'forms.yandex.ru/u/files/?path=')
                    assert link.split('.')[-1].lower() in EXTENSIONS
                    assert '_' in link
                    assert re.match('[0-9a-zA-Z\.\-_а-яА-Я ]+', link.split('_', 1)[1])
                    photos.append(link)
                except:
                    log.error(f'Failed on link {link}')
                    raise
        return photos

    def __str__(self):
        return ' - '.join([
            f'answer {cm(self._create_time, color=color.Yellow)}',
            f'{cm(self._work_name, color=color.Cyan)}',
            f'{cm(len(self.get_photos()), color=color.Magenta)} files',
            f'{cm(self._original_name, color=color.Green)}',
        ])


def get_latest_file(dir_name, regexp):
    candidates = library.files.walkFiles(dir_name, regexp=regexp)
    candidates = sorted(candidates, key=lambda f: os.path.getmtime(f))
    if candidates:
        candidate = candidates[-1]
        log.info(f'File with largest mtime: {cm(candidate, color=color.Cyan)}')
        return candidate
    else:
        return None


def run(args):
    sleep_time = args.sleep

    # old_form_id = '5fd491a3dfc5aebea76233ef'
    form_id = '61f81cd1e03b86bced1d0ebd'
    answers_page = f'https://forms.yandex.ru/admin/{form_id}/answers'
    ya_disk_page = f'https://disk.yandex.ru/client/disk/Yandex.Forms/{form_id}'

    log.info(f'Click «Save to Yandex.Disk» with images in JSON at {cm(answers_page, color=color.Green)}')
    log.info(f'Delete old versions at {cm(ya_disk_page, color=color.Green)}')

    answer_location = library.location.ya_disk('Yandex.Forms', form_id)
    regexp = r'.*202122 Физика 554.*\.json'
    old_latest_file = get_latest_file(answer_location, regexp)
    new_latest_file = None

    answers_joiner = AnswersJoiner(form_id)
    if args.sync:
        log.info(f'Syncing answers to dir {cm(answer_location, color=color.Green)}')
        answers_joiner.sync_with_yadisk(form_id)
        new_latest_file = get_latest_file(answer_location, regexp)
        while (new_latest_file is None) or (new_latest_file == old_latest_file):
            log.info(f'Waiting for {sleep_time} seconds for the new file to sync')
            time.sleep(sleep_time)
            new_latest_file = get_latest_file(answer_location, regexp)

    yandex_form_file = new_latest_file or old_latest_file
    log.info(f'Using: {cm(yandex_form_file, color=color.Cyan)}')
    with open(yandex_form_file) as f:
        yandex_form_raw = json.load(f)

    answers = [YFAnswer(dict(row)) for row in yandex_form_raw]
    answers.sort()
    for answer in answers:
        log.info(f'Got {answer}')
        answers_joiner.add_answer(answer)
    answers_joiner.Download()


def populate_parser(parser):
    parser.add_argument('-s', '--sync', help='Sync form data from yandex server to Yandex.Disk', action='store_true')
    parser.add_argument('--sleep', help='Sleep time for syncing', default=5, type=int)
    parser.set_defaults(func=run)
