import os
import bs4
import lxml
import requests
import mimetypes
from tenacity import retry, stop_after_attempt

url = 'https://konachan.com/jpeg/60febdadab2abefb56606d1a3ed6d6f7/Konachan.com%20-%20299490%20bow%20breasts%20brown_eyes%20brown_hair%20close%20nipples%20open_shirt%20original%20petals%20school_uniform%20sourenkio%20twintails.jpg '


@retry(reraise=True, stop=stop_after_attempt(3))
def get_response_header(url):
    try:
        session = requests.session()
        response = session.head(url, timeout=3)
        return response

    except Exception:
        return None


resp = get_response_header(url)
print(resp.headers)
