import os
import bs4
import lxml
import requests
import mimetypes
from retrying import retry

url = 'https://konachan.org'


@retry(stop_max_attempt_number=3)
def get_head():
    session = requests.session()
    response = session.head(url, timeout=3)
    print(1)


get_head()
