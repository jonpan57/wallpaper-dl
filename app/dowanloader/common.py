import os

from .. import log, config


class Downloader:
    category = 'downloader'
    subcategory = ''

    def __init__(self, job):
        self.out = job.out
        self.session = job.extractor.session
        self.config = config.Config(self.category)

        self.default = self.config['default', 'bool']
        if self.default:
            self.default_directory = self.config['default-directory']
        else:
            self.default_directory=
        # 默认路径情况下，可以添加功能，根据文件类型自动识别到图片、音乐、视频、文档等文件夹；根据URL自动识别到对应的文件夹
        self.temp = self.config['temp', 'bool']  # 是否开启临时缓存文件下载

        self.log = log.Log(self.category + '.' + self.subcategory)
        # 添加临时文件夹判断

    def download(self, url, path):
        '''从url下载到path'''
