import library.location
import library.process
import library.files

from library.convert.pdf_to_jpeg import (
    PdfBook,
    disable_trim,
    page_shift,
    params,
    source_link,
    structure,
    ppi,
)

from library.structure.structure import Structure

import logging
log = logging.getLogger(__name__)

books_cfg = library.files.load_yaml_data('books.yaml')

@page_shift(lambda self, pageNumber: -2 if pageNumber < 110 else -3)
@structure(books_cfg['ComicsBook']['structure'])
class ComicsBook(PdfBook):
    pass


@params(books_cfg['ChernoutsanBook']['params'])
@structure(
    books_cfg['ChernoutsanBook']['structure'],
    indices=books_cfg['ChernoutsanBook']['indices']
)
class ChernoutsanBook(PdfBook):
    pass


@page_shift(books_cfg['Maron_9_Sbornik']['page_shift'])
@params(books_cfg['Maron_9_Sbornik']['params'])
@structure(books_cfg['Maron_9_Sbornik']['structure'])
class Maron_9_Sbornik(PdfBook):
    pass


@page_shift(books_cfg['Maron_8_Sbornik']['page_shift'])
@params(books_cfg['Maron_8_Sbornik']['params'])
@structure(books_cfg['Maron_8_Sbornik']['structure'])
class Maron_8_Sbornik(PdfBook):
    pass


@page_shift(books_cfg['Maron_8_SR_KR']['page_shift'])
@params(books_cfg['Maron_8_SR_KR']['params'])
@structure(books_cfg['Maron_8_SR_KR']['structure'])
class Maron_8_SR_KR(PdfBook):
    pass


@page_shift(books_cfg['Maron_9_SR_KR']['page_shift'])
@params(books_cfg['Maron_9_SR_KR']['params'])
@structure(books_cfg['Maron_9_SR_KR']['structure'])
class Maron_9_SR_KR(PdfBook):
    pass


@page_shift(books_cfg['Maron_9_Didaktika']['page_shift'])
@params(books_cfg['Maron_9_Didaktika']['params'])
@structure(books_cfg['Maron_9_Didaktika']['structure'])
class Maron_9_Didaktika(PdfBook):
    pass


@page_shift(books_cfg['Maron_8_Didaktika']['page_shift'])
@params(books_cfg['Maron_8_Didaktika']['params'])
@structure(books_cfg['Maron_8_Didaktika']['structure'])
class Maron_8_Didaktika(PdfBook):
    pass


@page_shift(books_cfg['Kirik_8']['page_shift'])
@source_link(books_cfg['Kirik_8']['source_link'])
@params(books_cfg['Kirik_8']['params'])
@structure(books_cfg['Kirik_8']['structure'])
class Kirik_8(PdfBook):
    pass


@page_shift(books_cfg['Kirik_9']['page_shift'])
@source_link(books_cfg['Kirik_9']['source_link'])
@params(books_cfg['Kirik_9']['params'])
@structure(books_cfg['Kirik_9']['structure'])
class Kirik_9(PdfBook):
    pass


@page_shift(books_cfg['Gendenshteyn_8']['page_shift'])
@source_link(books_cfg['Gendenshteyn_8']['source_link'])
@params(books_cfg['Gendenshteyn_8']['params'])
@structure(books_cfg['Gendenshteyn_8']['structure'])
class Gendenshteyn_8(PdfBook):
    pass


@page_shift(books_cfg['Gendenshteyn_10']['page_shift'])
@source_link(books_cfg['Gendenshteyn_10']['source_link'])
@params(books_cfg['Gendenshteyn_10']['params'])
@structure(books_cfg['Gendenshteyn_10']['structure'])
class Gendenshteyn_10(PdfBook):
    pass


@page_shift(books_cfg['Gendenshteyn_11']['page_shift'])
@source_link(books_cfg['Gendenshteyn_11']['source_link'])
@params(books_cfg['Gendenshteyn_11']['params'])
@structure(books_cfg['Gendenshteyn_11']['structure'])
class Gendenshteyn_11(PdfBook):
    pass


@page_shift(books_cfg['Gendenshteyn_9']['page_shift'])
@source_link(books_cfg['Gendenshteyn_9']['source_link'])
@params(books_cfg['Gendenshteyn_9']['params'])
@structure(books_cfg['Gendenshteyn_9']['structure'])
class Gendenshteyn_9(PdfBook):
    pass


@params(books_cfg['Gorbushin']['params'])
@structure(books_cfg['Gorbushin']['structure'])
class Gorbushin(PdfBook):
    pass


@params(books_cfg['Gelfgat_11']['params'])
@structure(books_cfg['Gelfgat_11']['structure'])
class Gelfgat_11(PdfBook):
    pass

@page_shift(books_cfg['Vishnyakova']['page_shift'])
@structure(books_cfg['Vishnyakova']['structure'])
class Vishnyakova(PdfBook):
    pass


