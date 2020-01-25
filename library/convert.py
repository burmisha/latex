# -*- coding: utf-8 -*-

import subprocess
import os

import logging
log = logging.getLogger('convert')


class PdfBook(object):
    def __init__(
        self,
        pdfPath=None,
        dstPath=None,
        pageShift=None,
        name='page',
        overwrite=False,
    ):
        self.PdfPath = pdfPath
        self.DstPath = dstPath
        self.PageShift = pageShift
        self.NameTemplate = '%s-%%03d.png' % name
        self.Overwrite = overwrite
        log.info('Extracting "%s" to "%s"', self.PdfPath, self.DstPath)

    def GetPageShift(self, pageNumber):
        if self.PageShift:
            if isinstance(pageShift, int):
                return pageShift
            else:
                return self.PageShift(pageNumber)
        else:
            return 0

    def EnsureDir(self, dirname):
        log.debug(u'Checking %s', dirname)
        if not os.path.isdir(dirname):
            log.info(u'Create missing %s', dirname)
            os.mkdir(dirname)

    def GetParams(self):
        return []
    def ExtractPage(self, pageNumber, dirName=None):
        assert isinstance(pageNumber, int)
        assert 1 <= pageNumber < 1000
        pageIndex = self.GetPageShift(pageNumber) + pageNumber - 1
        assert 1 <= pageIndex < 1000

        self.EnsureDir(self.DstPath)
        if dirName:
            dirName = os.path.join(self.DstPath, dirName)
            self.EnsureDir(dirName)
        else:
            dirName = self.DstPath
        fileName = self.NameTemplate % pageNumber
        log.info('  Page %d -> %s', pageNumber, fileName)
        fileName = os.path.join(dirName, fileName)

        if os.path.exists(fileName) and not self.Overwrite:
            log.debug('Already generated %s', fileName)
            return False

        command = [
            'magick',
            'convert',
            '-log', '%t %e',
            '-density', '600',
            '-resample', '200',
            '-trim',
            '+repage',
            # '-transparent', '"#ffffff"',
            '-type', 'Grayscale',
            '-background', 'white',
            # '-define', 'png:compression-level=9',
            '-flatten',
        ] + self.GetParams() + [
            u'%s[%d]' % (self.PdfPath, pageIndex),
            fileName,
        ]
        log.debug('Running %r', command)
        result = subprocess.call(command)
        if result != 0:
            log.error('Failed to convert on %r', command)
            raise RuntimeError('Convert failed')
        else:
            return True


class ComicsBook(PdfBook):
    def GetPageShift(self, pageNumber):
        if pageNumber < 110:
            return -2
        else:
            return -3

    def Save(self):
        for index, dirName, first, last in [
            (1, u'Движение', 9, 24),
            (2, u'Яблоко и Луна', 24, 39),
            (3, u'Пуля и параболическое движение', 39, 43),
            (4, u'Движение спутников и невесомость', 43, 48),
            (5, u'Другие орбиты', 48, 53),
            (6, u'Третий закон Ньютона', 53, 59),
            (7, u'Подробнее о силах', 59, 70),
            (8, u'Импульс и импульс силы', 70, 79),
            (9, u'Энергия', 79, 89),
            (10, u'Столкновения', 89, 96),
            (11, u'Вращение', 96, 106),
            (12, u'Заряд', 111, 123),
            (13, u'Электрические поля', 123, 129),
            (14, u'Конденсаторы', 129, 134),
            (15, u'Электрический ток', 134, 148),
            (16, u'Последовательное и параллельное соединение', 148, 155),
            (17, u'Магнитные поля', 155, 166),
            (18, u'Постоянные магниты', 166, 170),
            (19, u'Закон электромагнитной индукции Фарадея', 170, 175),
            (20, u'Относительность', 175, 183),
            (21, u'Катушки индуктивности', 183, 186),
            (22, u'Постоянный и переменный ток', 186, 195),
            (23, u'Уравнения Максвелла и свет', 195, 201),
            (24, u'Квантовая электродинамика', 201, 214),
        ]:
            dirName = u'%02d %s' % (index, dirName)
            for pageNumber in range(first, last):
                self.ExtractPage(pageNumber, dirName=dirName)

class ChernoutsanBook(PdfBook):
    def Save(self):
        for chapterIndex, chapter, partIndex, part, first, last in [
            (1, u'Кинематика', 1, u'Примеры решения', 6, 26),
        ]:
            dirName = u'%02d %s - %02d %s' % (chapterIndex, chapter, partIndex, part)
            for pageNumber in range(first, last):
                self.ExtractPage(pageNumber, dirName=dirName)
