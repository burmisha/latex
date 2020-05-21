# -*- coding: utf-8 -*-

import time

import logging
log = logging.getLogger(__name__)

# Selenium also requires geckodriver
# Use 'brew install geckodriver'
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains



# TODO: strange texts
DELETE_SCRIPT = '''
$('iframe').remove();
$('.adsbygoogle').remove();
$('[id^=yandex_rtb_]').remove();

$('.minor').remove();
$("span:contains('Раздел кодификатора ФИПИ')").remove();
$("span:contains('Источник: Тренировочная работа по физике')").remove();
$("span:contains('Источник: ЕГЭ по физике')").remove();
$("span:contains('Источник: ЕГЭ по фи­зи­ке')").remove();
$("a:contains('Пройти тестирование по этим заданиям')").remove();
$("a:contains('Вернуться к каталогу заданий')").remove();
$("a:contains('Версия для печати и копирования в MS Word')").remove();

$('.left_column').remove();
$('.new_header').remove();
$('.new_topheader').remove();
$('.subj_nav').remove();
$('.left_column_btn').remove();
$('.pred_btn').remove();
$('.orange_select').remove();
$('#tophref').remove();
$('#sm2-container').remove();
$('.footer').remove();
$('.content > dev > br').remove();
$('hr').remove();
$('body > div:nth-child(7)').remove();
$('body > div:nth-child(6)').remove();
$('body > div:nth-child(5)').remove();
$('.sgia-main-content > span:nth-child(3)').remove();
$('.sgia-main-content > br').remove();
$('.s2b51bef0').remove();

$('body').css('background', 'fff');
$('body').css('background-image', 'none');
'''

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

    def MakeFullScreenshot(self, url, totalCount=None, filename=None):
        log.info('Making screenshot of %s', url)
        log.info('Starting Firefox')
        driver = webdriver.Firefox()
        try:
            driver.set_window_size(720, 768)
            log.info('Loading %s', url)
            driver.get(url)
            oldCount = 0
            count = len(driver.find_elements_by_class_name('problem_container'))
            while (oldCount != count) and (count != totalCount):
                log.info('%d -> %d, loading more', oldCount, count)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                if totalCount is None:
                    time.sleep(2)
                else:
                    time.sleep(1)
                oldCount = count
                count = len(driver.find_elements_by_class_name('problem_container'))
            log.info('Loaded %d problems', count)
            driver.execute_script(DELETE_SCRIPT)

            # dirty hack to zoom for better typesetting
            # https://github.com/SeleniumHQ/selenium/issues/4244
            driver.execute_script('document.body.style.MozTransform = "scale(1.30)";')
            driver.execute_script('document.body.style.MozTransformOrigin = "0 0";')

            with open(filename, 'wb') as pngFile:
                pngFile.write(driver.find_element_by_class_name('prob_list').screenshot_as_png)
        except:
            log.error('Exiting browser')
            driver.quit()
            raise
        else:
            log.info('Exiting browser')
            driver.quit()


def run(args):
    physEge = PhysEge()
    # physEge.GetParts()
    physEge.MakeFullScreenshot('https://phys-ege.sdamgia.ru/test?theme=334', filename='/Users/burmisha/screenshot.png')

def populate_parser(parser):
    parser.set_defaults(func=run)