@structure(books_cfg['Baumansky2000']['structure'])
class Baumansky2000(PdfBook):
    pass


@page_shift(books_cfg['Goldfarb']['page_shift'])
@structure(books_cfg['Goldfarb']['structure'])
class Goldfarb(PdfBook):
    pass


@page_shift(books_cfg['Belolipetsky']['page_shift'])
@structure(books_cfg['Belolipetsky']['structure'])
class Belolipetsky(PdfBook):
    pass


@page_shift(books_cfg['Rymkevich']['page_shift'])
@structure(books_cfg['Rymkevich']['structure'])
class Rymkevich(PdfBook):
    pass


@page_shift(books_cfg['Bendrikov']['page_shift'])
@ppi(books_cfg['Bendrikov']['ppi'])
@structure(books_cfg['Bendrikov']['structure'])
class Bendrikov(PdfBook):
    pass


@params(books_cfg['Problems_3800']['params'])
@source_link(books_cfg['Problems_3800']['source_link'])
@structure(books_cfg['Problems_3800']['structure'])
class Problems_3800(PdfBook):
    pass


@page_shift(books_cfg['Maron_11_Conspects']['page_shift'])
@structure(books_cfg['Maron_11_Conspects']['structure'])
class Maron_11_Conspects(PdfBook):
    pass


@ppi(books_cfg['ZFTSH']['ppi'])
class ZFTSH(PdfBook):
    pass


@ppi(books_cfg['Mathus_mechanics']['ppi'])
@structure(books_cfg['Mathus_mechanics']['structure'])
class Mathus_mechanics(PdfBook):
    pass


@ppi(books_cfg['Mathus_termodynamics']['ppi'])
@structure(books_cfg['Mathus_termodynamics']['structure'])
class Mathus_termodynamics(PdfBook):
    pass


@ppi(books_cfg['Mathus_quantum']['ppi'])
@structure(books_cfg['Mathus_quantum']['structure'])
class Mathus_quantum(PdfBook):
    pass


@ppi(books_cfg['Mathus_electricity']['ppi'])
@structure(books_cfg['Mathus_electricity']['structure'])
class Mathus_electricity(PdfBook):
    pass


@ppi(books_cfg['Mathus_wave_optics']['ppi'])
@structure(books_cfg['Mathus_wave_optics']['structure'])
class Mathus_wave_optics(PdfBook):
    pass


@ppi(books_cfg['Mathus_geom_optics']['ppi'])
@structure(books_cfg['Mathus_geom_optics']['structure'])
class Mathus_geom_optics(PdfBook):
    pass


@ppi(books_cfg['Mathus_relativity']['ppi'])
@structure(books_cfg['Mathus_relativity']['structure'])
class Mathus_relativity(PdfBook):
    pass


@ppi(250)
@structure([('Кодификатор', 1, 8)])
class FIPI_kodificator(PdfBook):
    pass


@ppi(250)
@structure([('Справочные материалы', 2, 3)])
class FIPI_demo(PdfBook):
    pass


@ppi(200)
@structure([('Статград - ЕГЭ', 1, 39)])
class Statgrad39(PdfBook):
    pass


@ppi(200)
@structure([('Статград - ЕГЭ', 1, 34)])
class Statgrad34(PdfBook):
    pass


@ppi(300)
@structure([('Бланки - ЕГЭ', 1, 9)])
class BlankiEge(PdfBook):
    pass


@ppi(300)
@structure([('Кодификатор - карточки', 1, 35)])
@disable_trim()
class KodificatorCards(PdfBook):
    pass


def get_dst_path(*pdf_path):
    return library.location.no_sync('Книги - физика - картинки', *pdf_path)


def locate_file(location, filename):
    regexp = f'{filename}.pdf'
    located = []
    for file in library.files.walkFiles(location, extensions=['pdf']):
        if filename in file:
            located.append(file)
    assert len(located) == 1, f'{location!r}, {regexp!r} -> {located}'
    return located[0]


