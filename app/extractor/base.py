# extractor类，解决登录和解析网址
import requests


class BaseExtractor:
    def __init__(self, url, **options):
        self.url = url
        self.session = requests.Session()
        self.response = self.session.get(url)
