import requests

session = requests.Session()
resp = session.get('https://bing.ioliu.cn/')

print(resp.cookies)
