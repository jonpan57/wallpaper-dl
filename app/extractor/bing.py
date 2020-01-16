import os
import bs4
import lxml
from ..extractor.base import Extractor
from ..dowanloader.http import HttpDownloader


class BingExtractor(Extractor):
    _section = 'BingExtractor'
    image_link = []

    def __init__(self, url, **options):
        super().__init__(url, **options)
        self.root = url
        self._crawl_image_link()

    def _crawl_image_link(self):
        flag = True
        while flag:
            response = self.session.get(url=self.url)
            current_page = os.path.basename(self.url)
            next_page = self._find_next_page(response.text)
            if current_page == next_page:
                flag = False
            else:
                pass

    def image(self, text):
        bs = bs4.BeautifulSoup(text, 'lxml')
        bs.find_all('img').get('src')

    def _find_next_page(self, text):
        bs = bs4.BeautifulSoup(text, 'lxml')
        page_tag = bs.find('div', class_='page').find('span').get_text()
        max_page = int(page_tag.split('/')[1])
        return max_page
