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

    def checkIfExists(self):
        if not os.exists(self.default_path):
            os.makedirs(self.default_path, exists=True)

    def download(self, url, path, **options):
        pass

    def preProgress(self):
        pass

    def postProgress(self):
        pass
