import library.files
import library.location
import library.process

from library.util.asserts import assert_equals
from library.logging import cm, color

import os
import platform
import subprocess
import shutil
import attr


import pytesseract
from PIL import Image

from typing import List, Union

import logging
log = logging.getLogger(__name__)


@attr.s
class DestinationPage:
    index: int = attr.ib()
    dst_dir: str = attr.ib()
    name_template: str = attr.ib()


class PagesRange:
    first_index: int = attr.ib()  # including
    last_index: int = attr.ib()  # including

    def __init__(self, str_range: Union[int, str]):
        pages_range = str(str_range).strip()
        if '-' in pages_range:
            first_page, last_page = pages_range.split('-')
        elif '+' in pages_range:
            first_page, more_pages = pages_range.split('+')
            last_page = int(first_page) + int(more_pages)
        else:
            first_page, last_page = pages_range, pages_range
        self.first_index = int(first_page)
        self.last_index = int(last_page)
        assert self.first_index <= self.last_index

    def get_pages_indicies(self):
        return list(range(self.first_index, self.last_index + 1))


def test_pages_range():
    data = [
        (1, [1]),
        ('1', [1]),
        ('1+2', [1, 2, 3]),
        ('1-3', [1, 2, 3]),
    ]
    for pages_range_str, canonic in data:
        pages_range = PagesRange(pages_range_str)
        result = pages_range.get_pages_indicies()
        assert result == canonic, f'Broken get_pages_indicies:\nexpected:\t{canonic}\ngot:\t\t{result}'


test_pages_range()


def _get_indices(indices):
    if indices is None:
        first_level_index = 1
        second_level_index = 1
    else:
        first_level_index, second_level_index = indices

    if first_level_index is None:
        first_level_index = 1
    if second_level_index is None:
        second_level_index = 1

    return first_level_index, second_level_index


def was_indexed(items):
    return all(item[0][0].isdigit() for item in items)


def _get_pages(first_page, last_page, dst_dir, name_template):
    for page_index in range(first_page, last_page + 1):
        yield DestinationPage(
            index=page_index,
            dst_dir=dst_dir,
            name_template=name_template,
        )


def parse_simple_structure(data, *, indices=None, plain=None):
    assert isinstance(data, list)
    first_level_start_index, second_level_start_index = _get_indices(indices)

    already_has_first_index = was_indexed(data)
    if len(data) == 1:
        plain = True

    for first_level_index, first_level_item in enumerate(data, first_level_start_index):
        assert isinstance(first_level_item, tuple)

        if already_has_first_index: 
            name_template = f'{first_level_item[0]}'
        else:
            name_template = f'{first_level_index:02} {first_level_item[0]}'

        if plain:
            dst_dir = None
        else:
            dst_dir = name_template

        if len(first_level_item) == 3:
            _, first_page, last_page = first_level_item  
            for page in _get_pages(first_page, last_page, dst_dir, name_template):
                yield page

        elif len(first_level_item) == 2:
            second_level_items = first_level_item[1]
            already_has_second_index = was_indexed(second_level_items)

            for second_level_index, second_level_item in enumerate(first_level_item[1], second_level_start_index):
                assert isinstance(second_level_item, tuple)
                assert len(second_level_item) == 3
                second_level_name, first_page, last_page = second_level_item

                if already_has_second_index:
                    second_level_template = second_level_name
                else:
                    second_level_template = f'{second_level_index:02} {second_level_name}'

                for page in _get_pages(first_page, last_page, name_template, second_level_template):
                    yield page

        else:
            raise RuntimeError(f'Structure is not supported: {first_level_item}')


class Structure:
    def __init__(self, data, indices=None, plain=None):
        self._data = data
        self._indices = indices
        self._plain = plain

    def get_pages(self):
        for page in parse_simple_structure(self._data, indices=self._indices, plain=self._plain):
            yield page


