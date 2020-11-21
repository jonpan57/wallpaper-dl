import os

from ..config import Config


class Downloader:
    category = 'downloader'

    def __init__(self, extractor):
        self.session = extractor.session
        self.config = Config(self.category)
        self.temp = self.config['temp', 'bool']  # 临时文件下载
        self.tempdir = self.config['tempdir']  # 临时文件目录

    def download(self, url, path):
        '''从url下载到path_fmt'''
