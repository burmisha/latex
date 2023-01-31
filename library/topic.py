from thefuzz import process, fuzz
import yaml
import attr

from library.logging import cm, color, one_line_pairs
import library.location
from typing import List, Optional
import collections
import re


import logging
log = logging.getLogger(__name__)


@attr.s
class Topic:
    Grade: int = attr.ib()
    ChapterIndex: int = attr.ib()
    PartIndex: int = attr.ib()
    ChapterTitle: str = attr.ib()
    PartTitle: str = attr.ib()
    Terms: List[str] = attr.ib()

    @property
    def index(self):
        return f'{self.Grade}-{self.ChapterIndex}-{self.PartIndex}'

    @property
    def title(self):
        return f'{self.ChapterTitle} - {self.PartTitle}'

    def __str__(self):
        return (
            f'topic {cm(self.index, color=color.Cyan)} '
            f'{cm(self.title, color=color.Green)} '
            f'with {len(self.Terms)} terms'
        )

    @property
    def extended_terms(self) -> List[str]:
        return [
            f'{self.ChapterTitle} {self.PartTitle} {term}'
            for term in self.Terms
        ]


TAGS_SPLITTER = ','
DESCRIPTION_SPLITTER = '|'


@attr.s
class Tag:
    name: str = attr.ib()
    description: str = attr.ib()

    @property
    def grade(self) -> int:
        return int(self.name.split('_')[0])


@attr.s
class TaggedTopic:
    description: str = attr.ib()
    tags: List[Tag] = attr.ib()


class TopicDetector:
    SEARCH_MIN_THRESHOLD = 50
    SEARCH_DELTA_MULTIPLIER = 0.95

    def tags_by_raw(self, raw_tags: str) -> List[Tag]:
        tags = [self.tag_by_name[tag.strip()] for tag in raw_tags.split(TAGS_SPLITTER)]
        return tags

    def create_tags(self, config) -> List[Tag]:
        tags = []
        for key, value in config.items():
            tag = Tag(
                name=key,
                description=value,
            )
            tags.append(tag)
        return tags

    def create_tagged_topics(self, config) -> List[TaggedTopic]:
        tagged_topics = []
        for row in config:
            raw_tags, description = row.split(DESCRIPTION_SPLITTER)
            tagged_topic = TaggedTopic(
                description=description.strip(),
                tags=self.tags_by_raw(raw_tags),
            )
            tagged_topics.append(tagged_topic)
        return tagged_topics

    def create_topics(self, config):
        chapter_values = collections.defaultdict(int)
        part_values = collections.defaultdict(int)
        for row in config:
            tags = self.tags_by_raw(row)

            grade = tags[0].grade
            part_index = f'{grade} {tags[1].name}'
            if part_index not in part_values:
                chapter_values[grade] += 1
            part_values[part_index] += 1

            yield Topic(
                Grade=grade,
                ChapterIndex=chapter_values[grade],
                PartIndex=part_values[part_index],
                ChapterTitle=tags[1].description,
                PartTitle=tags[2].description,
                Terms=[tt.description for tt in self.tagged_topics if tt.tags == tags],
            )

    def __init__(self):
        config = library.files.load_yaml_data('topics.yaml')

        self.tag_by_name = {tag.name: tag for tag in self.create_tags(config['tags'])}
        self.tagged_topics = self.create_tagged_topics(config['tagged_topics'])

        self._topic_by_extended_term = collections.defaultdict(list)
        for topic in self.create_topics(config['program']):
            for extended_term in topic.extended_terms:
                self._topic_by_extended_term[extended_term].append(topic)

        self._validate()

    def _validate(self):
        assert self.get_topic_index('МКТ и термодинамика Термодинамика Внутренняя энергия идеального газа') is not None
        assert self.get_topic_index('МКТ и термодинамика Термодинамика Циклические процессы') is not None
        assert self.get_topic_index('Урок 343 - Затухающие колебания - 1') is not None
        assert self.get_topic_index('электрический потенциал') is not None
        # assert self.get_topic_index('Урок 229. Работа электрического поля. Потенциал. Электрическое напряжение') is not None
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

    def get_topic_index(self, title, grade: Optional[int]=None):
        if grade:
            candidates = {
                extended_term: [topic for topic in topics if topic.Grade == grade]
                for extended_term, topics in self._topic_by_extended_term.items()
            }
        else:
            candidates = dict(self._topic_by_extended_term)

        best_extended_terms = process.extract(
            title,
            candidates.keys(),
            limit=2,
            scorer=fuzz.token_sort_ratio,
        )

        best_extended_term = None
        if best_extended_terms[0][1] >= self.SEARCH_MIN_THRESHOLD:
            if len(best_extended_terms) == 1:
                best_extended_term = best_extended_terms[0][0]
            elif best_extended_terms[1][1] < self.SEARCH_DELTA_MULTIPLIER * best_extended_terms[0][1]:
                best_extended_term = best_extended_terms[0][0]

        topics = self._topic_by_extended_term[best_extended_term] if best_extended_term else []
        topic = topics[0] if len(topics) == 1 else None

        log.debug(
            f'Search topic index by title {cm(title, color=color.Cyan)}: {cm(topic, color=color.Cyan)}\n'
            f'  Best keys are: {one_line_pairs(sorted([(v, k) for k, v in best_extended_terms], reverse=True))}\n'
            f'  Topic indices {topics}'
        )
        return topic


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
