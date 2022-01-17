import logging

from scrapy import logformatter


class WeiboLogFormatter(logformatter.LogFormatter):

    def dropped(self, item, exception, response, spider):
        formatter = super().dropped(item, exception, response, spider)
        formatter['level'] = logging.DEBUG
        return formatter
