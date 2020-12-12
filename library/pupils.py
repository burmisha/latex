import Levenshtein


import collections
import re

import library.picker

import logging
log = logging.getLogger(__name__)

from library.logging import cm


class Pupil(object):
    def __init__(self, name=None, surname=None):
        self.Name = name
        self.Surname = surname

    def GetFullName(self, surnameFirst=False):
        if surnameFirst:
            parts = [self.Surname, self.Name]
        else:
            parts = [self.Name, self.Surname]
        return ' '.join(part for part in parts if part)

    def GetRandomSeedPart(self):
        return f'{self.Name} {self.Surname}'

    def __str__(self):
        return f'{self.Name} {self.Surname}'

    def __lt__(self, other):
        if self.Surname < other.Surname:
            return True
        elif self.Surname == other.Surname and self.Name < other.Name:
            return True
        else:
            return False


class NameLookup:
    def __init__(self, names_dict):
        assert names_dict
        for name in names_dict:
            assert name
        self._names = names_dict
        self._unique_names = {}

        counter = collections.Counter()
        for name, value in self._names.items():
            parts = sorted(self._split(name))
            parts += [
                ' '.join(parts),
                ' '.join(parts[::-1]),
            ]
            for part in parts:
                counter[part] += 1
                self._unique_names[part] = value

        for part, count in sorted(counter.items()):
            if count != 1:
                log.debug(f'{part} has {count} duplicates, will not use')
                del self._unique_names[part]
            else:
                log.debug(f'Using {part} → {self._unique_names[part]}')

    def _split(self, line):
        parts = re.split(r'\s|-|,|;|\.', line)
        return [p.strip() for p in parts if len(p) >= 2]

    def _distance(self, name_1, name_2):
        name_1_strip = name_1.strip().lower()
        name_2_strip = name_2.strip().lower()
        assert len(name_1_strip) >= 2
        assert len(name_2_strip) >= 2
        distance = Levenshtein.distance(name_1_strip, name_2_strip)
        return distance

    def Find(self, candidate_name):
        best_matches = set()
        best_match_distance = None
        for part in sorted(self._split(candidate_name)):
            for key, value in sorted(self._unique_names.items()):
                distance = self._distance(part, key)
                if best_match_distance is None or distance < best_match_distance:
                    best_matches = set([value])
                    best_match_distance = distance
                elif distance == best_match_distance:
                    best_matches.add(value)

        if best_match_distance is None or best_match_distance >= 2 or len(best_matches) != 1:
            log.warn(cm(f'Could not find name for {candidate_name}: best matches are {best_matches} is bad ({best_match_distance})', bg='red'))
            return None

        name = list(best_matches)[0]
        return name


class Pupils(object):
    def __init__(self, pupils_id=None, pupils=[], letter=None, grade=None, add_me=None, only_me=None, year=None):
        self._id = pupils_id
        self._pupils_list = pupils
        self._me = Pupil(name='Михаил', surname='Бурмистров')
        self.Letter = letter
        self.Grade = grade
        assert 2010 <= year < 2099
        self.Year = f'{year}-{year-2000+1}'
        self._add_me = add_me
        self._only_me = only_me
        assert isinstance(self.Grade, int)
        assert 6 <= self.Grade <= 11
        self.LatinLetter = {
            'А1': 'A1',
            'А': 'A',
            'Т': 'T',
            'Л': 'L',
            'М': 'M',
            'АБ': 'AB',
        }[self.Letter]
        self._name_lookup = NameLookup(dict([
            (pupil.GetFullName(), pupil)
            for pupil in self.Iterate()
        ]))

    def Iterate(self, add_me=False, only_me=False):
        me = ['Михаил Бурмистров']
        if self._add_me or add_me:
            yield self._me
        if self._only_me is None or not only_me:
            for pupil in self._pupils_list:
                yield pupil

    def FindByName(self, name):
        pupil = self._name_lookup.Find(name)
        if pupil is None:
            if ' ' in name:
                new_name, new_surname = name.split(' ', 1)
            else:
                new_name, new_surname = name, ''
            return Pupil(name=new_name, surname=new_surname)
        return pupil

    def GetRandomSeedPart(self):
        return '{}-{}'.format(self.Grade, self.Letter)


