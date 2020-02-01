import os
import re
import mimetypes


class PathFormat:
    def __init__(self, extractor):
        self.session = extractor.session
        self.path = extractor.config('Directory')
        self.filename = extractor.filename

    def format(self, response, path=None, filename=None):
        path = self._get_file_path(path)
        filename = self._get_file_name(response, filename)
        return path + filename

    def _get_file_path(self, path):
        # 还需添加自定义路径合法性检查
        if path is None:
            path = self.path
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def _get_file_name(self, response, filename):
        # 获取下载文件名的多种方式及优先级：用户自定义 > Content-Disposition > url路径定义
        if filename or self.filename:
            if filename is None:
                filename = self.filename
            extension = mimetypes.guess_type(response.headers.get('Content-Type'))
            return filename + extension

        elif 'Content-Disposition' in response.headers:
            disposition = response.headers.get('Content-Disposition')
            return re.search(r'filename="(.+?)"', disposition).group(1)

        else:
            return os.path.basename(response.request.url)
