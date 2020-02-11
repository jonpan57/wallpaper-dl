import os
import bs4
import lxml
import requests
import mimetypes
from tenacity import retry, stop_after_attempt

url = 'https://konachan.org'


@retry(reraise=True, stop=stop_after_attempt(3))
def get_head():
    try:
        session = requests.session()
        response = session.head(url, timeout=3)
        return response
    except Exception as e:
        return None


s = get_head()
print(int(s))

