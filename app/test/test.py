import os
import bs4
import lxml
import requests
import mimetypes
from tenacity import retry, stop_after_attempt

url = 'https://wallpaperscraft.com'
resolution = '1280x720'
links = []
response = requests.get(url)
bs = bs4.BeautifulSoup(response.text, 'lxml')
link_list = bs.find_all('img', class_='wallpapers__image')

for link in link_list:
    temp = link.get('src')
    links.append(temp.replace('300x168', resolution))

s='https://images.wallpaperscraft.com/image/pens_pencils_multicolor_160648_1920x1080.jpg'
p=s.split('_')
print(p[-2])