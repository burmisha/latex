# -*- coding: utf-8 -*-

import subprocess

import logging
log = logging.getLogger(__name__)


def run(command):
    log.debug(u'Running %s', u' '.join(command))
    result = subprocess.call(command)
    if result != 0:
        raise RuntimeError(u'Command failed: %s: %s' % (command, ' '.join(command)))
