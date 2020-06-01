# extractor类，解决登录和解析网址
import bs4
import lxml
import requests

from app.log import Log
from app.config import Config


class Extractor:
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
        self.log = Log(self.category)
        self.config = Config(self.category)

        self._cookie_jar = self.session.cookies
        self._cookie_file = None

        self._retries = int(self.config('retries'))
        self._timeout = int(self.config('timeout'))
        self._verify = bool(self.config('verify'))
        self._stream = bool(self.config('stream'))

        if self._retries < 0:
            self._retries = float('inf')

        self._init_headers()
        self._init_cookies()
        self._init_proxies()

    def __iter__(self):
        return self.items()

    def items(self):
        pass

    def skip(self, num):
        return 0

    def request(self, url, method='GET', session=None, retries=None, encoding=None, **kwargs):
        tries = 1
        session = self.session if session is None else session
        retries = self._retries if retries is None else retries
        kwargs.setdefault('timeout', self._timeout)
        kwargs.setdefault('verify', self._verify)

        while True:
            try:
                response = session.request(method, url, **kwargs)

            except requests.exceptions as e:
                return None
            else:
                code = response.status_code
                if 200 <= code < 500:
                    if encoding:
                        response.encoding = encoding
                    return response
                if code == 404:
                    pass  # page not fonnd

                # msg = "'{} {}' for '{}'".format(code, response.reason, url)
                if code < 500 and code != 429 and code != 430:  # 不是很理解
                    break

            # self.log.debug("%s (%s/%s)", msg, tries, retries + 1)
            if tries > retries:
                break
            tries += 1

    def login(self):
        """Login and set necessary cookies"""

    def _get_auth_info(self):
        username = self.config('username')
        password = None
        if username:
            password = self.config('password')

    def metadata(self, page):
        """Return a dict with general metadata"""

    def images(self, page):
        """Return a list of all (image-url, metadata)-tuples"""

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

        cookies = self.config('cookie')
        if cookies:
            if isinstance(eval(cookies), dict):
                self._update_cookie_dict(cookies, self.cookie_domain)
            elif isinstance(eval(cookies), str):  # 以后待补充
                pass
            else:
                pass

    def _stroe_cookies(self):
        pass

    def _update_cookies_dict(self, cookies, cookie_domain):
        set_cookie = self._cookie_jar.set
        for name, value in cookies:
            set_cookie(name, value, domain=cookie_domain)

    def _update_cookies_file(self, cookie_file):
        pass

    def _init_proxies(self):
        """
        单个请求：
            {"http": "http://10.10.1.10:3128","https": "http://10.10.1.10:1080"}

        需要使用HTTP Basic Auth，可以使用 http://username:password@host/ 语法：
            {"http": "http://username:password@10.10.1.10:3128/"}

        需要特定的连接方式或者主机设置代理，使用 scheme://hostname 作为 key：
             {'http://10.20.1.128': 'http://10.10.1.10:5323'}
        """
        proxies = self.config('Proxy')
        if proxies:
            try:
                proxies = eval(proxies)
            except SyntaxError:
                pass
            else:
                if isinstance(proxies, dict):
                    self.session.proxies = proxies

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
        response = self.request(url=self.url)
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
