from tools.books import get_all_books
from library.convert import PagesRange

import library.process

import fnmatch
import os

import logging
log = logging.getLogger(__name__)


def runRecognize(args):
    fn_filter = args.filter
    assert fn_filter, f'No filter provided: {fn_filter}'

    pages = PagesRange(args.pages)
    indices = list(pages.get_pages_indicies())

    for book in get_all_books():
        basename = os.path.basename(book.PdfPath)
        if not fnmatch.fnmatch(basename, fn_filter):
            continue
        log.info(f'Processing {book}')
        library.process.pbcopy(book.decode_as_text(indices=indices))


def populate_parser(parser):
    parser.add_argument('-f', '--filter', help='fnmatch expresiion for book basename', required=True)
    parser.add_argument('-p', '--pages', help='Pages indices', required=True)
    parser.set_defaults(func=runRecognize)
