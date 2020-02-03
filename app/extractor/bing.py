import os
import bs4
import lxml
from .common import Extractor
from ..dowanloader.http import HttpDownloader


class BingExtractor(Extractor):
    filename_fmt = '{year}{month}-{filename}'

    def __init__(self):
        super().__init__()

        self.category = 'bing'
        self.url = self.config('Root')
        self.is_last_page = False

    def next(self):
        self.links.clear()
        if self.is_last_page:
            return False
        else:
            self._get_page_link()
            return True

    def filename(self, response):
        url = response.request.url.split('/')
        return self.filename_fmt.format(year=url[-3], month=url[-2], filename=url[-1])

    def _get_page_link(self):
        print(self.url)
        response = self.session.get(url=self.url)
        bs = bs4.BeautifulSoup(response.text, 'lxml')
        self._find_page_link(bs)
        next_page = self._find_next_page(bs)
        if next_page is None:
            self.is_last_page = True
        else:
            self.url = next_page

    def _find_page_link(self, bs):
        links = bs.find_all('img', class_='alignleft wp-post-image')
        for link in links:
            temp = link.get('src')
            self.links.append(temp.replace('-300x200', ''))

    @staticmethod
    def _find_next_page(bs):
        next_page = bs.find('a', class_='next page-numbers')
        if next_page:
            return next_page.get('href')
        else:
            return None
