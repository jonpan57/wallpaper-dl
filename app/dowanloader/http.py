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
            print(url + ' --> Request Timeout')

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
            print(url + ' --> Status Code ' + str(response.status_code))

    @retry(stop=stop_after_attempt(super()._retries))
    def _get_response_header(self, url):
        try:
            response = self.session.head(url, timeout=self._timeout)
            return response

        except Exception:
            return None

    @retry(stop=stop_after_attempt(super()._retries))
    def _get_response_body(self, url, stream, verify, header=None):
        try:
            response = self.session.get(url, stream=stream, verify=verify, headers=header)
            return response
        except Exception:
            return None

    @staticmethod
    def _get_file_size(response):  # 获取下载文件总大小
        if 'Content-Length' in response.headers:
            return int(response.headers.get('Content-Length'))
        else:
            return 0

    def _range_download(self, url, pathname, total_size):
        retries = self._retries
        if os.path.exists(pathname):
            temp_size = os.path.getsize(pathname)
            if temp_size < total_size:
                header = {'Range': 'bytes={}-'.format(temp_size)}
                while retries:
                    try:
                        response = self.session.get(url, stream=self._stream, verify=self._verify, headers=header)
                        with open(pathname, 'ab') as f:
                            for chunk in response.iter_content(chunk_size=self._chunk_size):
                                if chunk:
                                    f.write(chunk)
                                    f.flush()
                    except Exception:
                        retries -= 1
                    else:
                        retries = 0
            else:
                pass
        else:
            while retries:
                try:
                    response = self.session.get(url, stream=self._stream, verify=self._verify)
                    with open(pathname, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=self._chunk_size):
                            if chunk:
                                f.write(chunk)
                                f.flush()
                except Exception:
                    retries -= 1
                else:
                    retries = 0

    def _chunked_download(self, url, path, filename):
        pass
