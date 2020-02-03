from concurrent.futures import ThreadPoolExecutor
from app import config


class Processor:
    category = 'processor'

    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=int(self.config('Max_workers')))

    def config(self, option, value=None):
        if value:
            config.write(self.category, option, value)
            return config.get(self.category, option)
        else:
            return config.get(self.category, option)

    def submit(self, func, extractor):
        for link in extractor.link_list:
            print(link)
            self.executor.submit(func, link)
