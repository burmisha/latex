import library.datetools
import library.files
from library.pupils import get_study_year

from typing import Iterable
import itertools
import datetime

import logging
log = logging.getLogger(__name__)

import os
import shutil

AFTER_DAYS = 12


class LessonPaper:
    def __init__(self, name: str):
        if ('/' in name) or (name.count('.') > 1) or (not library.files.path_is_ok(name)):
            raise RuntimeError(f'Invalid lesson paper: {name}')
        self._name = name.split('.', 1)[0]
        self.dt = datetime.datetime.strptime(name[:10], '%Y-%m-%d')

    @property
    def year_plus_one(self):
        study_year = get_study_year(self._name)
        return f'{study_year}-' + f'{study_year+1}'[2:]

    @property
    def ipad_dirname(self) -> str:
        return f'{self.year_plus_one} Дистант'

    @property
    def basename(self) -> str:
        return f'{self._name}.docx'

    @property
    def ipad_location(self) -> str:
        return os.path.join(self.ipad_dirname, self.basename)

    @property
    def ready_location(self) -> str:
        pupils = library.pupils.get_class_from_string(self._name)
        if pupils is None:
            if ('ужок' not in self.basename) and ('амена' not in self.basename):
                raise RuntimeError(f'Invalid {self._name}')
            dst_dir = os.path.join('12 - кружок - 9-10-11', f'{self.year_plus_one} Кружок и допы')
        else:
            dst_dir = pupils.get_path(archive=True)
        return os.path.join(dst_dir, self.basename)


class TemplateConfig:
    def __init__(self, data: dict):
        self._data = data

    @property
    def lesson_papers(self) -> Iterable[LessonPaper]:
        for row in self._data['ipad']:
            yield LessonPaper(row)


def runTemplate(args):
    nowDelta = library.datetools.NowDelta()
    template_config = TemplateConfig(library.files.load_yaml_data('template.yaml'))

    now = datetime.datetime.now()
    future = now + datetime.timedelta(days=AFTER_DAYS)

    ipadTemplate = library.location.udr('Шаблоны', 'template-2-columns.docx')
    ipadCopier = library.files.FileCopier(ipadTemplate)
    for lesson_paper in template_config.lesson_papers:
        if now <= lesson_paper.dt <= future:
            ipadCopier.CreateFile(library.location.ipad(lesson_paper.ipad_location))

    one_column_template = library.location.udr('Шаблоны', 'template-1-column.docx')
    one_column = library.files.FileCopier(one_column_template, destination_dir=library.location.udr('11 класс', 'Вишнякова'))
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


    textbookTemplate = library.location.udr('Шаблоны', 'Рабочая тетрадь - Шаблон.docx')
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
        copier = library.files.FileCopier(textbookTemplate, destination_dir=library.location.udr(class_dir))
        copier.CreateFile(f'{filename} - Рабочая тетрадь.docx')

    zoomRenamer = library.files.ZoomRenamer(library.files.Location.Zoom)
    for dir_name in library.files.walkFiles(library.files.Location.Zoom, dirsOnly=True, regexp='.*2198986972$'):
        zoomRenamer.RenameOne(dir_name)

    last_date = now - datetime.timedelta(days=0 if args.today else 1)

    ipad_dirnames = {
        lesson_paper.ipad_dirname
        for lesson_paper in template_config.lesson_papers
    }
    ipad_files = [
        filename
        for ipad_dirname in ipad_dirnames
        for filename in library.files.walkFiles(
            library.location.ipad(ipad_dirname),
            extensions=['.docx']
        )
    ]
    for src_file in ipad_files:
        lesson_paper = LessonPaper(os.path.basename(src_file))
        if lesson_paper.dt <= last_date:
            dst_file = library.location.udr(lesson_paper.ready_location)
            if os.path.exists(dst_file):
                raise RuntimeError(f'Exists {dst_file}')
            log.info(f'Moving file {src_file!r} to {dst_file!r}')
            shutil.move(src_file, dst_file)
        else:
            log.info(f'Skipping ipad file: {src_file}')


def populate_parser(parser):
    parser.add_argument('-t', '--today', help='Today papers are ready, move them too', action='store_true')
    parser.set_defaults(func=runTemplate)
