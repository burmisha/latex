from tools.books import get_all_books

import logging
log = logging.getLogger(__name__)


def runConvert(args):
    for book in get_all_books():
        log.info(f'Processing {book}')
        book.Validate(create_missing=args.create_missing)
        book.Save(overwrite=args.overwrite_existing, dry_run=args.dry_run)
        book.GetStrangeFiles(remove=args.remove_strange_files)
        # if 'Генденштейн' in book.PdfPath and '11' in book.PdfPath:
        #     library.process.pbcopy(book.decode_as_text(indices=list(range(4, 14))))


def populate_parser(parser):
    parser.add_argument('--remove-strange-files', help='Remove strange files', action='store_true')
    parser.add_argument('--overwrite-existing', help='Overwrite already extracted files', action='store_true')
    parser.add_argument('--create-missing', help='Create missing root dirs for books', action='store_true')
    parser.add_argument('--dry-run', help='Do not create anything', action='store_true')
    parser.set_defaults(func=runConvert)
