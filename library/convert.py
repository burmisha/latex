import library.files

import os
import platform
import subprocess

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


class DocxToPdf(object):
    def __init__(self):
        assert platform.system() == 'Darwin', 'DocxToPdf converter is configured for macOS only'
        self.__GroupContainerDir = os.path.join(os.environ['HOME'], 'Library', 'Group Containers', 'UBF8T346G9.Office')
        assert os.path.exists(self.__GroupContainerDir)
        assert os.path.isdir(self.__GroupContainerDir)

    def ConvertFile(self, source_file, destination_file):
        log.info('Converting \'%s\' to \'%s\'', source_file, destination_file)
        assert os.path.exists(source_file)
        assert os.path.isfile(source_file)
        assert source_file.endswith('.docx')
        assert destination_file.endswith('.pdf')
        assert not os.path.exists(destination_file)

        tmp_docx_file = os.path.join(self.__GroupContainerDir, '_convert_tmp.docx')
        tmp_pdf_file = os.path.join(self.__GroupContainerDir, '_convert_tmp.pdf')
        for file in [tmp_docx_file, tmp_pdf_file]:
            if os.path.exists(file):
                assert os.path.isfile(file), u'Expected file: \'%s\'' % file
                os.remove(file)

        shutil.copy(source_file, tmp_docx_file)
        apple_script = '''
            tell application "Microsoft Word"
                activate
                set tmp_docx_file to "{tmp_docx_file}"
                set tmp_pdf_file to "{tmp_pdf_file}"
                open tmp_docx_file
                save as active document file name tmp_pdf_file file format format PDF
                close active window saving no
            end tell
        '''.format(
            tmp_docx_file=tmp_docx_file,
            tmp_pdf_file=tmp_pdf_file,
        )

        # https://stackoverflow.com/questions/2940916/how-do-i-embed-an-applescript-in-a-python-script
        # https://discussions.apple.com/thread/7571530
        # https://superuser.com/questions/338165/convert-batch-of-word-files-to-pdfs-in-mac-os-x
        # https://stackoverflow.com/questions/51844514/macos-automator-applescript-solution-for-exporting-docx-to-pdf
        # https://stackoverflow.com/questions/16534292/basic-powershell-batch-convert-word-docx-to-pdf
        # https://apple.stackexchange.com/questions/59532/create-automator-service-with-a-python-script
        # https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptX/Concepts/work_with_as.html#//apple_ref/doc/uid/TP40001568-BABEBGCF

        p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate(apple_script)
        assert p.returncode == 0, u'returncode expected to by 0, got %s (%r)' % p.returncode
        assert stdout == '', u'stdout expected to by empty, got %s (%r)' % stdout
        assert stderr == '', u'stderr expected to by empty, got %s (%r)' % stderr

        assert os.path.exists(tmp_pdf_file)
        assert os.path.isfile(tmp_pdf_file)

        shutil.move(tmp_pdf_file, destination_file)
        log.info('Converted \'%s\' to \'%s\'', source_file, destination_file)
        os.remove(tmp_docx_file)

    def ConvertDir(self, source_directory, destination_directory=None, recursive=True, regexp=None):
        assert os.path.exists(source_directory)
        assert os.path.isdir(source_directory)
        if destination_directory:
            dst_path = os.path.join(source_directory, destination_directory)
        else:
            dst_path = source_directory
        assert os.path.exists(dst_path)
        assert os.path.isdir(dst_path)

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
            if not os.path.exists(pdf_file):
                self.ConvertFile(docx_file, pdf_file)
                new_converted += 1
            else:
                already_converted_count += 1
        log.info(u'Converted %d files (and found %d existing) in %s', new_converted, already_converted_count, source_directory)



class PdfToPdf(object):
    '''
    https://apple.stackexchange.com/questions/99210/mac-os-x-how-to-merge-pdf-files-in-a-directory-according-to-their-file-names
    $ brew install poppler
    '''

    def __init__(self, source_file):
        assert os.path.exists(source_file)
        assert os.path.isfile(source_file)
        assert source_file.endswith('.pdf')
        self._source_file = source_file
        self._tmp_dir = os.path.join(os.environ['HOME'], 'tmp')

    def Extract(self, pages, destination_file):
        log.info('Extracting pages %s to %s', pages, destination_file)
        assert isinstance(pages, str)
        assert destination_file.endswith('.pdf')
        parts = []
        for index, pages_range in enumerate(pages.split(',')):
            pages_range = pages_range.strip()
            if '-' in pages_range:
                first_page, last_page = pages_range.split('-')
            else:
                first_page, last_page = pages_range, pages_range
            first_page, last_page = int(first_page), int(last_page)
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
