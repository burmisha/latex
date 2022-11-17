from fuzzywuzzy import process, fuzz
import yaml
import attr

from library.logging import cm, color, one_line_pairs
import library.location
from typing import List
import collections
import re


import logging
log = logging.getLogger(__name__)


@attr.s
class TopicIndex:
    Grade: int = attr.ib()
    ChapterIndex: int = attr.ib()
    PartIndex: int = attr.ib()
    Index: int = attr.ib()
    ChapterTitle: str = attr.ib()
    PartTitle: str = attr.ib()
    Title: str = attr.ib()

    @property
    def full_index(self):
        return f'{self.Grade}-{self.ChapterIndex}-{self.PartIndex}-{self.Index}'

    def __str__(self):
        return f'topic {cm(self.full_index, color=color.Cyan)} {cm(self.Title, color=color.Green)}'


class TopicDetector:
    SEARCH_MIN_THRESHOLD = 50
    SEARCH_DELTA_MULTIPLIER = 0.95

    def __init__(self):
        self.config = library.files.load_yaml_data('topics.yaml')

        self._matcher = collections.defaultdict(list)
        for grade, chapters in self.config.items():
            for chapter_index, chapter in enumerate(chapters, 1):
                chapter_name = chapter['name']
                for part_index, part in enumerate(chapter['parts'], 1):
                    part_name = part['name']
                    for index, title in enumerate(part['titles'], 1):
                        topic_index = TopicIndex(
                            grade,
                            chapter_index,
                            part_index,
                            index,
                            chapter_name,
                            part_name,
                            title,
                        )
                        joined_title = f'{chapter_name} {part_name} {title}'
                        self._matcher[joined_title].append(topic_index)

        assert self.get_topic_index('МКТ и термодинамика Термодинамика Внутренняя энергия идеального газа') is not None
        assert self.get_topic_index('МКТ и термодинамика Термодинамика Циклические процессы') is not None
        assert self.get_topic_index('Урок 343 - Затухающие колебания - 1') is not None
        # assert self.get_topic_index('Задачи на фотоэффект') is not None

    @property
    def get_grades(self) -> List[int]:
        grades = list(self.config.keys())
        grades.sort()
        return grades

    def get_parts(self, grades: List[int]):
        for grade in grades:
            for chapter in self.config[grade]:
                chapter_name = chapter['name']
                for part in chapter['parts']:
                    part_name = part['name']
                    if chapter_name == part_name:
                        yield f'{grade} - {chapter_name}'
                    else:
                        yield f'{grade} - {chapter_name} - {part_name}'

    def get_topic_index(self, title, grade=None):
        assert grade in (7, 8, 9, 10, 11, None)
        search_key = title.replace('класс', '')
        if grade:
            search_key = search_key.replace(str(grade), '')
        best_keys = process.extract(search_key, self._matcher.keys(), limit=2, scorer=fuzz.token_sort_ratio)

        best_key = None
        if best_keys[0][1] >= self.SEARCH_MIN_THRESHOLD:
            if len(best_keys) == 1:
                best_key = best_keys[0][0]
            elif best_keys[1][1] < self.SEARCH_DELTA_MULTIPLIER * best_keys[0][1]:
                best_key = best_keys[0][0]

        topic_indices = []
        if best_key:
            topic_indices = self._matcher[best_key]
            if grade:
                topic_indices = [topic_index for topic_index in topic_indices if topic_index.Grade == grade]
        if len(topic_indices) == 1:
            topic_index = topic_indices[0]
        else:
            topic_index = None

        log.debug((
            f'Search topic index by title {cm(title, color=color.Cyan)} in grade {grade}: {cm(topic_index, color=color.Cyan)}\n'
            f'  Best keys are: {one_line_pairs(sorted([(v, k) for k, v in best_keys], reverse=True))}\n'
            f'  Topic indices {topic_indices}'
        ))
        return topic_index


class TopicFilter:
    def __init__(self, cfg):
        if cfg:
            self._cfg = cfg

            grade, part, subpart = cfg.split('-')
            self._grade = int(grade)
            self._part = int(part)
            self._subpart = int(subpart)
        else:
            self._cfg = None

    def matches(self, topic):
        if self._cfg is None:
            return True

        if topic:
            return (
                self._grade == topic.Grade and
                self._part == topic.Part and
                self._subpart == topic.Subpart
            )

        return False


# TopicDetector()
