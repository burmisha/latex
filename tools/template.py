import library.datetools
import library.files

import itertools

import logging
log = logging.getLogger(__name__)

import os


def runTemplate(args):
    nowDelta = library.datetools.NowDelta()
    docxTemplate = library.location.udr('Шаблоны', 'template-2-columns.docx')
    ipadTemplate = library.location.ipad('2020-21 Кружок', '2020-10-00 Кружок - Шаблон.docx')

    fileCopier = library.files.FileCopier(docxTemplate, destination_dir=library.location.udr('11 класс', 'Вишнякова'))
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

    ipadTemplate = library.location.ipad('2020-21 Кружок', '2020-10-00 Кружок - Шаблон.docx')
    ipadCopier = library.files.FileCopier(ipadTemplate)

    nowFmt = nowDelta.Now(fmt='%F')
    futureFmt = nowDelta.After(days=12, fmt='%F')

    for date in [
        '2020-10-17',
    ]:
        if nowFmt <= date <= futureFmt:
            ipadCopier.CreateFile(library.location.ipad('2020-21 Кружок', f'{date} Кружок.docx'))
        else:
            log.info(f'Skipping {date}')

    textbookTemplate = library.location.udr('Шаблоны', 'Рабочая тетрадь - Шаблон.docx')
    for class_dir, filenames in {
        '9 класс': [
        ],
        '10 класс': [
            '10-1 - Кинематика',
            '10-2 - Динамика',
            '10-3 - Законы сохранения',
            '10-4 - Статика и гидростатика',
            '10-5 - МКТ',
            '10-6 - Термодинамика',
            '10-7 - Электростатика',
            '10-8 - Постоянный ток',
        ],
    }.items():
        copier = library.files.FileCopier(textbookTemplate, destination_dir=library.location.udr(class_dir))
        for filename in filenames:
            copier.CreateFile(f'{filename} - Рабочая тетрадь.docx')


    distantCopier = library.files.FileCopier(
        docxTemplate,
        destination_dir=library.location.ipad('2020 дистант')
    )
    for dateClass in [
        # '2020-10-20-10', '2020-10-20-9', '2020-10-22-9', '2020-10-22-10', '2020-10-23-10',  # week 2–1
        # '2020-10-27-10', '2020-10-27-9', '2020-10-29-9', '2020-10-29-10', '2020-10-30-10', '2020-10-30-8', # week 2–2
        # '2020-11-03-10', '2020-11-03-9', '2020-11-05-9', '2020-11-05-10', '2020-11-06-10',  # week 2–4
        #                                  '2020-11-12-9', '2020-11-12-10', '2020-11-13-10',  # week 2–3 is missing some lessons
        # '2020-11-17-10', '2020-11-17-9', '2020-11-19-9', '2020-11-19-8',                    # week 2–5
        # '2020-11-24-10', '2020-11-24-9', '2020-11-26-9', '2020-11-26-10', '2020-11-27-10'  # week 3–1
        '2020-12-01-10', '2020-12-01-9', '2020-12-03-9', '2020-12-03-10', '2020-12-04-10'  # week 3–2
    ]:
        if nowFmt <= dateClass <= futureFmt:
            distantCopier.CreateFile(f'{dateClass} - с урока.docx')
        else:
            log.info(f'Skipping {dateClass}: {nowFmt}, {futureFmt}')

    zoomRenamer = library.files.ZoomRenamer(library.files.Location.Zoom)
    for dir_name in library.files.walkFiles(library.files.Location.Zoom, dirsOnly=True, regexp='.*2198986972$'):
        zoomRenamer.RenameOne(dir_name)

    yesterday = nowDelta.Before(days=1, fmt='%F')
    monthAgo = nowDelta.Before(days=32, fmt='%F')
    fileMover = library.files.FileMover()
    fileMover.Move(
        source=library.location.ipad('2020-21 Кружок'),
        destination=library.location.udr('12 - кружок - 9-10-11'),
        re='.*ужок.docx$',
        matching=lambda b: monthAgo <= b[:10] <= yesterday,
    )
    fileMover.Move(
        source=library.location.ipad('2020 дистант'),
        destination=library.location.udr('10 класс', '2020-21 10АБ Физика - Архив'),
        re='^....-..-..-10 .* с урока.*\.docx$',
        matching=lambda b: monthAgo <= b[:10] <= yesterday,
    )
    fileMover.Move(
        source=library.location.ipad('2020 дистант'),
        destination=library.location.udr('9 класс', '2020-21 9М Физика - Архив'),
        re='^....-..-..-9 .* с урока.*\.docx$',
        matching=lambda b: monthAgo <= b[:10] <= yesterday,
    )
    fileMover.Move(
        source=library.location.ipad('2020 дистант'),
        destination=library.location.udr('8 класс', '2020-21 Архив'),
        re='^....-..-..-8 .* с урока.*\.docx$',
        matching=lambda b: monthAgo <= b[:10] <= yesterday,
    )


def populate_parser(parser):
    parser.set_defaults(func=runTemplate)
