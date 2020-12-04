import library.convert
import library.files
import library.location

import os

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


def run(args):
    docxToPdf = library.convert.DocxToPdf()
    docxToPdf.ConvertDir(
        library.location.udr('11 класс', 'Вишнякова'),
        recursive=False,
        regexp='.*Вишнякова - [0-9].*',
    )
    docxToPdf.ConvertDir(
        library.location.udr('11 класс', 'Вишнякова'),
        recursive=False,
        regexp='.*Вишнякова - .* - Все условия.*',
    )
    docxToPdf.ConvertDir(library.location.udr('10 класс'), recursive=False, regexp='.*Рабочая тетрадь.*')
    docxToPdf.ConvertDir(library.location.udr('9 класс'), recursive=False, regexp='.*Рабочая тетрадь.*')
    docxToPdf.ConvertDir(
        library.location.ipad('2020-21 Кружок'),
        destination_directory=library.location.udr('12 - кружок - 9-10-11', '2020-21 Кружок и допы - Видео и материалы'),
        regexp=r'.*\b[Кк]ружок\.docx$',
    )
    docxToPdf.ConvertDir(
        library.location.udr('12 - кружок - 9-10-11'),
        destination_directory='2020-21 Кружок и допы - Видео и материалы',
        regexp=r'.*\b[Кк]ружок\.docx$',
        recursive=False,
    )
    docxToPdf.ConvertDir(
        library.location.udr('10 класс', '2020-21 10АБ Физика - Архив'),
        destination_directory=library.location.udr('10 класс', '2020-21 10АБ Физика'),
        regexp=r'.*с урока.*\.docx$',
        recursive=False,
    )
    docxToPdf.ConvertDir(
        library.location.udr('9 класс', '2020-21 9М Физика - Архив'),
        destination_directory=library.location.udr('9 класс', '2020-21 9М Физика'),
        regexp=r'.*с урока.*\.docx$',
        recursive=False,
    )
    docxToPdf.ConvertDir(
        library.location.udr('8 класс', '2020-21 Архив'),
        regexp=r'.*с урока\.docx$',
        recursive=False,
    )


    if args.extract:
        extractor_configs = [
            (
                library.location.udr('11 класс', 'Вишнякова', 'Вишнякова - Базовый курс - Все условия.pdf'),
                None,
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
            (
                library.location.udr('10 класс', '10-1 - Кинематика - Рабочая тетрадь.pdf'),
                library.location.udr('10 класс', '2020-21 10АБ Физика', '10-1 Кинематика'),
                {
                    '1+3':         '10-1-1 - Кинематика - Неделя 1 - Материалы.pdf',
                    '5':           '10-1-1 - Кинематика - Неделя 1 - ДЗ.pdf',
                    '7':           '10-1-2 - Кинематика - Неделя 2 - ДЗ.pdf',
                    '9+2':         '10-1-2 - Кинематика - Неделя 2 - Материалы.pdf',
                    '13':          '10-1-3 - Кинематика - Неделя 3 - ДЗ.pdf',
                    '14+3, 19':    '10-1-3 - Кинематика - Неделя 3 - Материалы.pdf',
                    '21+3':        '10-1-4 - Кинематика - Неделя 4 - Материалы.pdf',
                    '26':          '10-1-4 - Кинематика - Неделя 4 - ДЗ.pdf',
                    '29':          '10-1-5 - Кинематика - Неделя 5 - ДЗ.pdf',
                    '30, 32+2':    '10-1-5 - Кинематика - Неделя 5 - Материалы.pdf',
                },
            ),
            (
                library.location.udr('10 класс', '10-2 - Динамика - Рабочая тетрадь.pdf'),
                library.location.udr('10 класс', '2020-21 10АБ Физика', '10-2 Динамика'),
                {
                    '1':        '10-2-1 - Динамика - Неделя 1 - ДЗ.pdf',
                    '2+3':      '10-2-1.1 - Динамика - Неделя 1 - Материалы-1.pdf',
                    # '6':        '10-2-1.2 - Динамика - Неделя 1 - Тест.pdf',
                    '7+3':      '10-2-1.2 - Динамика - Неделя 1 - Материалы-2.pdf',
                    '6, 11+6':  '10-2-1.3 - Динамика - Неделя 1 - Материалы-3.pdf',
                    '18':       '10-2-2 - Динамика - Неделя 2 - ДЗ.pdf',
                    '19+3':     '10-2-2.1 - Динамика - Неделя 2 - Материалы-1.pdf',
                    # '23':       '10-2-2.1 - Динамика - Неделя 2 - Тест.pdf',
                    '24+2':     '10-2-2.2 - Динамика - Неделя 2 - Материалы-2.pdf',
                    # '27+1':     '10-2-2.2 - Динамика - Неделя 2 - Тест.pdf',
                    # '29':       '10-2-2.3 - Динамика - Неделя 2 - Тест.pdf',
                    '30+2':     '10-2-2.3 - Динамика - Неделя 2 - Материалы-3.pdf',
                    '34':       '10-2-3 - Динамика - Неделя 3 - ДЗ.pdf',
                    '35+3':     '10-2-3.1 - Динамика - Неделя 3 - Материалы-1.pdf',
                    # '39':       '10-2-3.1 - Динамика - Неделя 3 - Тест.pdf',
                    '40+3':     '10-2-3.2 - Динамика - Неделя 3 - Материалы-2.pdf',
                    '44+3':     '10-2-3.3 - Динамика - Неделя 3 - Материалы-3.pdf',
                    # '48':       '10-2-3.3 - Динамика - Неделя 3 - Тест.pdf',
                    '49+1':     '10-2-4.1 - Динамика - Неделя 4 - Материалы-1.pdf',
                    '51':       '10-2-4 - Динамика - Неделя 4 - ДЗ.pdf',
                },
            ),
            (
                library.location.udr('10 класс', '10-3 - Законы сохранения - Рабочая тетрадь.pdf'),
                library.location.udr('10 класс', '2020-21 10АБ Физика', '10-3 Законы сохранения'),
                {
                    '1':        '10-3-1 - Законы сохранения - Неделя 1 - ДЗ.pdf',
                    '2+6':      '10-3-1.1 - Законы сохранения - Неделя 1 - Материалы-1.pdf',
                    # '9':        '10-3-1.3 - Законы сохранения - Неделя 1 - Тест.pdf',
                    '10+4':      '10-3-1.2 - Законы сохранения - Неделя 1 - Материалы-2.pdf',
                    '17':        '10-3-2 - Законы сохранения - Неделя 2 - ДЗ.pdf',
                    '18+6':      '10-3-2.1 - Законы сохранения - Неделя 2 - Материалы-1.pdf',
                    '25+3':      '10-3-2.2 - Законы сохранения - Неделя 2 - Материалы-2.pdf',
                    '29+1':      '10-3-2.3 - Законы сохранения - Неделя 2 - Материалы-3.pdf',
                },
            ),
            (
                library.location.udr('10 класс', '10-4 - Статика и гидростатика - Рабочая тетрадь.pdf'),
                '2020-21 10АБ Физика',
                {
                    '1':        '10-4-1 - Статика и гидростатика - Неделя 1 - ДЗ.pdf',
                    '2+5':      '10-4-1.1 - Статика и гидростатика - Неделя 1 - Материалы-1.pdf',
                    '8+3':      '10-4-1.2 - Статика и гидростатика - Неделя 1 - Материалы-2.pdf',
                    '12+3':     '10-4-1.3 - Статика и гидростатика - Неделя 1 - Материалы-3.pdf',
                    '16':       '10-4-1 - Статика и гидростатика - Неделя 3 - Тест-1.pdf',
                },
            ),
            (
                library.location.udr('9 класс', '9-2 - Динамика - Рабочая тетрадь.pdf'),
                '2020-21 9М Физика',
                {
                    '1+1':  '9-2-1.1 - Динамика - Неделя 1 - Материалы-1.pdf',
                    '3':    '9-2-1.1 - Динамика - Неделя 1 - ДЗ-1.pdf',
                    # '4':    '9-2-1.2 - Динамика - Неделя 1 - Тест.pdf',
                    '5+1':  '9-2-1.2 - Динамика - Неделя 1 - Материалы-2.pdf',
                    '7+1':  '9-2-2.1 - Динамика - Неделя 2 - Материалы-1.pdf',
                    # '9':    '9-2-2.1 - Динамика - Неделя 2 - Тест.pdf',
                    '14+3': '9-2-2.2 - Динамика - Неделя 2 - Материалы-2.pdf',
                    '18+1': '9-2-2.2 - Динамика - Неделя 2 - ДЗ.pdf',
                    '29':   '9-2-3.1 - Динамика - Неделя 3 - Материалы-1.pdf',
                    # '32':   '9-2-3.2 - Динамика - Неделя 3 - Тест-1.pdf',
                    '31':   '9-2-3.1 - Динамика - Неделя 3 - ДЗ-1.pdf',
                    # '32':   '9-2-3.2 - Динамика - Неделя 3 - Тест-2.pdf',
                    # '33':   '9-2-3.3 - Динамика - Неделя 3 - Тест-3.pdf',
                    '34+1': '9-2-3.3 - Динамика - Неделя 3 - Материалы-2.pdf',
                    '37+2,41+3': '9-2-4.2 - Динамика - Неделя 4 - Материалы-1.pdf',
                    # '40':   '9-2-4.2 - Динамика - Неделя 4 - Тест-1.pdf',
                },
            ),
            (
                library.location.udr('9 класс', '9-3 - Законы сохранения - Рабочая тетрадь.pdf'),
                '2020-21 9М Физика',
                {
                    '1+1': '9-3-1.1 - Законы сохранения - Неделя 1 - Материалы-1.pdf',
                    # '3':   '9-3-1.2 - Законы сохранения - Неделя 1 - Тест-1.pdf',
                    '4+1,8+1': '9-3-1.2 - Законы сохранения - Неделя 1 - Материалы-2.pdf',
                    '10+1': '9-3-2.1 - Законы сохранения - Неделя 2 - Материалы-1.pdf',
                    '12+5': '9-3-2.2 - Законы сохранения - Неделя 2 - Материалы-2.pdf',
                },
            ),
            (
                library.location.udr('9 класс', '9-4 - Колебания и волны - Рабочая тетрадь.pdf'),
                '2020-21 9М Физика',
                {
                    '1+1': '9-4-1.1 - Колебания и волны - Неделя 1 - Материалы-1.pdf',
                },
            ),
        ]
        for source_file, destination_directory, config in extractor_configs:
            pdfExtractor = PdfExtractor(
                source_file=source_file,
                destination_directory=destination_directory,
            )
            for pages, filename in config.items():
                pdfExtractor.Extract(pages, filename)


def populate_parser(parser):
    parser.add_argument('-e', '--extract', help='Extract pages from pdf to separate files', action='store_true')
    parser.set_defaults(func=run)
