import subprocess
import webbrowser
import time

import logging
log = logging.getLogger(__name__)

from library.logging import cm, color


def now_ts():
    return time.time()


def run(command, cwd=None):
    str_command = ' '.join(command)
    start = now_ts()
    result = subprocess.run(command, capture_output=True, cwd=cwd)
    end = now_ts()
    delta = f'{end - start:.3f}'
    if result.returncode == 0:
        log.debug(f'Completed {cm(str_command, color=color.Cyan)} in {cm(delta, color=color.Cyan)} seconds')
    else:
        log.debug(f'Failed {cm(str_command, color=color.Red)} in {cm(delta, color=color.Red)} seconds')
        raise RuntimeError(f'Command failed with code {result.returncode}, command: {str_command!r}')
    return result


def communicate(*, command=None, input=None):
    start = now_ts()
    p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(input.encode('utf-8'))
    end = now_ts()
    delta = f'{end - start:.3f}'
    assert stdout == b'', f'expecting empty stdout, got {stdout.decode("utf-8")}'
    assert stderr == b'', f'expecting empty stderr, got {stderr.decode("utf-8")}'
    assert p.returncode == 0, f'returncode expected to be 0, got {p.returncode}'


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
