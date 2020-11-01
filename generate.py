#!/usr/bin/env python3

import library
import tools

import argparse
import time

import logging
log = logging.getLogger(__name__)


def CreateArgumentsParser():
    parser = argparse.ArgumentParser(
        description='One script to run all tools',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    loggingGroup = parser.add_argument_group('Logging arguments')
    defaultLogFormat = ' '.join([
        # '%(relativeCreated)d',
        '%(asctime)s.%(msecs)03d',
        '%(name)15s:%(lineno)-4d',
        '%(levelname)-7s',
        '%(message)s',
    ])
    loggingGroup.add_argument('--log-format', help='Logging format', default=defaultLogFormat)
    loggingGroup.add_argument('--log-separator', help='Logging string separator', choices=['space', 'tab'], default='space')
    loggingGroup.add_argument('-v', '--verbose', help='Enable debug logging', action='store_true')

    subparsers = parser.add_subparsers()

    generateParser = subparsers.add_parser('generate', help='Generate all LaTeX-files and papers')
    tools.generate_all.populate_parser(generateParser)

    luckyParser = subparsers.add_parser('lucky', help='Find lucky pupils')
    library.lucky.populate_parser(luckyParser)

    tripodParser = subparsers.add_parser('tripod', help='Generate tripod results')
    library.tripod.populate_parser(tripodParser)

    downloadParser = subparsers.add_parser('download', help='Download extra files')
    library.download.populate_parser(downloadParser)

    qrParser = subparsers.add_parser('qr', help='Form QR codes')
    tools.qr.populate_parser(qrParser)

    reshuegeParser = subparsers.add_parser('reshu-ege', help='Reshu EGE')
    tools.reshuege.populate_parser(reshuegeParser)

    znaniumParser = subparsers.add_parser('znanium', help='Znanium')
    tools.znanium.populate_parser(znaniumParser)

    convertParser = subparsers.add_parser('convert', help='Convert pdf books into jpeg')
    tools.convert.populate_parser(convertParser)

    templateParser = subparsers.add_parser('template', help='Create template files')
    tools.template.populate_parser(templateParser)

    docx2PdfParser = subparsers.add_parser('docx2pdf', help='Convert docx files to pdf ones')
    tools.docx2pdf.populate_parser(docx2PdfParser)

    gformsParser = subparsers.add_parser('gforms', help='Create JS scripts for Google Forms')
    tools.google_forms.populate_parser(gformsParser)

    checkerParser = subparsers.add_parser('checker', help='Check csv forms')
    tools.checker.populate_parser(checkerParser)

    return parser


def main():
    parser = CreateArgumentsParser()
    args = parser.parse_args()

    logFormat = args.log_format.replace('\t', ' ')
    logFormat = logFormat.replace(' ', {'space': ' ', 'tab': '\t'}[args.log_separator])
    logLevel = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=logLevel, format=logFormat, datefmt='%H:%M:%S')

    log.info('Start')
    start_time = time.time()
    args.func(args)
    finish_time = time.time()
    log.info('Finished in %.2f seconds', finish_time  - start_time)


if __name__ == '__main__':
    main()
