import os

import logging
log = logging.getLogger(__name__)


class Location:
    Home = os.environ['HOME']
    Dropbox = os.path.join(Home, 'Dropbox')
    YandexDisk = os.path.join(Home, 'Yandex.Disk.localized')
    Zoom = os.path.join(Home, 'Documents', 'Zoom')


def zoom(*args):
    path = os.path.join(Location.Zoom, *args)
    return path


def udr(*args):
    path = os.path.join(Location.YandexDisk, 'УДР', 'Общие материалы физиков УДР', *args)
    return path


def ipad(*args):
    path = os.path.join(Location.Dropbox, '_iPad-Word', *args)
    return path
