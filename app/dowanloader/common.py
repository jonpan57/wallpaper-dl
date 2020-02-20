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

    def download(self, url, path_fmt):
        # 以后加入覆盖下载和中止下载选项
        try:
            self._start_download(url, path_fmt)
        except Exception as e:
            raise e
        finally:
            self._end_download(url)

    def _start_download(self, url, **options):
        pass

    def _end_download(self, url):
        pass

    def pre_progress(self):
        pass

    def post_progress(self):
        pass
