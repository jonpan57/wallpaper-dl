import requests

url1 = 'https://wallhaven.cc/api/v1/w/l395qq'
url2 = 'https://wallhaven.cc/api/v1/w/l395qq'
session = requests.Session()
response = session.get(url1)
print(response.history)
response=session.get(url2)
print(response.reason)