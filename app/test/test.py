import os
import bs4
import lxml
import requests
import mimetypes

url = 'https://konachan.com/post?page=11335&tags='
html = requests.get(url)
bs = bs4.BeautifulSoup(html.text, 'lxml')
next_page = bs.find('a', class_='next_page')
# ul = bs.find_all('a', class_='directlink smallimg')
print(next_page)
