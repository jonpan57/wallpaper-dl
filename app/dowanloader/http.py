import os
import re
import tqdm
import requests
import mimetypes

from .base import Downloader
from .. import util


class HttpDownloader(Downloader):
    def __init__(self, extractor):
        super().__init__(extractor)
        self.pathfmt = util.PathFormat(extractor)

    def download(self, url, **options):
        response = self._get_response(url)

        if response and response.status_code == requests.codes.ok:
            pathname = self.pathfmt.format(response, options.get('path'), options.get('filename'))
            if response.headers.get('Accept-Ranges') == 'bytes':  # 支持断点续传的标志，同时也可以多线程下载
                total_size = self._get_file_size(response)
                self._range_download(url, pathname, total_size)
            else:
                pass
        else:
            print(url + ' --> Status Code ' + response.status_code)

    def _get_response(self, url):
        try:
            response = self.session.head(url, timeout=self._timeout)

        except ConnectionError:
            print(url + ' --> Connection Timeout !')
            return None

        else:
            return response

    def _get_file_size(self):  # 获取下载文件总大小
        if 'Content-Length' in self.response.headers:
            total_size = int(self.response.headers.get('Content-Length'))
        else:
            total_size = 0
        return total_size

    def _range_download(self, url, pathname, total_size):
        if os.path.exists(pathname):
            temp_size = os.path.getsize(pathname)
            if temp_size == total_size:
                pass
            else:
                header = {'Range': 'bytes={}-'.format(temp_size)}
                response = self.session.get(url=url, headers=header)
                with open(pathname, 'ab') as f:
                    for chunk in response.iter_content(chunk_size=self.chunk_size):
                        if chunk:
                            f.write(chunk)
                            f.flush()
        else:
            response = self.session.get(url=url)
            with open(pathname, 'wb') as f:
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        f.write(chunk)
                        f.flush()

    def _chunked_download(self, url, path, filename):
        pass
