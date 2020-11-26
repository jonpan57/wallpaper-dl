# extractor类，解决登录和解析网址
import bs4
import ast
import time
import lxml
import requests

from .. import log, config, util


class Extractor:
    category = 'extractor'
    subcategory = ''

    directory_fmt = '{category}'
    filename_fmt = '{filename}.{extension}'
    archive_fmt = ''
    cookie_domain = ''

    root = ''

    _request_last = 0  # 上次请求时间
    _request_interval = 0  # 请求时间间隔
    _request_interval_min = 0  # 请求最小时间间隔

    def __init__(self, match):
        self.session = requests.Session()
        self.log = log.Log(self.category)
        self.config = config.Config(self.category)
        self.url = match.string

        self._cookie_jar = self.session.cookies
        self._cookie_file = None

        self._retries = self.config['retries', 'int']
        self._timeout = self.config['timeout', 'int']
        self._verify = self.config['verify', 'bool']
        self._stream = self.config['stream', 'bool']
        self._request_interval = self.config['interval', 'int']

        if self._retries < 0:
            self._retries = float('inf')

        if self._request_interval < self._request_interval_min:
            self._request_interval = self._request_interval_min

        self._init_headers()
        self._init_cookies()
        self._init_proxies()
        self._init_auth()
        self._init_cert()

    def __iter__(self):
        return self.items()

    def items(self):
        pass

    def skip(self, num):
        return 0

    def request(self, url, *, method='GET', session=None, retries=None, encoding=None, fatal=True, notfound=None,
                **kwargs):  # 这个*是限制后面的一定要输入关键字参数，不能输入位置参数
        tries = 1
        session = self.session if session is None else session
        retries = self._retries if retries is None else retries
        kwargs.setdefault('timeout', self._timeout)
        kwargs.setdefault('verify', self._verify)
        response = None

        if self._request_interval:
            seconds = (self._request_interval - (time.time() - self._request_last))
            if seconds > 0:
                self.log.debug('请求等待{}秒钟'.format(seconds))
                time.sleep(seconds)

        while True:
            try:
                response = session.request(method, url, **kwargs)

            except (requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout,
                    requests.exceptions.ChunkedEncodingError,
                    requests.exceptions.ContentDecodingError) as exc:
                msg = exc
            except requests.exceptions.RequestException as exc:
                pass
                # raise exception.HTTPError(exc)，添加报错
            else:
                """
                转储功能,缓存页面，可考虑加入
                """
                code = response.status_code
                if 200 <= code < 400 or fatal is None and \
                        (400 <= code < 500) or not fatal and \
                        (400 <= code < 429 or 431 <= code < 500):
                    if encoding:
                        response.encoding = encoding
                    return response
                if notfound and code == 404:
                    pass  # raise exception.NotFoundError(notfound)，添加报错

                reason = response.reason
                msg = "'{} {}' for '{}'".format(code, reason, url)
                if code < 500 and code != 429 and code != 430:  # 不是很理解
                    break
            finally:
                self._request_last = time.time()
            self.log.debug("{} ({}/{})".format(msg, tries, retries + 1))

            if tries > retries:
                break
            time.sleep(tries)
            tries += 1

        # raise exception.HttpError(msg, response)，添加报错

    def metadata(self, page):
        """Return a dict with general metadata"""

    def images(self, page):
        """Return a list of all (image-url, metadata)-tuples"""

    def _init_headers(self):
        headers = self.session.headers
        headers.clear()
        headers['Accept'] = self.config['Accept']
        headers['Accept-Encoding'] = self.config['Accept-Encoding']
        headers['Accept-Language'] = self.config['Accept-Language']
        headers['Connection'] = self.config['Connection']
        headers['Upgrade-Insecure-Requests'] = self.config['Upgrade-Insecure-Requests']
        headers['User-Agent'] = self.config['User-Agent']

    def _init_cookies(self):
        if self.cookie_domain is None:
            return

        cookies = self.config['cookie']
        if cookies:
            if type(ast.literal_eval(cookies)) is dict:  # 字典直接使用
                self._update_cookies_dict(cookies, self.cookie_domain)
            elif type(ast.literal_eval(cookies)) is str:  # 路径表明要载入文件
                pass
            else:
                pass

    def _store_cookies(self):
        if self._cookie_file and self.config['cookie-update', 'bool']:
            try:
                with open(self._cookie_file, 'w') as fp:
                    util.save_cookies_text(fp, self._cookie_jar)
            except OSError as exc:
                self.log.warning('Cookies: {}'.format(exc))

    def _update_cookies(self, cookies, *, domain=''):
        if type(cookies) is dict:
            self._update_cookies_dict(cookies, domain or self.cookie_domain)
        else:
            setcookie = self._cookie_jar.set_cookie
            try:
                cookies = iter(cookies)
            except TypeError:
                setcookie(cookies)
            else:
                for cookie in cookies:
                    setcookie(cookie)

    def _update_cookies_dict(self, cookies, cookie_domain):
        set_cookie = self._cookie_jar.set
        for name, value in cookies:
            set_cookie(name, value, domain=cookie_domain)

    def _check_cookies(self, cookienames, *, domain=None):
        if not self._cookie_jar:
            return False
        if domain is None:
            domain = self.cookie_domain
        names = set(cookienames)
        now = time.time()

        for cookie in self._cookie_jar:
            if cookie.name in names and cookie.domain == domain:
                if cookie.expires and cookie.expires < now:
                    self.log.warning('Cookie {}，已经过期'.format(cookie.name))
                else:
                    names.discard(cookie.name)
                    if not names:
                        return True
        return False

    def _init_proxies(self):
        """
        单个请求：
            {"http": "http://10.10.1.10:3128","https": "http://10.10.1.10:1080"}

        需要使用HTTP Basic Auth，可以使用 http://username:password@host/ 语法：
            {"http": "http://username:password@10.10.1.10:3128/"}

        需要特定的连接方式或者主机设置代理，使用 scheme://hostname 作为 key：
             {'http://10.20.1.128': 'http://10.10.1.10:5323'}
        """
        proxies = self.config['proxy']
        if proxies:
            try:
                proxies = ast.literal_eval(proxies)
            except SyntaxError:
                self.log.error('代理配置的参数异常')
            else:
                if type(proxies) is dict:
                    self.session.proxies = proxies
                else:
                    self.log.error('代理配置的参数异常')

    def _init_auth(self):
        pass

    def _init_cert(self):
        pass
