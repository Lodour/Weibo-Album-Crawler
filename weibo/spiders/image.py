import os.path
from collections import defaultdict
from urllib.parse import urlparse

import scrapy

from weibo import api
from weibo import configs
from weibo.items import ImageItem


class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['weibo.com']

    def start_requests(self):
        for target in configs.TARGETS:
            uid = os.path.basename(urlparse(target.rstrip('/')).path)
            yield scrapy.Request(api.info(uid), callback=self.parse_info)

    def parse_info(self, response):
        user = response.json()['user']
        uid, uname = user['id'], user['screen_name']
        meta = {'uid': uid, 'uname': uname}
        yield scrapy.Request(api.get_image_wall(uid), callback=self.parse_image_wall, meta=meta)

    def parse_image_wall(self, response):
        # prepare data
        data = response.json()
        uid, uname = response.meta['uid'], response.meta['uname']

        # continue to next page
        since = data['since_id']
        yield scrapy.Request(api.get_image_wall(uid, since), callback=self.parse_image_wall, meta=response.meta)

        # collect images by mid
        image_urls_of_mid = defaultdict(list)
        for image in data['list']:
            pid, mid = image['pid'], image['mid']
            image_urls_of_mid[mid].append(api.large_image(pid))

        # yield images by mid
        for mid, image_urls in image_urls_of_mid.items():
            yield ImageItem(uid=uid, uname=uname, mid=mid, image_urls=image_urls)
