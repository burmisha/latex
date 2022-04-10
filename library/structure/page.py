from library.util.asserts import assert_equals
import attr

from typing import List, Union

import logging
log = logging.getLogger(__name__)


@attr.s
class DestinationPage:
    index: int = attr.ib()
    dst_dir: str = attr.ib()
    name_template: str = attr.ib()


class PagesRange:
    def __init__(self, str_range: Union[int, str]):
        pages_range = str(str_range).strip()
        if '-' in pages_range:
            first_page, last_page = pages_range.split('-')
        elif '+' in pages_range:
            first_page, more_pages = pages_range.split('+')
            last_page = int(first_page) + int(more_pages)
        else:
            first_page, last_page = pages_range, pages_range
        self.first_index = int(first_page)
        self.last_index = int(last_page)
        assert self.first_index <= self.last_index

    @property
    def pages_indicies(self) -> List[int]:
        return list(range(self.first_index, self.last_index + 1))


def test_pages_range():
    data = [
        (1, [1]),
        ('1', [1]),
        ('1+2', [1, 2, 3]),
        ('1-3', [1, 2, 3]),
    ]
    for pages_range_str, canonic in data:
        pages_range = PagesRange(pages_range_str)
        assert_equals('pages_indicies', canonic, pages_range.pages_indicies)


test_pages_range()
