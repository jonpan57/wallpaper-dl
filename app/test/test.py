import os
import bs4
import lxml
import requests
import mimetypes
from tenacity import retry, stop_after_attempt

url = 'https://www.bingwallpaperhd.com/wp-content/uploads/2018/08/ArcticFoxSibs.jpg'

root = '/home/manjaro/图片/gallery/bing/201808-ArcticFoxSibs.jpg'

session = requests.session()
headers = session.headers
headers.clear()
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
headers['Accept'] = '*/*'
headers['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
headers['Accept-Encoding'] = 'gzip, deflate'
headers['Connection'] = 'keep-alive'
headers['Upgrade-Insecure-Requests'] = '1'

session.head('https://www.bingwallpaperhd.com')

print(session.headers)
resp = session.get(url=url, stream=True, verify=False)

with open(root, 'wb') as f:
    for chunk in resp.iter_content(chunk_size=16384):
        if chunk:
            f.write(chunk)
            f.flush()
