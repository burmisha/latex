import attr
from enum import Enum
from typing import List, Optional


class SourceFormat(str, Enum):
    Video = 'video'
    Text = 'text'


@attr.s
class Material:
    title: str = attr.ib()
    url: str = attr.ib()
    source_format: str = attr.ib()
    extra_title: Optional[str] = attr.ib(default=None)


def get_videos() -> List[Material]:
    return []


def get_materials() -> List[Material]:
    return []
