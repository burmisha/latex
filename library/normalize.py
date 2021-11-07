import library.location

import re
import textwrap

import logging
log = logging.getLogger(__name__)


class TitleCanonizer:
    def __init__(self, replacements=None):
        if replacements is None:
            log.debug('Using default replacements')
            replacements = [
                (r'^Физика[\.:] ', ''),
                (r' Центр онлайн-обучения «Фоксфорд»$', ''),
                (r'\.$', ''),
                (r' \(осн\)\.?', '.'),
                (r'^8 кл - ([0-9]{3})', r'Урок \1'),
                (r' \(осн, запись 2014 года\)\.', r'.'),
                (r' \| Видеоурок', r''),
                (r' \| ', r' и '),
                (r'\((\w+)\)', r'- \1 -'),
                (r'[\(\)"\?]', r''),
                (r'(\. )?[Чч](асть|\.)? *(\d)', r' - \3'),
                (r'Подготоcка к ЕГЭ по физике. Занятие', r' - '),
                (r'ВарІант', r'Вариант'),
                (r'Урок (\d+)\.', r'Урок \1 -'),
                (r'(\w) [Рр]ешение задач', r'\1 - решение задач'),
                (r'\. [Рр]ешение задач', r' - решение задач'),
                (r'[Фф]..... +(\d\d?) +класс *([:.-] *)?(\w)', r'\1 класс - \3'),
                (r':', r' - '),
                (r'  +', ' '),
                (r'ур-ни', r'уравнени'),
            ]

        self._Replacements = replacements

    def Canonize(self, title):
        canonized = str(title)
        for pattern, replacement in self._Replacements:
            canonized = re.sub(pattern, replacement, canonized)
        canonized = canonized.strip()
        return canonized


def test_title_canonizer():
    title_canonizer = TitleCanonizer()
    for src, canonic_dst in [
        ('Физика 10 класс  : Второй', '10 класс - Второй'),
        ('Физика 10 класс - Прямолинейное', '10 класс - Прямолинейное'),
        ('Физика 10 класс - Прямолинейное равноускоренное движение', '10 класс - Прямолинейное равноускоренное движение'),
        ('Физика 10  класс : Прямолинейное', '10 класс - Прямолинейное'),
        ('Физика 9 класс Закон', '9 класс - Закон'),
        ('частиц (часть 1)', 'частиц - 1'),
        ('импульса ч.2', 'импульса - 2'),
        ('Закон. Решение задач', 'Закон - решение задач'),
        ('распад Решение задач', 'распад - решение задач'),
    ]:
        dst = title_canonizer.Canonize(src)
        assert dst == canonic_dst, f'Expected {canonic_dst!r}, got {dst!r} from {src!r}'


test_title_canonizer()
