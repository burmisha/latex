# -*- coding: utf-8 -*-

import library.files

import subprocess
import os

import logging
log = logging.getLogger(__name__)


class PdfBook(object):
    def __init__(
        self,
        pdfPath=None,
        dstPath=None,
        pageShift=None,
    ):
        assert pdfPath.endswith('.pdf')
        assert os.path.exists(pdfPath)
        self.PdfPath = pdfPath
        self.DstPath = dstPath

    def GetPageShift(self, pageNumber):
        if hasattr(self, 'PageShift'):
            if isinstance(self.PageShift, int):
                return self.PageShift
            else:
                return self.PageShift(pageNumber)
        else:
            return 0

    def GetPpi(self):
        return 200

    def EnsureDir(self, dirname):
        log.debug(u'Checking %s', dirname)
        if not os.path.isdir(dirname):
            log.info(u'Create missing %s', dirname)
            os.mkdir(dirname)

    def GetParams(self):
        if hasattr(self, 'ParamsList'):
            return self.ParamsList
        else:
            return []

    def GetDirFilename(self, dirName, nameTemplate, pageNumber):
        self.EnsureDir(self.DstPath)
        if dirName:
            dirName = os.path.join(self.DstPath, dirName)
            self.EnsureDir(dirName)
        else:
            dirName = self.DstPath
        fileName = u'%s - %03d.png' % (nameTemplate, pageNumber)
        fileName = os.path.join(dirName, fileName)
        return dirName, fileName

    def ExtractPage(self, pageNumber, dirName=None, nameTemplate=None, overwrite=False):
        assert isinstance(pageNumber, int)
        assert 1 <= pageNumber < 1000
        pageIndex = self.GetPageShift(pageNumber) + pageNumber - 1
        assert 1 <= pageIndex < 1000

        dirName, fileName = self.GetDirFilename(dirName, nameTemplate, pageNumber)
        log.info('  Page %d -> %s', pageNumber, fileName)

        self.EnsureDir(self.DstPath)
        self.EnsureDir(dirName)

        if os.path.exists(fileName) and not overwrite:
            log.debug('Already generated %s', fileName)
            return False

        command = [
            'magick',
            'convert',
            '-log', '%t %e',
            '-density', str(self.GetPpi() * 3),
            '-resample', str(self.GetPpi()),
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

    def Save(self, overwrite=False):
        structure = self.GetStructure()
        data = list(structure())
        log.info('Saving %d pages from "%s" to "%s"', len(data), self.PdfPath, self.DstPath)
        for pageNumber, dirName, nameTemplate in data:
            self.ExtractPage(pageNumber, dirName=dirName, nameTemplate=nameTemplate, overwrite=overwrite)

    def GetStrangeFiles(self, remove=False):
        log.debug('Checking for strange files in %s', self.DstPath)
        found = set(library.files.walkFiles(self.DstPath, extensions=['.png']))
        structure = self.GetStructure()
        known = set(self.GetDirFilename(dirName, nameTemplate, pageNumber)[1] for pageNumber, dirName, nameTemplate in structure())
        strange = sorted(found - known)
        log.info('Found %d strange files (expected %d, found %d) in %s', len(strange), len(known), len(found), self.DstPath)
        for file in strange:
            log.info('Unknown file %s', file)
            if remove:
                os.remove(file)


def page_shift(shift):
    def decorator(cls):
        cls.PageShift = shift
        return cls
    return decorator


def params(params_list):
    def decorator(cls):
        cls.ParamsList = params_list
        return cls
    return decorator


def source_link(link):
    # now link is unused
    def decorator(cls):
        cls.SourceLink = link
        return cls
    return decorator
