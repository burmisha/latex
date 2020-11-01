import library

import logging
log = logging.getLogger(__name__)



def run(args):
    checker = library.checker.Checker(
        library.location.udr('10 класс', '2020-21 10AБ Физика - Архив', '2020.10.30 10АБ - Тест по динамике - 4.csv.zip'),
        ['А', 'Б', 'А', 'В', 'А', 'В', 'А', 'А', 'Б', '25600', '6400', '8'],
    )



def populate_parser(parser):
    # parser.add_argument('--filter', help='Find forms containg this substring')
    parser.set_defaults(func=run)
