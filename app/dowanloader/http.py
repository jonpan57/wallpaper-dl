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

        response = self._request_head(url=url)

        if response is None:
            print(url + ' --> Request timeout by head')

        elif response.status_code == requests.codes.ok:
            pathname = self.path_fmt.format(response)

            if response.headers.get('Accept-Ranges') == 'bytes':  # 支持断点续传的标志，同时也可以多线程下载
                self._range_download(url, path_fmt)
            elif response.headers.get('Transfer-Encoding') == 'chunked':
                pass
            else:
                pass

        else:
            print(url + ' --> Status code ' + str(response.status_code))

    def _range_download(self, url, path_fmt):
        # check for .temp file
        temp_size = path_fmt.temp_size()
        if temp_size:
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

        elif code == 416 and current_size:
            pass
        else:
            pass  # to be added

        with pathfmt.open(mode) as file:

        if 0 <= temp_size < total_size:
            # header = {'Range': 'bytes={}-'.format(temp_size)}
            response = self._request_get(url=url, stream=self._stream, verify=self._verify)
            if response:
                self._write_file(response, pathname, 'wb')
            else:
                print(url + ' --> Request Timeout By Get')

        elif 0 < temp_size == total_size:
            pass

        else:
            response = self._request_get(url=url, stream=self._stream, verify=self._verify)
            if response:
                self._write_file(response, pathname, 'wb')
            else:
                print(url + ' --> Request Timeout By Get')

    def _chunked_download(self, url, path, filename):
        pass

    @retry(reraise=True, stop=stop_after_attempt(3))
    def _request_head(self, url):
        try:
            return self.session.head(url=url, timeout=self._timeout)

        except requests.exceptions as e:
            # self.log.warning(e)
            return False

    @retry(reraise=True, stop=stop_after_attempt(3))
    def _request_get(self, url, stream, verify, header=None):
        try:
            return self.session.get(url=url, stream=stream, verify=verify, headers=header, timeout=self._timeout)

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