def get_basic_books():
    books_config = [
        (ComicsBook, 'Физика в комиксах'),
        (ChernoutsanBook, 'Сборник - Черноуцан - 2011'),
        (Maron_9_Sbornik, '9 - Марон - Сборник вопросов и задач - 2019'),
        (Maron_8_Sbornik, '8 - Марон - Сборник вопросов и задач - 2019'),
        (Maron_8_SR_KR, '8 - Марон - СР и КР - 2017'),
        (Maron_9_SR_KR, '9 - Марон - СР и КР - 2018'),
        (Maron_9_Didaktika, '9 - Марон - Дидактические материалы - 2014'),
        (Maron_8_Didaktika, '8 - Марон - Дидактические материалы - 2013'),
        (Kirik_8, '8 - Кирик - СР и КР - 2014'),
        (Kirik_9, '9 - Кирик - СР и КР - 2016'),
        (Gendenshteyn_8, '8 - Генденштейн - 2012'),
        (Gendenshteyn_9, '9 - Генденштейн - 2012'),
        (Gendenshteyn_10, '10 - Генденштейн - Задачник - 2014'),
        (Gendenshteyn_11, '11 - Генденштейн - Задачник - 2014'),
        (Gelfgat_11, '11 - Гельфгат - Задачник - 2004'),
        (Gorbushin, 'Горбушин - Как можно учить физике'),
        (Goldfarb, '10-11 - Гольдфарб - Сборник'),
        (Vishnyakova, 'Вишнякова - Физика - сборник задач к ЕГЭ - 2015'),
        (Baumansky2000, 'Бауманский - 2000 - Васюков - Сборник для поступающих'),
        (Belolipetsky, 'Сборник - Белолипецкий - Задачник с лягушками'),
        (Rymkevich, '9-11 - Рымкевич - Сборник'),
        (Problems_3800, '3800 задач по физике'),
        (Bendrikov, 'Бендриков - Лебедь рак и щука - 2010'),
        (Maron_11_Conspects, '11 - Марон - ОпКонспект - 2013'),
    ]
    for book_class, pdfPath in books_config:
        yield book_class(
            pdfPath=locate_file(library.location.udr('Книги - физика'), pdfPath),
            dstPath=get_dst_path(pdfPath),
        )


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
        book_class = ZFTSH(
            pdfPath=locate_file(library.location.udr('Материалы - ЗФТШ', 'ЗФТШ-2013'), file_name),
            dstPath=get_dst_path('ЗФТШ', file_name),
        )
        structure = Structure(
            [
                ('Вступление', parts[0][0], parts[0][1]),
                ('Теория', parts[1][0], parts[1][1]),
                ('Задачи', parts[2][0], parts[2][1]),
            ],
            plain=True,
        )
        book_class.set_structure(structure)
        yield book_class


def get_mathus_books():
    mathus_config = [
        (Mathus_mechanics, '9 - Механика - пособие'),
        (Mathus_termodynamics, '10 - Термодинамика - пособие'),
        (Mathus_electricity, '10 - Электродинамика - пособие'),
        (Mathus_wave_optics, '11 - Волновая оптика - пособие'),
        (Mathus_quantum, '11 - Квантовая физика - пособие'),
        (Mathus_geom_optics, '11 - Геометрическая оптика - пособие'),
        (Mathus_relativity, '11 - Теория относительности - пособие'),
    ]
    for book_class, file_name in mathus_config:
        yield book_class(
            pdfPath=locate_file(library.location.udr('Материалы - mathus'), file_name),
            dstPath=get_dst_path(f'Mathus - {file_name}'),
        )


def get_ege_books():
    yield FIPI_kodificator(
        pdfPath=library.location.udr('11 ЕГЭ', 'ФИПИ 2019', 'ФИ_КОДИФ 2019.pdf'),
        dstPath=get_dst_path('11 - ЕГЭ', 'Кодификатор ФИПИ 2019'),
    )
    yield FIPI_kodificator(
        pdfPath=library.location.udr('11 ЕГЭ', 'ФИПИ 2021', 'ФИ-11 ЕГЭ 2021 КОДИФ.pdf'),
        dstPath=get_dst_path('11 - ЕГЭ', 'Кодификатор ФИПИ 2021'),
    )
    yield FIPI_demo(
        pdfPath=library.location.udr('11 ЕГЭ', 'ФИПИ 2021', 'ФИ-11 ЕГЭ 2021 ДЕМО.pdf'),
        dstPath=get_dst_path('11 - ЕГЭ', 'Демовариант 2021'),
    )
    yield Statgrad39(
        pdfPath=library.location.udr('11 ЕГЭ', 'Статград', '2021 Статград ЕГЭ-5', 'Zadanie_FI11_17052021.pdf'),
        dstPath=get_dst_path('11 - ЕГЭ', 'Статград 2021-05-17'),
    )
    yield Statgrad34(
        pdfPath=library.location.udr('11 ЕГЭ', 'Статград', '2022 Статград ЕГЭ-2', 'Zadanie_FI11_20122021.pdf'),
        dstPath=get_dst_path('11 - ЕГЭ', 'Статград 2021-12-20'),
    )
    yield BlankiEge(
        pdfPath=library.location.udr('11 ЕГЭ', 'blanki-ege-2020-all.pdf'),
        dstPath=get_dst_path('11 - ЕГЭ', 'Бланки'),
    )
    yield KodificatorCards(
        pdfPath=library.location.udr('11 ЕГЭ', '11 Кодификатор.pdf'),
        dstPath=get_dst_path('11 - ЕГЭ', 'Кодификатор - карточки'),
    )


def get_all_books():
    books_funcs = [
        get_basic_books,
        get_zftsh_books,
        get_mathus_books,
        get_ege_books,
    ]

    for books_func in books_funcs:
        for book in books_func():
            yield book
