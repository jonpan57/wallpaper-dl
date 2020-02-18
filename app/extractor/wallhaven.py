import os
import mimetypes

from .common import Extractor


class WallhavenExtractor(Extractor):
    filename_fmt = '{id}{extension}'

    def __init__(self, match):
        super().__init__()
        self.category = 'wallhaven'
        self.root = self.config('Root')
        self.url = self.root + match

    def filename(self, response):
        filename = os.path.basename(response.request.url).split('%20')
        extension = mimetypes.guess_extension(response.headers.get('Content-Type'))
        return self.filename_fmt.format(id=filename[2], extension=extension)

    def _find_page_links(self, bs):
        links = bs.find_all('img', class_='lazyload loaded')
        for link in links:
            temp = link.get('src')
            self.links.append(temp.replace('small', 'full'))

    def _find_next_page(self, bs):
        next_page = bs.find('a', class_='next_page')
        if next_page:
            return self.root + next_page.get('href')
        else:
            return None
