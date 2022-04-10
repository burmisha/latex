import library.files
import library.process

from library.structure.structure import Structure
from library.structure.page import DestinationPage
from library.logging import cm, color

import os

import pytesseract
from PIL import Image
import attr
from typing import List, Union, Callable, Optional

import logging
log = logging.getLogger(__name__)


@attr.s
class BookConfig:
    pdf_file: str = attr.ib()
    dst_dir: str = attr.ib()
    structure: Structure = attr.ib()
    ppi: Optional[int] = attr.ib(default=200)
    trim: Optional[bool] = attr.ib(default=True)
    page_shift: Optional[Union[int, Callable]] = attr.ib(default=0)
    magick_params: Optional[List[str]] = attr.ib(default=[])
    source_link: Optional[str] = attr.ib(default=None)

    def _get_pdf_index(self, page_index: int):
        assert 1 <= page_index < 1000, f'Invalid page index: {page_index}'

        if isinstance(self.page_shift, int):
            shift = self.page_shift
        else:
            shift = self.page_shift(page_index)

        pdf_index = shift + page_index - 1
        assert 0 <= pdf_index < 1000, f'Invalid pdf index: {pdf_index}'

        return pdf_index

    def save_one_page(self, *, page: DestinationPage = None, force: bool = False, dry_run: bool = False):
        pdf_index = self._get_pdf_index(page.index)

        filename = self._get_filename(page)
        if os.path.exists(filename) and not force:
            log.debug(f'Already generated from {page.index}: {filename}')
            return

        log.info(f'  page {page.index} -> {os.path.basename(filename)!r}')
        if dry_run:
            return

        command = self._get_magick_params() + [f'{self.pdf_file}[{pdf_index}]', filename]
        library.process.run(command)

    def Validate(self, create_missing=False):
        assert library.files.is_file(self.pdf_file)
        if create_missing:
            if not os.path.isdir(self.dst_dir):
                log.info(f'Create missing {self.dst_dir}')
                os.mkdir(self.dst_dir)

        assert library.files.is_dir(self.dst_dir)

    def _ensure_dir(self, dirname):
        assert library.files.path_is_ok(dirname)
        if not os.path.isdir(dirname):
            log.info(f'Create missing {dirname}')
            os.mkdir(dirname)

    def _get_filename(self, page: DestinationPage) -> str:
        self._ensure_dir(self.dst_dir)

        if page.dst_dir:
            dir_name = os.path.join(self.dst_dir, page.dst_dir)
            self._ensure_dir(dir_name)
        else:
            dir_name = self.dst_dir

        fileName = os.path.join(dir_name, f'{page.name_template} - {page.index:03d}.png')
        assert library.files.path_is_ok(fileName)

        return fileName

    def _get_magick_params(self) -> List[str]:
        params = [
            'magick',
            'convert',
            '-log', '%t %e',
            '-density', str(self.ppi * 3),
            '-resample', str(self.ppi),
        ]

        if self.trim:
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

        return params + self.magick_params

    def save_all_pages(self, *, force: bool=False, dry_run: bool=False):
        for page in self.structure.get_pages():
            self.save_one_page(
                page=page,
                force=force,
                dry_run=dry_run,
            )

    def __str__(self):
        basename = os.path.basename(self.pdf_file)
        pages_count = len(list(self.structure.get_pages()))
        return f'book {cm(basename, color=color.Green)} with {cm(pages_count, color=color.Green)} pages:\nSource file:\t\t{self.pdf_file}\nDestination dir:\t{self.dst_dir}'

    def get_strange_files(self, remove: bool=False):
        found = set(library.files.walkFiles(self.dst_dir, extensions=['.png']))
        assert all(library.files.path_is_ok(file) for file in found)

        known = set([self._get_filename(page) for page in self.structure.get_pages()])
        strange = sorted(found - known)
        log.info(f'  expected {cm(len(known), color=color.Blue)} files, found {cm(len(found), color=color.Blue)} ones -> got {cm(len(strange), color=color.Blue)} strange files')
        for file in strange:
            log.info(f'Unknown file {cm(file, color=color.Red)}')
            if remove:
                os.remove(file)

    def decode_as_text(self, *, indices: List[int]=None) -> str:
        result = ''
        languages = [
            'rus',
            'eng',
            'equ',  # https://tesseract-ocr.github.io/tessdoc/Data-Files
        ]
        log.info(f'Reading pages {indices}')
        processed_indices = set()
        for page in self.structure.get_pages():
            if page.index in processed_indices or (indices and page.index not in indices):
                continue
            filename = self._get_filename(page)
            log.info(f'Reading {page}')
            text = pytesseract.image_to_string(Image.open(filename), lang='+'.join(languages))
            text = text.strip()

            index_str = str(page.index)
            if text[-len(index_str):] == index_str:
                text = text[:-len(index_str)]

            result += text.strip() + '\n'
            processed_indices.add(page.index)

        return result
