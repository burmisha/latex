from library.structure.page import DestinationPage
from library.util.asserts import assert_equals


def _get_indices(indices):
    if indices is None:
        first_level_index = 1
        second_level_index = 1
    else:
        first_level_index, second_level_index = indices

    if first_level_index is None:
        first_level_index = 1
    if second_level_index is None:
        second_level_index = 1

    return first_level_index, second_level_index


def was_indexed(items):
    return all(item[0][0].isdigit() for item in items)


def _get_pages(first_page, last_page, dst_dir, name_template):
    for page_index in range(first_page, last_page + 1):
        yield DestinationPage(
            index=page_index,
            dst_dir=dst_dir,
            name_template=name_template,
        )


def parse_simple_structure(data, *, indices=None, plain=None):
    assert isinstance(data, list)
    first_level_start_index, second_level_start_index = _get_indices(indices)

    already_has_first_index = was_indexed(data)
    if len(data) == 1:
        plain = True

    for first_level_index, first_level_item in enumerate(data, first_level_start_index):
        assert isinstance(first_level_item, (tuple, list)), f'{first_level_item!r} is not tuple'

        if already_has_first_index:
            name_template = f'{first_level_item[0]}'
        else:
            name_template = f'{first_level_index:02} {first_level_item[0]}'

        if plain:
            dst_dir = None
        else:
            dst_dir = name_template

        if len(first_level_item) == 3:
            _, first_page, last_page = first_level_item
            for page in _get_pages(first_page, last_page, dst_dir, name_template):
                yield page

        elif len(first_level_item) == 2:
            second_level_items = first_level_item[1]
            already_has_second_index = was_indexed(second_level_items)

            for second_level_index, second_level_item in enumerate(first_level_item[1], second_level_start_index):
                assert isinstance(second_level_item, (tuple, list)), f'{second_level_item!r} is not tuple'
                assert len(second_level_item) == 3
                second_level_name, first_page, last_page = second_level_item

                if already_has_second_index:
                    second_level_template = second_level_name
                else:
                    second_level_template = f'{second_level_index:02} {second_level_name}'

                for page in _get_pages(first_page, last_page, name_template, second_level_template):
                    yield page

        else:
            raise RuntimeError(f'Structure is not supported: {first_level_item}')


class Structure:
    def __init__(self, data, indices=None, plain=None):
        self._data = data
        self._indices = indices
        self._plain = plain

    def get_pages(self):
        for page in parse_simple_structure(self._data, indices=self._indices, plain=self._plain):
            yield page


def test_parse_simple_structure():
    data = [
        (
            Structure([('Раздел', 1, 1)]),
            [DestinationPage(1, None, '01 Раздел')],
        ),
        (
            Structure([('Раздел', 1, 3)]),
            [
                DestinationPage(1, None, '01 Раздел'),
                DestinationPage(2, None, '01 Раздел'),
                DestinationPage(3, None, '01 Раздел'),
            ],
        ),
        (
            Structure([('Кинематика', 2, 3), ('Динамика', 3, 3)]),
            [DestinationPage(2, '01 Кинематика', '01 Кинематика'), DestinationPage(3, '01 Кинематика', '01 Кинематика'), DestinationPage(3, '02 Динамика', '02 Динамика')],
        ),
        (
            Structure([
                ('А', [('Б', 1, 2)]),
            ]),
            [
                DestinationPage(1, '01 А', '01 Б'),
                DestinationPage(2, '01 А', '01 Б'),
            ],
        ),
        (
            Structure([
                ('А', [('Б', 1, 2), ('В', 2, 2)]),
                ('Ф', [('Д', 3, 3), ('Г', 4, 4)]),
            ]),
            [
                DestinationPage(1, '01 А', '01 Б'),
                DestinationPage(2, '01 А', '01 Б'),
                DestinationPage(2, '01 А', '02 В'),
                DestinationPage(3, '02 Ф', '01 Д'),
                DestinationPage(4, '02 Ф', '02 Г'),
            ],
        ),
        (
            Structure([
                ('А', [('3 Б', 1, 2), ('4 В', 2, 2)]),
                ('Ф', [('Д', 3, 3), ('Г', 4, 4)]),
            ]),
            [
                DestinationPage(1, '01 А', '3 Б'),
                DestinationPage(2, '01 А', '3 Б'),
                DestinationPage(2, '01 А', '4 В'),
                DestinationPage(3, '02 Ф', '01 Д'),
                DestinationPage(4, '02 Ф', '02 Г'),
            ],
        ),
    ]
    for structure, canonic in data:
        result = list(structure.get_pages())
        assert_equals('Broken structure', canonic, result)


test_parse_simple_structure()


def test_structures():
    data = [
        (
            Structure([('Раздел', 1, 3)]),
            [DestinationPage(1, None, '01 Раздел'), DestinationPage(2, None, '01 Раздел'), DestinationPage(3, None, '01 Раздел')],
        ),
        (
            Structure([('Кинематика', 2, 3), ('Динамика', 3, 3)]),
            [DestinationPage(2, '01 Кинематика', '01 Кинематика'), DestinationPage(3, '01 Кинематика', '01 Кинематика'), DestinationPage(3, '02 Динамика', '02 Динамика')],
        ),
        (
            Structure([
                ('А', [('Б', 1, 2), ('В', 2, 2)]),
                ('Ф', [('Д', 3, 3), ('Г', 4, 4)]),
            ]),
            [
                DestinationPage(1, '01 А', '01 Б'),
                DestinationPage(2, '01 А', '01 Б'),
                DestinationPage(2, '01 А', '02 В'),
                DestinationPage(3, '02 Ф', '01 Д'),
                DestinationPage(4, '02 Ф', '02 Г'),
            ],
        ),
        (
            Structure([
                ('А', [('3 Б', 1, 2), ('4 В', 2, 2)]),
                ('Ф', [('Д', 3, 3), ('Г', 4, 4)]),
            ]),
            [
                DestinationPage(1, '01 А', '3 Б'),
                DestinationPage(2, '01 А', '3 Б'),
                DestinationPage(2, '01 А', '4 В'),
                DestinationPage(3, '02 Ф', '01 Д'),
                DestinationPage(4, '02 Ф', '02 Г'),
            ],
        ),
    ]
    for structure, canonic in data:
        result = list(structure.get_pages())
        assert result == canonic, f'Broken structure:\nexpected:\t{canonic}\ngot:\t\t{result}'


test_structures()
