from typing import List

import library.check.ege
import library.files
from library.logging import cm, color

import logging
log = logging.getLogger(__name__)


EMPTY_ANSWER = '-'


def load_n_split(line: str) -> List[str]:
    return [
        item.strip() if item != EMPTY_ANSWER else ''
        for item in line.split()
    ]


def format_answers(name: str, results: List[library.check.ege.Result], sizes: dict):
    name_fmt = f'%-{sizes[0]}s'
    parts = [cm(name_fmt % name, color=color.Cyan)]
    for number, result in enumerate(results, 1):
        size = sizes[number] + 2
        parts.append(result.colored_str + result.str_fill(size))

    return ''.join(parts)


def run(args):
    ege_config = library.files.load_yaml_data('ege.yaml')
    for ege_name, data in ege_config.items():
        log.info(f'Ege on {cm(ege_name, color=color.Cyan)}')
        correct_answers = load_n_split(data['correct'])
        correct_results = []
        max_sizes = {0: 0}
        numbers_header= []
        for number, correct in enumerate(correct_answers, 1):
            correct_result = library.check.ege.check_answer(number, correct, correct)
            correct_results.append(correct_result)
            max_sizes[number] = len(correct_result.correct)
            numbers_header.append(library.check.ege.Result(1, 1, str(number), str(number), colors_by_char=[color.Green] * len(str(number))))

        pupil_results = [
            ('%30s' % 'Номера', numbers_header),
            ('%30s' % 'Ответы', correct_results),
        ]
        for line_index, (pupil_name, answer_line) in enumerate(data['answers'].items(), 1):
            pupil_answers = load_n_split(answer_line)
            if len(pupil_answers) != len(correct_answers):
                raise ValueError(f'Invalid answers len for {pupil_name}: got {len(pupil_answers)}, expecting {len(correct_answers)}')

            results = []
            for number, (correct, answer) in enumerate(zip(correct_answers, pupil_answers), 1):
                result = library.check.ege.check_answer(number, correct, answer)
                results.append(result)
                max_sizes[number] = max(max_sizes[number], len(result.answer))

            total = sum(result.value for result in results)
            pupil_prefix = f'{pupil_name:>23}' + '  %-2d %-2d  ' % (line_index, total)
            max_sizes[0] = max(max_sizes[number], len(pupil_prefix))
            pupil_results.append((pupil_prefix, results))

        for index, (pupil, results) in enumerate(pupil_results):
            if not (index + 3) % 5:
                log.info('')
            log.info(format_answers(pupil, results, max_sizes))
            

def populate_parser(parser):
    parser.set_defaults(func=run)
