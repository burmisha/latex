# -*- coding: utf-8 -*-

import itertools
import library
import os
import shutil
import subprocess

import logging
log = logging.getLogger(__name__)


class FileCopier(object):
    def __init__(self, source_file, destination_dir=None):
        assert os.path.exists(source_file)
        assert os.path.isfile(source_file)
        self._source_file = source_file
        log.info(u'Using source file \'%s\'', self._source_file)

        if destination_dir is None:
            self._destination_dir = None
        else:
            self.SetDestinationDir(destination_dir)

    def SetDestinationDir(self, destination_dir):
        assert os.path.exists(destination_dir)
        assert os.path.isdir(destination_dir)
        self._destination_dir = destination_dir
        log.info(u'Using destination dir \'%s\'', self._destination_dir)

    def CreateFile(self, destination_file):
        if self._destination_dir:
            destination_path = os.path.join(self._destination_dir, destination_file)
        else:
            destination_path = destination_file

        if not os.path.exists(destination_path):
            log.info(u'Creating \'%s\' from template', destination_path)
            shutil.copy(self._source_file, destination_path)
        else:
            log.debug(u'File %s already exists', destination_path)


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


def runTemplate(args):
    fileCopier = FileCopier(library.files.udrPath('template-2-columns.docx'))
    fileCopier.SetDestinationDir(library.files.udrPath(u'11 класс', u'2020 весна'))
    chapters = [
        # u'1.1 - Кинематика',
        # u'1.2 - Динамика',
        # u'1.3 - Статика',
        # u'1.4 - Законы сохранения',
        # u'1.5 - Колебания и волны',
        # u'2.1 - Молекулярная физика',
        # u'2.2 - Термодинамика',
        # u'3.1 - Электрическое поле',
        # u'3.2 - Законы постоянного тока',
        # u'3.3 - Магнитное поле',
        # u'3.4 - Электромагнитная индукция',
        # u'3.5 - Электромагнитные колебания и волны',
        # u'3.6 - Оптика',
        # u'4 - Основы СТО',
        # u'5.1 - Корпускулярно-волновой дуализм',
        # u'5.2 - Физика атома',
        # u'5.3 - Физика атомного ядра',
    ]
    courses = [
        u'БК',  # базовый курс
        # u'УК',  # углубленный курс
    ]
    file_types = [
        u'решения',
        u'условия',
    ]
    for chapter, course, file_type in itertools.product(chapters, courses, file_types):
        filename = u'Вишнякова - %s - %s - %s.docx' % (chapter, course, file_type)
        fileCopier.CreateFile(filename)

    if args.docx_2_pdf:
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


def populate_parser(parser):
    parser.add_argument('--docx-2-pdf', help='Run converter too', action='store_true')
    parser.set_defaults(func=runTemplate)
