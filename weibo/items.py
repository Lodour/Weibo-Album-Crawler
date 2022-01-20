# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    uuid = scrapy.Field()  # as the cache key
    filename = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
