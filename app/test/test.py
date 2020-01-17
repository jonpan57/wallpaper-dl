import requests
import bs4
import lxml

url = 'https://www.bingwallpaperhd.com/page/427'
response = requests.get(url)
bs = bs4.BeautifulSoup(response.text, 'lxml')
next = bs.find('a', class_='next page-numbers')
print(next)
