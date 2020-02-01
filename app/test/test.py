import requests

session = requests.session()

url = 'https://www.bingwallpaperhd.com/wp-content/uploads/2019/06/BiwaLake.jpg'
session.headers.update({'Range':'1'})
print(session.headers)
session.headers.pop('Range')
print(session.headers)
