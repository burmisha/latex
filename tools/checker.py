import library.checker
import library.location
import library.process

import os

import logging
log = logging.getLogger(__name__)


def get_checkers():
    checkers = [
        library.checker.Checker(
            library.location.udr('10 класс', '2020-21 10AБ Физика - Архив', '2020.10.29 10АБ - Тест по динамике - 3.csv.zip'),
            ['В', 'В', 'А', 'В', 'А', 'Б', '400', '1000000', '0[,\.]02( м)?', '500( [НH]/м)?', '0[,\.]02', '0[,\.]102(75)?', '0[,\.]14', '160', '2[kк].*', '4[kк].*', r'.*\b400\b.*\b75\b.*'],
            marks=[10, 13, 15],
        ),
        library.checker.Checker(
            library.location.udr('10 класс', '2020-21 10AБ Физика - Архив', '2020.10.30 10АБ - Тест по динамике - 4.csv.zip'),
            [
                'А', 'Б', 'А', 'В', 'А', 'В', 'А', 'А', 'Б',
                [
                    library.checker.ProperAnswer('25600( к[мл])?', value=2),
                    library.checker.ProperAnswer('32000( к[мл])?', value=1),
                ],
                [library.checker.ProperAnswer('6400( ?км)?', value=2)],
                [library.checker.ProperAnswer('8', value=2)],
            ],
            marks=[6, 8, 10],
        ),
    ]

    checkers_dict = {}
    for checker in checkers:
        key = os.path.basename(checker._csv_file).replace('.', '-')
        assert key not in checkers_dict
        checkers_dict[key] = checker
    return checkers_dict


def run(args):
    test_filter = args.filter
    pupil_filter = args.name

    checkers_dict = get_checkers()
    matched_keys = sorted([key for key in checkers_dict if not test_filter or test_filter.replace('.', '-') in key])

    if len(matched_keys) > 1:
        log.warning('Too many matches for \'%s\':%s', test_filter, library.logging.log_list(matched_keys))
    elif len(matched_keys) == 1:
        pupil_results = checkers_dict[matched_keys[0]].Check(pupil_filter)
        results_text = ['ФИО\tОтметка'] + [f'{pr._name}\t{pr._mark}' for pr in pupil_results if pr]
        library.process.pbcopy('\n'.join(results_text))
        log.info('Copied names and marks to clipboard')
    else:
        log.warning('No test forms results to match \'%s\'\nAvailable ones:%s', test_filter, library.logging.log_list(sorted(checkers_dict)))



def populate_parser(parser):
    parser.add_argument('-f', '--filter', help='Filter test')
    parser.add_argument('-n', '--name', help='Filter pupil')
    parser.set_defaults(func=run)
