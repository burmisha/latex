import attr
from enum import Enum
from typing import List


class SourceFormat(str, Enum):
    Video = 'video'
    Text = 'text'



@attr.s
class Material:
    source_format: str = attr.ib()
    raw_title: str = attr.ib()
    url: str = attr.ib()


def get_videos() -> List[Material]:
    return []


def get_materials() -> List[Material]:
    return []
