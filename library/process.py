import subprocess
import webbrowser

import logging
log = logging.getLogger(__name__)


def run(command):
    log.debug('Running %s', ' '.join(command))
    result = subprocess.call(command)
    if result != 0:
        raise RuntimeError('Command failed: %s: %s' % (command, ' '.join(command)))


def pbcopy(text, name=None):
    subprocess.run('pbcopy', universal_newlines=True, input=text)
    log.info(f'Copied {name or "text"} to clipboard')


def say(text, rate=100):
    subprocess.run(['say', '-r', '200'], universal_newlines=True, input=text)


class TabOpener:
    def __init__(self, browser):
        self._controller = webbrowser.get(browser)

    def open(self, url):
        self._controller.open_new_tab(url)
