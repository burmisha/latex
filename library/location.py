import os
import functools

import logging
log = logging.getLogger(__name__)


class Location:
    Home = os.environ['HOME']
    Dropbox = os.path.join(Home, 'Dropbox')
    YandexDisk = os.path.join(Home, 'Yandex.Disk.localized')
    Zoom = os.path.join(Home, 'Documents', 'Zoom')
    Downloads =  os.path.join(Home, 'Downloads')
    Root = os.path.dirname(os.path.dirname(os.path.join(__file__)))


zoom = functools.partial(os.path.join, Location.Zoom)
udr = functools.partial(os.path.join, Location.YandexDisk, 'УДР', 'Общие материалы физиков УДР')
ipad = functools.partial(os.path.join, Location.Dropbox, '_iPad-Word')
ya_disk = functools.partial(os.path.join, Location.YandexDisk)
downloads = functools.partial(os.path.join, Location.Downloads)
root = functools.partial(os.path.join, Location.Root)
no_sync = functools.partial(os.path.join, Location.Home, 'no_sync')
tmp = functools.partial(os.path.join, Location.Home, 'tmp')
external_toshiba = functools.partial(os.path.join, os.sep, 'Volumes', 'tosh2tb', 'УДР - external')
