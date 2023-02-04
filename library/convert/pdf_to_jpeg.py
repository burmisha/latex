import library.files
import library.process

from library.structure.structure import Structure
from library.structure.page import DestinationPage
from library.logging import cm, color

import os

import pytesseract
from PIL import Image
import attr
from typing import List, Optional

import logging
log = logging.getLogger(__name__)

EXTENSION = 'png'


class PageIndexer:
    def __init__(self, shift=0):
        self._shift = shift

    def get_index(self, original_index: int):
        assert 1 <= original_index < 1000, f'Invalid original index: {original_index}'

        if isinstance(self._shift, int):
            shift = self._shift
        else:
            shift = self._shift(original_index)

        index = shift + original_index - 1
        assert 0 <= index < 1000, f'Invalid ready index: {index}'
        return index


@attr.s
class BookConfig:
    pdf_file: str = attr.ib()
    dst_dir: str = attr.ib()
    structure: Structure = attr.ib()
    ppi: Optional[int] = attr.ib(default=200)
    trim: Optional[bool] = attr.ib(default=True)
    page_indexer: Optional[PageIndexer] = attr.ib(default=PageIndexer())
    magick_params: Optional[List[str]] = attr.ib(default=[])
    source_link: Optional[str] = attr.ib(default=None)

    def save_one_page(self, *, page: DestinationPage=None, force: bool=False, dry_run: bool=False):
        filename = self._get_filename(page)
        if os.path.exists(filename) and not force:
            log.debug(f'Already generated from {page.index}: {filename}')
            return

        log.info(f'  page {page.index} -> {os.path.basename(filename)!r}')
        pdf_index = self.page_indexer.get_index(page.index)
        command = self._get_magick_params() + [f'{self.pdf_file}[{pdf_index}]', filename]
        if not dry_run:
            library.process.run(command)

    def validate(self, create_missing=False):
        assert library.files.is_file(self.pdf_file)
        if create_missing:
            library.files.ensure_dir(self.dst_dir)

    def _get_filename(self, page: DestinationPage) -> str:
        if page.dst_dir:
            dir_name = os.path.join(self.dst_dir, page.dst_dir)
            library.files.ensure_dir(dir_name)
        else:
            dir_name = self.dst_dir

        fileName = os.path.join(dir_name, f'{page.name_template} - {page.index:03d}.{EXTENSION}')
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
        return '\n'.join([
            f'book {cm(basename, color=color.Green)} with {cm(pages_count, color=color.Green)} pages:'
            f'\tSource file:\t\t{self.pdf_file}',
            f'\tDestination dir:\t{self.dst_dir}',
        ])

    def get_strange_files(self, remove: bool=False):
        found = set(library.files.walkFiles(self.dst_dir, extensions=[f'.{EXTENSION}']))
        assert all(library.files.path_is_ok(file) for file in found)

        known = set([self._get_filename(page) for page in self.structure.get_pages()])
        strange = sorted(found - known)
        log.info(f'  expected {cm(len(known), color=color.Blue)} files, found {cm(len(found), color=color.Blue)} ones -> got {cm(len(strange), color=color.Blue)} strange files')
        for file in strange:
            log.info(f'Unknown file {cm(file, color=color.Red)}')
            if remove:
                os.remove(file)

    def decode_as_text(self, *, indices: List[int]=None) -> str:
        languages = [
            'rus',
            'eng',
            'equ',  # https://tesseract-ocr.github.io/tessdoc/Data-Files
        ]

        pages_to_process = []
        processed_indices = set()
        for page in self.structure.get_pages():
            if page.index in processed_indices or (indices and page.index not in indices):
                continue
            pages_to_process.append(page)
            processed_indices.add(page.index)

        log.info(f'Reading pages {indices} -> {sorted(processed_indices)}')

        result = ''
        for page in pages_to_process:
            log.info(f'Reading {page} ...')

            filename = self._get_filename(page)
            text = pytesseract.image_to_string(
                Image.open(filename),
                lang='+'.join(languages),
            )
            text = text.strip()

            index_str = str(page.index)
            if text[-len(index_str):] == index_str:
                text = text[:-len(index_str)]

            result += text.strip() + '\n'

        return result
