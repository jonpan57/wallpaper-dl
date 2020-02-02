import os
import bs4
import lxml
from .common import Extractor


class KonachanExtractor(Extractor):
    filename_fmt = '{year}-{month}-{filename}'
    link_list = []

    def __init__(self, url):
        super().__init__(url)
        self._section = 'konachan'
        self.root = url
        self.default_path = self.config('Default_path')
        self._crawl_image_link()

    def _crawl_image_link(self):
        is_last_page = False
        self.url = self.root + '/post'
        while not is_last_page:
            print(self.url)
            response = self.session.get(url=self.url)
            bs = bs4.BeautifulSoup(response.text, 'lxml')
            self._find_page_link(bs)
            next_page = self._find_next_page(bs)
            print(next_page)
            if next_page is None:
                is_last_page = True
            else:
                self.url = self.root + next_page

    def _find_page_link(self, bs):
        links = bs.find_all('a', class_='directlink largeimg')
        for link in links:
            temp = link.get('href')
            self.link_list.append(temp)

    def _find_next_page(self, bs):
        next_page = bs.find('a', class_='next_page')
        if next_page:
            return next_page.get('href')
        else:
            return None
