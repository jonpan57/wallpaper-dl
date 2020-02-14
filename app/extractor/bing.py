import os
import bs4
import lxml

from .common import Extractor


class BingExtractor(Extractor):
    filename_fmt = '{year}{month}-{filename}'

    def __init__(self):
        super().__init__()
        self.category = 'bing'
        self.url = self.config('Root')

    def filename(self, response):
        filename = response.request.url.split('/')
        return self.filename_fmt.format(year=filename[-3], month=filename[-2], filename=filename[-1])

    def _get_page_link(self):
        print(self.url)
        response = self._get_response_body(url=self.url)
        if response is None:
            print(self.url + ' --> Request timeout and unfinished task')
            self.is_last_page = True
        else:
            bs = bs4.BeautifulSoup(response.text, 'lxml')
            self._find_page_link(bs)
            next_page = self._find_next_page(bs)
            if next_page is None:
                self.is_last_page = True
                print('All done!!!')
            else:
                self.url = next_page

    def _find_page_link(self, bs):
        links = bs.find_all('img', class_='alignleft wp-post-image')
        for link in links:
            self.links.append(link.get('src').replace('-300x200', ''))

    @staticmethod
    def _find_next_page(bs):
        next_page = bs.find('a', class_='next page-numbers')
        if next_page:
            return next_page.get('href')
        else:
            return None
