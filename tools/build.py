import os

import library.location
import library.files
import library.process

from library.logging import cm, color

import logging
log = logging.getLogger(__name__)


def run(args):
    generared_paths = [
        library.location.root('school-554', 'generated-2018-19'),
        library.location.root('school-554', 'generated-2019-20'),
        library.location.root('school-554', 'generated-2020-21'),
    ]

    filenames_regex = '.*(task|answer).*'
    for dir_name in generared_paths:
        tex_files = library.files.walkFiles(
            dir_name,
            recursive=False,
            extensions=['.tex'],
            regexp=filenames_regex,
        )
        for filename in sorted(tex_files):
            basename = os.path.basename(filename)
            cmd = ['latexmk', '-pdf', basename]
            log.info(f'Building {cm(basename, color=color.Green)}')
            library.process.run(cmd, cwd=dir_name)

    if args.clean:
        for dir_name in generared_paths:
            misc_files = library.files.walkFiles(
                dir_name,
                recursive=False,
                extensions=[
                    '.aux',
                    '.fdb_latexmk',
                    '.fls',
                    '.log',
                    '.out',
                    '.synctex(busy)',
                ],
                regexp=filenames_regex,
            )
            for misc_file in sorted(misc_files):
                os.remove(misc_file)


def populate_parser(parser):
    parser.add_argument('--clean', help='Delete tmp files', action='store_true', default=False)
    parser.set_defaults(func=run)
