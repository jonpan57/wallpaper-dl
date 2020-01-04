import logging
import requests


class Extractor:
    def __init__(self, url):
        self.session = requests.session()
        self.log = logging.getLogger()
        self.url = url

        self._cookiefile = None
        self._cookiejar = self.session.cookies