classes_config = {
    'Гагик Аракелян':           ['2018-10-Т',   '2019-11-Т',                ],
    'Ирен Аракелян':            ['2018-10-Т',   '2019-11-Т',    '2019-11S-Т'],
    'Сабина Асадуллаева':       ['2018-10-Т',   '2019-11-Т',                ],
    'Вероника Битерякова':      ['2018-10-Т',   '2019-11-Т',                ],
    'Юлия Буянова':             ['2018-10-Т',   '2019-11-Т',    '2019-11S-Т'],
    'Пелагея Вдовина':          ['2018-10-Т',   '2019-11-Т',                ],
    'Леонид Викторов':          ['2018-10-Т',   '2019-11-Т',    '2019-11S-Т'],
    'Фёдор Гнутов':             ['2018-10-Т',   '2019-11-Т',    '2019-11S-Т'],
    'Илья Гримберг':            ['2018-10-Т',   '2019-11-Т',                ],
    'Иван Гурьянов':            ['2018-10-Т',   '2019-11-Т',                ],
    'Артём Денежкин':           ['2018-10-Т',   '2019-11-Т',                ],
    'Виктор Жилин':             ['2018-10-Т',   '2019-11-Т',    '2019-11S-Т'],
    'Дмитрий Иванов':           ['2018-10-Т',   '2019-11-Т',    '2019-11S-Т'],
    'Олег Климов':              ['2018-10-Т',   '2019-11-Т',    '2019-11S-Т'],
    'Анна Ковалева':            ['2018-10-Т',   '2019-11-Т',                ],
    'Глеб Ковылин':             ['2018-10-Т',   '2019-11-Т',                ],
    'Даниил Космынин':          ['2018-10-Т',   '2019-11-Т',                ],
    'Алина Леоничева':          ['2018-10-Т',   '2019-11-Т',    '2019-11S-Т'],
    'Ирина Лин':                ['2018-10-Т',   '2019-11-Т',    '2019-11S-Т'],
    'Олег Мальцев':             ['2018-10-Т'                                ],
    'Ислам Мунаев':             ['2018-10-Т',   '2019-11-Т',                ],
    'Александр Наумов':         ['2018-10-Т',   '2019-11-Т',    '2019-11S-Т'],
    'Георгий Новиков':          ['2018-10-Т',   '2019-11-Т',    '2019-11S-Т'],
    'Егор Осипов':              ['2018-10-Т',   '2019-11-Т',    '2019-11S-Т'],
    'Руслан Перепелица':        ['2018-10-Т',   '2019-11-Т',    '2019-11S-Т'],
    'Михаил Перин':             ['2018-10-Т',   '2019-11-Т',                ],
    'Егор Подуровский':         ['2018-10-Т',   '2019-11-Т',    '2019-11S-Т'],
    'Роман Прибылов':           ['2018-10-Т',   '2019-11-Т',                ],
    'Александр Селехметьев':    ['2018-10-Т',   '2019-11-Т',    '2019-11S-Т'],
    'Алексей Тихонов':          ['2018-10-Т',   '2019-11-Т',                ],
    'Алина Филиппова':          ['2018-10-Т',   '2019-11-Т',    '2019-11S-Т'],
    'Дарья Шашкова':            [               '2019-11-Т',                ],
    'Алина Яшина':              ['2018-10-Т',   '2019-11-Т',    '2019-11S-Т'],

    'Никита Бекасов':           ['2018-11-А'],
    'Ольга Борисова':           ['2018-11-А'],
    'Александр Воробьев':       ['2018-11-А'],
    'Юлия Глотова':             ['2018-11-А'],
    'Александр Гришков':        ['2018-11-А'],
    'Валерия Жмурина':          ['2018-11-А'],
    'Камиля Измайлова':         ['2018-11-А'],
    'Константин Ичанский':      ['2018-11-А'],
    'Алексей Карчава':          ['2018-11-А'],
    'Данил Колобашкин':         ['2018-11-А'],
    'Анастасия Межова':         ['2018-11-А'],
    'Роман Мигдисов':           ['2018-11-А'],
    'Валерия Никулина':         ['2018-11-А'],
    'Даниил Пахомов':           ['2018-11-А'],
    'Дарья Рогова':             ['2018-11-А'],
    'Валерия Румянцева':        ['2018-11-А'],
    'Светлана Румянцева':       ['2018-11-А'],
    'Назар Сабинов':            ['2018-11-А'],
    'Михаил Тетерин':           ['2018-11-А'],
    'Арсланхан Уматалиев':      ['2018-11-А'],
    'Дарья Холодная':           ['2018-11-А'],

    'Максим Аксенов':           ['2018-7-М',    '2019-8-М'              ],
    'Маргарита Ахметова':       [               '2019-8-М'              ],
    'Елизавета Бовшина':        ['2018-7-М'                             ],
    'Даниил Булатов':           ['2018-7-М'                             ],
    'Иракли Гиоргидзе':         ['2018-7-М'                             ],
    'Артём Глембо':             ['2018-7-М',    '2019-8-М', '2020-9-М'  ],
    'Наталья Гончарова':        ['2018-7-М',    '2019-8-М', '2020-9-М'  ],
    'Святослав Григорьев':      ['2018-7-М'                             ],
    'Алиса Давыдова':           ['2018-7-М'                             ],
    'Василий Еланкин':          ['2018-7-М'                             ],
    'Мария Ермишина':           ['2018-7-М'                             ],
    'Файёзбек Касымов':         ['2018-7-М',    '2019-8-М', '2020-9-М'  ],
    'Александр Кирпиченко':     ['2018-7-М'                             ],
    'Александр Козинец':        [               '2019-8-М', '2020-9-М'  ],
    'Андрей Куликовский':       [                           '2020-9-М'  ],
    'Полина Лоткова':           [                           '2020-9-М'  ],
    'Екатерина Медведева':      ['2018-7-М',    '2019-8-М', '2020-9-М'  ],
    'Константин Мельник':       ['2018-7-М',    '2019-8-М', '2020-9-М'  ],
    'Степан Небоваренков':      ['2018-7-М',    '2019-8-М', '2020-9-М'  ],
    'Матвей Неретин':           ['2018-7-М',    '2019-8-М', '2020-9-М'  ],
    'Мария Никонова':           ['2018-7-М',    '2019-8-М', '2020-9-М'  ],
    'Алексей Никул':            ['2018-7-М'                             ],
    'Даниил Палаткин':          ['2018-7-М',    '2019-8-М', '2020-9-М'  ],
    'Станислав Пикун':          [                           '2020-9-М'  ],
    'Илья Пичугин':             [               '2019-8-М', '2020-9-М'  ],
    'Кирилл Севрюгин':          [                           '2020-9-М'  ],
    'Илья Стратонников':        ['2018-7-М',    '2019-8-М', '2020-9-М'  ],
    'Юта Тихонравова':          ['2018-7-М'                             ],
    'Федотова Дарья':           [               '2019-8-М'              ],
    'Арсений Храмов':           ['2018-7-М',    '2019-8-М'              ],
    'Иван Шустов':              ['2018-7-М',    '2019-8-М', '2020-9-М'  ],
    'Антон Яковлев':            ['2018-7-М'                             ],

    'Ирина Ан':                 ['2018-8-А1',   '2019-9-А', '2020-10-АБ'],
    'Софья Андрианова':         ['2018-8-А1',   '2019-9-А', '2020-10-АБ'],
    'Владимир Артемчук':        ['2018-8-А1',   '2019-9-А', '2020-10-АБ'],
    'Софья Белянкина':          ['2018-8-А1',   '2019-9-А', '2020-10-АБ'],
    'Варвара Егиазарян':        ['2018-8-А1',   '2019-9-А', '2020-10-АБ'],
    'Владислав Емелин':         ['2018-8-А1',   '2019-9-А', '2020-10-АБ'],
    'Артём Жичин':              ['2018-8-А1',   '2019-9-А', '2020-10-АБ'],
    'Елизавета Карманова':      ['2018-8-А1',   '2019-9-А'],
    'Дарья Кошман':             [                           '2020-10-АБ'],
    'Анна Кузьмичёва':          ['2018-8-А1',   '2019-9-А', '2020-10-АБ'],
    'Алёна Куприянова':         ['2018-8-А1',   '2019-9-А', '2020-10-АБ'],
    'Ярослав Лавровский':       ['2018-8-А1'],
    'Анастасия Ламанова':       ['2018-8-А1',   '2019-9-А', '2020-10-АБ'],
    'Виктория Легонькова':      ['2018-8-А1',   '2019-9-А', '2020-10-АБ'],
    'Семён Мартынов':           ['2018-8-А1',   '2019-9-А', '2020-10-АБ'],
    'Варвара Минаева':          ['2018-8-А1',   '2019-9-А', '2020-10-АБ'],
    'Михаил Неудачин':          ['2018-8-А1'],
    'Леонид Никитин':           [                           '2020-10-АБ'],
    'Ксения Новикова':          ['2018-8-А1'],
    'Тимур Перла':              ['2018-8-А1'],
    'Тимофей Полетаев':         ['2018-8-А1',   '2019-9-А', '2020-10-АБ'],
    'Илья Родионов':            ['2018-8-А1'],
    'Андрей Рожков':            [               '2019-9-А', '2020-10-АБ'],
    'Тимур Сидиков':            [               '2019-9-А'],
    'Рената Таржиманова':       ['2018-8-А1',   '2019-9-А', '2020-10-АБ'],
    'Арсений Трофимов':         [                           '2020-10-АБ'],
    'Глеб Урбанский':           ['2018-8-А1',   '2019-9-А'],
    'Кирилл Швец':              [               '2019-9-А'],
    'Андрей Щербаков':          ['2018-8-А1',   '2019-9-А', '2020-10-АБ'],
    'Михаил Ярошевский':        ['2018-8-А1',   '2019-9-А', '2020-10-АБ'],

    'Алексей Алимпиев':         [                           '2020-10-АБ'],
    'Евгений Васин':            [                           '2020-10-АБ'],
    'Герман Говоров':           [                           '2020-10-АБ'],
    'София Журавлева':          [                           '2020-10-АБ'],
    'Константин Козлов':        [                           '2020-10-АБ'],
    'Наталья Кравченко':        [                           '2020-10-АБ'],
    'Сергей Малышев':           [                           '2020-10-АБ'],
    'Алина Полканова':          [                           '2020-10-АБ'],
    'Сергей Пономарёв':         [                           '2020-10-АБ'],
    'Егор Свистушкин':          [                           '2020-10-АБ'],
    'Дмитрий Соколов':          [                           '2020-10-АБ'],

    'Милана Абраамян':      ['2019-9-Л'],
    'Тимур Азимов':         ['2019-9-Л'],
    'Полина Алташина':      ['2019-9-Л'],
    'Аркадий Артемов':      ['2019-9-Л'],
    'Анастасия Базарова':   ['2019-9-Л'],
    'Артём Вартанов':       ['2019-9-Л'],
    'Арина Гайдукевич':     ['2019-9-Л'],
    'Виктор Галан':         ['2019-9-Л'],
    'Дарья Дербышева':      ['2019-9-Л'],
    'Данил Долматов':       ['2019-9-Л'],
    'Зинаида Евдокимова':   ['2019-9-Л'],
    'Софья Евсикова':       ['2019-9-Л'],
    'София Заика':          ['2019-9-Л'],
    'Софья Иосилевская':    ['2019-9-Л'],
    'Маргарита Карманова':  ['2019-9-Л'],
    'Варвара Карпенко':     ['2019-9-Л'],
    'Виктория Кемайкина':   ['2019-9-Л'],
    'Софья Корянова':       ['2019-9-Л'],
    'Николай Кузьмин':      ['2019-9-Л'],
    'Джейн Либерман':       ['2019-9-Л'],
    'Мария Лукина':         ['2019-9-Л'],
    'Елизавета Майорова':   ['2019-9-Л'],
    'Марьям Марова':        ['2019-9-Л'],
    'Гульнара Сафина':      ['2019-9-Л'],
    'Анастасия Свиридова':  ['2019-9-Л'],
    'Евгения Сивачева':     ['2019-9-Л'],
    'Илья Скаков':          ['2019-9-Л'],
    'Валерия Тарасова':     ['2019-9-Л'],
    'Алёна Шальнева':       ['2019-9-Л'],

    'Антон Аникеев':        ['2018-6-Л'],
    'Евдокия Антонова':     ['2018-6-Л'],
    'Даниил Войнов':        ['2018-6-Л'],
    'Кристина Демина':      ['2018-6-Л'],
    'Мария Демина':         ['2018-6-Л'],
    'Карина Егиазарян':     ['2018-6-Л'],
    'Вячеслав Есин':        ['2018-6-Л'],
    'Евгений Камболин':     ['2018-6-Л'],
    'Даниил Кулиев':        ['2018-6-Л'],
    'Арсений Митрохин':     ['2018-6-Л'],
    'Максим Мокроусов':     ['2018-6-Л'],
    'Дмитрий Николаев':     ['2018-6-Л'],
    'Мария Потапова':       ['2018-6-Л'],
    'Олеся Сазонова':       ['2018-6-Л'],
    'Хадижат Тагирова':     ['2018-6-Л'],
    'Вячеслав Фёдоров':     ['2018-6-Л'],
    'Дмитрий Хомяков':      ['2018-6-Л'],
    'Артем Чекарев':        ['2018-6-Л'],
    'Ярослав Чернега':      ['2018-6-Л'],
    'Константин Четкин':    ['2018-6-Л'],
    'Анастасия Шоколенко':  ['2018-6-Л'],
    'Степан Шубин':         ['2018-6-Л'],
    'Андрей Щербаков - 2':  ['2018-6-Л'],
    'Анна Щербакова':       ['2018-6-Л'],
}


