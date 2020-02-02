import multiprocessing
import requests
import bs4
import os

from app.extractor.bing import BingExtractor
# from app.extractor.konachan import KonachanExtractor
from app.dowanloader.http import HttpDownloader
from app.processor.common import Processor

bing = BingExtractor()
downloader = HttpDownloader(bing)
processor = Processor()
processor.submit(downloader.download, bing)

if __name__ == '__main__':
    pass
