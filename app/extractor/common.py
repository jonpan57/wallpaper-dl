# extractor类，解决登录和解析网址
import requests

from app.config import Config


class Extractor(Config):
    category = 'extractor'

    directory_fmt = '{category}'
    filename_fmt = '{filename}{extension}'
    cookie_domain = ''
    root = ''
    links = []
    is_last_page = False

    def __init__(self):
        self.session = requests.Session()

        self._cookie_jar = self.session.cookies
        self._cookie_file = None

        self._retries = int(self.config('Retries'))

        self._init_headers()
        self._init_cookies()
        self._init_proxies()

    def _init_headers(self):
        headers = self.session.headers
        headers.clear()
        headers['User-Agent'] = self.config('User-Agent')
        headers['Accept'] = self.config('Accept')
        headers['Accept-Language'] = self.config('Accept-Language')
        headers['Accept-Encoding'] = self.config('Accept-Encoding')
        headers['Connection'] = self.config('Connection')
        headers['Upgrade-Insecure-Requests'] = self.config('Upgrade-Insecure-Requests')

    def _init_cookies(self):
        if self.cookie_domain is None:
            return

        cookies = self.config('Cookie')
        if cookies:
            if isinstance(eval(cookies), dict):
                self._update_cookie_dict(cookies, self.cookie_domain)
            elif isinstance(eval(cookies), str):  # 以后待补充
                pass
            else:
                pass

    def _init_proxies(self):
        proxies = self.config('Proxy')
        if proxies:
            self.session.proxies = eval(proxies)

    def _update_cookie_dict(self, cookies, cookie_domain):
        set_cookie = self._cookie_jar.set
        for name, value in cookies:
            set_cookie(name, value, domain=cookie_domain)

    def _update_cookie_file(self, cookie_file):
        pass
