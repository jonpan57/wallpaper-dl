from concurrent.futures import ThreadPoolExecutor
from ..config import Config
from ..util import PathFormat


class Processor(Config):
    category = 'processor'

    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=int(self.config('MaxWorkers')))

    def submit(self, func, extractor):
        pathfmt = PathFormat(extractor)
        link = extractor.link

        self.executor.submit(func, link, pathfmt)


