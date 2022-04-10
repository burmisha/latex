import library.files

import os
import requests
import attr
from library.logging import cm, color
import logging
log = logging.getLogger(__name__)
from typing import List


@attr.s
class DownloadItem:
    filename: str = attr.ib()
    url: str = attr.ib()


def _create_missing_local_dir(dirname: str, filename: str):
    local_dirname = os.path.dirname(filename)
    base_dir = os.path.join(dirname, local_dirname)
    if not os.path.isdir(base_dir):
        log.info(f'Create missing {base_dir}')
        os.mkdir(base_dir)


def download_items(items, dirname: str, force=False):
    log.info(f'Download into {dirname}:')
    for download_item in items:
        _create_missing_local_dir(dirname, download_item.filename)

        fullname = os.path.join(dirname, download_item.filename)
        assert library.files.path_is_ok(fullname)

        if not force and os.path.exists(fullname):
            log.info(f'    Already exists: {download_item.filename} ...')
            continue

        log.info(f'    Download {url} into {download_item.filename} ...')
        response = requests.get(url)
        if response.ok and response.content:
            with open(fullname, 'wb') as f:
                f.write(response.content)
        else:
            log.error(f'{cm("Could not download", color=color.Red)} {url}: {response}')
            # raise RuntimeError(f'Could not download')
            

