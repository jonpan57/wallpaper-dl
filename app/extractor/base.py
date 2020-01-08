# extractor类，解决登录和解析网址
import requests

from .. import config


class Extractor:
    def __init__(self, url, **options):
        self.url = url
        self.session = requests.Session()

        self._init_headers()
        self._init_cookies()
        self._init_proxies()

    def _init_headers(self):
        headers = self.session.headers
        headers.clear()
        headers['User-Agent'] = config.get('')

    def _init_cookies(self):
        pass

    def _init_proxies(self):
        pass
