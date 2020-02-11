import os
import bs4
import lxml
import mimetypes
from tenacity import retry, stop_after_attempt
from .common import Extractor


class KonachanExtractor(Extractor):
    filename_fmt = '{id}{extension}'

    def __init__(self):
        super().__init__()

        self.category = 'konachan'
        self.root = self.config('Root')
        self.url = self.root + '/post'
        self.is_last_page = False

    def next(self):
        self.links.clear()
        if self.is_last_page:
            return False
        else:
            self._get_page_link()
            return True

    def filename(self, response):
        basename = os.path.basename(response.request.url)
        url = basename.split('%20')
        extension = mimetypes.guess_extension(response.headers.get('Content-Type'))
        return self.filename_fmt.format(id=url[2], extension=extension)

    def _get_page_link(self):
        print(self.url)
        response = self._get_response_body(url=self.url)
        if response is None:
            print(self.url + ' --> Request Timeout')
            self.is_last_page = True
            print('Not done')
        else:
            bs = bs4.BeautifulSoup(response.text, 'lxml')
            self._find_page_link(bs)
            next_page = self._find_next_page(bs)
            if next_page is None:
                self.is_last_page = True
                print('All done!')
            else:
                self.url = next_page

    def _find_page_link(self, bs):
        links = bs.find_all('a', class_='directlink')
        for link in links:
            self.links.append(link.get('href'))

    def _find_next_page(self, bs):
        next_page = bs.find('a', class_='next_page')
        if next_page:
            return self.root + next_page.get('href')
        else:
            return None

    @retry(reraise=True, stop=stop_after_attempt(10))
    def _get_response_body(self, url):
        try:
            response = self.session.get(url)
            return response

        except Exception:
            return None
