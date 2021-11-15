import library.location
import library.files
import library.convert

import logging
log = logging.getLogger(__name__)


def run_recombinate(args):
    memorial = library.files.load_yaml_data('recombinate.yaml')['memorial']
    for src_name, pages in memorial.items():
        src_file = library.location.tmp('memorial', 'src', src_name)
        dst_name = src_name.replace('.pdf', '_export.pdf')
        dst_file = library.location.tmp('memorial', 'dst', dst_name)
        pdf_to_pdf = library.convert.PdfToPdf(src_file)
        pdf_to_pdf.Extract(pages, dst_file)


def populate_parser(parser):
    parser.set_defaults(func=run_recombinate)
