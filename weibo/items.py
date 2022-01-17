# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ImageItem(scrapy.Item):
    uid = scrapy.Field()
    uname = scrapy.Field()
    mid = scrapy.Field()
    pid = scrapy.Field()

    image_urls = scrapy.Field()
    images = scrapy.Field()
