import requests
import tqdm
import re
import os

from .base import BaseDownloader


class Downloader(BaseDownloader):
    def __init__(self, url, path, filename=None):
        self.url = url  # 下载地址
        self.path = path  # 下载路径
        self.response = self.getResponse()  # 响应头
        self.filename = self.getFilename(filename)  # 文件名

    def getResponse(self):
        try:
            resp = requests.head(self.url, timeout=5)
        except:
            pass  # 判断是否能下载的，需补充
        else:
            return resp

    def getFilename(self, filename):  # 获取下载文件名的多种方式及优先级：用户自定义 > Content-Disposition > url路径定义
        if filename:  # 以后可以添加文件名合法性判断
            filename = filename
        elif 'Content-Disposition' in self.response.headers:
            content = self.response.headers.get('Content-Disposition')
            filename = re.search(r'filename="(.+?)"', content).group(1)
        else:
            filename = os.path.basename(self.url)

        return filename

    def getFilesize(self):  # 获取下载文件总大小
        if 'Content-Length' in self.response.headers:
            total_size = int(self.response.headers.get('Content-Length'))
        else:
            total_size = 0
        return total_size

    def donwload(self):  # 下载文件
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
