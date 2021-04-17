import library.check
import library.picker
import library.process
import classes.variants

import logging
log = logging.getLogger(__name__)

def get_checkers():
    for work in classes.variants.get_simple_variants():
        if work._answers is not None:
            yield work._human_name, library.check.checker.Checker(work._human_name, work._answers, work._thresholds)

    for work in classes.variants.get_all_variants():
        if work._human_name is not None:
            yield work._human_name, library.check.checker.Checker(work._human_name, work.get_tasks(), work._thresholds)


def run(args):
    checker_filter = args.filter
    pupil_filter = args.name

    key_picker = library.picker.KeyPicker(key=library.picker.letters_key)
    for key, checker in get_checkers():
        key_picker.add(key, checker)

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
