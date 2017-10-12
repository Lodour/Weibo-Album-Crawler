import settings
from weibo.core import Crawler

for target in settings.TARGETS:
    Crawler(target).run()
