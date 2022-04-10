import os
import re
import requests

from library.download.multiple import DownloadItem

from library.logging import cm, colorize_json, color
import logging
log = logging.getLogger(__name__)


class ZnakKachestva:
    HOST = 'http://znakka4estva.ru'

    def _get_presentation_urls(self):
        for page_index in range(1, 14):
            page_url = f'{self.HOST}/prezentacii/fizika-i-energetika/'
            log.info(f'Processing page {page_index}: {page_url}')
            response = requests.get(page_url, params={'page': page_index})
            for line in response.text.split('\n'):
                if 'blog-img-wrapper' in line and 'href="' + page_url in line:
                    l = re.sub(r'.*href="', '', line)
                    presentation_url = re.sub(r'" class=".*', '', l)
                    log.info(f'    New presentation: {presentation_url}')
                    yield presentation_url

    def get_items(self):
        for presentation_url in self._get_presentation_urls():
            response = requests.get(presentation_url)
            for line in response.text.split('\n'):
                if '<h1 class="pull-sm-left">' in line:
                    l = re.sub(r'.*"pull-sm-left">', '', line)
                    ll = re.sub(r'<.*', '', l)
                    split_position = ll.find('. ')
                    name = ll[split_position + 2:]
                    grade = int(presentation_url.split('/')[-2].split('-')[0])
                    assert 7 <= grade <= 11, f'Invalid grade: {grade}'
                    link = f'{self.HOST}/uploads/category_items/{name}.ppt'
                    filename = re.sub(r'\. (\d)\. ', r'. 0\1. ', ll)
                    yield DownloadItem(
                        filename=os.path.join(f'{grade} класс', f'{filename}.ppt'),
                        url=link,
                    )

def get_items():
    znakKachestva = ZnakKachestva()
    return znakKachestva.get_items()
