import logging
import mimetypes
from ..config import Config

section = 'downloader'


class BaseDownloader:
    def __init__(self, extractor):
        self.session = extractor.session

        self._chunk_size = Config(section, 'chunk_size').value

    def download(self, url, path, options=None):
        self.preProgress()
        if options is None:
            options = {}
        total_size = None
        response = self.session.get(url)
        filename = self.getFilename(response, options.get('filename'))
        self.postProgress()

    def getFilename(self, response, filename=None):
        if filename:
            content_type = response.headers['Content-Type']
            filename = filename + mimetypes.guess_type(content_type)

        else:
            pass

        return filename

    def preProgress(self):
        pass

    def postProgress(self):
        pass