def test_parse_simple_structure():
    data = [
        (
            Structure([('Раздел', 1, 1)]),
            [DestinationPage(1, None, '01 Раздел')],
        ),
        (
            Structure([('Раздел', 1, 3)]),
            [
                DestinationPage(1, None, '01 Раздел'), 
                DestinationPage(2, None, '01 Раздел'), 
                DestinationPage(3, None, '01 Раздел'),
            ],
        ),
        (
            Structure([('Кинематика', 2, 3), ('Динамика', 3, 3)]),
            [DestinationPage(2, '01 Кинематика', '01 Кинематика'), DestinationPage(3, '01 Кинематика', '01 Кинематика'), DestinationPage(3, '02 Динамика', '02 Динамика')],
        ),
        (
            Structure([
                ('А', [('Б', 1, 2)]),
            ]),
            [
                DestinationPage(1, '01 А', '01 Б'),
                DestinationPage(2, '01 А', '01 Б'),
            ],
        ),
        (
            Structure([
                ('А', [('Б', 1, 2), ('В', 2, 2)]),
                ('Ф', [('Д', 3, 3), ('Г', 4, 4)]),
            ]),
            [
                DestinationPage(1, '01 А', '01 Б'),
                DestinationPage(2, '01 А', '01 Б'),
                DestinationPage(2, '01 А', '02 В'),
                DestinationPage(3, '02 Ф', '01 Д'),
                DestinationPage(4, '02 Ф', '02 Г'),
            ],
        ),
        (
            Structure([
                ('А', [('3 Б', 1, 2), ('4 В', 2, 2)]),
                ('Ф', [('Д', 3, 3), ('Г', 4, 4)]),
            ]),
            [
                DestinationPage(1, '01 А', '3 Б'),
                DestinationPage(2, '01 А', '3 Б'),
                DestinationPage(2, '01 А', '4 В'),
                DestinationPage(3, '02 Ф', '01 Д'),
                DestinationPage(4, '02 Ф', '02 Г'),
            ],
        ),
    ]
    for structure, canonic in data:
        result = list(structure.get_pages())
        assert_equals('Broken structure', canonic, result)


test_parse_simple_structure()


def test_structures():
    data = [
        (
            Structure([('Раздел', 1, 3)]),
            [DestinationPage(1, None, '01 Раздел'), DestinationPage(2, None, '01 Раздел'), DestinationPage(3, None, '01 Раздел')],
        ),
        (
            Structure([('Кинематика', 2, 3), ('Динамика', 3, 3)]),
            [DestinationPage(2, '01 Кинематика', '01 Кинематика'), DestinationPage(3, '01 Кинематика', '01 Кинематика'), DestinationPage(3, '02 Динамика', '02 Динамика')],
        ),
        (
            Structure([
                ('А', [('Б', 1, 2), ('В', 2, 2)]),
                ('Ф', [('Д', 3, 3), ('Г', 4, 4)]),
            ]),
            [
                DestinationPage(1, '01 А', '01 Б'),
                DestinationPage(2, '01 А', '01 Б'),
                DestinationPage(2, '01 А', '02 В'),
                DestinationPage(3, '02 Ф', '01 Д'),
                DestinationPage(4, '02 Ф', '02 Г'),
            ],
        ),
        (
            Structure([
                ('А', [('3 Б', 1, 2), ('4 В', 2, 2)]),
                ('Ф', [('Д', 3, 3), ('Г', 4, 4)]),
            ]),
            [
                DestinationPage(1, '01 А', '3 Б'),
                DestinationPage(2, '01 А', '3 Б'),
                DestinationPage(2, '01 А', '4 В'),
                DestinationPage(3, '02 Ф', '01 Д'),
                DestinationPage(4, '02 Ф', '02 Г'),
            ],
        ),
    ]
    for structure, canonic in data:
        result = list(structure.get_pages())
        assert result == canonic, f'Broken structure:\nexpected:\t{canonic}\ngot:\t\t{result}'


test_structures()


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
        return [
            'magick',
            'convert',
            '-log', '%t %e',
            '-density', str(self._ppi * 3),
            '-resample', str(self._ppi),
        ] + (['-trim'] if self.should_trim else []) + [
            '+repage',
            # '-transparent', '"#ffffff"',
            '-type', 'Grayscale',
            '-background', 'white',
            # '-define', 'png:compression-level=9',
            '-flatten',
        ] + self._magick_params

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
            log.info(f'Unknown file {cm(file, color=color.Red)!r}')
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


