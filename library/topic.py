from fuzzywuzzy import process, fuzz
import yaml

from library.logging import cm, color, one_line_pairs
import library.location

import collections
import re


import logging
log = logging.getLogger(__name__)


TopicIndex = collections.namedtuple('TopicIndex', ['Grade', 'Part', 'Subpart', 'Index'])


class TopicDetector:
    SEARCH_MIN_THRESHOLD = 80
    SEARCH_DELTA_MULTIPLIER = 0.95

    def __init__(self):
        topics_file = library.location.root('data', 'topics.yaml')
        with open(topics_file) as f:
            config = yaml.safe_load(f)

        self._matcher = collections.defaultdict(list)
        for grade, parts in config.items():
            for part_index, subparts in parts.items():
                for subpart_index, titles in subparts.items():
                    if isinstance(subpart_index, int):
                        for index, title in enumerate(titles, 1):
                            topic_index = TopicIndex(grade, part_index, subpart_index, index)
                            assert topic_index not in self._matcher[title]
                            joined_title = ' '.join([subparts.get('name', ''), title]).strip()
                            self._matcher[joined_title].append(topic_index)

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
