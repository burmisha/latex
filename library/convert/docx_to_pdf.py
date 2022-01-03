import library.files
import library.location
import library.process

import os
import platform
import shutil

import logging
log = logging.getLogger(__name__)


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


