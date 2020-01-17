import multiprocessing
import requests
import bs4
import os

from app.extractor.bing import BingExtractor
from app.dowanloader.http import HttpDownloader

bing = BingExtractor('https://www.bingwallpaperhd.com')
downloader = HttpDownloader(bing)

if __name__ == '__main__':
    pass
