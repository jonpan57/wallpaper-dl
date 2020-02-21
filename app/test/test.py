import os


url = 'https://w.wallhaven.cc/full/vg/wallhaven-vgrwe8.jpg'
root='/home/administrator/图片'

s=os.stat(url).st_size
print(s)