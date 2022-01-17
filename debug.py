"""
This script is for debugging only.
"""
from scrapy.cmdline import execute

if __name__ == '__main__':
    cmd = 'scrapy crawl video'
    execute(cmd.split())
