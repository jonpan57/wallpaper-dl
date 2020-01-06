import os
import logging
from .. import config

down = 'downloader'


class BaseDownloader:
    def __init__(self, extractor):
        self.session = extractor.session
        self.timeout = config.get(down, 'timeout')
        self.chunk_size = config.get(down, 'chunk_size')
        self.default_path = config.get(down, 'default_path')
        self._checkIfExists()

    def _checkIfExists(self):
        if not os.path.exists(self.default_path):
            os.makedirs(self.default_path, exist_ok=True)

    def preProgress(self):
        pass

    def postProgress(self):
        pass
