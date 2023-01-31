import library.files
from library.pupils import get_study_year

from typing import List
import itertools
import datetime

import logging
log = logging.getLogger(__name__)

import os
import shutil


def today():
    now = datetime.datetime.now()
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


class LessonPaper:
    def __init__(self, name: str):
        if ('/' in name) or (name.count('.') > 1) or (not library.files.path_is_ok(name)):
            raise RuntimeError(f'Invalid lesson paper: {name}')
        self._name = name.split('.', 1)[0]
        self.dt = datetime.datetime.strptime(self._name[:10], '%Y-%m-%d')
        self._basename = f'{self._name}.docx'
        study_year = get_study_year(self._name)
        self._year_plus_one = f'{study_year}-' + f'{study_year+1}'[2:]

    @property
    def ipad_location(self) -> str:
        return library.location.ipad(f'{self._year_plus_one} Дистант', self._basename)

    @property
    def ready_location(self) -> str:
        pupils = library.pupils.get_class_from_string(self._name)
        if pupils is None:
            if ('ужок' not in self._name) and ('амена' not in self._name):
                raise RuntimeError(f'Invalid {self._name}')
            dst_dir = os.path.join('12 - кружок - 9-10-11', f'{self._year_plus_one} Кружок и допы')
        else:
            dst_dir = pupils.get_path(archive=True)
        return library.location.udr(dst_dir, self._basename)


assert LessonPaper('2023-01-29 Кружок').ipad_location.endswith('2022-23 Дистант/2023-01-29 Кружок.docx')
assert LessonPaper('2023-01-29 Кружок').ready_location.endswith('12 - кружок - 9-10-11/2022-23 Кружок и допы/2023-01-29 Кружок.docx')
assert LessonPaper('2021-06-30-10 - занятие').ipad_location.endswith('2020-21 Дистант/2021-06-30-10 - занятие.docx')
assert LessonPaper('2021-06-30-10 - занятие').ready_location.endswith('10 класс/2020-21 10АБ Физика - private/2021-06-30-10 - занятие.docx')


class TemplateConfig:
    def __init__(self, data: dict):
        self._data = data

    @property
    def lesson_papers(self) -> List[LessonPaper]:
        return [LessonPaper(row) for row in self._data['ipad']]


def create_lesson_papers(lesson_papers: List[LessonPaper], after_days: int):
    from_dt = today()
    to_dt = from_dt + datetime.timedelta(days=after_days)
    log.info(f'Creating files: from {from_dt:%Y-%m-%d} to {to_dt:%Y-%m-%d} (including)')

    ipadTemplate = library.location.udr('Шаблоны', 'template-2-columns.docx')
    ipadCopier = library.files.FileCopier(ipadTemplate)

    for lesson_paper in lesson_papers:
        if from_dt <= lesson_paper.dt <= to_dt:
            ipadCopier.CreateFile(lesson_paper.ipad_location)


def create_vishnyakova():
    one_column = library.files.FileCopier(
        library.location.udr('Шаблоны', 'template-1-column.docx'),
        destination_dir=library.location.udr('11 класс', 'Вишнякова'),
    )
    chapters = [
        # '1.1 - Кинематика',
        # '1.2 - Динамика',
        # '1.3 - Статика',
        # '1.4 - Законы сохранения',
        # '1.5 - Колебания и волны',
        # '2.1 - Молекулярная физика',
        # '2.2 - Термодинамика',
        # '3.1 - Электрическое поле',
        # '3.2 - Законы постоянного тока',
        '3.3 - Магнитное поле',
        '3.4 - Электромагнитная индукция',
        # '3.5 - Электромагнитные колебания и волны',
        # '3.6 - Оптика',
        # '4 - Основы СТО',
        # '5.1 - Корпускулярно-волновой дуализм',
        # '5.2 - Физика атома',
        # '5.3 - Физика атомного ядра',
    ]
    courses = [
        'БК',  # базовый курс
        # 'УК',  # углубленный курс
    ]
    for chapter, course in itertools.product(chapters, courses):
        one_column.CreateFile(f'Вишнякова - {chapter} - {course} - решения.docx')


def create_text_books():
    textbookTemplate = library.location.udr('Шаблоны', 'Рабочая тетрадь - Шаблон.docx')
    copier = library.files.FileCopier(textbookTemplate)
    for filename in [
        '10-1 - Кинематика',
        '10-2 - Динамика',
        '10-3 - Законы сохранения',
        '10-4 - Статика и гидростатика',
        '10-5 - Повторение механики',
        '10-6 - МКТ',
        '10-7 - Термодинамика',
        '10-8 - Электростатика',
        '10-9 - Постоянный ток',
        '11-1 - Магнитное поле',
        '11-2 - Электромагнитная индукция',
        '11-3 - Механические колебания',
        '11-4 - Электромагнитные колебания',
        '11-5 - Механические и ЭМ волны',
        '11-6 - Световые волны - Волновая оптика',
        '11-6 - Световые волны - Геометрическая оптика',
        '11-7 - Элементы теории относительности',
        '11-8 - Квантовая физика',
        '11-9 - Астрономия',
    ]:
        class_dir = filename.split('-', 1)[0] + ' класс'
        textbook_file = library.location.udr(class_dir, f'{filename} - Рабочая тетрадь.docx')
        copier.CreateFile(textbook_file)


def rename_zoom():
    zoomRenamer = library.files.ZoomRenamer(library.files.Location.Zoom)
    for dir_name in library.files.walkFiles(library.files.Location.Zoom, dirsOnly=True, regexp='.*2198986972$'):
        zoomRenamer.RenameOne(dir_name)


def move_from_ipad(lesson_papers, use_today: bool):
    to_date = today()
    if use_today:
        to_date += datetime.timedelta(days=1)

    log.info(f'Move files from iPad up to: {to_date}')

    available_ipad_dirs = set(
        os.path.dirname(lesson_paper.ipad_location)
        for lesson_paper in lesson_papers
    )
    all_ipad_files = [
        filename
        for ipad_dir in available_ipad_dirs
        for filename in library.files.walkFiles(ipad_dir, extensions=['.docx'])
    ]

    for ipad_file in all_ipad_files:
        lesson_paper = LessonPaper(os.path.basename(ipad_file))
        if lesson_paper.dt < to_date:
            if os.path.exists(lesson_paper.ready_location):
                raise RuntimeError(f'Exists {dst_file}')
            log.info(f'Moving {ipad_file!r} from iPad to {lesson_paper.ready_location!r}')
            shutil.move(ipad_file, lesson_paper.ready_location)
        else:
            log.info(f'Skipping iPad file: {src_file}')


def runTemplate(args):
    template_config = TemplateConfig(library.files.load_yaml_data('template.yaml'))
    create_lesson_papers(template_config.lesson_papers, args.after)
    create_vishnyakova()
    create_text_books()
    rename_zoom()
    move_from_ipad(template_config.lesson_papers, use_today=args.today)


def populate_parser(parser):
    parser.add_argument('-t', '--today', help='Today papers are ready, move them too', action='store_true')
    parser.add_argument('-a', '--after', help='After days', type=int, default=12)
    parser.set_defaults(func=runTemplate)
