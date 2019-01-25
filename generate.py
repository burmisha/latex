#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import os

import problems

log = logging.getLogger('generate')


def walkFiles(dirname, extensions=[], dirsOnly=False):
    dirName = str(dirname)
    logName = 'dirs' if dirsOnly else 'files'
    log.debug('Looking for %s of types %r in %s', logName, extensions, dirName)
    count = 0
    if not os.path.exists(dirName):
        log.error('Path %r is missing', dirName)
    for root, dirs, files in os.walk(dirName):
        if dirsOnly:
            for directory in dirs:
                count += 1
                yield os.path.join(root, directory)
        else:
            for filename in files:
                if not extensions or any(filename.endswith(extension) for extension in extensions):
                    count += 1
                    yield os.path.join(root, filename)
    log.debug('Found %d %s in %s', count, logName, dirName)


def generate(args):
    tasksGenerators = [
        problems.gendenshteyn7.Gendenshteyn7(),
        problems.gendenshteyn8.Gendenshteyn8(),
        problems.getaclass.GetAClass(),
    ]
    taskNumber = args.task_number
    for tasksGenerator in tasksGenerators:
        log.info('Using %r for tasks in %r', tasksGenerator, tasksGenerator.GetBookName())
        generatedTasks = set()
        for task in sorted(tasksGenerator(), key=lambda task: task.GetFilename()):
            if taskNumber and taskNumber not in task.GetFilename():
                continue
            filename = os.path.join('problems', tasksGenerator.GetBookName(), task.GetFilename())
            generatedTasks.add(filename)
            log.info('Saving file %s', filename)
            with open(filename, 'w') as f:
                f.write(task.GetTex().encode('utf-8'))
        allTasks = set(walkFiles(tasksGenerator.GetBookName(), extensions=['tex']))
        manualTasks = sorted(allTasks - generatedTasks)
        if args.show_manual:
            log.info('Got %d manual tasks in %s', len(manualTasks), tasksGenerator.GetBookName())
            for manualTask in manualTasks:
                log.info('  Manual task: %r', manualTask)


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

    parser.add_argument('--show-manual', '--sm', help='Show manual files', action='store_true')
    parser.add_argument('--task-number', '--tn', help='Process only one task having number')

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
# 