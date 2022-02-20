#!/usr/bin/env python3

import requests
import os
URL = 'https://ru.wikipedia.org/wiki/%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0_%D0%B8%D0%B7%D0%BE%D1%82%D0%BE%D0%BF%D0%BE%D0%B2'

from collections import defaultdict


def download_file(url, file):
    r = requests.get(url)
    assert r.ok
    with open(file, 'wb') as f:
        f.write(r.content)


class FallTime:
    Stable = 'stable'
    Instable = 'instable'
    Instable = 'instable'
    Upto10d = 'upto10d'
    Upto100d = 'upto100d'
    Upto10y = 'upto10y'
    Upto10ky = 'upto10ky'
    Upto700my = 'upto700my'
    Morethan700my = 'morethan700my'


def get_fall_time(line):
    if 'Период полураспада: Стабильный' in line:
        return FallTime.Stable
    elif 'Период полураспада: Нестабильный' in line:
        return FallTime.Instable
    elif 'Период полураспада: 1 — 10 дней' in line:
        return FallTime.Upto10d
    elif 'Период полураспада: 10 — 100 дней' in line:
        return FallTime.Upto100d
    elif 'Период полураспада: 100 дней — 10 лет' in line:
        return FallTime.Upto10y
    elif 'Период полураспада: 10 — 10 000 лет' in line:
        return FallTime.Upto10ky
    elif 'Период полураспада: 10 тыс. — 700 млн лет' in line:
        return FallTime.Upto700my
    elif 'Период полураспада: &gt;700 млн лет' in line:
        return FallTime.Morethan700my
    else:
        raise RuntimeError(f'Unknown line: {line}')


def get_element(line):
    r = line.split('>')[-1].split()
    assert len(r) == 2
    int(r[0])
    return r


def parse_file(file):
    elements = defaultdict(list)

    with open(file) as f:
        for line in f.readlines():
            if '<sup>' in line:
                line = line.strip()
                line = line.replace('<small>', '')
                line = line.replace('</small>', '')
                line = line.replace('<sup>', '')
                line = line.replace('</sup>', ' ')
                line = line.replace('</div>', '')
                line = line.replace('</a>', '')
                line = line.replace('</td>', '')
                line = line.replace('; Ядерный изомер: Нестабильный', '')
                line = line.replace('; Ядерный изомер: 10 — 10 000 лет', '')
                line = line.replace('; Ядерный изомер: 10 тыс. — 700 млн лет', '')
                line = line.replace('; Ядерный изомер: 1 — 10 дней', '')
                line = line.replace('style="background:white;" ', ' ')
                line = line.replace('  ', ' ')
                line = line.replace(' – Изотоп', '')

                # print(line)
                # print(get_element(line), get_fall_time(line))

                a_str, x = get_element(line)
                fall_time = get_fall_time(line)
                elements[x].append(
                    (int(a_str), fall_time)
                )

    data = list(elements.items())
    data.sort(key=lambda x: min(a for a in x[1]))
    for element, isotopes in data:
        isotopes.sort(key=lambda x: x[0])
        stable_a = []
        lower_a = None
        upper_a = None
        for a, fall_time in isotopes:
            if not lower_a or a < lower_a:
                lower_a = a
            if not upper_a or upper_a < a:
                upper_a = a
            if fall_time != FallTime.Instable:
                stable_a.append(a)

        print(f'{element:3s} {lower_a}...{upper_a}, {stable_a}')


if __name__ == '__main__':
    tmp_file = os.path.join(os.getenv('HOME'), 'tmp', 'elements.html')
    download_file(URL, tmp_file)
    parse_file(tmp_file)
