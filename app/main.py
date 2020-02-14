import multiprocessing
import requests
import bs4
import os

# from app.extractor.bing import BingExtractor
from .extractor.konachan import KonachanExtractor
# from .extractor.wallpapercraft import WallpaperCraftExtractor
from .dowanloader.http import HttpDownloader
from .processor.common import Processor


processor = Processor()

# bing = BingExtractor()
konachan = KonachanExtractor()

downloader = HttpDownloader(konachan)
processor.submit(downloader.download, konachan)
