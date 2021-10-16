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
            recursive=True,
            extensions=['.tex'],
            regexp=filenames_regex,
        )
        for tex_file in sorted(tex_files):
            assert tex_file.endswith('.tex')
            pdf_name = tex_file[:-3] + 'pdf'
            tex_dir = os.path.dirname(tex_file)
            tex_name = os.path.basename(tex_file)

            cmd = ['latexmk', '-pdf', tex_name]
            log.info(f'Building {cm(tex_name, color=color.Green)}')
            library.process.run(cmd, cwd=tex_dir)

            pdf_dir = os.path.join(os.path.dirname(pdf_name), 'pdf')
            if not os.path.isdir(pdf_dir):
                log.info(f'Create missing {pdf_dir}')
                os.mkdir(pdf_dir)

            pdf_dst = os.path.join(pdf_dir, os.path.basename(pdf_name))

            log.info(f'Copy {pdf_name} to {pdf_dst}')
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
                ],
                regexp=filenames_regex,
            )
            for misc_file in sorted(misc_files):
                os.remove(misc_file)


def populate_parser(parser):
    parser.add_argument('--clean', help='Delete tmp files', action='store_true', default=False)
    parser.add_argument('--all', help='Build all files (not only latest year)', action='store_true', default=False)
    parser.set_defaults(func=run)
