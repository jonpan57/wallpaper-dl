import os
import re
import hashlib
import mimetypes


class PathFormat:
    def __init__(self, extractor):
        self.filename_fmt = extractor.filename_fmt
        self.directory_fmt = extractor.directory_fmt

        try:
            self.filename = extractor.filename
        except AttributeError:
            return None

        self.extension = ''

    def format(self, response, path, filename):
        path = self._get_file_path(path)
        filename = self._get_file_name(response, filename)
        return path + filename

    def set_extension(self, extension, real=True):
        if real:
            self.extension = extension

    def enable_temp(self, temp_directory=None):
        if self.extension:
            self.temp_path += '.temp'
        else:
            self.set_extension('temp', False)
            if temp_directory:
                self.temp_path = os.path.join(temp_directory, os.path.basename(self.temp_path))

    def temp_size(self):
        try:
            return os.stat(self.temp_path).st_size
        except OSError:
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


def remove_file(path):
    try:
        os.unlink(path)
    except OSError:
        pass
