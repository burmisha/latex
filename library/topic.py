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

    @property
    def is_grade(self) -> bool:
        return 'grade' in self.name


@attr.s
class TaggedTopic:
    description: str = attr.ib()
    tags: List[Tag] = attr.ib()


class TopicDetector:
    SEARCH_MIN_THRESHOLD = 50
    SEARCH_DELTA_MULTIPLIER = 0.95

    def _tags_by_raw(self, raw_tags: str) -> List[Tag]:
        tags = [self.tag_by_name[tag.strip()] for tag in raw_tags.split(TAGS_SPLITTER)]
        return tags

    def _create_tagged_topics(self, tagged_topics_config) -> List[TaggedTopic]:
        tagged_topics = []
        for row in tagged_topics_config:
            raw_tags, description = row.split(DESCRIPTION_SPLITTER)
            tagged_topic = TaggedTopic(
                description=description.strip(),
                tags=self._tags_by_raw(raw_tags),
            )
            tagged_topics.append(tagged_topic)
        return tagged_topics

    def _create_topics(self, program):
        chapter_values = collections.defaultdict(int)
        part_values = collections.defaultdict(int)
        for grade_name, rows in program.items():
            grade_tag = self.tag_by_name[grade_name]
            assert grade_tag.is_grade
            grade = grade_tag.grade
            for row in rows:
                tags = self._tags_by_raw(row)
                part_index = f'{grade} {tags[0].name}'
                if part_index not in part_values:
                    chapter_values[grade] += 1
                part_values[part_index] += 1

                yield Topic(
                    Grade=grade,
                    ChapterIndex=chapter_values[grade],
                    PartIndex=part_values[part_index],
                    ChapterTitle=tags[0].description,
                    PartTitle=tags[1].description,
                    Terms=[tt.description for tt in self.tagged_topics if tt.tags == [grade_tag] + tags],
                )

    def __init__(self):
        config = library.files.load_yaml_data('topics.yaml')

        self.tag_by_name = {
            name: Tag(name=name, description=description)
            for name, description in config['tags'].items()
        }
        self.tagged_topics = self._create_tagged_topics(config['tagged_topics'])

        self._topic_by_extended_term = collections.defaultdict(list)
        for topic in self._create_topics(config['program']):
            for extended_term in topic.extended_terms:
                self._topic_by_extended_term[extended_term].append(topic)

        self._validate()

    def _validate(self):
        assert self.get_topic_index('МКТ и термодинамика Термодинамика Внутренняя энергия идеального газа') is not None
        assert self.get_topic_index('МКТ и термодинамика Термодинамика Циклические процессы') is not None
        assert self.get_topic_index('Урок 343 - Затухающие колебания - 1') is not None
        assert self.get_topic_index('электрический потенциал') is not None
        tag_10 = self.tag_by_name['10_grade']
        assert len(self.get_second_tags([tag_10])) == 5
        # assert self.get_topic_index('Урок 229. Работа электрического поля. Потенциал. Электрическое напряжение') is not None
        # assert self.get_topic_index('Задачи на фотоэффект') is not None

    @property
    def grade_tags(self) -> List[Tag]:
        return [tag for tag in self.tag_by_name.values() if tag.is_grade]

    def get_second_tags(self, grade_tags: List[Tag]) -> List[Tag]:
        tags = []
        tags_set = set()
        for tagged_topic in self.tagged_topics:
            if tagged_topic.tags[0] in grade_tags:
                second_tag = tagged_topic.tags[1]
                if second_tag.name not in tags_set:
                    tags.append(second_tag)
                    tags_set.add(second_tag.name)
        return tags

    def get_third_tags(self, grade_tags: List[Tag], second_tags: List[Tag]) -> List[Tag]:
        tags = []
        tags_set = set()
        for tagged_topic in self.tagged_topics:
            if tagged_topic.tags[0] in grade_tags and tagged_topic.tags[1] in second_tags:
                third_tag = tagged_topic.tags[2]
                if third_tag.name not in tags_set:
                    tags.append(third_tag)
                    tags_set.add(third_tag.name)
        return tags


    def get_tagged_topics(self, tags: List[Tag]) -> List[TaggedTopic]:
        tag_names = set(tag.name for tag in tags)
        return [
            tagged_topic
            for tagged_topic in self.tagged_topics
            if set(tag.name for tag in tagged_topic.tags) & tag_names
        ]

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
