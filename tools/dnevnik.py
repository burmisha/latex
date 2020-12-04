import library.mesh
import library.datetools
from library.logging import colorize_json

import json

import logging
log = logging.getLogger(__name__)


def run(args):
    client = library.mesh.Client()

    schedule_items = client.get_schedule_items(from_date=args.from_date, to_date=args.to_date)
    for schedule_item in sorted(schedule_items, key=lambda x: x._iso_date_time):
        log.info(schedule_item)
        if schedule_item._id in args.set_all_absent:
            for student_id in schedule_item._group._student_ids:
                client.set_absent(student_id=student_id, lesson_id=schedule_item._id)

    for _, student in client.get_student_profiles().items():
        log.debug(student)

    for res in [
        # client.get('/acl/api/users', {
        #     'ids': 14650300
        # }),
        # client.get('/jersey/api/lesson_replacements', {
        #     'academic_year_id': current_year.id,
        #     'begin_date': '2020/11/30',
        #     'end_date': '2020/12/06',
        #     'pid': client.get_teacher_id(),
        #     'teacher_id': client.get_teacher_id()
        # }),
        # client.get('/core/api/homeworks', {
        #     'academic_year_id': current_year.id,
        #     'begin_date': '30.11.2020',
        #     'end_date': '06.12.2020',
        #     'group_ids': '5404115,5472791,5396206,5351031,5351036',
        #     'pid': client.get_teacher_id(),
        #     'with_entries': True
        # }),
    ]:
        log.info(f'Got\n{colorize_json(res)}')


def populate_parser(parser):
    now_delta = library.datetools.NowDelta(default_fmt='%Y-%m-%d')
    parser.add_argument('-a', '--set-all-absent', help='Set all absent for schedult item', type=int, action='append', default=[])
    parser.add_argument('-f', '--from-date', help='Search lessons from date', default=now_delta.Before(days=10))
    parser.add_argument('-t', '--to-date', help='Search lessons to date', default=now_delta.After(days=5))
    parser.set_defaults(func=run)
