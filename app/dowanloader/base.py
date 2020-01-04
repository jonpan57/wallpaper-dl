import os
import sys
import time
import logging


class BaseDownloader:
    def __init__(self, extractor):
        self.session = extractor.session
        self.chunk_size = 16384
        self._total_size = None

    def donwload(self):
        self.pre_process()

        self.post_process()

    def pre_process(self):
        pass

    def post_process(self):
        pass
