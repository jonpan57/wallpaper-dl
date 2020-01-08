# import os
#
# default_path = 'koanachan/'
# if not os.path.exists(default_path):
#     os.makedirs(default_path, exist_ok=True)

import requests
import mimetypes

# mt = mimetypes.guess_extension('image/jpeg')
session = requests.Session()
session.headers.clear()
print(session.headers)

# print(mt)
# print(mimetypes.guess_extension(resp.headers['Content-Type']))


# def test(a, b, **c):
#     print(a)
#     print(b)
#     print(c.get('test'))
#
#
# d = {'test': 123}
# test(1, 2)
