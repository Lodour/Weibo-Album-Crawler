# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import os
from urllib.parse import urlparse

from scrapy.pipelines.images import ImagesPipeline


class WeiboPipeline:
    def process_item(self, item, spider):
        return item


class WeiboImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        uid, uname, mid = item['uid'], item['uname'], item['mid']
        filename = os.path.basename(urlparse(request.url).path)
        return os.path.join(f'{uid}_{uname}', f'{mid}_{filename}')
