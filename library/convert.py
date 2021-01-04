import library.files
import library.location
import library.logging
import library.process

import os
import platform
import subprocess
import shutil

import logging
log = logging.getLogger(__name__)


class Structure:
    def __call__(self):
        raise NotImplementedError('Could not get structure')

    def _impl(self, sub_dir=None, start_index=None, parts=None):
        has_digit = all(part[0].isdigit() for part, _, _ in parts)  # all subfiles start with digit
        for index, (part_name, first, last) in enumerate(parts, start_index):
            if first > last:
                log.error('Error in book config for %r, %r', first, last)
                raise RuntimeError('Broken pages range in structure')

            if has_digit:
                name = f'{part_name}'
            else:
                name = f'{index:02d} {part_name}'

            for page in range(first, last + 1):
                yield page, sub_dir(index, name), name


class ZeroDStructure(Structure):
    def __init__(self, data, startIndex=1):
        self.Data = data
        self.StartIndex = startIndex

    def __call__(self):
        for result in self._impl(
            sub_dir=lambda index, name: None,
            start_index=self.StartIndex,
            parts=self.Data,
        ):
            yield result


class OneDStructure(Structure):
    def __init__(self, data, startIndex=1):
        self.Data = data
        self.StartIndex = startIndex

    def __call__(self):
        for result in self._impl(
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

    def __call__(self):
        for chapterIndex, (chapterName, parts) in enumerate(self.Data, self.FirstLevelStartIndex):
            for result in self._impl(
                sub_dir=lambda index, name: f'{chapterIndex:02d} {chapterName}',
                start_index=self.SecondLevelStartIndex,
                parts=parts,
            ):
                yield result


class PdfBook:
    def __init__(
        self,
        pdfPath=None,
        dstPath=None,
        pageShift=None,
    ):
        assert pdfPath.endswith('.pdf')
        assert library.files.is_file(pdfPath)
        assert library.files.is_dir(dstPath)

        assert library.files.path_is_ok(pdfPath)
        assert library.files.path_is_ok(dstPath)
        self.PdfPath = pdfPath
        self.DstPath = dstPath

        if not hasattr(self, '_ppi'):
            self._ppi = 200

        if not hasattr(self, '_magick_params'):
            self._magick_params = []

    def GetPageShift(self, pageNumber):
        if hasattr(self, 'PageShift'):
            if isinstance(self.PageShift, int):
                return self.PageShift
            else:
                return self.PageShift(pageNumber)
        else:
            return 0

    def EnsureDir(self, dirname):
        assert library.files.path_is_ok(dirname)
        if not os.path.isdir(dirname):
            log.info(f'Create missing {dirname}')
            os.mkdir(dirname)

    def GetFilename(self, dirName, nameTemplate, pageNumber):
        self.EnsureDir(self.DstPath)
        if dirName:
            dirName = os.path.join(self.DstPath, dirName)
            self.EnsureDir(dirName)
        else:
            dirName = self.DstPath
        fileName = os.path.join(dirName, f'{nameTemplate} - {pageNumber:03d}.png')
        assert library.files.path_is_ok(fileName)
        return fileName

    def ExtractPage(self, pageNumber, dirName=None, nameTemplate=None, overwrite=False):
        assert isinstance(pageNumber, int)
        assert 1 <= pageNumber < 1000
        pageIndex = self.GetPageShift(pageNumber) + pageNumber - 1
        assert 1 <= pageIndex < 1000

        fileName = self.GetFilename(dirName, nameTemplate, pageNumber)
        log.info(f'  Page {pageNumber} -> {fileName}')

        if os.path.exists(fileName) and not overwrite:
            log.debug(f'Already generated {fileName}')
            return

        command = [
            'magick',
            'convert',
            '-log', '%t %e',
            '-density', str(self._ppi * 3),
            '-resample', str(self._ppi),
            '-trim',
            '+repage',
            # '-transparent', '"#ffffff"',
            '-type', 'Grayscale',
            '-background', 'white',
            # '-define', 'png:compression-level=9',
            '-flatten',
        ] + self._magick_params + [
            f'{self.PdfPath}[{pageIndex}]',
            fileName,
        ]
        library.process.run(command)

    def Save(self, overwrite=False):
        data = list(self._structure())
        log.info(f'Saving {len(data)} pages from \'{self.PdfPath}\' to \'{self.DstPath}\'')
        for pageNumber, dirName, nameTemplate in data:
            self.ExtractPage(pageNumber, dirName=dirName, nameTemplate=nameTemplate, overwrite=overwrite)

    def GetStrangeFiles(self, remove=False):
        log.debug(f'Looking for for strange files in {self.DstPath}')

        found = set(library.files.walkFiles(self.DstPath, extensions=['.png']))
        assert all(library.files.path_is_ok(file) for file in found)

        knownFiles = []
        for pageNumber, dirName, nameTemplate in self._structure():
            filename = self.GetFilename(dirName, nameTemplate, pageNumber)
            knownFiles.append(filename)

        known = set(knownFiles)
        strange = sorted(found - known)
        log.info(f'Found {len(strange)} strange files (expected {len(known)}, found {len(found)}) in {self.DstPath}')
        for file in strange:
            log.info(f'Unknown file {file}', )
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

    def Extract(self, pages, destination_file):
        log.info('Extracting pages %s to %s', pages, destination_file)
        assert isinstance(pages, str)
        assert destination_file.endswith('.pdf')
        parts = []
        for index, pages_range in enumerate(pages.split(',')):
            pages_range = pages_range.strip()
            if '-' in pages_range:
                first_page, last_page = pages_range.split('-')
            elif '+' in pages_range:
                first_page, more_pages = pages_range.split('+')
                last_page = int(first_page) + int(more_pages)
            else:
                first_page, last_page = pages_range, pages_range
            first_page, last_page = int(first_page), int(last_page)  # including both
            assert first_page <= last_page

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
