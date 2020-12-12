import library.pupils

import random
import time

import logging
log = logging.getLogger(__name__)


def getLucky(grade=None, count=None, seed=None):
    className = f'2020 {grade}'
    pupilsList = list(library.pupils.get_class_from_string(className).Iterate())
    random.seed(seed)
    random.shuffle(pupilsList)
    if count:
        pupilsList = pupilsList[:count]
    for index, pupil in enumerate(pupilsList, 1):
        log.info(f'Lucky person {index:2d}:  {pupil}')
    return None


def run(args):
    getLucky(grade=args.grade, count=args.count, seed=args.seed)


def populate_parser(parser):
    parser.add_argument('-g', '--grade', help='Grade', type=int, choices=[9, 10])
    parser.add_argument('-c', '--count', help='Count', type=int)
    parser.add_argument('-s', '--seed', help='Random seed (default is now)', type=int, default=int(time.time()))
    parser.set_defaults(func=run)
