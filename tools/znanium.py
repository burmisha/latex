import library

import os
import time

import logging
log = logging.getLogger(__name__)

from PIL import Image
from io import BytesIO

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

    def SaveAllPages(self, pageCount=None, filenameFmt=None, descDict={}):
        assert filenameFmt.endswith('.png'), 'Invalid filename format: %s' % filenameFmt

        with library.firefox.get_driver() as driver:
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

                pageDesc = descDict.get(pageNumber, '')
                if pageDesc:
                    pageDesc = ' - ' + pageDesc

                filename = filenameFmt % (pageNumber, pageDesc)
                if os.path.exists(filename):
                    log.info('Skipping page %s as "%s" exists', pageNumber, filename)
                    continue

                imageJoiner = ImageJoiner(filename)
                for img in subcont.find_elements_by_xpath('./img'):
                    decodedPng = img.get_attribute('src').split(',', 1)[1].decode('base64')
                    imageJoiner.AddImage(decodedPng)
                imageJoiner.Save()


def run(args):
    rootPath = library.files.UdrPath('Материалы - Znanium')
    for bookName, bookUrl, dataUrl, password, pageCount, descDict in [
        (
            'Горбушин',
            'https://znanium.com/catalog/document?id=338171',
            'https://znanium.com/read?id=338172',
            'нулевые',
            84,
            {
                1: '1.2.11',
                2: '1.3.16',
                3: '1.1.11',
                4: '1.4.7',
                5: '1.1.10',
                6: '1.4.14',
                7: '1.5.18',
                8: '2.1.25',
                9: '2.1.49',
                10: '2.3.18',
                11: '2.1.60',
                12: '2.1.43',
                13: '2.2.26',
                14: '2.4.11',
                15: '2.2.4',
                16: '2.2.5',
                17: '2.2.22',
                18: '2.5.23',
                19: '2.4.9',
                20: '2.4.10',
                21: '2.3.47',
                22: '2.3.36',
                23: '2.3.32',
                24: '4.3.10',
                25: '4.3.20',
                26: '2.6.39',
                27: '2.4.13',
                28: '2.8.44',
                29: '2.8.25',
                30: '4.2.4',
                31: '2.8.31',
                32: '5.1.11',
                33: '5.1.8',
                34: '5.5.10',
                35: '5.6.30',
                36: '5.6.31',
                37: '5.6.22-1',
                38: '5.6.22-2',
                39: '5.6.28',
                40: '5.9.19',
                41: '4.5.24',
                42: '4.5.14',
                43: '7.4.17',
                44: '8.1.21',
                45: '7.1.17',
                46: '7.1.24',
                47: '6.5.29',
                48: '6.5.18',
                49: '6.6.19',
                50: '6.6.17',
                51: '7.1.28',
                52: '7.4.34',
                53: '8.4.7',
                54: '11.1.32',
                55: '8.3.14-b',
                56: '9.1.3-b',
                57: '9.3.18',
                58: '9.3.23',
                59: '9.2.14',
                60: '11.1.20',
                61: '11.1.24',
                62: '11.5.11',
                63: '11.5.17',
                64: '11.5.18',
                65: '11.2.14',
                66: '11.2.15',
                67: '11.2.17',
                68: '11.5.25',
                69: '11.5.26',
                70: '3.2.31',
                71: '3.2.22',
                72: '3.1.14',
                73: '3.2.36',
                74: '7.1.23',
                75: '7.4.35',
                76: '9.1.8',
                77: '7.4.36',
                78: '11.5.23',
                79: '11.5.24',
                80: '3.3.15',
                81: '3.3.21',
                82: '13.2.10',
                83: '13.2.20',
                84: '13.3.16',
            }
        ),
    ]:
        znanium = Znanium(bookUrl=bookUrl, dataUrl=dataUrl, password=password)
        dirName = rootPath(bookName, create_missing_dir=True)
        pages = znanium.SaveAllPages(
            filenameFmt=rootPath(bookName, '%s - %%02d%%s.png' % bookName),
            pageCount=pageCount,
            descDict=descDict,
        )


def populate_parser(parser):
    parser.set_defaults(func=run)