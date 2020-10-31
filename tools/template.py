import library.files

import itertools

import logging
log = logging.getLogger(__name__)

import datetime
import time
import os


def formatTimestamp(timestamp, fmt='%Y-%m-%d %H:%M:%S'):
    if isinstance(timestamp, int):
        return datetime.datetime.utcfromtimestamp(timestamp).strftime(fmt)
    elif isinstance(timestamp, datetime.datetime):
        return timestamp.strftime(fmt)
    else:
        raise RuntimeException(f'Unknown timestamp {timestamp}')


class NowDelta:
    def __init__(self, dt=None):
        if dt is None:
            self._now = datetime.datetime.now()
        else:
            if isinstance(dt, int):
                self._now = datetime.datetime.utcfromtimestamp(dt)
            elif isinstance(dt, datetime.datetime):
                self._now = dt
            else:
                raise RuntimeException(f'Unknown datetime {dt}')

    def _Format(self, dt, fmt=None):
        if fmt:
            return formatTimestamp(dt, fmt=fmt)
        else:
            return dt

    def Before(self, fmt=None, **kwargs):
        dt = self._now - datetime.timedelta(**kwargs)
        return self._Format(dt, fmt=fmt)

    def Now(self, fmt=None):
        dt = self._now
        return self._Format(dt, fmt=fmt)

    def After(self, fmt=None, **kwargs):
        dt = self._now + datetime.timedelta(**kwargs)
        return self._Format(dt, fmt=fmt)


def runTemplate(args):
    nowDelta = NowDelta()
    docxTemplate = library.location.udr('template-2-columns.docx')
    ipadTemplate = library.location.ipad('2020-21 Кружок', '2020-10-00 Кружок - Шаблон.docx')

    fileCopier = library.files.FileCopier(docxTemplate, destination_dir=library.location.udr('11 класс', '2020 весна'))
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
    circleCopier = library.files.FileCopier(ipadTemplate)

    nowFmt = nowDelta.Now(fmt='%F')
    futureFmt = nowDelta.After(days=12, fmt='%F')

    for date in [
        '2020-10-17',
    ]:
        if nowFmt <= date <= futureFmt:
            circleCopier.CreateFile(library.location.ipad('2020-21 Кружок', f'{date} Кружок.docx'))
        else:
            log.info(f'Skipping {date}')

    distantCopier = library.files.FileCopier(
        docxTemplate,
        destination_dir=library.location.ipad('2020-2 дистант')
    )
    for dateClass in [
        # '2020-10-20-10', '2020-10-20-9', '2020-10-22-9', '2020-10-22-10', '2020-10-23-10',  # week 2–1
        '2020-10-27-10',  # week 2–2
        '2020-10-27-9',
        '2020-10-29-9',
        '2020-10-29-10',
        '2020-10-30-10',
        '2020-10-30-8',
    ]:
        if nowFmt <= dateClass <= futureFmt:
            distantCopier.CreateFile(f'{dateClass} - с урока.docx')
        else:
            log.debug(f'Skipping {dateClass}')

    zoomRenamer = library.files.ZoomRenamer(library.files.Location.Zoom)
    for dir_name in library.files.walkFiles(library.files.Location.Zoom, dirsOnly=True, regexp='.*2198986972$'):
        zoomRenamer.RenameOne(dir_name)

    yesterday = nowDelta.Before(days=1, fmt='%F')
    monthAgo = nowDelta.Before(days=32, fmt='%F')
    fileMover = library.files.FileMover()
    # fileMover.Move(
    #     source=library.location.ipad('2020-21 Кружок'),
    #     destination=library.location.udr('12 - кружок - 9-10-11'),
    #     re='.*ужок.docx$',
    #     matching=lambda b: monthAgo <= b[:10] <= yesterday,
    # )
    # fileMover.Move(
    #     source=library.location.ipad('2020-2 дистант'),
    #     destination=library.location.udr('10 класс', '2020-21 10AБ Физика - Архив'),
    #     re='^....-..-..-10 .* с урока.docx$',
    #     matching=lambda b: monthAgo <= b[:10] <= yesterday
    # )
    # fileMover.Move(
    #     source=library.location.ipad('2020-2 дистант'),
    #     destination=library.location.udr('9 класс', '2020-21 9М Физика - Архив'),
    #     re='^....-..-..-9 .* с урока.docx$',
    #     matching=lambda b: monthAgo <= b[:10] <= yesterday,
    # )
    fileMover.Move(
        source=library.location.ipad('2020-2 дистант'),
        destination=library.location.udr('8 класс', '2020-21 Архив'),
        re='^....-..-..-8 .* с урока.docx$',
        # matching=lambda b: monthAgo <= b[:10] <= yesterday,
    )


def populate_parser(parser):
    parser.set_defaults(func=runTemplate)
