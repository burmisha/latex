#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging

import gendenshteyn7

log = logging.getLogger('problems')


def generate(args):
    tasksGenerators = [
        gendenshteyn7.Gendenshteyn7(),
    ]
    for tasksGenerator in tasksGenerators:
        log.info('Using %r', tasksGenerator)
        for task in tasksGenerator():
            filename = task.GetFilename()
            log.info('Saving file %s', filename)
            with open(filename, 'w') as f:
                f.write(task.GetTex().encode('utf-8'))


def CreateArgumentsParser():
    fmtClass = {'formatter_class': argparse.ArgumentDefaultsHelpFormatter}
    parser = argparse.ArgumentParser(description='Generate LaTeX-files', **fmtClass)

    loggingGroup = parser.add_argument_group('Logging arguments')
    defaultLogFormat = ' '.join([
        # '%(relativeCreated)d',
        '%(asctime)s.%(msecs)03d',
        # '%(name)10s:%(lineno)-3d',
        '%(levelname)-7s',
        '%(message)s',
    ])
    loggingGroup.add_argument('--log-format', help='Logging format', default=defaultLogFormat)
    loggingGroup.add_argument('--log-separator', help='Logging string separator', choices=['space', 'tab'], default='space')
    loggingGroup.add_argument('--verbose', help='Enable debug logging', action='store_true')

    parser.set_defaults(func=generate)
    return parser


def main():
    parser = CreateArgumentsParser()
    args = parser.parse_args()

    logFormat = args.log_format.replace('\t', ' ')
    logFormat = logFormat.replace(' ', {'space': ' ', 'tab': '\t'}[args.log_separator])
    logLevel = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=logLevel, format=logFormat, datefmt='%H:%M:%S')

    log.info('Start')
    args.func(args)
    log.info('Finish')


if __name__ == '__main__':
    main()
