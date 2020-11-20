import os
from app.log import Log
from app.config import Config


class Downloader:
    category = 'downloader'

    def __init__(self, extractor):
        self.session = extractor.session
        self.config = Config(self.category).config
        # self.log = Log(self.category + '.' + self.subcategory)

        self.temp = self.config('temp', convert='bool')  # 临时文件下载
        self.tempdir = self.config('tempdir')  # 临时文件目录

    def download(self, url, path):
        '''从url下载到path_fmt'''
