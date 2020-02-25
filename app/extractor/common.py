# extractor类，解决登录和解析网址
import bs4
import lxml
import requests

from tenacity import retry, stop_after_attempt
from app.config import Config


class Extractor(Config):
    category = 'extractor'
    subcategory = ''
    directory_fmt = '{category}'
    filename_fmt = '{filename}{extension}'
    archive_fmt = ''
    cookie_domain = ''

    root = ''
    links = []
    link = ''

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

    @property
    def link(self):
        try:
            link = self.links.pop(0)
        except IndexError:
            link = ''
        finally:
            return link

    def next(self):
        self.links.clear()
        if self.is_last_page:
            return False
        else:
            self._get_page_links()
            return True

    def filename(self):
        pass

    def _get_page_links(self):
        print(self.url)
        response = self._request(url=self.url)
        if response:
            bs = bs4.BeautifulSoup(response.text, 'lxml')
            self._find_page_links(bs)
            next_page = self._find_next_page(bs)
            if next_page:
                self.url = next_page
            else:
                self.is_last_page = True
                print('All done!')
        else:
            print(self.url + ' --> Request Timeout')
            self.is_last_page = True
            print('Not done')

    def _find_page_links(self, bs):
        pass

    def _find_next_page(self, bs):
        pass

    @retry(reraise=True, stop=stop_after_attempt(10))
    def _request(self, url, method='GET', **kwargs):
        try:
            response = self.session.request(method, url, timeout=self._timeout, verify=self._verify, **kwargs)

        except requests.exceptions as e:
            return None
        else:
            code = response.status_code
            if 200 <=
