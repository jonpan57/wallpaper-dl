import requests
import os

path = 'teat/aab/bet/'
filename = 'text.txt'
if not os.path.exists(path):
    os.makedirs(path, exist_ok=True)
with open(path + filename, 'wb') as f:
    f.write(b'a')