class NamesPicker:
    def __init__(self, config):
        cfg = collections.defaultdict(list)
        for name, classes_names in config.items():
            if name.endswith(' - 2') or name.endswith(' - 3'):
                name = name[:-4]
            for class_name in classes_names:
                assert name not in cfg[class_name]
                cfg[class_name].append(name)

        self._key_picker = library.picker.KeyPicker(key=library.picker.letters_key)
        for pupils_id, names in cfg.items():
            pupils_list = []
            for fullName in names:
                name, surname = fullName.split(' ')
                pupils_list.append(Pupil(name=name, surname=surname))

            start_year, class_id, letter = pupils_id.split('-')
            grade = int(''.join(s for s in class_id if s.isdigit()))
            pupils = Pupils(
                pupils_id=pupils_id,
                pupils=pupils_list,
                letter=letter,
                grade=grade,
                add_me=True,
                only_me=False,
                year=int(start_year),
            )
            self._key_picker.add(pupils_id, pupils)

    def get(self, key):
        return self._key_picker.get(key)


names_picker = NamesPicker(classes_config)


def get_class_from_string(value, addMyself=False, onlyMe=False):
    assert isinstance(value, str), f'Trying to search not by str: {value}'
    assert ' ' in value, f'No space in class name: {value}'

    parts = value.split()
    date_part, class_part = parts[0], parts[1]

    year = int(date_part[:4])
    if re.match(r'20\d\d[\.-]\d{2}[\.-]\d{2}', date_part):
        if int(date_part[5:7]) <= 8:  # Aug
            year -= 1
    elif re.match(r'20\d\d', date_part):
        pass
    else:
        raise RuntimeError(f'Could not guess class from {value}')

    key = f'{year} {class_part}'
    pupils = names_picker.get(key)
    assert pupils

    log.debug(f'Returning {len(pupils._pupils_list)} pupils from {pupils._id} (search key: {key})')
    return pupils
