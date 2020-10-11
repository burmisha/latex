import library.convert
import library.files

import logging
log = logging.getLogger(__name__)


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
        pdfExtractor = library.convert.PdfToPdf(library.files.udrPath(u'10 класс', u'10-1 - Кинематика - Рабочая тетрадь.pdf'))
        pdfExtractor.Extract('5, 1-4', library.files.udrPath(u'10 класс', u'tmp.pdf'))


def populate_parser(parser):
    parser.add_argument('--run-extractor', help='Extract pdf files', action='store_true')
    parser.set_defaults(func=run)
