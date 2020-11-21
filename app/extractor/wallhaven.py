import os
import bs4
import lxml
import mimetypes

from .common import Extractor


class WallhavenExtractor(Extractor):
    filename_fmt = '{category}_{purity}_{id}_{resolution}.{extension}'

    def __init__(self, match):
        super().__init__()
        self.category = 'wallhaven'
        self.root = self.config['Root']
        self.url = self.root + match
        self.api = WallhevanAPI(self)

    def filename(self, response):
        filename = os.path.basename(response.request.url).split('%20')
        extension = mimetypes.guess_extension(response.headers.get('Content-Type'))
        return self.filename_fmt.format(id=filename[2], extension=extension)

    def _get_page_links(self):
        pass

    def _find_page_links(self, bs):
        ul = bs.find_all('ul')
        for li in ul:
            link = li.find('img', class_='lazyload')
            png = li.find('span', class_='png')
            if png:
                temp = link.get('src')
                self.links.append(temp.replace('/small/', '/full/').replace('.jpg', '.png'))
            else:
                temp = link.get('src')
                self.links.append(temp.replace('/small/', '/full/'))

    def _find_next_page(self, bs):
        next_page = bs.find('a', class_='next_page')
        if next_page:
            return self.root + next_page.get('href')
        else:
            return None

    def login(self):
        response = self.request('https://wallhaven.cc/login')
        if response:
            bs = bs4.BeautifulSoup(response.text, 'lxml')
            token = bs.find(name='input', attrs={'name': '_token'}).get('value')
            data = {
                '_token': token,
                'username': self.config('Username'),
                'password': self.config('Password'),
            }
            self.session.post('https://wallhaven.cc/auth/login', data=data)


class WallhevanAPI:
    def __init__(self, extractor):
        self.extractor = extractor

        self.api_key = extractor.config['api-key']
        if self.api_key is None:
            self.api_key = 'wxlFzOHZajyFmYto3MSAoczXCQ8KkEEM'
            extractor.log.debug('使用默认API Key')
        else:
            extractor.log.debug('使用自定义API Key')
        self.url_info = extractor.root + extractor.config('api-info')
        self.url_search = extractor.root + extractor.config('api-search')

    def info(self, wallpaper_id):
        url = self.url_info + wallpaper_id
        return url

    def search(self):
