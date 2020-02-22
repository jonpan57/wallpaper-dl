import os
import time
import requests

from tenacity import retry, stop_after_attempt
from .common import Downloader
from ..util import PathFormat


class HttpDownloader(Downloader):
    def __init__(self, extractor):
        super().__init__(extractor)

    def _start_download(self, url, path_fmt):
        # select the download mode by response
        response = self._request_head(url=url)
        if response:
            if response.status_code == requests.codes.ok:
                if response.headers.get('Transfer-Encoding') == 'chunked':
                    self._chunked_download(response, path_fmt)
                elif response.headers.get('Accept-Ranges') == 'bytes':
                    self._range_download(response, path_fmt)
                else:
                    pass
            else:
                print(url + ' --> status code ' + str(response.status_code))
        else:
            print(url + ' --> request timeout via head')

    def _range_download(self, response, path_fmt):
        url = response.requests.url

        # check content Length
        if path_fmt.get('size'):
            total_size = int(path_fmt.get('size'))
        elif 'Content-Length' in response.headers:
            total_size = int(response.headers.get('Content-Length'))
        else:
            total_size = 0

        # check for .temp file
        temp_size = path_fmt.temp_size()
        if temp_size:
            header = {'Range': 'bytes={}-'.format(temp_size)}

        if temp_size < total_size:
            header = {'Range': 'bytes={}-'.format(temp_size)}

        # connect to remote resources via head
        response = self._request_get(url=url, headers=header, stream=self._stream, verify=self._verify)

        # check response
        code = response.status_code
        if code == 200:
            offset = 0
            total_size = response.headers.get('Content-Length')

        elif code == 206:
            offset = temp_size
            total_size = response.headers["Content-Range"].rpartition("/")[2]

        elif code == 416 and temp_size:
            pass
        else:
            pass  # to be added

        with path_fmt.open(mode) as file:

        if 0 <= temp_size < total_size:
            # header = {'Range': 'bytes={}-'.format(temp_size)}
            response = self._request_get(url=url)
            if response:
                self._write_file(response, pathname, 'wb')
            else:
                print(url + ' --> Request Timeout By Get')

        elif 0 < temp_size == total_size:
            pass

        else:
            response = self._request_get(url=url)
            if response:
                self._write_file(response, pathname, 'wb')
            else:
                print(url + ' --> Request Timeout By Get')

    def _chunked_download(self, url, path, filename):
        pass

    @retry(reraise=True, stop=stop_after_attempt(3))
    def _request_head(self, url, header=None):
        try:
            return self.session.head(url=url, headers=header, timeout=self._timeout)
        except requests.exceptions as e:
            # self.log.warning(e)
            return False

    @retry(reraise=True, stop=stop_after_attempt(3))
    def _request_get(self, url, header=None):
        try:
            return self.session.get(url=url, headers=header, stream=self._stream, verify=self._verify,
                                    timeout=self._timeout)

        except requests.exceptions as e:
            # self.log.warning(e)
            return False

    @staticmethod
    def _get_file_size(response, filesize):  # 获取下载文件总大小
        if filesize:
            return filesize
        elif 'Content-Length' in response.headers:
            return int(response.headers.get('Content-Length'))
        else:
            return -1

    def receive(self, response, file):
        for data in response.iter_content(self.chunk_size):
            file.write(data)

    # def _receive_rate(self, response, file):
    #     t1 = time.time()
    #     rate = self.rate
    #
    #     for data in response.iter_content(self.chunk_size):
    #         file.write(data)
    #
    #         t2 = time.time()  # current time
    #         actual = t2 - t1  # actual elapsed time
    #         expected = len(data) / rate  # expected elapsed time
    #
    #         if actual < expected:
    #             # sleep if less time elapsed than expected
    #             time.sleep(expected - actual)
    #             t1 = time.time()
    #         else:
    #             t1 = t2

    def _end_download(self, url):
        pass
