import os
from typing import Type
from urllib.parse import urlparse

import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline

from weibo.items import ImageItem, VideoItem


class WeiboMediaPipelineMixin(object):
    """
    Mixin class for media pipelines.

    Set the `item_type` attribute to let the pipeline ignore other item types.
    """
    item_type: Type[scrapy.Item]

    def process_item(self, item, spider):
        if isinstance(item, self.item_type):
            return super().process_item(item, spider)
        return item


class WeiboImagesPipeline(WeiboMediaPipelineMixin, ImagesPipeline):
    """
    Pipeline to download images.

    Save images to "IMAGES_STORE / ID_NAME / MID_IMAGE.jpg"
    """

    item_type = ImageItem

    def file_path(self, request, response=None, info=None, *, item=None):
        uid, uname, mid = item['uid'], item['uname'], item['mid']
        filename = os.path.basename(urlparse(request.url).path)
        return os.path.join(f'{uid}_{uname}', f'{mid}_{filename}')


class WeiboVideosPipeline(WeiboMediaPipelineMixin, FilesPipeline):
    """
    Pipeline to download videos.

    Save videos to "FILES_STORE / ID_NAME / MID.mp4"
    """

    item_type = VideoItem

    def file_path(self, request, response=None, info=None, *, item=None):
        uid, uname, mid = item['uid'], item['uname'], item['mid']
        _, ext = os.path.splitext(urlparse(request.url).path)
        return os.path.join(f'{uid}_{uname}', f'{mid}{ext}')
