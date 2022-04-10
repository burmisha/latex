import library.location
import library.files

from library.convert.pdf_to_jpeg import BookConfig
from library.structure.structure import Structure


BOOKS_CFG = library.files.load_yaml_data('books.yaml')

MATHUS_PREFIX = 'Mathus'
MATHUS_PPI = 250
ZFTSH_PPI = 250

def get_dst_path(*pdf_path):
    return library.location.no_sync('Книги - физика - картинки', *pdf_path)


def locate_file(location, filename):
    located = []
    for file in library.files.walkFiles(location, extensions=['pdf']):
        if filename in file:
            located.append(file)
    assert len(located) == 1, f'{location!r}, {filename!r} -> {located}'
    return located[0]


def get_basic_books():
    for key, params in BOOKS_CFG.items():
        if key.startswith(MATHUS_PREFIX):
            yield BookConfig(
                pdf_file=locate_file(library.location.udr('Материалы - mathus'), params['pdf_file']),
                dst_dir=get_dst_path(f'Mathus - {params["pdf_file"]}'),
                structure=Structure(params['structure']),
                ppi=MATHUS_PPI,
            )
        else:
            if key == 'ComicsBook':
                params['page_shift'] = lambda page_index: -2 if page_index < 110 else -3
            params['structure'] = Structure(params['structure'], indices=params.get('indices', None))
            if 'indices' in params:
                del params['indices']

            pdf_file = params['pdf_file']
            if isinstance(pdf_file, list):
                assert isinstance(params['dst_dir'], list)
                params['pdf_file'] = library.location.udr(*pdf_file)
                params['dst_dir'] = get_dst_path(*params['dst_dir'])
            else:
                assert isinstance(pdf_file, str)
                params['pdf_file'] = locate_file(library.location.udr('Книги - физика'), pdf_file)
                params['dst_dir'] = get_dst_path(pdf_file)

            yield BookConfig(**params)


def get_zftsh_books():
    zftsh_config = [
        ([(1, 2), (3, 14), (14, 16)], 'Физика 8 - 1 - Гидростатика и аэростатика'),
        ([(1, 2), (3, 19), (19, 20)], 'Физика 8 - 2 - Тепловые явления'),
        ([(1, 2), (3, 24), (24, 28)], 'Физика 8 - 3 - Электрические явления'),
        ([(1, 2), (3, 20), (20, 23)], 'Физика 8 - 4 - Законы отражения и преломления'),
        ([(1, 2), (3, 16), (16, 20)], 'Физика 8 - 5 - Тонкие линзы'),
        ([(1, 2), (3, 27), (27, 28)], 'Физика 9 - 1 - Векторы в физике'),
        ([(1, 2), (3, 26), (26, 28)], 'Физика 9 - 2 - Кинематика'),
        ([(1, 2), (3, 25), (25, 28)], 'Физика 9 - 3 - Динамика'),
        ([(1, 2), (3, 26), (26, 28)], 'Физика 9 - 4 - Статика'),
        ([(1, 2), (3, 23), (23, 26)], 'Физика 9 - 5 - Работа и энергия'),
        ([(1, 2), (3, 21), (21, 24)], 'Физика 9 - 6 - Движение по окружности'),
        ([(1, 2), (3, 24), (24, 28)], 'Физика 10 - 1 - Импульс, сохранение, изменение'),
        ([(1, 2), (3, 26), (26, 28)], 'Физика 10 - 2 - МКТ, идеальный газ'),
        ([(1, 2), (3, 22), (22, 25)], 'Физика 10 - 3 - Сохранение энергии, тепловые процессы'),
        ([(1, 2), (3, 30), (30, 32)], 'Физика 10 - 4 - Электростатика'),
        ([(1, 1), (2, 15), (16, 16)], 'Физика 10 - 5 - Постоянный ток'),
        ([(1, 2), (3, 14), (14, 16)], 'Физика 10 - 6 - Магнитное поле'),
        ([(1, 2), (3, 29), (29, 32)], 'Физика 11 - 1 - Основные законы механики'),
        ([(1, 2), (3, 25), (26, 28)], 'Физика 11 - 2 - Молекулярная физика и термодинамика'),
        ([(1, 2), (3, 29), (29, 32)], 'Физика 11 - 3 - Электростатика и законы постоянного тока'),
        ([(1, 2), (3, 29), (29, 32)], 'Физика 11 - 4 - Электромагнитная индукция и колебания'),
        ([(1, 2), (3, 27), (27, 30)], 'Физика 11 - 5 - Геометрическая оптика'),
        ([(1, 2), (3, 30), (30, 32)], 'Физика 11 - 6 - Физическая оптика и квантовая физика'),
    ]
    for parts, file_name in zftsh_config:
        structure = Structure(
            [
                ('Вступление', parts[0][0], parts[0][1]),
                ('Теория', parts[1][0], parts[1][1]),
                ('Задачи', parts[2][0], parts[2][1]),
            ],
            plain=True,
        )
        yield BookConfig(
            pdf_file=locate_file(library.location.udr('Материалы - ЗФТШ', 'ЗФТШ-2013'), file_name),
            dst_dir=get_dst_path('ЗФТШ', file_name),
            structure=structure,
            ppi=ZFTSH_PPI,
        )


def get_all_books():
    books_funcs = [
        get_basic_books,
        get_zftsh_books,
    ]

    for books_func in books_funcs:
        for book in books_func():
            yield book
