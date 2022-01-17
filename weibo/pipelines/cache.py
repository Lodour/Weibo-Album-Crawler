import os
import pickle

from scrapy.exceptions import DropItem


class BaseMediaKeyPipeline(object):
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


class MediaKeyDuplicatesPipeline(BaseMediaKeyPipeline):
    preload_cache = True

    def process_item(self, item, spider):
        key = item.get(spider.media_cache_key)
        if key in self.keys_seen:
            raise DropItem(f'Duplicate media key found in item.')
        return item


class MediaKeyCachePipeline(BaseMediaKeyPipeline):
    preload_cache = False

    def close_spider(self, spider):
        cache = self.keys_seen | self.load_cache()
        with open(self.cache_file, 'wb') as fp:
            pickle.dump(cache, fp)

    def process_item(self, item, spider):
        if item.get(spider.media_results_key):
            key = item.get(spider.media_cache_key)
            self.keys_seen.add(key)
        return item
