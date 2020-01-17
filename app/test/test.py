import requests
import bs4
import lxml
import mimetypes

url = 'https://www.bingwallpaperhd.com/page/427'
response = requests.get(url)
bs = bs4.BeautifulSoup(response.text, 'lxml')
next = bs.find('a', class_='next page-numbers')
print(next)

i = mimetypes.guess_type(None)
print(i)
