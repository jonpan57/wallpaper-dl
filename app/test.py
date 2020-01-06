import requests
import mimetypes

# mt = mimetypes.guess_extension('image/jpeg')
# session = requests.Session()
# resp = session.head(
#     'https://konachan.com/jpeg/5496bc9c1f16125a94054fc6a3b3f31f/Konachan.com%20-%20297584%20fromage_tart%20saigyouji_yuyuko_%28living%29%20touhou.jpg')
#
# print(mt)
# print(mimetypes.guess_extension(resp.headers['Content-Type']))
# print(resp.cookies)


# def test(a, b, **c):
#     print(a)
#     print(b)
#     print(c.get('test'))
#
#
# d = {'test': 123}
# test(1, 2)

import os
from . import config

default_path = config.get('downloader', 'default_path')
if not os.exists(default_path):
    os.makedirs(default_path, exists=True)
