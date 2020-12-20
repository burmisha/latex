import os

import logging
log = logging.getLogger(__name__)


class Location:
    Home = os.environ['HOME']
    Dropbox = os.path.join(Home, 'Dropbox')
    YandexDisk = os.path.join(Home, 'Yandex.Disk.localized')
    Zoom = os.path.join(Home, 'Documents', 'Zoom')
    Downloads =  os.path.join(Home, 'Downloads')


def zoom(*args):
    path = os.path.join(Location.Zoom, *args)
    return path


def udr(*args):
    path = os.path.join(Location.YandexDisk, 'УДР', 'Общие материалы физиков УДР', *args)
    return path


def ipad(*args):
    path = os.path.join(Location.Dropbox, '_iPad-Word', *args)
    return path


def ya_disk(*args):
    path = os.path.join(Location.YandexDisk, *args)
    return path


def downloads(*args):
    path = os.path.join(Location.Downloads, *args)
    return path
