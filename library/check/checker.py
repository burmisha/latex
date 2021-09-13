import library.pupils
import library.location
import generators.variant

import collections
import os
import re

import logging
log = logging.getLogger(__name__)

from library.logging import cm, color, log_list, one_line_pairs


from library.check.result import PupilResult
from library.check.proper_answer import ProperAnswer
from library.check.pupil_answer import PupilAnswer

class Checker:
    def __init__(self, test_name, answers, marks=None):
        pupils = library.pupils.get_class_from_string(test_name, addMyself=True)
        self._pupils = pupils
        self._csv_file = pupils.get_path(test_name + '.csv.zip', archive=True)
        self._marks = marks or [None, None, None]
        assert len(self._marks) == 3

        self._raw_answers = answers

        self._all_answers = [collections.Counter() for answer in self._raw_answers]
        self._all_results = collections.Counter()
        self._all_marks = collections.Counter()

    def _get_proper_answer_list(self, answer, pupil):
        if isinstance(answer, generators.variant.VariantTask):
            answer = answer.GetRandomTask(pupil).GetTestAnswer()

        if isinstance(answer, (str, int)):
            answer_dict = {
                str(answer): 1,
            }
        elif isinstance(answer, dict):
            for key, value in answer.items():
                assert isinstance(key, (str, int))
            answer_dict = answer
        else:
            raise RuntimeError(f'got invalid answer: {answer}')

        return [
            ProperAnswer(key, weight=value)
            for key, value in answer_dict.items()
        ]

    def GetPupilResult(self, row):
        pupil_result = PupilResult(len(self._raw_answers), row, self._marks)
        pupil = self._pupils.FindByName(pupil_result._original_name)
        pupil_result.SetPupil(pupil)

        for index, (pupil_answer, answer) in enumerate(zip(pupil_result._answers, self._raw_answers)):
            pupil_answer.Check(self._get_proper_answer_list(answer, pupil))
            self._all_answers[index][pupil_answer._value] += 1

        self._all_marks[pupil_result.GetMark()] += 1
        self._all_results[pupil_result.GetResult()] += 1

        return pupil_result

    def Check(self, pupil_filter):
        zipped_csv = library.files.ZippedCsv(self._csv_file)
        found_pupils = set()
        for row in zipped_csv.ReadDicts():
            pupil_result = self.GetPupilResult(row)

            pupil_name = pupil_result._pupil.GetFullName()
            found_pupils.add(pupil_name)

            if pupil_filter and (not pupil_name or pupil_filter.lower() not in pupil_name.lower()):
                continue

            log.info(pupil_result)
            yield pupil_result

        if not pupil_filter:
            for index, stats in enumerate(self._all_answers):
                stats_line = []
                valid_answers_list = self._get_proper_answer_list(self._raw_answers[index], self._pupils._me)
                for answer_str, count in stats.most_common():
                    pupil_answer = PupilAnswer(answer_str)
                    pupil_answer.Check(valid_answers_list)
                    stats_line.append(f'{cm(answer_str, color=pupil_answer._color)}: {cm(count, color=color.Cyan)}')
                stats_line = ",  ".join(stats_line)
                log.info(f'Task {index + 1:>2}: {stats_line}.')

            log.info(f'Results: {one_line_pairs(sorted(self._all_results.items()))}')
            log.info(f'Marks: {one_line_pairs(sorted(self._all_marks.items()))}')
            not_found = set(p.GetFullName() for p in self._pupils.Iterate()) - found_pupils
            log.info(f'Not found:{log_list(sorted(not_found))}')
