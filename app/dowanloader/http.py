import os
import requests

from tenacity import retry, stop_after_attempt
from .common import Downloader
from .. import util


class HttpDownloader(Downloader):
    def __init__(self, extractor):
        super().__init__(extractor)
        self.path_fmt = util.PathFormat(extractor)

    def _start_download(self, url, **options):
        response = self._get_response_header(url)

        if response is None:
            print(url + ' --> Request timeout by head')

        elif response.status_code == requests.codes.ok:
            pathname = self.path_fmt.format(response, options.get('path'), options.get('filename'))

            if response.headers.get('Accept-Ranges') == 'bytes':  # 支持断点续传的标志，同时也可以多线程下载
                total_size = self._get_file_size(response)
                self._range_download(url, pathname, total_size)

            elif response.headers.get('Transfer-Encoding') == 'chunked':
                pass
            else:
                pass

        else:
            print(url + ' --> Status code ' + str(response.status_code))

    def _range_download(self, url, pathname, total_size):
        try:
            temp_size = os.path.getsize(pathname)
        except FileNotFoundError:
            temp_size = -1

        if temp_size < total_size:
            print(temp_size + '<' + total_size)
            header = {'Range': 'bytes={}-'.format(temp_size)}
            response = self._get_response_body(url, stream=self._stream, verify=self._verify, headers=header)
            if response is None:
                print(url + ' --> Request Timeout By Get')
            else:
                self._write_file(response, pathname, 'ab')

        elif temp_size == total_size:
            pass

        else:
            response = self._get_response_body(url, stream=self._stream, verify=self._verify)
            if response is None:
                print(url + ' --> Request Timeout By Get')
            else:
                self._write_file(response, pathname, 'wb')

    def _chunked_download(self, url, path, filename):
        pass

    @retry(reraise=True, stop=stop_after_attempt(3))
    def _get_response_header(self, url):
        try:
            response = self.session.head(url, timeout=self._timeout)
            return response

        except Exception:
            return None

    @retry(reraise=True, stop=stop_after_attempt(3))
    def _get_response_body(self, url, stream, verify, header=None):
        try:
            response = self.session.get(url, stream=stream, verify=verify, headers=header)
            print('test')
            return response

        except Exception:
            return None

    @staticmethod
    def _get_file_size(response):  # 获取下载文件总大小
        if 'Content-Length' in response.headers:
            return int(response.headers.get('Content-Length'))
        else:
            return -1

    def _write_file(self, response, pathname, mode):
        with open(pathname, mode) as f:
            for chunk in response.iter_content(chunk_size=self._chunk_size):
                if chunk:
                    f.write(chunk)
