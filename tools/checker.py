import library.checker
import library.location
import library.picker
import library.process
import classes.variants

import logging
log = logging.getLogger(__name__)

ms2_re = r'( ?м/[cс]\^?2| м/\([cс]\^?2\))?'


def get_checkers():
    config = [
        ('2020.10.22 9М - Тест по динамике - 1', list('ББВВААВААБ'), [5, 7, 9]),
        ('2020.10.27 9М - Тест по динамике - 2', list('АВАВАББВ') + ['1.5', '24', '5', '50'], [4, 6, 8]),
        ('2020.10.22 10АБ - Тест по динамике - 1',
            ['Неверно', 'Верно', 'Верно', 'Неверно', '([Кк]илограмм.?|кг)', '([Нн]ьютон.?|Н)', f'1.6{ms2_re}', f'16{ms2_re}', f'2{ms2_re}', '6( Н)?'],
            [5, 7, 9],
        ),
        ('2020.10.27 10АБ - Тест по динамике - 2', [13, 17, 120, 20, 2, 40, 15], [3, 4, 5]),
        ('2020.10.29 10АБ - Тест по динамике - 3',
            list('ВВАВАБ') + ['400', '1000000', r'0.02( м)?', '500( Н/м)?', r'0.02', r'0.102(75)?', r'0.14', '160', '2[kк].*', '4[kк].*', r'.*\b400\b.*\b75\b.*'],
            [10, 13, 15],
        ),
        ('2020.10.30 10АБ - Тест по динамике - 4',
            list('АБАВАВААБ') + [{'25600( к[мл])?': 2, '32000( к[мл])?': 1}, {'6400( км)?': 2}, {'8': 2}],
            [6, 8, 10],
        ),
        ('2020.11.03 10АБ - Тест по динамике - 5', ['А', 'В', 12, 240, '0.05', '100 Н?', 5], [4, 5, 6]),
        ('2020.11.03 9М - Тест по динамике - 3', list('БАВАБАБВАВ'), [5, 7, 9]),
        ('2020.11.05 9М - Тест по динамике - 4', list('ВБВБААВББА'), [5, 7, 9]),
        ('2020.11.06 10АБ - Тест по динамике - 6', [5, {'-?5': 1, '6.73': 1}, '-?3.(2[67]|3|23|256)', 0, 80, 120, 18, 5], [3, 5, 7],),
        ('2020.11.12 9М - Динамика - 6', list('АББВВ') + ['(0.5|1/2)', 2, 120, 2], [3, 5, 7]),
        ('2020.11.13 10АБ - Законы сохранения - 1', list('АБАБВА') + [{8000: 2}, {'12.6': 2}, {10: 2}, {5: 2}], [4, 8, 11]),
        ('2020.11.19 9М - Законы сохранения - 1', list('АБАБВА') + [{'2( кг\*м/с)?': 2}, {'2( м/c)?': 2}, {'3( м/с)?': 2}, {'0.1( м/c)?': 2, '1/10': 2}], [6, 8, 10]),
        ('2020.12.04 10АБ - Статика и гидростатика - 1', [{'1/56': 2, 56: 2}, {15: 2, 12: 1}, {8: 2}, {100: 2}, {75: 2, 225: 1}, {5: 2}, {60: 2}], [6, 8, 10]),
        ('2020.12.08 9М - Колебания и волны - 1', list('ВВАВБАВБ'), [5, 6, 7]),
        ('2020.12.10 9М - Колебания и волны - 2', list('ВБВВ') + [{'Б': 1, 'В': 1}] + list('АВА'), [5, 6, 7]),
        ('2020.12.17 9М - Колебания и волны - 3', list('АВБАВБ') + [{'А': 0, 'Б': 0}] + list('ВАБ'), [6, 7, 8]),
    ]

    for test_name, answers, marks in config:
        yield test_name, library.checker.Checker(test_name, answers, marks)

    for work in classes.variants.get_all_variants():
        if work._human_name is not None:
            yield work._human_name, library.checker.Checker(work._human_name, work.get_tasks(), work._thresholds)


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
