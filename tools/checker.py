import library.checker
import library.location
import library.picker
import library.process

import logging
log = logging.getLogger(__name__)

ms2_re = r'( ?м/[cс]\^?2| м/\([cс]\^?2\))?'


def get_checkers():
    config = {
        '2020.10.22 9М - Тест по динамике - 1': ('ББВВААВААБ', [5, 7, 9]),
        '2020.10.27 9М - Тест по динамике - 2': (
            list('АВАВАББВ') + ['1.5', '24', '5', '50'],
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
            list('ВВАВАБ') + ['400', '1000000', r'0.02( м)?', '500( Н/м)?', r'0.02', r'0.102(75)?', r'0.14', '160', '2[kк].*', '4[kк].*', r'.*\b400\b.*\b75\b.*'],
            [10, 13, 15],
        ),
        '2020.10.30 10АБ - Тест по динамике - 4': (
            list('АБАВАВААБ') + [
                {'25600( к[мл])?': 2, '32000( к[мл])?': 1},
                {'6400( км)?': 2},
                {'8': 2},
            ],
            [6, 8, 10],
        ),
        '2020.11.03 10АБ - Тест по динамике - 5': (
            ['А', 'В', 12, 240, '0.05', '100 Н?', 5],
            [4, 5, 6],
        ),
        '2020.11.03 9М - Тест по динамике - 3': ('БАВАБАБВАВ', [5, 7, 9]),
        '2020.11.05 9М - Тест по динамике - 4': ('ВБВБААВББА', [5, 7, 9]),
        '2020.11.06 10АБ - Тест по динамике - 6': (
            [5, {'5': 1, '6.73': 1}, '3.27', 0, 80, 120, 24, 5],
            [3, 5, 7],
        ),
    }

    for test_name, (answers, marks) in config.items():
        if ' 9М ' in test_name:
            test_file = library.location.udr('9 класс', '2020-21 9М Физика - Архив', test_name + '.csv.zip')
        elif ' 10АБ ' in test_name:
            test_file = library.location.udr('10 класс', '2020-21 10AБ Физика - Архив', test_name + '.csv.zip')
        else:
            raise RuntimeError(f'Unknown test_name: {test_name!r}')

        if isinstance(answers, str):
            answers = list(answers)

        yield test_name, library.checker.Checker(test_file, answers, marks)


def run(args):
    test_filter = args.filter
    pupil_filter = args.name

    key_picker = library.picker.KeyPicker(key=lambda x: x.replace('.', '').replace('-', ''))
    for key, checker in get_checkers():
        key_picker.add(key, checker)

    checker = key_picker.get(flt=test_filter)
    if checker:
        result = ['ФИО\tОтметка']
        for pupil_result in checker.Check(pupil_filter):
            if pupil_result:
                result.append(f'{pr._name}\t{pr._mark}')

        library.process.pbcopy('\n'.join(result))
        log.info('Copied names and marks to clipboard')


def populate_parser(parser):
    parser.add_argument('-f', '--filter', help='Filter test')
    parser.add_argument('-n', '--name', help='Filter pupil')
    parser.set_defaults(func=run)