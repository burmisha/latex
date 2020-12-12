from selenium import webdriver

import contextlib

import logging
log = logging.getLogger(__name__)


@contextlib.contextmanager
def get_driver():
    log.info('Starting browser')
    driver = webdriver.Firefox()
    try:
        yield driver
    except Exception as e:
        log.error(f'Closing browser on {e!r}: {e}')
        driver.quit()
        raise
    else:
        log.info('Closing browser')
        driver.quit()
