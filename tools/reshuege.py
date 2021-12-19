import library

import os
import time
import re

import logging
log = logging.getLogger(__name__)

from PIL import Image
from io import StringIO
from io import BytesIO

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
$("span:contains('Источник: Тренировочная работа по ')").remove();
$("span:contains('Источник: ЕГЭ')").remove();
$("span:contains('Источник: ГИА')").remove();
$("span:contains('Источник: РЕШУ')").remove();
$("span:contains('Источник: Яндекс')").remove();
$("span:contains('Источник: СтатГрад')").remove();
$("span:contains('Источник: Досрочная волна ЕГЭ')").remove();
$("span:contains('Источник: Пробный экзамен')").remove();
$("span:contains('Источник: Основная волна ЕГЭ')").remove();
$("span:contains('Классификатор базовой части')").remove();
$("span:contains('Классификатор стереометрии:')").remove();
$("span:contains('Методы геометрии:')").remove();
$("a:contains('Пройти тестирование по этим заданиям')").remove();
$("a:contains('Вернуться к каталогу заданий')").remove();
$("a:contains('Версия для печати и копирования в MS Word')").remove();

$('.Header').remove();
$('.SubjectNav').remove();
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
    def __init__(self, url, count=None, driver=None):
        self._url = url
        self._tasks_count = count
        self._driver = driver
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
        result = []
        problems_count = 0
        log.info(f'Parsing {url}')
        self._driver.get(url)
        for index, category in enumerate(self._driver.find_elements_by_xpath('//div[@class="cat_main"]/div[@class="cat_category"]'), 1):
            children = category.find_elements_by_xpath('./div[@class="cat_children"]/div[@class="cat_category"]/a[@class="cat_name"]')
            if children:
                cat_name = category.find_element_by_xpath('./b[@class="cat_name"]')
                task_counts = [
                    int(child.find_element_by_xpath('./../div[@class="cat_count"]').text)
                    for child in children
                ]
            else:
                cat_name = category.find_element_by_xpath('./b/a[@class="cat_name"]')
                children = [cat_name]
                task_counts = [int(category.find_element_by_xpath('./div[@class="cat_count"]').text)]

            if re.match('^Т?Задани[ея] ', cat_name.text):
                log.info(f'Skipping {cat_name.text}')
                continue

            part_index = int(cat_name.text.strip('Т').split('.')[0])
            assert index == part_index
            part_name = self._canonize_text(cat_name.text)

            parts = []
            for child, task_count in zip(children, task_counts):
                parts.append((self._canonize_text(child.text), child.get_attribute('href'), task_count))

            log.info(f'{part_index}. {part_name}')
            for name, link, task_count in parts:
                log.info(f'  - {name} ({task_count} заданий): {link}')
                problems_count += task_count

            result.append((part_name, parts))
        assert len(result) == self._tasks_count, f'Got {len(result)}, expected {self._tasks_count}'
        log.info(f'Found {self._tasks_count} tasks groups with total of {problems_count} problems')
        return result

    @retry(WebDriverException, tries=10, delay=20)
    def MakeFullScreenshot(self, url=None, totalCount=None, filename=None):
        pngJoiner = PngJoiner(filenameFmt=filename, minHeight=1200)
        if pngJoiner.WasSaved():
            log.debug('Skipping saved part')
            return
        elif totalCount == 0:
            log.debug('Skipping empty part')
            return
        elif totalCount is None:
            raise RuntimeError('Total count is required')

        log.info(f'Saving problems from {url} to {filename}')
        self._driver.set_window_size(720, 768)
        self._driver.get(url)

        pagers = list(self._driver.find_elements_by_class_name('pager_page'))
        if pagers:
            for pager in pagers[::-1]:
                if pager.text:
                    log.info(f'Speed up load by clicking on last pager: {pager.text}')
                    pager.click()
                    time.sleep(5)
                    break

        count = 0
        while count < totalCount:
            log.info(f'Loaded {count} of {totalCount} problems, scrolling')
            self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            count = len(self._driver.find_elements_by_class_name('problem_container'))
        log.info(f'Loaded all {totalCount} problems')

        log.debug('Cleaning up DOM')
        self._driver.execute_script(DELETE_SCRIPT)

        log.debug('Zoom for better typesetting')  # dirty hack, see https://github.com/SeleniumHQ/selenium/issues/4244
        self._driver.execute_script('document.body.style.MozTransform = "scale(1.30)";')
        self._driver.execute_script('document.body.style.MozTransformOrigin = "0 0";')

        log.debug('Saving png files')
        for problem in self._driver.find_elements_by_class_name('problem_container'):
            pngJoiner.AddImage(problem.screenshot_as_png, problem.size['height'])
        pngJoiner.Save(final=True)


def run(args):
    config = [
        ('Физика', 'https://phys-ege.sdamgia.ru', 30),
        ('Физика-ОГЭ', 'https://phys-oge.sdamgia.ru', 25),
        ('География', 'https://geo-ege.sdamgia.ru', 34),
        ('Химия', 'https://chem-ege.sdamgia.ru', 35),
        ('Математика', 'https://math-ege.sdamgia.ru', 19),
        ('Математика-База', 'https://mathb-ege.sdamgia.ru', 20),
        ('Информатика', 'https://inf-ege.sdamgia.ru', 27),
    ]
    with library.firefox.get_driver() as driver:
        for subject, link, count in config:
            rootPath = library.files.UdrPath(f'Материалы - Решу ЕГЭ - {subject}')
            rootPath(create_missing_dir=True)
            sdamGia = SdamGia(link, count=count, driver=driver)
            tasks = sdamGia.GetCatalog()
            for taskIndex, (taskName, parts) in enumerate(tasks, 1):
                dirName = '%02d %s' % (taskIndex, taskName)
                taskPath = rootPath(dirName, create_missing_dir=True)
                for partIndex, (partName, link, task_count) in enumerate(parts, 1):
                    log.info('Task %d of %d, part %d of %d', taskIndex, len(tasks), partIndex, len(parts))
                    filename = rootPath(taskPath, '%d - %s - %%02d.png' % (partIndex, partName))
                    sdamGia.MakeFullScreenshot(url=link, filename=filename, totalCount=task_count)


def populate_parser(parser):
    parser.set_defaults(func=run)