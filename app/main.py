import multiprocessing
import requests
import bs4
import os

from .extractor.bing import BingExtractor
from .extractor.konachan import KonachanExtractor
from .extractor.wallpapercraft import WallpaperCraftExtractor
from .dowanloader.http import HttpDownloader
from .processor.common import Processor

processor = Processor()

bing = BingExtractor()
konachan = KonachanExtractor()
wallpapercraft = WallpaperCraftExtractor(resolution='1920x1080')

downloader = HttpDownloader(wallpapercraft)
processor.submit(downloader.download, wallpapercraft)

