from concurrent.futures import ThreadPoolExecutor
from app.config import Config


class Processor(Config):
    category = 'processor'

    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=int(self.config('MaxWorkers')))

    def submit(self, func, extractor):
        while extractor.next():
            for link in extractor.links:
                self.executor.submit(func, link)
