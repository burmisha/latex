import library.files
import library.firefox

import attr
import os
import time
from typing import List

import logging
log = logging.getLogger(__name__)


from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


URLS = [
    # 'https://web.archive.org/web/20221003013745/https://uchitel.ru/community/graduates/',
    # 'https://web.archive.org/web/20221003023351/https://uchitel.ru/community/teachers/',
    # 'https://ya.ru',
    'https://lenta.ru/',
]

@attr.s
class UdrMember:
    nabor: int
    raw_name: str
    image: str


def scroll_to_element(driver, element):
    # https://stackoverflow.com/questions/44777053/selenium-movetargetoutofboundsexception-with-firefox
    if 'firefox' in driver.capabilities['browserName']:
        x = int(float(element.location['x']))
        y = int(float(element.location['y']))
        scroll_to = f'window.scrollTo({x},{y});'
        driver.execute_script(scroll_to)

    ActionChains(driver).scroll_to_element(element).perform()



def get_members_from_url(url: str) -> List[UdrMember]:
    with library.firefox.get_driver() as driver:
        log.info(f'Loading {url} ...')
        driver.get(url)
        log.info(f'Loaded {url}')

        # element_name = 'js-uncollapse-persons'
        element_name = 'topnews__button'
        try:
            for element in driver.find_elements(By.CLASS_NAME, element_name):
                log.info(f'One more {element_name}: {element}')
                scroll_to_element(driver, element)                
                element.click()
                time.sleep(1)
        except Exception as e:
            log.exception(e)
            time.sleep(300)
            raise

        time.sleep(120)


def run(args):
    for url in URLS:
        members = get_members_from_url(url)


def populate_parser(parser):
    parser.set_defaults(func=run)
