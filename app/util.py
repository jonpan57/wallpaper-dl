import os


class PathFormat:
    def __init__(self, extractor):
        self.session = extractor.session
        self.default_path = extractor.config('default_path')
        self.file_path = None
        self.file_name = None

    def _get_file_path(self, path):
        if path:
            if not os.path.exists(self):
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
