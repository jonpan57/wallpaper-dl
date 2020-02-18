from .common import Extractor


class BingExtractor(Extractor):
    filename_fmt = '{year}{month}-{filename}'

    def __init__(self):
        super().__init__()
        self.category = 'bing'
        self.url = self.config('Root')

    def filename(self, response):
        filename = response.request.url.split('/')
        return self.filename_fmt.format(year=filename[-3], month=filename[-2], filename=filename[-1])

    def _find_page_links(self, bs):
        links = bs.find_all('img', class_='alignleft wp-post-image')
        for link in links:
            temp = link.get('src')
            self.links.append(temp.replace('-300x200', ''))

    @staticmethod
    def _find_next_page(bs):
        next_page = bs.find('a', class_='next page-numbers')
        if next_page:
            return next_page.get('href')
        else:
            return None
