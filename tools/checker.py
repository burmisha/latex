import library.checker
import library.location
import library.process

import os

import logging
log = logging.getLogger(__name__)

ms2_re = r'( ?м/[cс]\^?2| м/\([cс]\^?2\))?'


def make_key(line):
    return line.replace('.', '').replace('-', '')


def get_checkers():
    config = {
        '2020.10.22 9М - Тест по динамике - 1': (
            ['Б', 'Б', 'В', 'В', 'А', 'А', 'В', 'А', 'А', 'Б',],
            [5, 7, 9],
        ),
        '2020.10.27 9М - Тест по динамике - 2': (
            ['А', 'В', 'А', 'В', 'А', 'Б', 'Б', 'В', '1.5', '24', '5', '50'],
            [4, 6, 8],
        ),
        '2020.10.22 10АБ - Тест по динамике - 1': (
            ['Неверно', 'Верно', 'Верно', 'Неверно', '([Кк]илограмм.?|кг)', '([Нн]ьютон.?|Н)', f'1.6{ms2_re}', f'16{ms2_re}', f'2{ms2_re}', '6( Н)?'],
            [5, 7, 9],
        ),
        '2020.10.27 10АБ - Тест по динамике - 2': (
            [13, 17, 120, 20, 2, 40, 15],
            [3, 4, 5],
        ),
        '2020.10.29 10АБ - Тест по динамике - 3': (
            ['В', 'В', 'А', 'В', 'А', 'Б', '400', '1000000', r'0.02( м)?', '500( [НH]/м)?', r'0.02', r'0.102(75)?', r'0.14', '160', '2[kк].*', '4[kк].*', r'.*\b400\b.*\b75\b.*'],
            [10, 13, 15],
        ),
        '2020.10.30 10АБ - Тест по динамике - 4': (
            [
                'А', 'Б', 'А', 'В', 'А', 'В', 'А', 'А', 'Б',
                [
                    library.checker.ProperAnswer('25600( к[мл])?', value=2),
                    library.checker.ProperAnswer('32000( к[мл])?', value=1),
                ],
                library.checker.ProperAnswer('6400( ?км)?', value=2),
                library.checker.ProperAnswer('8', value=2),
            ],
            [6, 8, 10],
        ),
        '2020.11.03 10АБ - Тест по динамике - 5': (
            ['А', 'В', 12, 240, '0.05', '100[НH]?', 5],
            [4, 5, 6],
        ),
        '2020.11.03 9М - Тест по динамике - 3': (
            list('БАВАБАБВАВ'),
            [5, 7, 9],
        ),
        '2020.11.05 9М - Тест по динамике - 4': (
            list('ВБВБААВББА'),
            [5, 7, 9],
        ),
        '2020.11.06 10АБ - Тест по динамике - 6': (
            [
                5, 
                [
                    library.checker.ProperAnswer(5, value=2),
                    library.checker.ProperAnswer('6.73', value=1),
                ],
                '3.27', 0, 80, 120, 24, 5],
            [3, 5, 7],
        ),
    }

    checkers = {}
    for test_name, (answers, marks) in config.items():
        if ' 9М ' in test_name:
            test_file = library.location.udr('9 класс', '2020-21 9М Физика - Архив', test_name + '.csv.zip')
        elif ' 10АБ ' in test_name:
            test_file = library.location.udr('10 класс', '2020-21 10AБ Физика - Архив', test_name + '.csv.zip')
        else:
            raise RuntimeError(f'Unknown test_name: {test_name!r}')

        key = make_key(test_name)
        assert key not in checkers
        checkers[key] = library.checker.Checker(test_file, answers, marks)

    return checkers


def run(args):
    test_filter = args.filter
    pupil_filter = args.name

    checkers_dict = get_checkers()
    matched_keys = sorted([key for key in checkers_dict if not test_filter or make_key(test_filter) in key])

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
