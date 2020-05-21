# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

# Selenium also requires geckodriver
# Use 'brew install geckodriver'
from selenium import webdriver


class PhysEge(object):
    def __init__(self):
        self.__Url = 'https://phys-ege.sdamgia.ru'

    def GetParts(self):
        log.info('Starting Firefox')
        driver = webdriver.Firefox()
        try:
            log.info('Loading %s', self.__Url)
            driver.get(self.__Url)
            log.info('Parsing DOM')
            tbody = driver.find_element_by_xpath('//form/table/tbody')

            taskName = None
            partName = None

            result = []
            for tr in tbody.find_elements_by_xpath('./tr'):
                tds = tr.find_elements_by_xpath('./td')
                if len(tds) == 1:
                    for tr_small in tds[0].find_elements_by_xpath('./div/table/tbody/tr'):
                        name = tr_small.find_element_by_xpath('./td[1]').text
                        a = tr_small.find_element_by_xpath('./td[1]/a').get_attribute('href')
                        partName = name.split('(')[0].strip().replace(', ', u' и ').replace(u' просмотреть', '')
                        assert partName
                        result[-1][1].append((partName, a))
                        log.info('  Part: %s, link: %s', partName, a)
                elif len(tds) == 2:
                    a = tds[0].find_element_by_xpath('./a')
                    a.click()  # selenium reqiures text to be displayed
                    taskNumber = int(a.text.split('.')[0].split(' ')[0])
                    taskName = a.text.split('.')[1].split('(')[0].strip().replace(', ', u' и ')
                    assert taskNumber == len(result) + 1
                    result.append((taskName, []))
                    log.info('Chapter %02d: %s', taskNumber, taskName)
                else:
                    pass
            assert len(result) == 32
        except:
            log.error('Exiting browser')
            driver.quit()
            raise
        else:
            log.info('Exiting browser')
            driver.quit()
        return result

    def MakeFullScreenshot(self, url):
        pass


def run(args):
    physEge = PhysEge()
    physEge.GetParts()


def populate_parser(parser):
    parser.set_defaults(func=run)