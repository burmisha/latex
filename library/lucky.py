import random
import logging
import time

import pupils

log = logging.getLogger('lucky')


def getLucky(grade=None, count=None):
    count = None
    className = 'class-2019-{}'.format(grade)
    pupilsList = list(pupils.getPupils(className).Iterate())
    random.seed(int(time.time()))
    random.shuffle(pupilsList)
    if count:
        pupilsList = pupilsList[:count]
    for index, pupil in enumerate(pupilsList):
        log.info('Lucky person %2d:  %s', index + 1, pupil)
    return None
