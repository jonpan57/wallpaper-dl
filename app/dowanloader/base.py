import os
import sys
import time
import logging


class BaseDownloader:
    def __init__(self, extractor):
        self.session = extractor.session
        self.chunk_size = 16384
        self.total_size =None
