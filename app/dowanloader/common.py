import os
from app.log import Log
from app.config import Config


class Downloader:
    category = 'downloader'
    subcategory = ''

    def __init__(self, extractor):
        self.session = extractor.session

        self.config = Config(self.category)
        self.log = Log('{}.{}'.format(self.category, self.subcategory))

        self.part = self.config('part')
        self.partdir = self.config('partdir')

    def download(self, url, pathfmt):
        '''从url下载到path_fmt'''
