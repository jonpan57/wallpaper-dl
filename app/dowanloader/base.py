import logging

class BaseDownloader:
    def __init__(self,extractor):
        self.url = url  # 下载地址
        self.path = path  # 下载路径
        self.chunk_size = 16384
