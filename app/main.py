import multiprocessing
import requests
import bs4
import os

# from app.extractor.bing import BingExtractor
from .extractor.konachan import KonachanExtractor
from .dowanloader.http import HttpDownloader
from .processor.common import Processor

konachan = KonachanExtractor()
downloader = HttpDownloader(konachan)
processor = Processor()
processor.submit(downloader.download, konachan)


