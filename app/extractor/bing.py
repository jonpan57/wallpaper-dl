import os
import bs4
import lxml
from .common import Extractor
from ..dowanloader.http import HttpDownloader


class BingExtractor(Extractor):
    filename_fmt = '{year}-{month}-{filename}'
    link_list = []

    def __init__(self):
        super().__init__()

        self.category = 'bing'
        self.root = self.config('Root')
        self._get_image_link()

    def _get_image_link(self):
        url = self.root
        is_last_page = False
        while not is_last_page:
            response = self.session.get(url=url)
            bs = bs4.BeautifulSoup(response.text, 'lxml')

            self._find_page_link(bs)
            next_page = self._find_next_page(bs)

            if next_page is None:
                is_last_page = True
            else:
                url = next_page

    def _find_page_link(self, bs):
        links = bs.find_all('img', class_='alignleft wp-post-image')
        for link in links:
            temp = link.get('src')
            self.link_list.append(temp.replace('-300x200', ''))

    @staticmethod
    def _find_next_page(bs):
        next_page = bs.find('a', class_='next page-numbers')
        if next_page:
            return next_page.get('href')
        else:
            return None

    def filename(self, response):
        url = response.request.url.split('/')
        return self.filename_fmt.format(year=url[-3], month=url[-2], filename=url[-1])
