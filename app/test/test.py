import requests
import mimetypes

url = 'https://www.bingwallpaperhd.com/wp-content/uploads/2019/06/BiwaLake.jpg'
session = requests.session()
response = session.head(url)
ct = response.headers.get('Content-Type')
ex=mimetypes.guess_extension(ct)
print(ex)
