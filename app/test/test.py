import os


# import hashlib
#
# url = 'https://w.wallhaven.cc/full/vg/wallhaven-vgrwe8.jpg'
# root = '/home/administrator/PycharmProjects/wallpager-download-tool/app/test/Konachan.com - 301361 breast_grab breasts cum tagme_(artist) tagme_(character).jpg'
#
#
# def md5sum(filename):
#     with open(filename, 'rb') as f:
#         m = hashlib.md5()
#         m.update(f.read())
#         return m.hexdigest()
#
#
# md5 = md5sum(root)
# print(md5)

class Test:
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        return self.data


test = Test('test')
s = test
print(s)