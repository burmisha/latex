import library.absent
import library.location
import library.files

import logging
log = logging.getLogger(__name__)


def run(args):
    for csv_file in library.files.walkFiles(library.location.downloads(), regexp='^meetingAttendanceList.*\.csv'):
        absent_file = library.absent.MSTeamsVisitors(csv_file)


def populate_parser(parser):
    parser.set_defaults(func=run)
