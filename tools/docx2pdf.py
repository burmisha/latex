import library.convert
import library.files

import os

import logging
log = logging.getLogger(__name__)

class PdfExtractor:
    def __init__(self, source_file=None, destination_directory=None):
        self._source_file = source_file
        self._destination_directory = os.path.join(os.path.dirname(self._source_file), destination_directory)
        assert os.path.exists(self._source_file)
        assert os.path.isfile(self._source_file)
        assert os.path.exists(self._destination_directory)
        assert os.path.isdir(self._destination_directory)

        self._pdf2pdf = library.convert.PdfToPdf(self._source_file)

    def Extract(self, pages, destination_filename):
        dst_file = os.path.join(self._destination_directory, destination_filename)
        if not library.files.is_older(self._source_file, dst_file):
            self._pdf2pdf.Extract(pages, dst_file)
        else:
            log.info(f'Skipping existing file \'{destination_filename}\'')

    def ExtractConfig(self, pages_config):
        for pages, filename in pages_config.items():
            self.Extract(pages, filename)


def run(args):
    docxToPdf = library.convert.DocxToPdf()
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
        pdfExtractor = PdfExtractor(
            source_file=library.files.udrPath(u'10 класс', u'10-1 - Кинематика - Рабочая тетрадь.pdf'),
            destination_directory='2020-21 10AБ Физика',
        )
        pdfExtractor.ExtractConfig({
            '5, 1-4': '10-1-1 - Кинематика - Неделя 1 - auto.pdf',
        })


def populate_parser(parser):
    parser.add_argument('--run-extractor', help='Extract pdf files', action='store_true')
    parser.set_defaults(func=run)
