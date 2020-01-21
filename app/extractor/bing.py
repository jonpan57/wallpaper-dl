import os
import bs4
import lxml
from .common import Extractor
from ..dowanloader.http import HttpDownloader


class BingExtractor(Extractor):
    _category = 'bing'
    link_list = []

    root = 'https://www.bingwallpaperhd.com'

    def __init__(self, url):
        super().__init__(url)
        self.root = url
        self.default_path = self.config('Default_path')
        self._crawl_image_link()
        print(self.link_list)

    def _crawl_image_link(self):
        is_last_page = False
        while not is_last_page:
            print(self.url)
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
        next_page = bs.find('a', class_='next page-numbers')
        if next_page:
            return next_page.get('href')
        else:
            return None
