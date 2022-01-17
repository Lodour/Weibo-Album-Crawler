import logging

from scrapy import logformatter


class WeiboLogFormatter(logformatter.LogFormatter):
    """
    Set DropItem to the debug level because we need to drop a lot of items.
    """

    def dropped(self, item, exception, response, spider):
        formatter = super().dropped(item, exception, response, spider)
        formatter['level'] = logging.DEBUG
        return formatter
