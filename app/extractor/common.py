# extractor类，解决登录和解析网址
import requests

import app.configuration.config as config

print(config.get('Downloader', 'Retries'))


class Extractor:
    _section = 'Extractor'
    cookie_domain = ''

    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

        self._cookie_file = None
        self._cookie_jar = self.session.cookies

        self._init_headers()
        self._init_cookies()
        self._init_proxies()

    def configure(self, option, value=None):
        if value:
            config.write(self._section, option, value)
            return config.get(self._section, option)
        else:
            return config.get(self._section, option)

    def _init_headers(self):
        headers = self.session.headers
        headers.clear()
        headers['User-Agent'] = self.configure('User-Agent')
        headers['Accept'] = self.configure('Accept')
        headers['Accept-Language'] = self.configure('Accept-Language')
        headers['Accept-Encoding'] = self.configure('Accept-Encoding')
        headers['Connection'] = self.configure('Connection')
        headers['Upgrade-Insecure-Requests'] = self.configure('Upgrade-Insecure-Requests')
        print(headers)

    def _init_cookies(self):
        if self.cookie_domain is None:
            return

        cookies = self.configure('Cookie')
        if cookies:
            if isinstance(eval(cookies), dict):
                self._update_cookie_dict(cookies, self.cookie_domain)
            elif isinstance(eval(cookies), str):  # 以后待补充
                pass
            else:
                pass

    def _init_proxies(self):
        proxies = self.configure('Proxy')
        if proxies:
            self.session.proxies = eval(proxies)

    def _update_cookie_dict(self, cookies, cookie_domain):
        set_cookie = self._cookie_jar.set
        for name, value in cookies:
            set_cookie(name, value, domain=cookie_domain)

    def _update_cookie_file(self, cookie_file):
        pass
