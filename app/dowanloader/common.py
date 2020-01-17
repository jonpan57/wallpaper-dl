import os
import logging
from app.configuration import config


class Downloader:
    _section = 'Downloader'

    def __init__(self, extractor):
        self.session = extractor.session

        self._retries = self.config('Retries')
        self._timeout = self.config('Timeout')
        self._steam = self.config('Steam')
        self._verify = self.config('Verify')
        self._chunk_size = self.config('Chunk_size')

    def config(self, option, value=None):
        if value:
            config.write(self._section, option, value)
            return config.get(self._section, option)
        else:
            return config.get(self._section, option)

    def download(self, url, **options):
        # 以后加入覆盖下载和中止下载选项
        try:
            self._start_download(url, **options)
        except Exception as e:
            raise e

    def _start_download(self, url, **options):
        pass

    def _end_download(self):
        pass

    def pre_progress(self):
        pass

    def post_progress(self):
        pass
