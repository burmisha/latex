# -*- coding: utf-8 -*-

import library

import os
import time

import logging
log = logging.getLogger(__name__)

from PIL import Image
from io import BytesIO

# Selenium also requires geckodriver
# Use 'brew install geckodriver'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ImageJoiner(object):
    def __init__(self, filename=None):
        self.__Filename = filename
        self.__Parts = []

    def Save(self):
        height = sum(part.size[1] for part in self.__Parts)
        image = Image.new('RGB', (self.__Parts[0].size[0], height))
        offset = 0
        for part in self.__Parts:
            image.paste(part, (0, offset))
            offset += part.size[1]
        log.info('  Saving image %s', self.__Filename)
        image.save(self.__Filename)

    def AddImage(self, pngImage):
        self.__Parts.append(Image.open(BytesIO(pngImage)))


class Znanium(object):
    def __init__(self, bookUrl=None, dataUrl=None, password=None):
        self.__BookUrl = bookUrl
        self.__DataUrl = dataUrl
        self.__Password = password

    def SaveAllPages(self, pageCount=None, filenameFmt=None):
        assert filenameFmt.endswith(' - %02d.png'), 'Invalid filename format: %s' % filenameFmt

        log.info('Starting Firefox')
        driver = webdriver.Firefox()
        try:
            # authorize
            driver.get(self.__BookUrl)
            for element in driver.find_elements_by_class_name('accordeon__toggle'):
                element.click()
            for element in driver.find_elements_by_class_name('js-enter-code__link'):
                element.click()
            driver.find_element_by_id('appx-verify2').send_keys(self.__Password)
            driver.find_element_by_id('appx-verify-ok2').click()

            # load pages one by one
            driver.get(self.__DataUrl)
            for pageNumber in range(1, 1 + pageCount):
                time.sleep(1)
                gopagenum = driver.find_element_by_id('gopagenum')
                gopagenum.send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE)  # clear
                gopagenum.send_keys(str(pageNumber), Keys.RETURN)
                time.sleep(1)
                subcont = driver.find_element_by_id('subcont%d' % pageNumber)
                imageJoiner = ImageJoiner(filenameFmt % pageNumber)
                for img in subcont.find_elements_by_xpath('./img'):
                    decodedPng = img.get_attribute('src').split(',', 1)[1].decode('base64')
                    imageJoiner.AddImage(decodedPng)
                imageJoiner.Save()
        except:
            log.error('Exiting browser')
            driver.quit()
            raise
        else:
            log.info('Exiting browser')
            driver.quit()


def run(args):
    rootPath = library.files.UdrPath(u'Материалы - Znanium')
    for bookName, bookUrl, dataUrl, password, pageCount in [
        (
            u'Горбушин', 
            'https://znanium.com/catalog/document?id=338171',
            'https://znanium.com/read?id=338172',
            u'нулевые',
            84,
        ),
    ]:
        znanium = Znanium(bookUrl=bookUrl, dataUrl=dataUrl, password=password)
        dirName = rootPath(bookName, create_missing_dir=True)
        pages = znanium.SaveAllPages(
            filenameFmt=rootPath(bookName, u'%s - %%02d.png' % bookName),
            pageCount=pageCount
        )


def populate_parser(parser):
    parser.set_defaults(func=run)