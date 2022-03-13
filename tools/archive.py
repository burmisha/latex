import library

import logging
log = logging.getLogger(__name__)

import zlib
import base64

import time


def run(args):
    src_file = library.location.root('data', 'marks.yaml')
    archive_file = f'{src_file}.archived'

    if args.extract:
        with open(archive_file) as f:
            data = f.read()

        t = base64.decodebytes(data.encode())
        decoded = zlib.decompress(t).decode()

        now = int(time.time())
        t_file = f'{src_file}.{now}'
        log.info(f'Extract: {t_file}')
        with open(t_file, 'w') as f:
            f.write(decoded)

        cmd = f'vimdiff {src_file} {t_file}'
        library.process.pbcopy(cmd)

    else:
        with open(src_file) as f:
            data = f.read()

        t = zlib.compress(data.encode())
        encoded = base64.encodebytes(t)

        log.info(f'Archive:\n\tsrc:\t{src_file}\n\tdst:\t{archive_file}')
        with open(archive_file, 'wb') as f:
            f.write(encoded)




def populate_parser(parser):
    parser.add_argument('-e', '--extract', help='Load from archive', action='store_true')
    parser.set_defaults(func=run)
