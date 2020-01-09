import os
import logging
from .. import config


class Downloader:
    _section = 'Downloader'

    def __init__(self, extractor):
        self.session = extractor.session
        self.timeout = self.config('timeout')
        self.chunk_size = self.config('chunk_size')
        self.default_path = self.config('default_path')
        self._check_if_exists()

    def config(self, option, value=None):
        if value:
            config.write(self._section, option, value)
            return config.get(self._section, option)
        else:
            return config.get(self._section, option)

    def _check_if_exists(self):
        if not os.path.exists(self.default_path):
            os.makedirs(self.default_path, exist_ok=True)

    def pre_progress(self):
        pass

    def post_progress(self):
        pass
