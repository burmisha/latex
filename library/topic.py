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

@attr.s
class Tag:
    name: str = attr.ib()
    description: str = attr.ib()


@attr.s
class TaggedTopic:
    description: str = attr.ib()
    tags: List[Tag] = attr.ib()


class TopicDetector:
    SEARCH_MIN_THRESHOLD = 50
    SEARCH_DELTA_MULTIPLIER = 0.95

    def __init__(self):
        config = library.files.load_yaml_data('topics.yaml')

        self.tags = {}
        tag_by_desc = {}
        for key, value in config['tags'].items():
            tag = Tag(name=key, description=value)
            self.tags[tag.name] = tag
            tag_by_desc[tag.description] = tag
            log.info(tag)
        del config['tags']

        self.tagged_topics = []
        for row in config['tagged_topics']:
            description, raw_tags = row.split('|')
            description = description.strip()
            tagged_topic = TaggedTopic(
                description=description,
                tags=[self.tags[tag.strip()] for tag in raw_tags.split(',')]
            )
            self.tagged_topics.append(tagged_topic)
            log.info(tagged_topic)
        del config['tagged_topics']


        self.config = {key: value for key, value in config.items()}

        

        self._topic_by_extended_term = collections.defaultdict(list)
        for grade, chapters in self.config.items():
            for chapter_index, chapter in enumerate(chapters, 1):
                chapter_name = chapter['name']
                for part_index, part in enumerate(chapter['parts'], 1):
                    topic = Topic(
                        Grade=grade,
                        ChapterIndex=chapter_index,
                        PartIndex=part_index,
                        ChapterTitle=chapter_name,
                        PartTitle=part['name'],
                        Terms=part['terms'],
                    )
                    # log.info(topic)
                    for extended_term in topic.extended_terms:
                        self._topic_by_extended_term[extended_term].append(topic)
                    for term in topic.Terms:
                        tags = [
                            f'{topic.Grade}_grade',
                            tag_by_desc[topic.ChapterTitle].name,
                            tag_by_desc[topic.PartTitle].name,
                        ]
                        log.info(f'{term}: {tags}')

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
            candidates = list(self._topic_by_extended_term.keys())

        best_extended_terms = process.extract(
            title,
            candidates,
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

        # log.info(best_extended_terms)
        # log.info(
        #     f'Search topic index by title {cm(title, color=color.Cyan)}: {cm(topic, color=color.Cyan)}\n'
        #     f'  Best keys are: {one_line_pairs(sorted([(v, k) for k, v in best_extended_terms], reverse=True))}\n'
        #     # f'  Best keys are: {best_extended_terms}\n'
        #     # f'  Topic indices {topics}'
        # )
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
