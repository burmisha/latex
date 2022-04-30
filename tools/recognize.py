from tools.books import get_all_books

from library.structure.page import PagesRange
from library.normalize import format_plain_text
from library.util import fn_filter

import library.process

import os

import logging
log = logging.getLogger(__name__)


def runRecognize(args):
    indices = []
    for str_page_range in args.pages.split(','):
        pages = PagesRange(str_page_range)
        indices += pages.pages_indicies

    for book in get_all_books():
        if not args.filter.match(os.path.basename(book.pdf_file)):
            continue
        log.info(f'Processing {book}')
        text = book.decode_as_text(indices=indices)
        text = format_plain_text(text, fill=False)
        library.process.pbcopy(text)


def populate_parser(parser):
    parser.add_argument('-f', '--filter', help='fnmatch expression for book basename', required=True, type=fn_filter.FnFilter)
    parser.add_argument('-p', '--pages', help='Pages indices', required=True)
    parser.set_defaults(func=runRecognize)
