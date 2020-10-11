# -*- coding: utf-8 -*-

import library

import itertools
import os
import shutil

import logging
log = logging.getLogger(__name__)


class FileCopier(object):
    def __init__(self, source_file, destination_dir=None):
        assert os.path.exists(source_file)
        assert os.path.isfile(source_file)
        self._source_file = source_file
        log.info(u'Using source file \'%s\'', self._source_file)

        if destination_dir is None:
            self._destination_dir = None
        else:
            self.SetDestinationDir(destination_dir)

    def SetDestinationDir(self, destination_dir):
        assert os.path.exists(destination_dir)
        assert os.path.isdir(destination_dir)
        self._destination_dir = destination_dir
        log.info(u'Using destination dir \'%s\'', self._destination_dir)

    def CreateFile(self, destination_file):
        if self._destination_dir:
            destination_path = os.path.join(self._destination_dir, destination_file)
        else:
            destination_path = destination_file

        if not os.path.exists(destination_path):
            log.info(u'Creating \'%s\' from template', destination_path)
            shutil.copy(self._source_file, destination_path)
        else:
            log.debug(u'File %s already exists', destination_path)


class PdfExtractor(object):
    def __init__(self, source_file):
        # https://apple.stackexchange.com/questions/99210/mac-os-x-how-to-merge-pdf-files-in-a-directory-according-to-their-file-names
        # brew install poppler
        assert os.path.exists(source_file)
        assert os.path.isfile(source_file)
        assert source_file.endswith('.pdf')
        self._source_file = source_file
        self._tmp_dir = os.path.join(os.environ['HOME'], 'tmp')

    def Extract(self, pages, destination_file):
        log.info('Extracting pages %s to %s', pages, destination_file)
        assert isinstance(pages, str)
        assert destination_file.endswith('.pdf')
        parts = []
        for index, pages_range in enumerate(pages.split(',')):
            pages_range = pages_range.strip()
            if '-' in pages_range:
                first_page, last_page = pages_range.split('-')
            else:
                first_page, last_page = pages_range, pages_range
            first_page, last_page = int(first_page), int(last_page)
            assert first_page <= last_page

            part_file = os.path.join(self._tmp_dir, 'part_%d.pdf')
            for page_index in range(first_page, last_page + 1):
                parts.append(part_file % page_index)
            separate_command = [
                'pdfseparate',
                '-f', '%d' % first_page,
                '-l', '%d' % last_page,
                self._source_file,
                part_file,
            ]
            library.process.run(separate_command)

        assert len(set(parts)) == len(parts)
        unite_command = ['pdfunite'] + parts + [destination_file]
        library.process.run(unite_command)

        for part_file in parts:
            log.debug('Removing tmp file %s', part_file)
            os.remove(part_file)


def runTemplate(args):
    fileCopier = FileCopier(library.files.udrPath('template-2-columns.docx'))
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

    if args.docx_2_pdf:
        docxToPdf = DocxToPdf()
        docxToPdf.ConvertDir(
            library.files.udrPath(u'11 класс', u'2020 весна'),
            recursive=False,
            regexp=u'.*Вишнякова - [0-9].*',
        )
        docxToPdf.ConvertDir(
            library.files.udrPath(u'10 класс'),
            destination_directory=u'2020-21 10AБ Физика',
            recursive=False,
            regexp=u'.*Неделя.*',
        )
        docxToPdf.ConvertDir(
            library.files.udrPath(u'10 класс'),
            recursive=False,
            regexp=u'.*Рабочая тетрадь.*',
        )

    if args.run_extractor:
        pdfExtractor = PdfExtractor(library.files.udrPath(u'10 класс', u'10-1 - Кинематика - Рабочая тетрадь.pdf'))
        pdfExtractor.Extract('5, 1-4', library.files.udrPath(u'10 класс', u'tmp.pdf'))


def populate_parser(parser):
    parser.add_argument('--run-extractor', help='Extract pdf files', action='store_true')
    parser.set_defaults(func=runTemplate)
