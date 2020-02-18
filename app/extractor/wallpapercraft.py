import os
import mimetypes

from .common import Extractor


class WallpaperCraftExtractor(Extractor):
    filename_fmt = '{id}_{resolution}{extension}'

    def __init__(self, catalog=None, sort=None, resolution=None):
        super().__init__()
        self.category = 'wallpapercraft'
        self.root = self.config('Root')

        if resolution:
            self.resolution = resolution
        else:
            self.resolution = '1280x720'

        if catalog or sort or resolution:
            if catalog:
                self.url = self.root + '/catalog/' + catalog
            else:
                self.url = self.root + '/all'
            if sort:
                self.url += '/' + sort
            if resolution:
                self.url += '/' + resolution
        else:
            self.url = self.root

    def filename(self, response):
        filename = os.path.basename(response.request.url).split('_')
        extension = mimetypes.guess_extension(response.headers.get('Content-Type'))
        return self.filename_fmt.format(id=filename[-2], resolution=self.resolution, extension=extension)

    def _find_page_links(self, bs):
        links = bs.find_all('img', class_='wallpapers__image')
        for link in links:
            temp = link.get('src')
            self.links.append(temp.replace('300x168', self.resolution))

    def _find_next_page(self, bs):
        next_page = bs.find('li', class_='pager__item_selected').find_next_sibling()
        if next_page:
            return self.root + next_page.a.get('href')
        else:
            return None
