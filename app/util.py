import os
import re
import hashlib
import mimetypes


class PathFormat:
    def __init__(self, extractor):
        self.path = extractor.config('Directory')
        try:
            self.filename = extractor.filename
        except AttributeError:
            return None

    def format(self, response, path, filename):
        path = self._get_file_path(path)
        filename = self._get_file_name(response, filename)
        return path + filename

    def temp_size(self):
        try:
            return os.path.getsize(self.temp_path)
        except FileNotFoundError:
            return 0

    def open(self, mode='wb'):
        return open(self.temp_path, mode)

    def md5sum(self, pathname):
        with open(pathname, 'rb') as f:
            m = hashlib.md5()
            m.update(f.read())
            return m.hexdigest()

    def _get_file_path(self, path):
        # 还需添加自定义路径合法性检查
        if not path:
            path = self.path
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def _get_file_name(self, response, filename):  # 获取下载文件名的多种方式及优先级，从上往下
        if filename:  # 用户自定义
            extension = mimetypes.guess_extension(response.headers.get('Content-Type'))
            return filename + extension

        elif self.filename:  # 默认定义
            return self.filename(response)

        elif 'Content-Disposition' in response.headers:  # 响应头定义
            return re.search(r'filename="(.+?)"', response.headers.get('Content-Disposition')).group(1)

        else:  # url路径定义
            return os.path.basename(response.request.url)


class Match:
    def __init__(self, **options):
        self.options = options
