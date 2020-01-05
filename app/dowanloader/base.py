import logging
import mimetypes
from .. import config

section = 'downloader'


class BaseDownloader:
    def __init__(self, extractor):
        self._session = extractor.session

        self._chunk_size = config.get(section, 'chunk_size')

    def download(self, url, path, options=None):
        self._preProgress()
        if options is None:
            options = {}
        total_size = None
        response = self._session.head(url)
        filename = self.getFilename(response, options.get('filename'))
        self._postProgress()

    def getFilename(self, response, filename=None):
        if filename:
            content_type = response.headers['Content-Type']
            filename = filename + mimetypes.guess_type(content_type)

        else:
            pass

        return filename

    def _preProgress(self):
        pass

    def _postProgress(self):
        pass
