import os
import time
import requests

from .common import Downloader
from .. import config, util, text


class HttpDownloader(Downloader):
    subcategory = 'http'

    def __init__(self, job):
        super().__init__(job)
        extractor = job.extractor
        self.config = config.Config('http')
        self.chunk_size = self.config['chunk-size']
        self.downloading = self.config['downloading', 'bool']  #
        self.adjust_extensions = self.config['adjust-extensions', 'bool']  # 调整后缀
        self.min_size = self.config['filesize-min', 'int']
        self.max_size = self.config['filesize-max', 'int']
        self.mtime = self.config['mtime', 'bool']
        self.rate = self.config['rate']

        self.retries = extractor._retries
        self.timeout = extractor._timeout
        self.stream = extractor._stream
        self.verify = extractor._verify

        if self.retries < 0:
            self.verify = float('inf')

        if self.min_size:
            min_size = text.parse_bytes(self.min_size)
            if not min_size:
                self.log.warning('无效的最小文件大小（{}）'.format(self.min_size))
            self.min_size = min_size
        if self.maxsize:
            maxsize = text.parse_bytes(self.maxsize)
            if not maxsize:
                self.log.warning('无效的最大文件大小（{}）'.format(self.maxsize))
            self.maxsize = maxsize
        if self.rate:
            rate = text.parse_bytes(self.rate)
            if rate:
                if rate < self.chunk_size:
                    self.chunk_size = rate
                self.rate = rate
                self.receive = self._receive_rate
            else:
                self.log.warning('无效的下载速度限制（{}）'.format(self.rate))

    def download(self, url, path):
        try:
            return self._start_download(url, path)
        except Exception:
            print()
            raise
        finally:
            if self.downloading and not self.temp:
                util.remove_file(path.temp_path)

    def _start_download(self, url, path):
        response = None
        tries = 0
        msg = ''

        if self.temp:
            path.enable_temp(self.temp_dir)

        while True:
            if tries:
                if response:
                    response.close()
                self.log.warning('{} ({}/{})'.format(msg, tries, self.retries))
                if tries > self.retries:
                    return False
                time.sleep(tries)
            tries += 1
            # select the download mode by response

            response = self._request_head(url=url)
            if response:
                if response.status_code == requests.codes.ok:
                    if response.headers.get('Transfer-Encoding') == 'chunked':
                        self._chunked_download(response, path)
                    elif response.headers.get('Accept-Ranges') == 'bytes':
                        self._range_download(response, path)
                    else:
                        pass
                else:
                    print(url + ' --> status code ' + str(response.status_code))
            else:
                print(url + ' --> request timeout via head')

    def _range_download(self, response, path):
        url = response.requests.url

        # check total size
        if path.get('size'):
            total_size = int(path.get('size'))
        elif 'Content-Length' in response.headers:
            total_size = int(response.headers.get('Content-Length'))
        else:
            total_size = 0

        # check for .temp file
        temp_size = path.temp_size()

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

    def _receive_rate(self, response, file):
        t1 = time.time()
        rate = self.rate

        for data in response.iter_content(self.chunk_size):
            file.write(data)

            t2 = time.time()  # 当前时间
            actual = t2 - t1  # 实际经过的时间
            expected = len(data) / rate  # 预期经过的时间

            if actual < expected:
                # 如果期望大于实际，则sleep一段时间
                time.sleep(expected - actual)
                t1 = time.time()
            else:
                t1 = t2

    def _end_download(self, url, path):  # 完成下载后对文件完整性的校验
        md5 = path.md5sun()
        if self.md5 == md5:
            pass
