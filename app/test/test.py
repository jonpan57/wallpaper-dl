import os
import requests

url = 'https://wallhaven.cc/auth/login'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0'}
session = requests.session()

data = {'username': 'vergil', 'password': '196900', '_token': 'UZptRapCZS6PN2ZBQEzaSzYwtAlfCtNr4iJovwLQ'}
response = session.post(url, data=data, headers=headers)
cookiss = response.cookies
print(cookiss)
