#!/usr/bin/env python3

import tools
from library.logging import cm

import argparse
import time

import logging
log = logging.getLogger(__name__)

DEFAULT_LOG_FIELDS = [
    '%(asctime)s.%(msecs)03d',
    '%(name)15s:%(lineno)-4d',
    '%(levelname)-7s',
    '%(message)s',
]

LOG_LEVELS = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG,
}


def get_log_format(args):
    log_separator = {'space': ' ', 'tab': '\t'}[args.log_separator]
    log_fields = args.log_field or DEFAULT_LOG_FIELDS
    return log_separator.join(log_fields)


def get_log_level(args):
    if args.warning:
        return logging.WARNING
    elif args.verbose:
        return logging.DEBUG
    elif args.log_level:
        return LOG_LEVELS[args.log_level.lower()]
    else:
        return logging.INFO


def CreateArgumentsParser():
    parser = argparse.ArgumentParser(
        description='One script to run all tools',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    log_format_group = parser.add_argument_group('Logging arguments')
    log_format_group.add_argument('--log-field', help='Logging fields, if missing will use default ones', default=[], action='append')
    log_format_group.add_argument('--log-separator', help='Logging string separator', choices=['space', 'tab'], default='space')
    log_format_group.add_argument('--log-datefmt', help='Logging default time format', default='%T')

    log_level_group = parser.add_mutually_exclusive_group()
    log_level_group.add_argument('-v', '--verbose', help='Enable debug logging', action='store_true')
    log_level_group.add_argument('-w', '--warning', help='Enable warning logging only', action='store_true')
    log_level_group.add_argument('--log-level', help='Set log level', choices=LOG_LEVELS.keys(), default=None)

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
        ('dnevnik', 'Run mesh tools', tools.dnevnik),
        ('yaform', 'Download yandex form results', tools.yaform),
    ]:
        subparser = subparsers.add_parser(
            mode_name,
            help=help_message,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        populate_module.populate_parser(subparser)

    return parser


def main():
    parser = CreateArgumentsParser()
    args = parser.parse_args()

    logging.basicConfig(
        level=get_log_level(args),
        format=get_log_format(args),
        datefmt=args.log_datefmt,
    )

    log.info('Start')
    start_time = time.time()
    try:
        args.func(args)
        finish_time = time.time()
        log.info(cm('Finished in %.2f seconds', color='green'), finish_time - start_time)
    except Exception:
        log.exception(cm('Failed', bg='red'))
        finish_time = time.time()
        log.error(cm('Failed in %.2f seconds', bg='red'), finish_time - start_time)


if __name__ == '__main__':
    main()
