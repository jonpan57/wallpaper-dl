import requests
import bs4
import lxml
import mimetypes

url = 'https://www.bingwallpaperhd.com/wp-content/uploads/2019/11/QueenVictoriaAgave.jpg'
session = requests.session()
session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'
session.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'

session.get(url)
print(session.headers)
session.headers.update({'Range': 'bytes=0-'})
session.get(url)
print(session.headers)
session.headers.pop('Range')
session.get(url)
print(session.headers)
