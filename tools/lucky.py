import library.pupils

import random
import time

import logging
log = logging.getLogger(__name__)


def getLucky(grade=None, count=None):
    className = f'2020-{grade}'
    pupilsList = list(library.pupils.getPupils(className).Iterate())
    random.seed(int(time.time()))
    random.shuffle(pupilsList)
    if count:
        pupilsList = pupilsList[:count]
    for index, pupil in enumerate(pupilsList, 1):
        log.info(f'Lucky person {index:2d}:  {pupil}')
    return None


def run(args):
    getLucky(grade=args.grade, count=args.count)


def populate_parser(parser):
    parser.add_argument('-g', '--grade', help='Grade', type=int, choices=[8, 9, 10], default=9)
    parser.add_argument('-c', '--count', help='Count', type=int)
    parser.set_defaults(func=run)
