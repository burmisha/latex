import os
import shutil

import library.location
import library.files
import library.process
from library import datetools

from library.logging import cm, color

import logging
log = logging.getLogger(__name__)


FILENAMES_RE = '.*(task|answer|classwork).*'
ACTIVE_YEARS = [2018, 2019, 2020, 2021]
WEEKS_TO_PROCESS = 4


def run(args):
    if args.all:
        date_from = str(ACTIVE_YEARS[0])
    else:
        date_from = datetools.NowDelta().Before(weeks=WEEKS_TO_PROCESS, fmt=datetools.DAY_DATE_FORMAT)
    log.info(f'Processing LaTeX files since {cm(date_from, color=color.Cyan)}')


    generared_paths = [
        library.location.root('school-554', f'generated-{year}-{year-2000+1}')
        for year in ACTIVE_YEARS
    ]

    for dir_name in generared_paths:
        tex_files = library.files.walkFiles(
            dir_name,
            recursive=True,
            extensions=['.tex'],
            regexp=FILENAMES_RE,
        )
        for tex_file in sorted(tex_files):
            assert tex_file.endswith('.tex')
            pdf_name = tex_file[:-3] + 'pdf'
            tex_dir = os.path.dirname(tex_file)
            tex_name = os.path.basename(tex_file)

            if tex_name < date_from:
                continue

            cmd = ['latexmk', '-pdf', tex_name]
            log.info(f'Building {cm(tex_name, color=color.Green)}')
            library.process.run(cmd, cwd=tex_dir)

            pdf_dir = os.path.join(os.path.dirname(pdf_name), 'pdf')
            if not os.path.isdir(pdf_dir):
                log.info(f'Create missing {pdf_dir}')
                os.mkdir(pdf_dir)

            pdf_dst = os.path.join(pdf_dir, os.path.basename(pdf_name))

            log.info(f'Copy:\n  \t{pdf_name} -> \n     ->\t{pdf_dst}')
            shutil.copy(pdf_name, pdf_dst)

    if args.clean:
        for dir_name in generared_paths:
            misc_files = library.files.walkFiles(
                dir_name,
                recursive=True,
                extensions=[
                    '.aux',
                    '.fdb_latexmk',
                    '.fls',
                    '.log',
                    '.out',
                    '.synctex(busy)',
                    '.synctex.gz',
                ],
                regexp=filenames_regex,
            )
            for misc_file in sorted(misc_files):
                os.remove(misc_file)


def populate_parser(parser):
    parser.add_argument('--clean', help='Delete tmp files', action='store_true', default=False)
    parser.add_argument('--all', help='Build all files rather than latest ones', action='store_true', default=False)
    parser.set_defaults(func=run)
