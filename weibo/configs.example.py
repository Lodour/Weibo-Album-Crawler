"""
This file contains weibo configs for the spider.
"""

STORE_PATH = './downloads'
CACHE_FILE = f'{STORE_PATH}/cache.pkl'

COOKIES = 'key=value; key=value; ...'

TARGETS = [
    'https://weibo.com/u/0000000000',
    'https://weibo.com/u/1111111111',
]
