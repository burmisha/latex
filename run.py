#!/usr/bin/env python3

import tools
from library.logging import cm, color
from library.process import say

import argparse
import time

import logging
log = logging.getLogger('main')

DEFAULT_LOG_FIELDS = [
    '%(asctime)s.%(msecs)03d',
    '%(name)20s:%(lineno)-4d',
    # '%(levelname)-7s',
    ' %(message)s',
]

DEFAULT_LOG_LEVEL = 'info'

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
        raise RuntimeError('No log level provided')


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
    log_level_group.add_argument('-v', '--verbose', help='Add debug logging', action='store_true')
    log_level_group.add_argument('-w', '--warning', help='Enable warning logging only', action='store_true')
    log_level_group.add_argument('--log-level', help='Set log level', choices=sorted(LOG_LEVELS.keys()), default=DEFAULT_LOG_LEVEL)

    subparsers = parser.add_subparsers()
    for mode_name, help_message, populate_module in [
        ('absent', 'Check absent files', tools.absent),
        ('build', 'Build pdf files from LaTeX', tools.build),
        ('checker', 'Check csv forms', tools.checker),
        ('convert', 'Convert pdf books into jpeg', tools.convert),
        ('dnevnik', 'Run mesh tools', tools.dnevnik),
        ('docx2pdf', 'Convert docx files to pdf ones', tools.docx2pdf),
        ('download', 'Download extra files', tools.download),
        ('generate', 'Generate all LaTeX-files and papers', tools.generate_all),
        ('gforms', 'Create JS scripts for Google Forms', tools.google_forms),
        ('lucky', 'Find lucky pupils', tools.lucky),
        ('qr', 'Form QR codes', tools.qr),
        ('reshu-ege', 'Reshu EGE', tools.reshuege),
        ('template', 'Create template files', tools.template),
        ('tripod', 'Generate tripod results', tools.tripod),
        ('yaform', 'Download yandex form results', tools.yaform),
        ('znanium', 'Znanium', tools.znanium),
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

    log.info(cm(f'Start', color=color.Green))
    start_time = time.time()
    try:
        args.func(args)
        finish_time = time.time()
        delta = finish_time - start_time
        log.info(cm('Finished in %.2f seconds', color=color.Green), delta)
        if delta >= 300:
            say('Готово', rate=250)
    except Exception as e:
        finish_time = time.time()
        log.critical(f'Error message: {cm(e, color=color.Red)}')
        delta = finish_time - start_time
        log.exception(cm(f'Failed in {delta:.2f} seconds', color=color.Red))
        if delta >= 30:
            msg = str(e)[:30]
            say(f'Ошибка: {msg}', rate=250)


if __name__ == '__main__':
    main()
