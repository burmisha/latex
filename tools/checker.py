import library

import logging
log = logging.getLogger(__name__)



def run(args):
    checkers = [
        library.checker.Checker(
            library.location.udr('10 класс', '2020-21 10AБ Физика - Архив', '2020.10.30 10АБ - Тест по динамике - 4.csv.zip'),
            [
                'А', 'Б', 'А', 'В', 'А', 'В', 'А', 'А', 'Б',
                [
                    library.checker.ProperAnswer('25600( к[мл])?', value=2),
                    library.checker.ProperAnswer('32000( ?к[мл])?', value=1),
                ],
                [library.checker.ProperAnswer('6400( ?км)?', value=2)],
                [library.checker.ProperAnswer('8', value=2)],
            ],
            marks=[7, 9, 11],
        ),
    ]
    test_filter = args.filter
    pupil_filter = args.name
    for checker in checkers:
        if not test_filter or test_filter in checker._csv_file:
            checker.Check(pupil_filter)



def populate_parser(parser):
    parser.add_argument('-f', '--filter', help='Filter test')
    parser.add_argument('-n', '--name', help='Filter pupil')
    parser.set_defaults(func=run)
