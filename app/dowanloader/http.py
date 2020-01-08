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
            file_path = self._get_file_path(options.get('path'))
            file_name = self._get_file_name(response, options.get('filename'))
            if response.headers.get('Accept-Ranges') == 'bytes':  # 支持断点续传的标志，同时也可以多线程下载
                total_size = self._get_file_size(response)

        else:
            print(url + ' --> Status Code ' + response.status_code)

    def _get_response(self, url):
        try:
            response = self.session.head(url, timeout=self.timeout)

        except ConnectionError:
            print(url + ' --> Connection Timeout !')
            return None

        else:
            return response

    def _get_file_path(self, path):
        if path:
            if not os.path.exists(self.path):
                os.makedirs(self.path, exist_ok=True)
            return path

        else:
            return self.default_path

    def _get_file_name(self, response, filename):
        # 获取下载文件名的多种方式及优先级：用户自定义 > Content-Disposition > url路径定义
        if filename:
            suffix = mimetypes.guess_type(response.headers.get('Content-Type'))
            return filename + suffix

        elif 'Content-Disposition' in response.headers:
            disposition = response.headers.get('Content-Disposition')
            return re.search(r'filename="(.+?)"', disposition).group(1)

        else:
            return os.path.basename(response.request.url)

    def _get_file_size(self):  # 获取下载文件总大小
        if 'Content-Length' in self.response.headers:
            total_size = int(self.response.headers.get('Content-Length'))
        else:
            total_size = 0
        return total_size

    def _range_download(self, url, path, filename):
        pass

    def _chunked_download(self, url, path, filename):
        pass

    def downloading(self):  # 下载文件
        chunk_size = 1024  # 设置每次写入块大小
        total_size = self.getFilesize()  # 关于从网页得到文件大小为零的情况，还需要再判断，后期补充

        print(self.filename)

        if os.path.exists(self.path + self.filename):  # 文件存在，判断是否需要断点续传
            temp_size = os.path.getsize(self.path + self.filename)  # 获取当前文件大小

            if temp_size == total_size:  # 通过比较文件大小，判断是否下载完成
                pass

            else:  # 文件未下载完全，开始断点续传
                header = {'Range': 'bytes={}-'.format(temp_size)}
                resp = requests.get(self.url, stream=True, verify=False, headers=header)
                with tqdm.tqdm(range(0, total_size), ascii=True) as pbar:  # 显示进度条
                    pbar.update(temp_size)
                    with open(self.path + self.filename, 'ab') as f:
                        for chunk in resp.iter_content(chunk_size=chunk_size):
                            if chunk:
                                pbar.update(len(chunk))
                                f.write(chunk)
                                f.flush()

        else:  # 文件不存在，开始下载
            resp = requests.get(self.url, stream=True, verify=False)
            with tqdm.tqdm(range(0, total_size), ascii=True) as pbar:  # 显示进度条
                with open(self.path + self.filename, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=chunk_size):
                        if chunk:
                            pbar.update(len(chunk))
                            f.write(chunk)
                            f.flush()
