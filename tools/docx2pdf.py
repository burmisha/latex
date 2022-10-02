from library.convert.pdf_to_pdf import PdfToPdf
from library.convert.docx_to_pdf import DocxToPdf
import library.files
import library.location
import library.pupils

import os
import yaml
import re
import attr

from typing import List

import logging
log = logging.getLogger(__name__)


class PdfExtractor:
    def __init__(self, *, source_file=None, destination_directory=None):
        self._source_file = source_file
        if destination_directory:
            self._destination_directory = os.path.join(os.path.dirname(self._source_file), destination_directory)
        else:
            self._destination_directory = os.path.dirname(self._source_file)
        assert library.files.is_file(self._source_file)
        assert library.files.is_dir(self._destination_directory)

        self._pdf2pdf = PdfToPdf(self._source_file)

    def Extract(self, pages, destination_filename):
        dst_file = os.path.join(self._destination_directory, destination_filename)
        if library.files.is_older(self._source_file, dst_file):
            log.debug(f'Skipping updated file {destination_filename!r} (no pages check: {pages})')
        else:
            self._pdf2pdf.Extract(pages, dst_file)


@attr.s
class ConvertConfig:
    src_dir: str = attr.ib()
    dst_dir: str = attr.ib()
    recursive: bool = attr.ib()
    regexp: str = attr.ib()


@attr.s
class ExtractConfig:
    source_file: str = attr.ib()
    destination_directory: str = attr.ib()
    pages_map: dict = attr.ib()



def get_convert_configs() -> List[ConvertConfig]:
    pupils_9m = library.pupils.get_class_from_string('2020 9М')
    pupils_10ab = library.pupils.get_class_from_string('2020 10АБ')
    pupils_11ba = library.pupils.get_class_from_string('2021 11БА')

    return [
        ConvertConfig(
            src_dir=library.location.udr('11 класс', 'Вишнякова'),
            dst_dir='generated',
            recursive=False,
            regexp='.*Вишнякова - [0-9].*',
        ),
        ConvertConfig(
            src_dir=library.location.udr('11 класс', 'Вишнякова'),
            dst_dir='generated',
            recursive=False,
            regexp='.*Вишнякова - .* - Все условия.*',
        ),
        ConvertConfig(
            src_dir=library.location.udr('11 класс'),
            dst_dir=None,
            recursive=True,
            regexp='.*Рабочая тетрадь.*',
        ),
        ConvertConfig(
            src_dir=library.location.udr('10 класс'),
            dst_dir=None,
            recursive=True,
            regexp='.*Рабочая тетрадь.*',
        ),
        ConvertConfig(
            src_dir=library.location.udr('9 класс'),
            dst_dir=None,
            recursive=True,
            regexp='.*Рабочая тетрадь.*',
        ),
        # TODO: move and convert
        # ConvertConfig(
        #     src_dir=library.location.ipad('2020-21 Дистант'),
        #     dst_dir=library.location.udr('12 - кружок - 9-10-11', '2020-21 Кружок и допы - Видео и материалы'),
        #     recursive=True,
        #     regexp=r'.*\b[Кк]ружок.*\.docx$',
        # ),
        ConvertConfig(
            src_dir=library.location.udr('12 - кружок - 9-10-11'),
            dst_dir='2020-21 Кружок и допы - Видео и материалы',
            recursive=False,
            regexp=r'.*\b[Кк]ружок.*\.docx$',
        ),
        ConvertConfig(
            src_dir=library.location.udr('12 - кружок - 9-10-11', '2021-22 Кружок и допы'),
            dst_dir=library.location.udr('12 - кружок - 9-10-11', '2021-22 Кружок и допы'),
            recursive=False,
            regexp=r'.*\b[Кк]ружок.*\.docx$',
        ),
        ConvertConfig(
            src_dir=pupils_10ab.get_path(archive=True),
            dst_dir=pupils_10ab.get_path(archive=False),
            recursive=False,
            regexp=r'.*с урока.*\.docx$',
        ),
        ConvertConfig(
            src_dir=pupils_9m.get_path(archive=True),
            dst_dir=pupils_9m.get_path(archive=False),
            recursive=False,
            regexp=r'.*с урока.*\.docx$',
        ),
        ConvertConfig(
            src_dir=pupils_11ba.get_path('11-1 - Магнитное поле', archive=True),
            dst_dir=pupils_11ba.get_path('11-1 - Магнитное поле', archive=False),
            recursive=False,
            regexp=r'.* - решения\.docx$',
        ),
        ConvertConfig(
            src_dir=library.location.udr('8 класс', '2020-21 Архив'),
            dst_dir=None,
            recursive=False,
            regexp=r'.*с урока\.docx$',
        ),
    ]


