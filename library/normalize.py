import library.location
from library.util.asserts import assert_equals


import re
import textwrap

import logging
log = logging.getLogger(__name__)


class TitleCanonizer:
    def __init__(self, replacements=None):
        self._regex_replacements = [
            (r'^Физика[\.:] +', ''),
            (r' Центр онлайн-обучения «Фоксфорд»$', ''),
            (r'\.$', ''),
            (r' -$', ''),
            (r' \(осн\)\.?', '.'),
            (r'^8 кл - ([0-9]{3})', r'Урок \1'),
            (r' \(осн, запись 2014 года\)\.', r'.'),
            (r' \| Видеоурок', r''),
            (r' \| ', r' и '),
            (r'\((\w+)\)', r'- \1 -'),
            (r'[\(\)"\?]', r''),
            (r'(\. )?[Чч](асть|\.)? *(\d)', r' - \3'),
            # (r'Подгото.ка к ЕГЭ по физике. Занятие', r' - '),
            (r'ВарІант', r'Вариант'),
            (r'Урок (\d+)\.', r'Урок \1 -'),
            (r'(\w) [Рр]ешение задач', r'\1 - решение задач'),
            (r'\. [Рр]ешение задач', r' - решение задач'),
            (r'[Фф]..... +(\d\d?) +класс *([:.-] *)?(\w)', r'\1 класс - \3'),
            (r':', r' - '),
            (r'  +', ' '),
            (r'ур-ни', r'уравнени'),
            (r'Центр онлайн-обучения «Фоксфорд»', ''),
            (r'[\?@\*№«»\\\[\]\(\)#\$%\^&"…!]', ''),
            (r'[–—]', '-'),
            (r' +', ' '),
            (r'\.+', '.'),
            (r' amp; ', ' and '),
            (r' - ?$', ''),
        ]

        self._replacements = [
            ('@Продолжение следует', ''),
            ('18+', ''),
            (': ', ' - '),
            ('/', ' ',),
            (' .', '.'),
            ('- -', '-'),
        ]


    def Canonize(self, title):
        canonized = str(title).strip()

        for pattern, replacement in self._replacements:
            canonized = canonized.replace(pattern, replacement)
            canonized = canonized.strip()

        for pattern, replacement in self._regex_replacements:
            canonized = re.sub(pattern, replacement, canonized)
            canonized = canonized.strip()

        return canonized.strip('.').strip()


def test_title_canonizer():
    data = [
        ('Физика 10 класс  : Второй', '10 класс - Второй'),
        ('Физика 10 класс - Прямолинейное', '10 класс - Прямолинейное'),
        ('Физика 10 класс - Прямолинейное равноускоренное движение', '10 класс - Прямолинейное равноускоренное движение'),
        ('Физика 10  класс : Прямолинейное', '10 класс - Прямолинейное'),
        ('Физика 9 класс Закон', '9 класс - Закон'),
        ('частиц (часть 1)', 'частиц - 1'),
        ('импульса ч.2', 'импульса - 2'),
        ('Закон. Решение задач', 'Закон - решение задач'),
        ('распад Решение задач', 'распад - решение задач'),
        ('ФИЗИКА 10 класс: Бросок под углом горизонта | Видеоурок', '10 класс - Бросок под углом горизонта'),
        ('123][/")(\\', '123'),
        ('1?@*№«»\\[]()#$%^&', '1'),
        ('Урок 351. Электромагнитная индукция (повторение)', 'Урок 351 - Электромагнитная индукция - повторение'),
    ]
    title_canonizer = TitleCanonizer()
    for src, canonic_dst in data:
        assert_equals('Broken canonizer', canonic_dst, title_canonizer.Canonize(src))


test_title_canonizer()


def format_plain_text(text: str, fill=False) -> str:
    r = text.replace('-\n', '').replace('.\n', '. ').replace(' -\n', ' - ')
    r = re.sub(r'(\w)\n(\w)', r'\1 \2', r)
    r = r.replace('\n \n', '\n\n')
    r = re.sub(r' (\w)\) ', r'\n     \1) ', r)
    r = re.sub(r'^(\w)\) ', r'    \1) ', r)
    r = re.sub(r',\n+', r', ', r)
    r = re.sub(r'\n\n+', r'\n', r)
    if fill:
        return textwrap.fill(
            r,
            width=120,
            expand_tabs=True,
            replace_whitespace=False,
            break_long_words=False,
            drop_whitespace=True,
            break_on_hyphens=False,
            tabsize=4,
        )
    else:
        return r


def test_format_plain_text():
    data = [
        ('a-\nb', 'ab'),
        ('a-\nb\n\nc', 'ab\nc'),
        ('''2. Металлический стержень мас-
сой т и длиной Г подвешен горизон-
тально на двух лёгких проводах дли-
ной [ каждый (рис. 4.2). Стержень на-
ходится в однородном магнитном поле,
индукция В которого направлена вер-
тикально вниз.''', '''2. Металлический стержень массой т и длиной Г подвешен горизонтально на двух лёгких проводах длиной [ каждый (рис. 4.2).
Стержень находится в однородном магнитном поле, индукция В которого направлена вертикально вниз.'''
        ),
        ('''23. Протон влетает в однородное магнитное поле с индук-
цией 0,3 Тл и движется по дуге окружности радиусом 5 см.
Затем протон влетает в однородное электрическое поле и
движется против вектора напряжённости поля.''', '''23. Протон влетает в однородное магнитное поле с индукцией 0,3 Тл и движется по дуге окружности радиусом 5 см. Затем
протон влетает в однородное электрическое поле и движется против вектора напряжённости поля.'''
        ),
        ('''18. Пройдя ускоряющую разность потенциалов 4 кВ, элек-
трон влетает в однородное магнитное поле с индукцией 40 мТл.
Скорость электрона перпендикулярна вектору магнитной ин-
дукции. По окружности какого радиуса движется электрон?''', '''18. Пройдя ускоряющую разность потенциалов 4 кВ, электрон влетает в однородное магнитное поле с индукцией 40 мТл.
Скорость электрона перпендикулярна вектору магнитной индукции. По окружности какого радиуса движется электрон?'''
        ),
    ]
    for text, canonic in data:
        result = format_plain_text(text, fill=True)
        assert result == canonic, f'Expected\n{canonic!r}\ngot\n{result!r}:\n\n{canonic}\n\n{result}'


test_format_plain_text()
