# Scrapy settings for weibo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'weibo'

SPIDER_MODULES = ['weibo.spiders']
NEWSPIDER_MODULE = 'weibo.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'weibo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'weibo.middlewares.WeiboSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'weibo.middlewares.WeiboDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'weibo.pipelines.WeiboImagesPipeline': 300,
}
IMAGES_STORE = './downloads'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

COOKIES = 'SINAGLOBAL=3842938301320.924.1638566098736; ULV=1638566098739:1:1:1:3842938301320.924.1638566098736:; XSRF-TOKEN=GPWRZkZV7omrKE5eNWVS-zP5; SSOLoginState=1642300421; WBPSESS=RfOIj0SLh4cA64kv9ZQrIi2LFOfYQEfchRcuKqxkKTkAKkiqqCssJhAKgQdN64N3Ltg9p4z_JRHp-symzbopvxwCN85jm1FCIVzMMYKLkql8nmAqILP4NI4PADDR8u-e-9Unz_OZHOE7INQB4oyRwQ==; SCF=Aud8cMJh_34pTmrmltAYktWEIj8uvCyeG-bway3QLP2cFBcalqhl5hLqSVJuA0EgncVYXUwDBV-mQ2IcEFg7VR4.; SUB=_2A25M4KxxDeRhGeRH6VEW9inOwz6IHXVvl5q5rDV8PUNbmtAfLW_wkW9NTckdWBGXm0-o91sdZY-yXu6MwiLdZ1_a; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whn0kGq.c3oulD0RyiQGEwh5JpX5KMhUgL.Foz4eoeNSoME1hz2dJLoIf4hIsHVi--fi-z7iKysi--Xi-iFiK.4i--fi-2fi-z0i--NiKLWiKnXi--Xi-zRiKn7i--fiKysi-8Wi--ciK.4i-zXi--fi-2Xi-24i--fi-z7iKysi--NiKyhi-8W; ALF=1673924511'
