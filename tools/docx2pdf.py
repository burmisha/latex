import library

import subprocess

import logging
log = logging.getLogger(__name__)


class DocxToPdf(object):
    def __init__(self):
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



def runDocx2Pdf(args):
    docxToPdf = DocxToPdf()
    docxToPdf.ConvertDir(
        library.files.udrPath(u'11 класс', u'2020 весна'),
        recursive=False,
        regexp=u'.*Вишнякова - [0-9].*',
    )
    docxToPdf.ConvertDir(
        library.files.udrPath(u'10 класс'),
        destination_directory=u'2020-21 10AБ Физика',
        recursive=False,
        regexp=u'.*Неделя.*',
    )
    docxToPdf.ConvertDir(
        library.files.udrPath(u'10 класс'),
        recursive=False,
        regexp=u'.*Рабочая тетрадь.*',
    )


def populate_parser(parser):
    parser.set_defaults(func=runDocx2Pdf)
