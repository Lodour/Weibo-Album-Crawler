import os.path
from urllib.parse import urlparse

import scrapy

from weibo import api, utils
from weibo import configs
from weibo.items import WeiboItem


class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['weibo.com']

    def start_requests(self):
        for target in configs.TARGETS:
            uid = os.path.basename(urlparse(target.rstrip('/')).path)
            yield scrapy.Request(api.info(uid), callback=self.parse_info)

    def parse_info(self, response):
        # prepare data
        user = response.json()['user']
        uid, uname = user['id'], user['screen_name']

        # prepare user folder
        folder = utils.prepare_folder(uid, uname, configs.STORE_PATH)

        # start from the 1st page
        meta = {'uid': uid, 'folder': folder}
        yield scrapy.Request(api.get_image_wall(uid), callback=self.parse_image_wall, meta=meta)

    def parse_image_wall(self, response):
        # prepare data
        data = response.json()
        uid, folder = response.meta['uid'], response.meta['folder']

        # continue to next page
        since = data['since_id']
        yield scrapy.Request(api.get_image_wall(uid, since), callback=self.parse_image_wall, meta=response.meta)

        # yield all images
        self.logger.info(f'{folder} found {len(data["list"]):2d} images (from {response.url})')
        for image in data['list']:
            pid, mid = image['pid'], image['mid']
            filename = f'{folder}/{mid}_{pid}.jpg'
            yield WeiboItem(uuid=pid, filename=filename, file_urls=[api.large_image(pid)])