PRIVATE_SUBSRINGS = [
    'Самостоятельная работа',
    'Проверочная работа',
    'Контрольная работа',
    'ЕГЭ - задание',
]


def is_private_lesson(lesson_name: str) -> bool:
    return any(s.lower() in lesson_name.lower() for s in PRIVATE_SUBSRINGS)


def get_extract_configs() -> List[ExtractConfig]:
    extract_configs = [
        ExtractConfig(
            source_file=library.location.udr('11 класс', 'Вишнякова', 'Вишнякова - Базовый курс - Все условия.pdf'),
            destination_directory=library.location.udr('11 класс', 'Вишнякова', 'generated'),
            pages_map={
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

    yaml_config = library.files.load_yaml_data('docx_2_pdf.yaml')

    for class_name, class_config in yaml_config.items():
        pupils = library.pupils.get_class_from_string(class_name)
        grade = pupils.Grade

        for part, part_config in class_config.items():
            part_index, part_name = part.split(' ', 1)
            prefix = f'{grade}-{part_index} - {part_name}'

            public_pages_map = {}
            private_pages_map = {}
            for pages, lesson_name in part_config.items():
                lesson_index, lesson_name = lesson_name.split(' ', 1)

                filename = [f'{grade}-{part_index}-{lesson_index}']
                if re.match(r'^\d{4}[\.-]\d{2}[\.-]\d{2}', lesson_name):
                    date = lesson_name[:10].replace('-', '.')
                    lesson_name = lesson_name[10:].strip()
                    filename.append(date)
                filename += [part_name, lesson_name]
                filename = ' - '.join(filename) + '.pdf'

                if is_private_lesson(lesson_name):
                    private_pages_map[pages] = filename
                else:
                    public_pages_map[pages] = filename

            if pupils.is_active:
                pdf_name = library.location.udr(
                    f'{grade} класс',
                    f'{prefix} - Рабочая тетрадь.pdf',
                )
            else:
                pdf_name = library.location.udr(
                    f'{grade} класс',
                    f'{pupils.Year} {pupils.Grade} Архив',
                    f'{prefix} - Рабочая тетрадь.pdf',
                )

            if public_pages_map:
                extract_configs.append(
                    ExtractConfig(
                        source_file=pdf_name,
                        destination_directory=pupils.get_path(prefix, archive=False),
                        pages_map=public_pages_map,
                    )
                )
            if private_pages_map:
                extract_configs.append(
                    ExtractConfig(
                        source_file=pdf_name,
                        destination_directory=pupils.get_path(prefix, archive=True),
                        pages_map=private_pages_map,
                    )
                )

    return extract_configs


def run(args):
    docxToPdf = DocxToPdf()
    for convert_config in get_convert_configs():
        docxToPdf.ConvertDir(
            convert_config.src_dir,
            destination_directory=convert_config.dst_dir,
            recursive=convert_config.recursive,
            regexp=convert_config.regexp,
        )

    for extract_config in get_extract_configs():
        pdfExtractor = PdfExtractor(
            source_file=extract_config.source_file,
            destination_directory=extract_config.destination_directory,
        )
        for pages, filename in extract_config.pages_map.items():
            pdfExtractor.Extract(pages, filename)


def populate_parser(parser):
    parser.set_defaults(func=run)
