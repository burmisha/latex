import library

import os
import time
import re

import logging
log = logging.getLogger(__name__)

from PIL import Image
from io import StringIO
from io import BytesIO

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from retry import retry


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
$("span:contains('Источник: ГИА')").remove();
$("span:contains('Источник: РЕШУ')").remove();
$("span:contains('Источник: Яндекс')").remove();
$("span:contains('Источник: Досрочная волна ЕГЭ')").remove();
$("span:contains('Источник: Пробный экзамен')").remove();
$("span:contains('Источник: Основная волна ЕГЭ')").remove();
$("span:contains('Классификатор базовой части')").remove();
$("span:contains('Классификатор стереометрии:')").remove();
$("span:contains('Методы геометрии:')").remove();
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
$('p').css('text-indent', '0pt');
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
            filename = self.__FilenameFmt % self.__Index
            log.info('  Saving image %s', filename)
            image.save(filename)

        if final:
            log.info('  Saved %d images', self.__Index + 1)
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
        self._url = url
        self.__TasksCount = tasksCount
        assert self._canonize_text('31. Реакции ионного обмена') == 'Реакции ионного обмена'
        assert self._canonize_text('За\xadда\xadния для подготовки (9)') == 'Задания для подготовки'

    def _canonize_text(self, text):
        assert isinstance(text, str)
        assert text
        result = text.replace('\xad', '').replace('/', '-').replace(':', ' - ')
        result = re.sub('^Т?[0-9]{1,2}\. (.*)', '\\1', result)
        result = result.split('(')[0]
        return result.strip()

    @retry(WebDriverException, tries=3, delay=30)
    def GetCatalog(self):
        url = '{}/prob_catalog'.format(self._url.strip('/'))
        driver = webdriver.Firefox()
        result = []
        try:
            driver.get(url)
            for index, category in enumerate(driver.find_elements_by_xpath('//div[@class="cat_main"]/div[@class="cat_category"]'), 1):
                children = category.find_elements_by_xpath('./div[@class="cat_children"]/div[@class="cat_category"]/a[@class="cat_name"]')
                if children:
                    cat_name = category.find_element_by_xpath('./b[@class="cat_name"]')
                else:
                    cat_name = category.find_element_by_xpath('./b/a[@class="cat_name"]')
                    children = [cat_name]

                if re.match('^Т?Задани[ея] ', cat_name.text):
                    log.info(f'Skipping {cat_name.text}')
                    continue

                part_index = int(cat_name.text.strip('Т').split('.')[0])
                assert index == part_index
                part_name = self._canonize_text(cat_name.text)
                parts = [(self._canonize_text(child.text), child.get_attribute('href')) for child in children]

                log.info(f'{part_index}. {part_name}')
                for name, link in parts:
                    log.info(f'  - {name}: {link}')

                result.append((part_name, parts))
        except:
            log.error('Exiting browser')
            driver.quit()
            raise
        else:
            log.info('Exiting browser')
            driver.quit()
        assert len(result) == self.__TasksCount
        return result

    @retry(WebDriverException, tries=10, delay=20)
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
    for subject, link, count in [
        ('Физика', 'https://phys-ege.sdamgia.ru', 32),
        ('Физика-ОГЭ', 'https://phys-oge.sdamgia.ru', 25),
        ('География', 'https://geo-ege.sdamgia.ru', 34),
        ('Химия', 'https://chem-ege.sdamgia.ru', 35),
        ('Математика', 'https://math-ege.sdamgia.ru/', 19),
        ('Математика-База', 'https://mathb-ege.sdamgia.ru/', 20),
    ]:
        rootPath = library.files.UdrPath('Материалы - Решу ЕГЭ - %s' % subject)
        rootPath(create_missing_dir=True)
        sdamGia = SdamGia(link, count)
        tasks = sdamGia.GetCatalog()
        # tasks = sdamGia.GetTasks()
        for taskIndex, (taskName, parts) in enumerate(tasks, 1):
            dirName = '%02d %s' % (taskIndex, taskName)
            taskPath = rootPath(dirName, create_missing_dir=True)
            for partIndex, (partName, link) in enumerate(parts, 1):
                log.info('Task %d of %d, part %d of %d', taskIndex, len(tasks), partIndex, len(parts))
                filename = rootPath(taskPath, '%d - %s - %%02d.png' % (partIndex, partName))
                sdamGia.MakeFullScreenshot(link, filename=filename)


def populate_parser(parser):
    parser.set_defaults(func=run)