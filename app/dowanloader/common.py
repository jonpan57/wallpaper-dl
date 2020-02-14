import os
import logging
from app.config import Config


class Downloader(Config):
    category = 'downloader'

    def __init__(self, extractor):
        self.session = extractor.session

        self._retries = int(self.config('Retries'))
        self._timeout = int(self.config('Timeout'))
        self._stream = bool(self.config('Stream'))
        self._verify = bool(self.config('Verify'))
        self._chunk_size = int(self.config('ChunkSize'))

    def download(self, url, **options):
        # 以后加入覆盖下载和中止下载选项
        self._start_download(url, **options)

    def _start_download(self, url, **options):
        pass

    def _end_download(self):
        pass

    def pre_progress(self):
        pass

    def post_progress(self):
        pass
