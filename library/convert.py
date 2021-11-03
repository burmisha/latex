import library.files
import library.location
import library.logging
import library.process

import os
import platform
import subprocess
import shutil
import attr

from typing import List

import logging
log = logging.getLogger(__name__)


@attr.s
class DestinationPage:
    index: int = attr.ib()
    dst_dir: str = attr.ib()
    name_template: str = attr.ib()


class Structure:
    def get_pages(self):
        raise NotImplementedError('Could not get structure')

    def _get_plain_pages(self, sub_dir=None, start_index=None, parts=None):
        has_digit = all(part[0].isdigit() for part, _, _ in parts)  # all subfiles start with digit
        for index, (part_name, first, last) in enumerate(parts, start_index):
            if first > last:
                log.error(f'Invalid pages range in book structure for {part_name!r}: [{first}, {last}]. End must be greater or equal')
                raise RuntimeError('Broken pages range in structure')

            if has_digit:
                name = f'{part_name}'
            else:
                name = f'{index:02d} {part_name}'

            for page in range(first, last + 1):
                yield DestinationPage(
                    index=page,
                    dst_dir=sub_dir(index, name),
                    name_template=name,
                )


class ZeroDStructure(Structure):
    def __init__(self, data, startIndex=1):
        self.Data = data
        self.StartIndex = startIndex

    def get_pages(self):
        for result in self._get_plain_pages(
            sub_dir=lambda index, name: None,
            start_index=self.StartIndex,
            parts=self.Data,
        ):
            yield result


class OneDStructure(Structure):
    def __init__(self, data, startIndex=1):
        self.Data = data
        self.StartIndex = startIndex

    def get_pages(self):
        for result in self._get_plain_pages(
            sub_dir=lambda index, name: f'{name}',
            start_index=self.StartIndex,
            parts=self.Data,
        ):
            yield result


class TwoDStructure(Structure):
    def __init__(self, data, firstLevelStartIndex=1, secondLevelStartIndex=1):
        self.Data = data
        self.FirstLevelStartIndex = firstLevelStartIndex
        self.SecondLevelStartIndex = secondLevelStartIndex

    def get_pages(self):
        for chapterIndex, (chapterName, parts) in enumerate(self.Data, self.FirstLevelStartIndex):
            for result in self._get_plain_pages(
                sub_dir=lambda index, name: f'{chapterIndex:02d} {chapterName}',
                start_index=self.SecondLevelStartIndex,
                parts=parts,
            ):
                yield result