class DocxToPdf:
    def __init__(self):
        assert platform.system() == 'Darwin', 'DocxToPdf converter is configured for macOS only'
        self.__GroupContainerDir = os.path.join(library.location.Location.Home, 'Library', 'Group Containers', 'UBF8T346G9.Office')
        assert library.files.is_dir(self.__GroupContainerDir)

    def get_apple_sript(self, *, docx: str=None, pdf: str=None) -> str:
        """
            https://stackoverflow.com/questions/2940916/how-do-i-embed-an-applescript-in-a-python-script
            https://discussions.apple.com/thread/7571530
            https://superuser.com/questions/338165/convert-batch-of-word-files-to-pdfs-in-mac-os-x
            https://stackoverflow.com/questions/51844514/macos-automator-applescript-solution-for-exporting-docx-to-pdf
            https://stackoverflow.com/questions/16534292/basic-powershell-batch-convert-word-docx-to-pdf
            https://apple.stackexchange.com/questions/59532/create-automator-service-with-a-python-script
            https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptX/Concepts/work_with_as.html#//apple_ref/doc/uid/TP40001568-BABEBGCF
            https://stackoverflow.com/questions/31697325/apple-script-ms-word-page-count-in-folder
            https://forums.macrumors.com/threads/applescript-ms-word-delete-last-sentence-paragraph.1767586/
        """
        return f'''
            tell application "Microsoft Word"
                activate
                set tmp_docx_file to "{docx}"
                set tmp_pdf_file to "{pdf}"
                open tmp_docx_file
                save as active document file name tmp_pdf_file file format format PDF
                close active window saving no
            end tell
        '''

    def ConvertFile(self, source_file, destination_file):
        assert library.files.is_file(source_file)
        assert source_file.endswith('.docx')
        assert destination_file.endswith('.pdf')

        if library.files.is_older(source_file, destination_file):
            log.debug(f'Skipping ready file {destination_file!r}')
            return False
        else:
            log.info(f'Converting {source_file!r} to {destination_file!r}')

        tmp_docx_file = os.path.join(self.__GroupContainerDir, '_convert_tmp.docx')
        tmp_pdf_file = os.path.join(self.__GroupContainerDir, '_convert_tmp.pdf')
        for file in [tmp_docx_file, tmp_pdf_file]:
            if os.path.exists(file):
                assert library.files.is_file(file)
                os.remove(file)

        shutil.copy(source_file, tmp_docx_file)

        library.process.communicate(
            command=['osascript', '-'],
            input=self.get_apple_sript(docx=tmp_docx_file, pdf=tmp_pdf_file).encode('utf-8'),
        )

        assert library.files.is_file(tmp_pdf_file)
        shutil.move(tmp_pdf_file, destination_file)
        log.info(f'Converted {source_file!r} to {destination_file!r}')
        os.remove(tmp_docx_file)
        return True

    def ConvertDir(self, source_directory, destination_directory=None, recursive=True, regexp=None):
        assert library.files.is_dir(source_directory)
        if destination_directory:
            dst_path = os.path.join(source_directory, destination_directory)
        else:
            dst_path = source_directory
        assert library.files.is_dir(dst_path)

        docx_suffix = '.docx'
        new_converted = 0
        already_converted_count = 0
        for docx_file in sorted(library.files.walkFiles(
            source_directory,
            extensions=[docx_suffix],
            recursive=recursive,
            regexp=regexp,
        )):
            basename = os.path.basename(docx_file)[:-len(docx_suffix)] + '.pdf'
            pdf_file = os.path.join(dst_path, basename)
            if self.ConvertFile(docx_file, pdf_file):
                new_converted += 1
            else:
                already_converted_count += 1
        log.info(f'Converted {new_converted:2d} files and found {already_converted_count:2d} existing in \'{source_directory}\'')


class PdfToPdf:
    '''
    https://apple.stackexchange.com/questions/99210/mac-os-x-how-to-merge-pdf-files-in-a-directory-according-to-their-file-names
    '''

    def __init__(self, source_file):
        assert library.files.is_file(source_file)
        assert source_file.endswith('.pdf')
        self._source_file = source_file
        self._tmp_dir = os.path.join(library.location.Location.Home, 'tmp')

    def Extract(self, pages, destination_file):
        log.info(f'Extracting pages {pages} to {destination_file}')
        assert isinstance(pages, (str, int))
        assert destination_file.endswith('.pdf'), f'Invalid destination_file name: {destination_file!r}'
        parts = []
        for index, pages_range_str in enumerate(str(pages).split(',')):
            pages_range = PagesRange(pages_range_str)
            part_template = os.path.join(self._tmp_dir, f'part_{index}_%d.pdf')  # pdfseparate requires %d in output
            parts.extend([part_template % page_index for page_index in pages_range.get_pages_indicies()])
            separate_command = [
                'pdfseparate',
                '-f', f'{pages_range.first_index}',
                '-l', f'{pages_range.last_index}',
                self._source_file,
                part_template,
            ]
            library.process.run(separate_command)

        assert len(set(parts)) == len(parts)
        unite_command = ['pdfunite'] + parts + [destination_file]
        library.process.run(unite_command)

        for part_file in parts:
            log.debug('Removing tmp file %s', part_file)
            os.remove(part_file)
