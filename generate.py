#!/usr/bin/env python3

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
    for mode_name, help_message, populate_module in [
        ('generate', 'Generate all LaTeX-files and papers', tools.generate_all),
        ('lucky', 'Find lucky pupils', tools.lucky),
        ('tripod', 'Generate tripod results', tools.tripod),
        ('download', 'Download extra files', tools.download),
        ('qr', 'Form QR codes', tools.qr),
        ('reshu-ege', 'Reshu EGE', tools.reshuege),
        ('znanium', 'Znanium', tools.znanium),
        ('convert', 'Convert pdf books into jpeg', tools.convert),
        ('template', 'Create template files', tools.template),
        ('docx2pdf', 'Convert docx files to pdf ones', tools.docx2pdf),
        ('gforms', 'Create JS scripts for Google Forms', tools.google_forms),
        ('checker', 'Check csv forms', tools.checker),
    ]:
        subparser = subparsers.add_parser(mode_name, help=help_message)
        populate_module.populate_parser(subparser)

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
    try:
        args.func(args)
        finish_time = time.time()
        log.info('Finished in %.2f seconds', finish_time  - start_time)
    except Exception:
        log.exception('Failed')
        finish_time = time.time()
        log.info('Failed in %.2f seconds', finish_time  - start_time)


if __name__ == '__main__':
    main()
