import os
import bs4
import lxml
import requests
import mimetypes

url = 'https://konachan.com/image/86b550ba08b89cbd8d44f208401ed52b/Konachan.com%20-%20299812%202girls%20animal%20bat%20cornelia_(girl_cafe_gun)%20girl_cafe_gun_(game)%20glasses%20halloween%20logo%20su_xiaozhen%20tagme_(artist).jpg'
headers = {'Range': 'bytes=845-'}
session = requests.session()
response = session.get(url, headers=headers)
print(response.headers)
