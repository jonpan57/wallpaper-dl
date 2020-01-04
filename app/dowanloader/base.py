import logging


class BaseDownloader:
    def __init__(self, extractor):
        self.session = extractor.session

        self._chunk_size = 16384
        self._total_size = None

    def download(self):
        self.pre_progress()



        self.post_progress()

    def pre_progress(self):
        pass

    def post_progress(self):
        pass
