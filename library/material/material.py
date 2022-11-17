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


def get_videos() -> List[Material]:
    return []


def get_materials() -> List[Material]:
    return []