def test_structures():
    data = [
        (
            ZeroDStructure([('Раздел', 1, 3)]),
            [DestinationPage(1, None, '01 Раздел'), DestinationPage(2, None, '01 Раздел'), DestinationPage(3, None, '01 Раздел')],
        ),
        (
            OneDStructure([('Кинематика', 2, 3), ('Динамика', 3, 3)]),
            [DestinationPage(2, '01 Кинематика', '01 Кинематика'), DestinationPage(3, '01 Кинематика', '01 Кинематика'), DestinationPage(3, '02 Динамика', '02 Динамика')],
        ),
        (
            TwoDStructure([
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
            TwoDStructure([
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

    def should_trim(self):
        if hasattr(self, 'enable_trim'):
            return self.enable_trim
        return True

    def Validate(self, create_missing=False):
        assert library.files.is_file(self.PdfPath)
        if create_missing:
            if not os.path.isdir(self.DstPath):
                log.info(f'Create missing {self.DstPath }')
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
        ] + (['-trim'] if self.should_trim() else []) + [
            '+repage',
            # '-transparent', '"#ffffff"',
            '-type', 'Grayscale',
            '-background', 'white',
            # '-define', 'png:compression-level=9',
            '-flatten',
        ] + self._magick_params

    def _extract_page(self, *, page=None, overwrite=False, dry_run=False):
        pdf_index = self.get_pdf_index(page.index) + page.index - 1

        filename = self.GetFilename(page)
        if os.path.exists(filename) and not overwrite:
            log.debug(f'Already generated from {page.index}: {filename}')
            return

        log.info(f'  Page {page.index} -> {filename}')
        if dry_run:
            return

        command = self.get_magick_params() + [f'{self.PdfPath}[{pdf_index}]', fileName]
        library.process.run(command)

    def Save(self, *, overwrite=False, dry_run=False):
        pages = list(self._structure.get_pages())
        log.info(f'Saving {len(pages)} pages from \'{self.PdfPath}\' to \'{self.DstPath}\'')
        for page in pages:
            self._extract_page(
                page=page,
                overwrite=overwrite,
                dry_run=dry_run,
            )

    def GetStrangeFiles(self, remove=False):
        log.debug(f'Looking for strange files in {self.DstPath}')

        found = set(library.files.walkFiles(self.DstPath, extensions=['.png']))
        assert all(library.files.path_is_ok(file) for file in found)

        knownFiles = []
        for page in self._structure.get_pages():
            filename = self.GetFilename(page)
            knownFiles.append(filename)

        known = set(knownFiles)
        strange = sorted(found - known)
        log.info(f'Found {len(strange)} strange files (expected {len(known)}, found {len(found)}) in {self.DstPath}')
        for file in strange:
            log.info(f'Unknown file {file}')
            assert library.files.path_is_ok(file, raise_on_error=False)
            if remove:
                os.remove(file)


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


def zero_d_structure(data, **kws):
    def decorator(cls):
        cls._structure = ZeroDStructure(data, **kws)
        return cls
    return decorator


def one_d_structure(data, **kws):
    def decorator(cls):
        cls._structure = OneDStructure(data, **kws)
        return cls
    return decorator


def two_d_structure(data, **kws):
    def decorator(cls):
        cls._structure = TwoDStructure(data, **kws)
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

    def ConvertFile(self, source_file, destination_file):
        assert library.files.is_file(source_file)
        assert source_file.endswith('.docx')
        assert destination_file.endswith('.pdf')

        if library.files.is_older(source_file, destination_file):
            log.debug(f'Skipping existing file \'{destination_file}\'')
            return False
        else:
            log.info(f'Converting \'{source_file}\' to \'{destination_file}\'')

        tmp_docx_file = os.path.join(self.__GroupContainerDir, '_convert_tmp.docx')
        tmp_pdf_file = os.path.join(self.__GroupContainerDir, '_convert_tmp.pdf')
        for file in [tmp_docx_file, tmp_pdf_file]:
            if os.path.exists(file):
                assert os.path.isfile(file), f'Expected file: \'{file}\''
                os.remove(file)

        shutil.copy(source_file, tmp_docx_file)
        apple_script = f'''
            tell application "Microsoft Word"
                activate
                set tmp_docx_file to "{tmp_docx_file}"
                set tmp_pdf_file to "{tmp_pdf_file}"
                open tmp_docx_file
                save as active document file name tmp_pdf_file file format format PDF
                close active window saving no
            end tell
        '''

        # https://stackoverflow.com/questions/2940916/how-do-i-embed-an-applescript-in-a-python-script
        # https://discussions.apple.com/thread/7571530
        # https://superuser.com/questions/338165/convert-batch-of-word-files-to-pdfs-in-mac-os-x
        # https://stackoverflow.com/questions/51844514/macos-automator-applescript-solution-for-exporting-docx-to-pdf
        # https://stackoverflow.com/questions/16534292/basic-powershell-batch-convert-word-docx-to-pdf
        # https://apple.stackexchange.com/questions/59532/create-automator-service-with-a-python-script
        # https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptX/Concepts/work_with_as.html#//apple_ref/doc/uid/TP40001568-BABEBGCF
        # https://stackoverflow.com/questions/31697325/apple-script-ms-word-page-count-in-folder
        # https://forums.macrumors.com/threads/applescript-ms-word-delete-last-sentence-paragraph.1767586/

        p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate(apple_script.encode('utf-8'))
        assert stdout == b'', 'stdout expected to by empty, got %s (%r)' % (stdout.decode('utf-8'), stdout.decode('utf-8'))
        assert stderr == b'', 'stderr expected to by empty, got %s (%r)' % (stderr.decode('utf-8'), stderr.decode('utf-8'))
        assert p.returncode == 0, 'returncode expected to be 0, got %s (%r)' % (p.returncode, p.returncode)

        assert library.files.is_file(tmp_pdf_file)

        shutil.move(tmp_pdf_file, destination_file)
        log.info(f'Converted \'{source_file}\' to \'{destination_file}\'')
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

    def _get_pages_range(self, str_range):
        pages_range = str_range.strip()
        if '-' in pages_range:
            first_page, last_page = pages_range.split('-')
        elif '+' in pages_range:
            first_page, more_pages = pages_range.split('+')
            last_page = int(first_page) + int(more_pages)
        else:
            first_page, last_page = pages_range, pages_range
        first_page, last_page = int(first_page), int(last_page)  # including both
        assert first_page <= last_page
        return first_page, last_page

    def Extract(self, pages, destination_file):
        log.info('Extracting pages %s to %s', pages, destination_file)
        assert isinstance(pages, (str, int))
        assert destination_file.endswith('.pdf')
        parts = []
        for index, pages_range in enumerate(str(pages).split(',')):
            first_page, last_page = self._get_pages_range(pages_range)
            part_file = os.path.join(self._tmp_dir, 'part_%d.pdf')
            for page_index in range(first_page, last_page + 1):
                parts.append(part_file % page_index)
            separate_command = [
                'pdfseparate',
                '-f', '%d' % first_page,
                '-l', '%d' % last_page,
                self._source_file,
                part_file,
            ]
            library.process.run(separate_command)

        assert len(set(parts)) == len(parts)
        unite_command = ['pdfunite'] + parts + [destination_file]
        library.process.run(unite_command)

        for part_file in parts:
            log.debug('Removing tmp file %s', part_file)
            os.remove(part_file)
