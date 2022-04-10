import library.files
import library.process

from library.structure.structure import Structure
from library.logging import cm, color

import os

import pytesseract
from PIL import Image

from typing import List

import logging
log = logging.getLogger(__name__)


class PdfBook:
    def __init__(
        self,
        pdfPath=None,
        dstPath=None,
        pageShift=None,
    ):
        assert pdfPath.endswith('.pdf'), f'Invalid pdf name: {pdfPath}'
        assert library.files.path_is_ok(pdfPath)
        assert library.files.path_is_ok(dstPath)
        self.PdfPath = pdfPath
        self.DstPath = dstPath

        if not hasattr(self, '_ppi'):
            self._ppi = 200

        if not hasattr(self, '_magick_params'):
            self._magick_params = []

    def set_structure(self, structure):
        assert isinstance(structure, Structure)
        self._structure = structure

    @property
    def should_trim(self) -> bool:
        if hasattr(self, 'enable_trim'):
            return self.enable_trim
        return True

    def Validate(self, create_missing=False):
        assert library.files.is_file(self.PdfPath)
        if create_missing:
            if not os.path.isdir(self.DstPath):
                log.info(f'Create missing {self.DstPath}')
                os.mkdir(self.DstPath)

        assert library.files.is_dir(self.DstPath)

    def get_pdf_index(self, page_index: int):
        assert 1 <= page_index < 1000, f'Invalid page index: {page_index}'

        if hasattr(self, 'PageShift'):
            if isinstance(self.PageShift, int):
                page_shift = self.PageShift
            else:
                page_shift = self.PageShift(page_index)
        else:
            page_shift = 0

        pdf_index = page_shift + page_index - 1
        assert 0 <= pdf_index < 1000, f'Invalid pdf index: {pdf_index}'

        return pdf_index

    def EnsureDir(self, dirname):
        assert library.files.path_is_ok(dirname)
        if not os.path.isdir(dirname):
            log.info(f'Create missing {dirname}')
            os.mkdir(dirname)

    def GetFilename(self, page):
        self.EnsureDir(self.DstPath)

        if page.dst_dir:
            dir_name = os.path.join(self.DstPath, page.dst_dir)
            self.EnsureDir(dir_name)
        else:
            dir_name = self.DstPath

        fileName = os.path.join(dir_name, f'{page.name_template} - {page.index:03d}.png')
        assert library.files.path_is_ok(fileName)

        return fileName

    def get_magick_params(self) -> List[str]:
        params = [
            'magick',
            'convert',
            '-log', '%t %e',
            '-density', str(self._ppi * 3),
            '-resample', str(self._ppi),
        ]

        if self.should_trim:
            params.append('-trim')
            # params += ['-fuzz', '5%']

        params += [
            '+repage',
            # '-transparent', '"#ffffff"',
            '-type', 'Grayscale',
            '-background', 'white',
            # '-define', 'png:compression-level=9',
            '-flatten',
        ]

        return params + self._magick_params

    def _extract_page(self, *, page=None, overwrite=False, dry_run=False):
        pdf_index = self.get_pdf_index(page.index)

        filename = self.GetFilename(page)
        if os.path.exists(filename) and not overwrite:
            log.debug(f'Already generated from {page.index}: {filename}')
            return

        log.info(f'  page {page.index} -> {os.path.basename(filename)!r}')
        if dry_run:
            return

        command = self.get_magick_params() + [f'{self.PdfPath}[{pdf_index}]', filename]
        library.process.run(command)

    def Save(self, *, overwrite=False, dry_run=False):
        for page in self._structure.get_pages():
            self._extract_page(
                page=page,
                overwrite=overwrite,
                dry_run=dry_run,
            )

    def __str__(self):
        basename = os.path.basename(self.PdfPath)
        pages_count = len(list(self._structure.get_pages()))
        return f'book {cm(basename, color=color.Green)} with {cm(pages_count, color=color.Green)} pages:\nSource file:\t\t{self.PdfPath}\nDestination dir:\t{self.DstPath}'

    def GetStrangeFiles(self, remove=False):
        found = set(library.files.walkFiles(self.DstPath, extensions=['.png']))
        assert all(library.files.path_is_ok(file) for file in found)

        known = set([self.GetFilename(page) for page in self._structure.get_pages()])
        strange = sorted(found - known)
        log.info(f'  expected {cm(len(known), color=color.Blue)} files, found {cm(len(found), color=color.Blue)} ones -> got {cm(len(strange), color=color.Blue)} strange files')
        for file in strange:
            log.info(f'Unknown file {cm(file, color=color.Red)}')
            if remove:
                os.remove(file)

    def decode_as_text(self, *, indices=None):
        result = ''
        languages = [
            'rus',
            'eng',
            'equ',  # https://tesseract-ocr.github.io/tessdoc/Data-Files
        ]
        log.info(f'Reading pages {indices}')
        processed_indices = set()
        for page in self._structure.get_pages():
            if page.index in processed_indices or (indices and page.index not in indices):
                continue
            filename = self.GetFilename(page)
            log.info(f'Reading {page}')
            text = pytesseract.image_to_string(Image.open(filename), lang='+'.join(languages))
            text = text.strip()

            index_str = str(page.index)
            if text[-len(index_str):] == index_str:
                text = text[:-len(index_str)]

            result += text.strip() + '\n'
            processed_indices.add(page.index)

        return result


def page_shift(shift):
    def decorator(cls):
        cls.PageShift = shift
        return cls
    return decorator


def params(params_list):
    def decorator(cls):
        assert isinstance(params_list, list)
        cls._magick_params = params_list
        return cls
    return decorator


def structure(data, **kws):
    def decorator(cls):
        cls._structure = Structure(data, **kws)
        return cls
    return decorator


def source_link(link):
    # now link is unused
    def decorator(cls):
        cls.SourceLink = link
        return cls
    return decorator


def disable_trim():
    def decorator(cls):
        cls.enable_trim = False
        return cls
    return decorator


def ppi(value):
    def decorator(cls):
        assert isinstance(value, int), f'Strange ppi: {value} is not int'
        assert 120 <= value <= 300, f'Strange ppi: {value} is out of range'
        cls._ppi = value
        return cls
    return decorator


