import library.check
import library.picker
import library.process
import tools.variants

import logging
log = logging.getLogger(__name__)


def run(args):
    checker_filter = args.filter
    pupil_filter = args.name

    key_picker = library.picker.KeyPicker(key=library.picker.letters_key)
    for work in classes.variants.get_all_variants():
        work_checker = work.get_checker()
        if work_checker:
            key_picker.add(work._task_id, work_checker)

    if args.all:
        for checker in key_picker.all(checker_filter):
            list(checker.Check(pupil_filter))
        return

    checker = key_picker.get(flt=checker_filter)
    if checker:
        result = ['ФИО\tОтметка']
        for pupil_result in checker.Check(pupil_filter):
            if pupil_result:
                result.append(f'{pupil_result._pupil.GetFullName(surnameFirst=True)}\t{pupil_result._mark}')

        library.process.pbcopy('\n'.join(result), name='names and marks')


def populate_parser(parser):
    parser.add_argument('-f', '--filter', help='Filter test')
    parser.add_argument('-n', '--name', help='Filter pupil')
    parser.add_argument('--all', '--all', help='Parse all forms matching filter', action='store_true')
    parser.set_defaults(func=run)
