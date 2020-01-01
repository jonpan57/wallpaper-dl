import requests
import re

content = 'inline; filename="SnowHare_ZH-CN9767012872_1920x1080.jpg"; filename*=utf-8''SnowHare_ZH-CN9767012872_1920x1080.jpg'
filename = re.search(r'filename="(.+?)"', content).group(0)
print(filename)
