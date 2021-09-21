import os
import shutil

import library.location
import library.files
import library.process

from library.logging import cm, color

import logging
log = logging.getLogger(__name__)


def run(args):
    years = [2018, 2019, 2020, 2021]
    if not args.all:
        years = years[-1:]
        log.warn(f'Processing only latest year: {years}')
    generared_paths = [
        library.location.root('school-554', f'generated-{year}-{year-2000+1}')
        for year in years
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
            assert filename.endswith('.tex')
            basename = os.path.basename(filename)
            cmd = ['latexmk', '-pdf', basename]
            log.info(f'Building {cm(basename, color=color.Green)}')
            library.process.run(cmd, cwd=dir_name)
            pdf_name = basename[:-3] + 'pdf'
            src = os.path.join(dir_name, pdf_name)
            dst = os.path.join(dir_name, 'pdf', pdf_name)
            log.info(f'Copy to {dst}')
            shutil.copy(src, dst)

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
    parser.add_argument('--all', help='Build all files (not only latest year)', action='store_true', default=False)
    parser.set_defaults(func=run)
