from library.util import fn_filter
from tools.books import get_all_books

import logging
log = logging.getLogger(__name__)


def runConvert(args):
    for book in get_all_books():
        if args.filter and not args.filter.match(book.pdf_file):
            continue
        log.info(f'Processing {book}')
        book.validate(create_missing=args.create_missing)
        book.save_all_pages(force=args.overwrite_existing, dry_run=args.dry_run)
        book.get_strange_files(remove=args.remove_strange_files)


def populate_parser(parser):
    parser.add_argument('-f', '--filter', help='fnmatch expression for book name', type=fn_filter.FnFilter)
    parser.add_argument('--remove-strange-files', help='Remove strange files', action='store_true')
    parser.add_argument('--overwrite-existing', help='Overwrite already extracted files', action='store_true')
    parser.add_argument('--create-missing', help='Create missing root dirs for books', action='store_true')
    parser.add_argument('--dry-run', help='Do not create anything', action='store_true')
    parser.set_defaults(func=runConvert)
