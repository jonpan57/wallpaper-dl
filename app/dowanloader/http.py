import os
import time
import requests

from .common import Downloader
from .. import log, config, util


class HttpDownloader(Downloader):
    subcategory = 'http'

    def __init__(self, extractor):
        super().__init__(extractor)
        self.log = log.Log(self.category + '.' + self.subcategory)
        self.config = config.Config('http')
        self.chunk_size = self.config['chunk-size']
        self.downloading = self.config['downloading', 'bool']
        self.rate = self.config['rate']

        self.retries = extractor._retries
        self.timeout = extractor._timeout
        self.verify = extractor._verify

        if self.retries < 0:
            self.verify = float('inf')

    def download(self, url, pathfmt):
        try:
            return self._start_download(url, pathfmt)
        except Exception:
            print()
            raise
        finally:
            if self.downloading and not self.temp:
                util.remove_file(pathfmt.temppath)

    def _start_download(self, url, pathfmt):
        response = None
        tries = 0
        msg = ''

        if self.temp:
            pathfmt.enable_temp(self.tempdir)

        while True:
            if tries:
                if response:
                    response.close()
                self.log.warning('{} ({}/{})'.format(msg, tries, self.retries))
                if tries > self.retries:
                    return False
            tries += 1
            # select the download mode by response

        response = self._request_head(url=url)
        if response:
            if response.status_code == requests.codes.ok:
                if response.headers.get('Transfer-Encoding') == 'chunked':
                    self._chunked_download(response, pathfmt)
                elif response.headers.get('Accept-Ranges') == 'bytes':
                    self._range_download(response, pathfmt)
                else:
                    pass
            else:
                print(url + ' --> status code ' + str(response.status_code))
        else:
            print(url + ' --> request timeout via head')

    def _range_download(self, response, pathfmt):
        url = response.requests.url

        # check total size
        if pathfmt.get('size'):
            total_size = int(pathfmt.get('size'))
        elif 'Content-Length' in response.headers:
            total_size = int(response.headers.get('Content-Length'))
        else:
            total_size = 0

        # check for .temp file
        temp_size = pathfmt.temp_size()

        if 0 < temp_size < total_size:
            header = {'Range': 'bytes={}-'.format(temp_size)}
            mode = 'ab'
        elif 0 < temp_size == total_size:
            pass

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

    def _end_download(self, url, path_fmt):
        md5 = path_fmt.md5sun()
        if self.md5 == md5:
            pass
