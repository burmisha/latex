import library.files

import itertools

import logging
log = logging.getLogger(__name__)


def runTemplate(args):
    fileCopier = library.files.FileCopier(library.files.udrPath('template-2-columns.docx'))
    fileCopier.SetDestinationDir(library.files.udrPath('11 класс', '2020 весна'))
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
        # '3.3 - Магнитное поле',
        # '3.4 - Электромагнитная индукция',
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
        fileCopier.CreateFile(f'Вишнякова - {chapter} - {course} - решения.docx')


def populate_parser(parser):
    parser.set_defaults(func=runTemplate)
