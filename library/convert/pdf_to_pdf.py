import library.files
import library.location
import library.process

from library.structure.page import PagesRange

import os

import logging
log = logging.getLogger(__name__)


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
