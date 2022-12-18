import attr
from enum import Enum
from typing import List, Optional


class SourceFormat(str, Enum):
    Video = 'video'
    Text = 'text'


@attr.s
class Material:
    source_format: str = attr.ib()
    title: str = attr.ib()
    canonized_title: Optional[str] = attr.ib(default=None)
    url: Optional[str] = attr.ib(default=None)
    extra_title: Optional[str] = attr.ib(default=None)
    topic: Optional[str] = attr.ib(default=None)

    @property
    def grade(self) -> Optional[int]:
        if 'класс' in self.extra_title:
            return int(self.extra_title.split(' ', 2)[0].strip())

        return None


def get_videos() -> List[Material]:
    return []


def get_materials() -> List[Material]:
    return []
