import random
import logging
import time

import pupils

log = logging.getLogger('lucky')


def getLucky(lucky):
    count = None
    if ':' in lucky:
        className, count = lucky.split(':')
        count = int(count)
    else:
        className = lucky
    className = 'class-2019-{}'.format(className)
    pupilsList = list(pupils.getPupils(className).Iterate())
    random.seed(int(time.time()))
    random.shuffle(pupilsList)
    if count:
        pupilsList = pupilsList[:count]
    for index, pupil in enumerate(pupilsList):
        log.info('Lucky person %2d:  %s', index + 1, pupil)
    return None
