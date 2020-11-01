import library.checker
import library.location
import library.process

import logging
log = logging.getLogger(__name__)


def get_checkers():
    return [
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


def run(args):
    test_filter = args.filter
    pupil_filter = args.name
    checkers = [c for c in get_checkers() if not test_filter or test_filter.replace('.', '-') in c._csv_file.replace('.', '-')]
    for checker in checkers:
        pupil_results = checker.Check(pupil_filter)
        results_text = ['ФИО\tОтметка'] + [f'{pr._name}\t{pr._mark}' for pr in pupil_results if pr]
        library.process.pbcopy('\n'.join(results_text))
        log.info('Copied names and marks to clipboard')


def populate_parser(parser):
    parser.add_argument('-f', '--filter', help='Filter test')
    parser.add_argument('-n', '--name', help='Filter pupil')
    parser.set_defaults(func=run)
