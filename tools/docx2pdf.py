import library.convert
import library.files
import library.location
import library.pupils

import os
import yaml

import logging
log = logging.getLogger(__name__)


class PdfExtractor:
    def __init__(self, source_file=None, destination_directory=None):
        self._source_file = source_file
        if destination_directory:
            self._destination_directory = os.path.join(os.path.dirname(self._source_file), destination_directory)
        else:
            self._destination_directory = os.path.dirname(self._source_file)
        assert library.files.is_file(self._source_file)
        assert library.files.is_dir(self._destination_directory)

        self._pdf2pdf = library.convert.PdfToPdf(self._source_file)

    def Extract(self, pages, destination_filename):
        dst_file = os.path.join(self._destination_directory, destination_filename)
        if library.files.is_older(self._source_file, dst_file):
            log.debug(f'Skipping updated file \'{destination_filename}\' (no pages check: {pages})')
        else:
            self._pdf2pdf.Extract(pages, dst_file)


def get_convert_config():
    pupils_9m = library.pupils.get_class_from_string('2020 9М')
    pupils_10ab = library.pupils.get_class_from_string('2020 10АБ')
    pupils_11ba = library.pupils.get_class_from_string('2021 11БА')

    return [
        (library.location.udr('11 класс', 'Вишнякова'), 'generated', False, '.*Вишнякова - [0-9].*'),
        (library.location.udr('11 класс', 'Вишнякова'), 'generated', False, '.*Вишнякова - .* - Все условия.*'),
        (library.location.udr('11 класс'), None, False, '.*Рабочая тетрадь.*'),
        (library.location.udr('10 класс'), None, False, '.*Рабочая тетрадь.*'),
        (library.location.udr('9 класс'), None, False, '.*Рабочая тетрадь.*'),
        (
            library.location.ipad('2020-21 Кружок'),
            library.location.udr('12 - кружок - 9-10-11', '2020-21 Кружок и допы - Видео и материалы'),
            True,
            r'.*\b[Кк]ружок.*\.docx$',
        ),
        (
            library.location.udr('12 - кружок - 9-10-11'),
            '2020-21 Кружок и допы - Видео и материалы',
            False,
            r'.*\b[Кк]ружок.*\.docx$',
        ),
        (
            pupils_10ab.get_path(archive=True),
            pupils_10ab.get_path(archive=False),
            False,
            r'.*с урока.*\.docx$',
        ),
        (
            pupils_9m.get_path(archive=True),
            pupils_9m.get_path(archive=False),
            False,
            r'.*с урока.*\.docx$',
        ),
        (
            pupils_11ba.get_path('11-1 - Магнитное поле', archive=True),
            pupils_11ba.get_path('11-1 - Магнитное поле', archive=False),
            False,
            r'.* - решения\.docx$',
        ),
        (
            library.location.udr('8 класс', '2020-21 Архив'),
            None,
            False,
            r'.*с урока\.docx$',
        ),
    ]


def get_extract_config():
    extract_config = [
        (
            library.location.udr('11 класс', 'Вишнякова', 'Вишнякова - Базовый курс - Все условия.pdf'),
            library.location.udr('11 класс', 'Вишнякова', 'generated'),
            {
                '1': 'Вишнякова - 1.1 - Кинематика - БК - условия.pdf',
                '2': 'Вишнякова - 1.2 - Динамика - БК - условия.pdf',
                '3': 'Вишнякова - 1.3 - Статика - БК - условия.pdf',
                '4': 'Вишнякова - 1.4 - Законы сохранения - БК - условия.pdf',
                '5': 'Вишнякова - 1.5 - Колебания и волны - БК - условия.pdf',
                '6': 'Вишнякова - 2.1 - Молекулярная физика - БК - условия.pdf',
                '7': 'Вишнякова - 2.2 - Термодинамика - БК - условия.pdf',
                '8': 'Вишнякова - 3.1 - Электрическое поле - БК - условия.pdf',
                '9': 'Вишнякова - 3.2 - Законы постоянного тока - БК - условия.pdf',
                '10': 'Вишнякова - 3.3 - Магнитное поле - БК - условия.pdf',
                '11': 'Вишнякова - 3.4 - Электромагнитная индукция - БК - условия.pdf',
                '12': 'Вишнякова - 3.5 - Электромагнитные колебания и волны - БК - условия.pdf',
                '13': 'Вишнякова - 3.6 - Оптика - БК - условия.pdf',
                '14': 'Вишнякова - 4 - Основы СТО - БК - условия.pdf',
                '15': 'Вишнякова - 5.1 - Корпускулярно-волновой дуализм - БК - условия.pdf',
                '16': 'Вишнякова - 5.2 - Физика атома - БК - условия.pdf',
                '17': 'Вишнякова - 5.3 - Физика атомного ядра - БК - условия.pdf',
            },
        ),
    ]

    class_config_2 = library.files.load_yaml_data('docx_2_pdf.yaml')

    for class_name, class_config in class_config_2.items():
        pupils = library.pupils.get_class_from_string(class_name)
        grade = pupils.Grade
        dst_dir = pupils.get_path(archive=False)

        for part, part_config in class_config.items():
            part_index, part_name = part.split(' ', 1)
            prefix = f'{grade}-{part_index} - {part_name}'

            pages_map = {}
            for pages, lesson_name in part_config.items():
                lesson_index, lesson_name = lesson_name.split(' ', 1)
                filename = f'{grade}-{part_index}-{lesson_index} - {part_name} - {lesson_name}.pdf'
                pages_map[pages] = filename

            extract_config.append((
                library.location.udr(f'{grade} класс', f'{prefix} - Рабочая тетрадь.pdf'),
                os.path.join(dst_dir, prefix),
                pages_map,
            ))


    return extract_config


def run(args):
    docxToPdf = library.convert.DocxToPdf()
    for src_dir, dst_dir, recursive, regexp in get_convert_config():
        docxToPdf.ConvertDir(
            src_dir,
            destination_directory=dst_dir,
            recursive=recursive,
            regexp=regexp,
        )

    for source_file, destination_directory, config in get_extract_config():
        pdfExtractor = PdfExtractor(
            source_file=source_file,
            destination_directory=destination_directory,
        )
        for pages, filename in config.items():
            pdfExtractor.Extract(pages, filename)


def populate_parser(parser):
    parser.set_defaults(func=run)
