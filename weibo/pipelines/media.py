import os
from typing import Type
from urllib.parse import urlparse

import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline

from weibo.items import ImageItem, VideoItem


class WeiboMediaPipelineMixin(object):
    item_type: Type[scrapy.Item]

    def process_item(self, item, spider):
        if isinstance(item, self.item_type):
            return super().process_item(item, spider)
        return item


class WeiboImagesPipeline(WeiboMediaPipelineMixin, ImagesPipeline):
    item_type = ImageItem

    def file_path(self, request, response=None, info=None, *, item=None):
        uid, uname, mid = item['uid'], item['uname'], item['mid']
        filename = os.path.basename(urlparse(request.url).path)
        return os.path.join(f'{uid}_{uname}', f'{mid}_{filename}')


class WeiboVideosPipeline(WeiboMediaPipelineMixin, FilesPipeline):
    item_type = VideoItem

    def file_path(self, request, response=None, info=None, *, item=None):
        uid, uname, mid = item['uid'], item['uname'], item['mid']
        _, ext = os.path.splitext(urlparse(request.url).path)
        return os.path.join(f'{uid}_{uname}', f'{mid}{ext}')
