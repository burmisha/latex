import subprocess

import logging
log = logging.getLogger(__name__)


def run(command):
    log.debug('Running %s', ' '.join(command))
    result = subprocess.call(command)
    if result != 0:
        raise RuntimeError('Command failed: %s: %s' % (command, ' '.join(command)))


def pbcopy(text):
    subprocess.run('pbcopy', universal_newlines=True, input=text)
