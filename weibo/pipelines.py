import os
import pickle

from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline


class WeiboMediaPipeline(FilesPipeline):
    """
    Pipeline to download media files with specified filename.
    """

    def file_path(self, request, response=None, info=None, *, item=None):
        return item['filename']


class BaseMediaKeyCachePipeline(object):
    """
    Base class for key-cache pipelines.

    This pipeline cache keys of downloaded images / videos, so they will not be downloaded even if you deleted them.
    Useful if you want to delete unwanted files forever.
    """

    # do we need to load existing key cache?
    preload_cache: bool

    def __init__(self, cache_file: str):
        self.cache_file = cache_file
        self.keys_seen = self.load_cache() if self.preload_cache else set()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings['CACHE_FILE'])

    def load_cache(self):
        cache = set()
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'rb') as fp:
                cache = pickle.load(fp)
        return cache


class MediaKeyDuplicatesPipeline(BaseMediaKeyCachePipeline):
    """
    Pipeline to drop items having cached keys.
    Must be placed BEFORE downloading pipelines.
    """

    # preload cache to check duplicates
    preload_cache = True

    def process_item(self, item, spider):
        if item['uuid'] in self.keys_seen:
            raise DropItem(f'Duplicate media key found in item.')
        return item


class MediaKeyCachePipeline(BaseMediaKeyCachePipeline):
    """
    Pipeline to cache keys of newly downloaded items.
    Must be placed AFTER downloading pipelines.
    """

    # no need to preload cache for updating
    preload_cache = False

    def close_spider(self, spider):
        cache = self.keys_seen | self.load_cache()
        with open(self.cache_file, 'wb') as fp:
            pickle.dump(cache, fp)

    def process_item(self, item, spider):
        if item['files']:
            self.keys_seen.add(item['uuid'])
        return item
