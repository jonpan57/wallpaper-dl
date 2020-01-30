import requests

session = requests.session()

url = 'https://www.bingwallpaperhd.com/wp-content/uploads/2019/06/BiwaLake.jpg'
response = session.head(url, timeout=10)

print(response)