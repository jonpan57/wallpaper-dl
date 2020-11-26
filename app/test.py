import requests

response = requests.request('GET', 'https://wallhaven.cc')
print(response.reason)
