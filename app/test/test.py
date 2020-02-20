import os
import bs4
import lxml
import json
import requests
import mimetypes
from tenacity import retry, stop_after_attempt

url = 'https://w.wallhaven.cc/full/vg/wallhaven-vgrwe8.jpg'
session = requests.session()
header = {'Range': 'bytes=564603-'}
try:
    response = session.head(url, headers=header, timeout=5)
except Exception as e:
    print(e)
print(response.status_code)
print(response.headers)
