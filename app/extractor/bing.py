import os
import bs4
import lxml
from ..extractor.common import Extractor
from ..dowanloader.http import HttpDownloader


class BingExtractor(Extractor):
    _section = 'BingExtractor'
    link_list = []

    def __init__(self, url, **options):
        super().__init__(url, **options)
        self.root = url
        self.default_path = self.config('Default_path')

        self._crawl_image_link()

    def _crawl_image_link(self):
        is_last_page = False
        while not is_last_page:
            response = self.session.get(url=self.url)
            bs = bs4.BeautifulSoup(response.text, 'lxml')
            self._find_page_link(bs)
            next_page = self._find_next_page(bs)
            if next_page is None:
                is_last_page = True
            else:
                self.url = next_page

    def _find_page_link(self, bs):
        links = bs.find_all('img', class_='alignleft wp-post-image')
        for link in links:
            temp = link.get('src')
            self.link_list.append(temp.replace('-300x200', ''))

    def _find_next_page(self, bs):
        temp = bs.find('div', class_='next page-numbers')
        if temp:
            next_page = temp.get('href')
            return next_page
        else:
            return None
