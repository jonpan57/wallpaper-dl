# import requests
# import bs4
# import lxml
# import mimetypes
#
# url = 'https://www.bingwallpaperhd.com'
# session = requests.session()
# session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'
# session.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
#
#
# response=session.get(url)
# print(session.headers)
# print(response.text)

import logging


def testing():
    formatter = logging.Formatter('%(asctime)s - %(name)s - file:%(filename)s, line %(lineno)d, in %(module)s %(funcName)s')
    sh = logging.StreamHandler()

    sh.setFormatter(formatter)
    log = logging.getLogger('test123')
    log.setLevel(logging.DEBUG)
    log.addHandler(sh)
    log.info('test1')
    log.warning('test2')
    log.debug('test3')
    log.error('test4')


testing()
