import os
import hashlib

url = 'https://w.wallhaven.cc/full/vg/wallhaven-vgrwe8.jpg'
root = '/home/administrator/PycharmProjects/wallpager-download-tool/app/test/Konachan.com - 301361 breast_grab breasts cum tagme_(artist) tagme_(character).jpg'


def md5sum(filename):
    with open(filename, 'rb') as f:
        m = hashlib.md5()
        m.update(f.read())
        return m.hexdigest()


md5 = md5sum(root)
print(md5)
