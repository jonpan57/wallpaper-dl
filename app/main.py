import multiprocessing
import requests
import bs4
import os



# https://blog.csdn.net/freeking101/article/details/62227161


def findMaxPage(url, tag, keyword, ext='span'):  # 通过首页找到最大页数
    html = requests.get(url)
    bs = bs4.BeautifulSoup(html.text, 'lxml')
    text = bs.find(tag, class_=keyword).find(ext).get_text()
    max_page = int(text.split('/')[1])

    return max_page


def getLinks(url, max_page):  # 获取所有图片下载链接
    links = []
    for i in range(1, max_page + 1):
        href = url + "/?p=" + str(i)
        html = requests.get(href)
        bs = bs4.BeautifulSoup(html.text, 'lxml')
        tags = bs.find_all('a', class_='ctrl download')
        for tag in tags:
            links.append(url + tag.get('herf'))

    return links


def startDown(links, path):
    pool = multiprocessing.Pool(processes=10)

    for link in links:
        down = Downloader(link, path)
        pool.apply(down.donwload)
    pool.close()
    pool.join()


if __name__ == '__main__':
    url = 'https://bing.ioliu.cn'
    path = 'Wallpager/'

    max_page = findMaxPage(url, 'div', 'page')
    links = getLinks(url, max_page)

    startDown(links, path)
    os.system('pause')
