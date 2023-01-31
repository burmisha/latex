import library.pupils
import library.datetools

import datetime
import random
import time

import logging
log = logging.getLogger(__name__)


def get_lucky(grade=None, count=None, seed=None, sort=False):
    now = datetime.datetime.now()
    pupilsList = list(library.pupils.get_class_from_string(f'{now:%Y-%m-%d} {grade}').Iterate())
    if sort:
        pupilsList.sort()
    else:
        if not seed:
            seed = int(time.time())
        random.seed(seed)
        random.shuffle(pupilsList)

    if count:
        pupilsList = pupilsList[:count]

    for index, pupil in enumerate(pupilsList, 1):
        log.info(f'  {index:2d}:  {pupil}')

    return None


def run(args):
    get_lucky(grade=args.grade, count=args.count, seed=args.seed, sort=args.sort)


def populate_parser(parser):
    parser.add_argument('-g', '--grade', help='Grade', required=True)
    parser.add_argument('-c', '--count', help='Count', type=int)
    parser.add_argument('-s', '--seed', help='Random seed (absent or 0 is now)', type=int, default=0)
    parser.add_argument('--sort', help='Sort', action='store_true')
    parser.set_defaults(func=run)
