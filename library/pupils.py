#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging

log = logging.getLogger(__name__)


class Pupils(object):
    def __init__(self, names=[], letter=None, grade=None):
        self.Names = names
        self.Letter = letter
        self.Grade = grade

    def Iterate(self):
        for name in self.Names:
            yield name


def getPupils(className):
    if className == 'class-2018-10':
        names = [
            u'Гагик Аракелян',
            u'Ирен Аракелян',
            u'Сабина Асадуллаева',
            u'Вероника Битерякова',
            u'Юлия Буянова',
            u'Пелагея Вдовина',
            u'Леонид Викторов',
            u'Фёдор Гнутов',
            u'Илья Гримберг',
            u'Иван Гурьянов',
            u'Артём Денежкин',
            u'Виктор Жилин',
            u'Дмитрий Иванов',
            u'Олег Климов',
            u'Анна Ковалева',
            u'Глеб Ковылин',
            u'Даниил Космынин',
            u'Алина Леоничева',
            u'Ирина Лин',
            u'Олег Мальцев',
            u'Ислам Мунаев',
            u'Александр Наумов',
            u'Георгий Новиков',
            u'Егор Осипов',
            u'Руслан Перепелица',
            u'Михаил Перин',
            u'Егор Подуровский',
            u'Роман Прибылов',
            u'Александр Селехметьев',
            u'Алексей Тихонов',
            u'Алина Филиппова',
            u'Алина Яшина',
        ]
        letter = u'T'
        grade = 10
    elif className == 'class-2018-11':
        names = [
            u'Никита Бекасов',
            u'Ольга Борисова',
            u'Александр Воробьев',
            u'Юлия Глотова',
            u'Александр Гришков',
            u'Валерия Жмурина',
            u'Камиля Измайлова',
            u'Константин Ичанский',
            u'Алексей Карчава',
            u'Данил Колобашкин',
            u'Анастасия Межова',
            u'Роман Мигдисов',
            u'Валерия Никулина',
            u'Даниил Пахомов',
            u'Дарья Рогова',
            u'Валерия Румянцева',
            u'Светлана Румянцева',
            u'Назар Сабинов',
            u'Михаил Тетерин',
            u'Арсланхан Уматалиев',
            u'Дарья Холодная',
        ]
        letter = u'А'
        grade = 11
    else:
        raise RuntimeError('No class config for %r' % className)

    names = [u'Михаил Бурмистров'] + names

    return Pupils(names=names, letter=letter, grade=grade)
