import library.convert
import library.files

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
        assert os.path.exists(self._source_file)
        assert os.path.isfile(self._source_file)
        assert os.path.exists(self._destination_directory)
        assert os.path.isdir(self._destination_directory)

        self._pdf2pdf = library.convert.PdfToPdf(self._source_file)

    def Extract(self, pages, destination_filename):
        dst_file = os.path.join(self._destination_directory, destination_filename)
        if library.files.is_older(self._source_file, dst_file):
            log.info(f'Skipping existing file \'{destination_filename}\'')
        else:
            self._pdf2pdf.Extract(pages, dst_file)

    def ExtractConfig(self, pages_config):
        for pages, filename in pages_config.items():
            self.Extract(pages, filename)


def run(args):
    docxToPdf = library.convert.DocxToPdf()
    docxToPdf.ConvertDir(
        library.files.udrPath('11 класс', '2020 весна'),
        recursive=False,
        regexp='.*Вишнякова - [0-9].*',
    )
    docxToPdf.ConvertDir(
        library.files.udrPath('11 класс', '2020 весна'),
        recursive=False,
        regexp='.*Вишнякова - .* - Все условия.*',
    )
    docxToPdf.ConvertDir(
        library.files.udrPath('10 класс'),
        recursive=False,
        regexp='.*Рабочая тетрадь.*',
    )

    if args.run_extractor:
        vishnyakovaExtractor = PdfExtractor(
            source_file=library.files.udrPath('11 класс', '2020 весна', 'Вишнякова - Базовый курс - Все условия.pdf'),
        )
        vishnyakovaExtractor.ExtractConfig({
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
        })

        kinematicsExtractor = PdfExtractor(
            source_file=library.files.udrPath('10 класс', '10-1 - Кинематика - Рабочая тетрадь.pdf'),
            destination_directory='2020-21 10AБ Физика',
        )
        kinematicsExtractor.ExtractConfig({
            '1-4':          '10-1-1 - Кинематика - Неделя 1 - Материалы.pdf',
            '5':            '10-1-1 - Кинематика - Неделя 1 - ДЗ.pdf',
            '7':            '10-1-2 - Кинематика - Неделя 2 - ДЗ.pdf',
            '9-11':         '10-1-2 - Кинематика - Неделя 2 - Материалы.pdf',
            '13':           '10-1-3 - Кинематика - Неделя 3 - ДЗ.pdf',
            '14-17, 19':    '10-1-3 - Кинематика - Неделя 3 - Материалы.pdf',
            '21-25':        '10-1-4 - Кинематика - Неделя 4 - Материалы.pdf',
            '26':           '10-1-4 - Кинематика - Неделя 4 - ДЗ.pdf',
            '29':           '10-1-5 - Кинематика - Неделя 5 - ДЗ.pdf',
            '30, 32-34':    '10-1-5 - Кинематика - Неделя 5 - Материалы.pdf',
        })

        dynamicsExtractor = PdfExtractor(
            source_file=library.files.udrPath('10 класс', '10-2 - Динамика - Рабочая тетрадь.pdf'),
            destination_directory='2020-21 10AБ Физика',
        )
        dynamicsExtractor.ExtractConfig({
            # '':          '10-2-1 - Динамика - Неделя 1 - Материалы.pdf',
            # '':          '10-2-1 - Динамика - Неделя 1 - ДЗ.pdf',
        })


def populate_parser(parser):
    parser.add_argument('--run-extractor', help='Extract pdf files', action='store_true')
    parser.set_defaults(func=run)
