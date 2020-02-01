import requests

session = requests.session()

url = 'https://www.bingwallpaperhd.com/wp-content/uploads/2019/06/BiwaLake.jpg'
fmt = '{year}-{month}-{filename}'
lists = url.split('/')
print(lists)
print(lists[-3])
s=fmt.format(year=lists[-3], month=lists[-2], filename=lists[-1])
print(s)
