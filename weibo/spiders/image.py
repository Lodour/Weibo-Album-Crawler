import os.path
from urllib.parse import urlparse

import scrapy

from weibo import api
from weibo import configs
from weibo.items import ImageItem


class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['weibo.com']
    media_cache_key = 'pid'

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

        # yield all images
        for image in data['list']:
            pid, mid = image['pid'], image['mid']
            yield ImageItem(uid=uid, uname=uname, mid=mid, pid=pid, image_urls=[api.large_image(pid)])
