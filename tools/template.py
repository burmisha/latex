import library.files

import itertools

import logging
log = logging.getLogger(__name__)


def runTemplate(args):
    fileCopier = library.files.FileCopier(library.files.udrPath('template-2-columns.docx'))
    fileCopier.SetDestinationDir(library.files.udrPath(u'11 класс', u'2020 весна'))
    chapters = [
        # u'1.1 - Кинематика',
        # u'1.2 - Динамика',
        # u'1.3 - Статика',
        # u'1.4 - Законы сохранения',
        # u'1.5 - Колебания и волны',
        # u'2.1 - Молекулярная физика',
        # u'2.2 - Термодинамика',
        # u'3.1 - Электрическое поле',
        # u'3.2 - Законы постоянного тока',
        # u'3.3 - Магнитное поле',
        # u'3.4 - Электромагнитная индукция',
        # u'3.5 - Электромагнитные колебания и волны',
        # u'3.6 - Оптика',
        # u'4 - Основы СТО',
        # u'5.1 - Корпускулярно-волновой дуализм',
        # u'5.2 - Физика атома',
        # u'5.3 - Физика атомного ядра',
    ]
    courses = [
        u'БК',  # базовый курс
        # u'УК',  # углубленный курс
    ]
    file_types = [
        u'решения',
        u'условия',
    ]
    for chapter, course, file_type in itertools.product(chapters, courses, file_types):
        filename = u'Вишнякова - %s - %s - %s.docx' % (chapter, course, file_type)
        fileCopier.CreateFile(filename)


def populate_parser(parser):
    parser.set_defaults(func=runTemplate)
