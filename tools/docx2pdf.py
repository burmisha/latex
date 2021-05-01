import library.convert
import library.files
import library.location

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
        assert os.path.exists(self._source_file), f'No file {self._source_file}'
        assert os.path.isfile(self._source_file), f'Not file {self._source_file}'
        assert os.path.exists(self._destination_directory), f'No dir {self._destination_directory}'
        assert os.path.isdir(self._destination_directory), f'Not dir {self._destination_directory}'

        self._pdf2pdf = library.convert.PdfToPdf(self._source_file)

    def Extract(self, pages, destination_filename):
        dst_file = os.path.join(self._destination_directory, destination_filename)
        if library.files.is_older(self._source_file, dst_file):
            log.debug(f'Skipping updated file \'{destination_filename}\' (no pages check: {pages})')
        else:
            self._pdf2pdf.Extract(pages, dst_file)


def get_convert_config():
    return [
        (library.location.udr('11 класс', 'Вишнякова'), 'generated', False, '.*Вишнякова - [0-9].*'),
        (library.location.udr('11 класс', 'Вишнякова'), 'generated', False, '.*Вишнякова - .* - Все условия.*'),
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
            library.location.udr('10 класс', '2020-21 10АБ Физика - Архив'),
            library.location.udr('10 класс', '2020-21 10АБ Физика'),
            False,
            r'.*с урока.*\.docx$',
        ),
        (
            library.location.udr('9 класс', '2020-21 9М Физика - Архив'),
            library.location.udr('9 класс', '2020-21 9М Физика'),
            False,
            r'.*с урока.*\.docx$',
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

    cfg_file = library.location.root('data', 'docx_2_pdf.yaml')
    with open(cfg_file) as f:
        class_config_2 = yaml.safe_load(f)

    for grade_key, grade_config in class_config_2.items():
        grade, dst_dir = grade_key.split(' ', 1)
        for part, part_config in grade_config.items():
            part_index, part_name = part.split(' ', 1)
            prefix = f'{grade}-{part_index} - {part_name}'
            pages_map = {}
            for pages, file_name_mask in part_config.items():
                assert ' ' in file_name_mask
                index, name = file_name_mask.split(' ', 1)
                filename = f'{grade}-{part_index}-{index} - {part_name} - {name}.pdf'
                pages_map[pages] = filename
            extract_config.append((
                library.location.udr(f'{grade} класс', f'{prefix} - Рабочая тетрадь.pdf'),
                library.location.udr(f'{grade} класс', f'{dst_dir}', prefix),
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
