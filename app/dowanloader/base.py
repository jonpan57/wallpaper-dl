import os
import logging
from .. import config


class Downloader:
    _section = 'Downloader'

    def __init__(self, extractor):
        self.session = extractor.session

        self._retries = self.config('retries')
        self._timeout = self.config('timeout')
        self._verify = self.config('verify')
        self._chunk_size = self.config('chunk_size')

    def config(self, option, value=None):
        if value:
            config.write(self._section, option, value)
            return config.get(self._section, option)
        else:
            return config.get(self._section, option)

    def download(self, url, pathname):
        # 以后加入覆盖下载和中止下载选项
        try:
            self._start_download(url, pathname)
        except KeyboardInterrupt as e:
            raise e

    def _start_download(self, url, pathname):
        pass

    def _end_download(self):
        pass

    def pre_progress(self):
        pass

    def post_progress(self):
        pass
