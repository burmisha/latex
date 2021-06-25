import library.pupils
import library.datetools

import random
import time

import logging
log = logging.getLogger(__name__)


def get_lucky(grade=None, count=None, seed=None):
    now_ts = int(time.time())
    if not seed:
        seed = now_ts
    className = library.datetools.formatTimestamp(now_ts, f'%Y-%m-%d {grade}')
    pupilsList = list(library.pupils.get_class_from_string(className).Iterate())
    random.seed(seed)
    random.shuffle(pupilsList)
    if count:
        pupilsList = pupilsList[:count]
    for index, pupil in enumerate(pupilsList, 1):
        log.info(f'  {index:2d}:  {pupil}')
    return None


def run(args):
    get_lucky(grade=args.grade, count=args.count, seed=args.seed)


def populate_parser(parser):
    parser.add_argument('-g', '--grade', help='Grade', type=int, choices=[9, 10])
    parser.add_argument('-c', '--count', help='Count', type=int)
    parser.add_argument('-s', '--seed', help='Random seed (None or 0 is now)', type=int, default=0)
    parser.set_defaults(func=run)
