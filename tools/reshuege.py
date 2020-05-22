# -*- coding: utf-8 -*-

import library

import os
import time

import logging
log = logging.getLogger(__name__)

from PIL import Image
from cStringIO import StringIO
from io import BytesIO

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
$("span:contains('Источник: Досрочный')").remove();
$("span:contains('Источник: Демо')").remove();
$("span:contains('Источник: Тренировочная работа по физике')").remove();
$("span:contains('Источник: ЕГЭ')").remove();
$("span:contains('Источник: РЕШУ')").remove();
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

# based on https://gist.github.com/fabtho/13e4a2e7cfbfde671b8fa81bbe9359fb
class PngJoiner(object):
    def __init__(self, filenameFmt=None, minHeight=None):
        assert filenameFmt.endswith(' - %02d.png'), 'Invalid filename format: %s' % filenameFmt
        self.__FilenameFmt = filenameFmt
        self.__LogFile = filenameFmt.replace(' - %02d.png', '.txt')
        self.__MinHeight = minHeight
        self.__OkMessage = 'Ok\n'
        self.Reset()

    def WasSaved(self):
        if os.path.exists(self.__LogFile):
            with open(self.__LogFile) as f:
                if f.read() == self.__OkMessage:
                    return True
        return False

    def Reset(self, inc=False):
        self.__Parts = []
        if inc:
            self.__Index += 1
        else:
            self.__Index = 0
        self.__TotalHeight = 0

    def Save(self, final=False):
        if self.__Parts:
            height = sum(part.size[1] for part in self.__Parts)
            image = Image.new('RGB', (self.__Parts[0].size[0], height))
            offset = 0
            for part in self.__Parts:
                image.paste(part, (0, offset))
                offset += part.size[1]
            image.save(self.__FilenameFmt % self.__Index)

        if final:
            with open(self.__LogFile, 'w') as logFile:
                logFile.write(self.__OkMessage)

    def AddImage(self, pngImage, height):
        self.__Parts.append(Image.open(BytesIO(pngImage)))
        self.__TotalHeight += height
        if self.__TotalHeight >= self.__MinHeight:
            self.Save(final=False)
            self.Reset(inc=True)


class SdamGia(object):
    def __init__(self, url, tasksCount=None):
        self.__Url = url
        self.__TasksCount = tasksCount

    def GetTasks(self):
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
                    hasChildren = not (u'просмотреть (' in a.text)
                    if hasChildren:
                        a.click()  # selenium reqiures text to be displayed
                        taskNumber = int(a.text.split('.')[0].split(' ')[0])
                        taskName = a.text.split('.')[1].split('(')[0].strip().replace(', ', u' и ')
                        assert taskNumber == len(result) + 1
                        result.append((taskName, []))
                    else:
                        taskNumber = int(tds[0].text.split(' ')[0].strip('.'))
                        assert taskNumber == len(result) + 1
                        taskName = tds[0].text.split('.')[1].split('(')[0].strip().replace(', ', u' и ').replace(u' просмотреть', '')
                        link = a.get_attribute('href')
                        result.append((taskName, [(taskName, link)]))
                    log.info('Chapter %02d: %s', taskNumber, taskName)
                else:
                    pass
            assert len(result) == self.__TasksCount
        except:
            log.error('Exiting browser')
            driver.quit()
            raise
        else:
            log.info('Exiting browser')
            driver.quit()
        return result

    def MakeFullScreenshot(self, url=None, totalCount=None, filename=None):
        pngJoiner = PngJoiner(filenameFmt=filename, minHeight=1200)
        if pngJoiner.WasSaved():
            log.info('Skipping saved part')
            return
        else:
            log.info('Making screenshot of %s to %s', url, filename)

        log.info('Starting Firefox')
        driver = webdriver.Firefox()
        try:
            driver.set_window_size(720, 768)
            log.info('Loading %s', url)
            driver.get(url)
            oldCount = 0
            count = len(driver.find_elements_by_class_name('problem_container'))
            while (oldCount != count) and (count != totalCount):
                log.info('  %d -> %d, loading more', oldCount, count)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                if totalCount is None:
                    time.sleep(2)
                else:
                    time.sleep(1)
                oldCount = count
                count = len(driver.find_elements_by_class_name('problem_container'))
            log.info('Loaded %d problems, cleaning up DOM', count)
            driver.execute_script(DELETE_SCRIPT)

            # dirty hack to zoom for better typesetting
            # https://github.com/SeleniumHQ/selenium/issues/4244
            driver.execute_script('document.body.style.MozTransform = "scale(1.30)";')
            driver.execute_script('document.body.style.MozTransformOrigin = "0 0";')

            log.info('Saving problems')
            for problem in driver.find_elements_by_class_name('problem_container'):
                pngJoiner.AddImage(problem.screenshot_as_png, problem.size['height'])
            pngJoiner.Save(final=True)

        except:
            log.error('Exiting browser')
            driver.quit()
            raise
        else:
            log.info('Exiting browser')
            driver.quit()


def run(args):
    rootPath = library.files.UdrPath(u'Материалы - Решу ЕГЭ - Физика')

    physEge = SdamGia('https://phys-ege.sdamgia.ru', 32)
    # geoEge = SdamGia('https://geo-ege.sdamgia.ru', 34)
    # chemEge = SdamGia('https://chem-ege.sdamgia.ru', 35)

    tasks = physEge.GetTasks()
    for taskIndex, (taskName, parts) in enumerate(tasks, 1):
        dirName = u'%02d %s' % (taskIndex, taskName)
        taskPath = rootPath(dirName, create_missing_dir=True)
        for partIndex, (partName, link) in enumerate(parts, 1):
            log.info('Task %d of %d, part %d of %d', taskIndex, len(tasks), partIndex, len(parts))
            filename = rootPath(taskPath, u'%d - %s - %%02d.png' % (partIndex, partName))
            physEge.MakeFullScreenshot(link, filename=filename)

    # physEge.MakeFullScreenshot('https://phys-ege.sdamgia.ru/test?theme=281', filename='/Users/burmisha/screenshot - %02d.png')
    # physEge.MakeFullScreenshot('https://phys-ege.sdamgia.ru/test?theme=334', filename='/Users/burmisha/screenshot.png')

def populate_parser(parser):
    parser.set_defaults(func=run)