from scrapy.cmdline import execute

if __name__ == '__main__':
    cmd = 'scrapy crawl image'
    execute(cmd.split())
