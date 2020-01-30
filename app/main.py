import multiprocessing
import requests
import bs4
import os

from app.extractor.bing import BingExtractor
from app.extractor.konachan import KonachanExtractor
from app.dowanloader.http import HttpDownloader

bing = BingExtractor()
# downloader = HttpDownloader(bing)

# konachan = KonachanExtractor('https://www.konachan.com')

if __name__ == '__main__':
    pass
