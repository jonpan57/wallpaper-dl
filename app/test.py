import requests, requests.utils

url = 'https://wallhaven.cc'
session = requests.Session()
response = session.get(url)
cook = requests.utils.dict_from_cookiejar(response.cookies)
print(cook)
