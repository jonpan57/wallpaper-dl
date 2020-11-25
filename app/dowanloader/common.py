import os

from .. import log, config


class Downloader:
    category = 'downloader'
    subcategory = ''

    def __init__(self, job):
        self.out = job.out
        self.session = job.session
        self.config = config.Config(self.category)

        self.default = self.config['default', 'bool']
        self.file_directory = self.config['default-directory'] if self.default else self.config['custom-directory']
        # 默认路径情况下，可以添加功能，根据文件类型自动识别到图片、音乐、视频、文档等文件夹；根据URL自动识别到对应的文件夹
        self.type_based = self.config['type_based', 'bool']
        self.url_based = self.config['url_based', 'bool']

        self.temp = self.config['temp', 'bool']  # 是否开启临时缓存文件下载
        self.temp_directory = self.config['temp-directory'] if self.temp else ''

        self.log = log.Log(self.category + '.' + self.subcategory)

    def download(self, url, path):
        '''从url下载到path'''
