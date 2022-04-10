from tools.books import get_all_books
from library.structure.page import PagesRange
from library.normalize import format_plain_text

import library.process

import fnmatch
import os

import logging
log = logging.getLogger(__name__)


class FnFilter:
    def __init__(self, fn_filter: str):
        assert fn_filter, f'No filter provided: {fn_filter}'
        self.fn_filter = fn_filter

    def match(self, value):
        return fnmatch.fnmatch(value, self.fn_filter)


def runRecognize(args):
    indices = []
    for str_page_range in args.pages.split(','):
        pages = PagesRange(str_page_range)
        indices += pages.pages_indicies

    for book in get_all_books():
        if not args.filter.match(os.path.basename(book.PdfPath)):
            continue
        log.info(f'Processing {book}')
        text = book.decode_as_text(indices=indices)
        text = format_plain_text(text, fill=False)
        library.process.pbcopy(text)


def populate_parser(parser):
    parser.add_argument('-f', '--filter', help='fnmatch expresiion for book basename', required=True, type=FnFilter)
    parser.add_argument('-p', '--pages', help='Pages indices', required=True)
    parser.set_defaults(func=runRecognize)
