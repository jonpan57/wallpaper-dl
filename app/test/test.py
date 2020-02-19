import os
import bs4
import lxml
import requests
import mimetypes
from tenacity import retry, stop_after_attempt

url = 'https://wallhaven.cc/search?categories=111&purity=111&sorting=date_added&order=desc&page=4'
session = requests.session()
login_url = 'https://wallhaven.cc/login'
response = session.get(login_url)
bs = bs4.BeautifulSoup(response.text, 'lxml')
temp = bs.find(name='input', attrs={'name': '_token'})
_token = temp.get('value')
data = {
    '_token': _token,
    'username': 'vergil',
    'password': '196900'
}
session.post('https://wallhaven.cc/auth/login', data=data)
login = session.get('https://wallhaven.cc/user/vergil')
print(login.text)
