import random
import logging
import time

import library.pupils

log = logging.getLogger('lucky')


def getLucky(grade=None, count=None):
    className = 'class-2020-{}'.format(grade)
    pupilsList = list(pupils.getPupils(className).Iterate())
    random.seed(int(time.time()))
    random.shuffle(pupilsList)
    if count:
        pupilsList = pupilsList[:count]
    for index, pupil in enumerate(pupilsList):
        log.info('Lucky person %2d:  %s', index + 1, pupil)
    return None


def runLucky(args):
    getLucky(grade=args.grade, count=args.count)


def populate_parser(parser):
    parser.add_argument('-g', '--grade', help='Grade', type=int, choices=[8, 9, 10])
    parser.add_argument('-c', '--count', help='Count', type=int)
    parser.set_defaults(func=runLucky)
