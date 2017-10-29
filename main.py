from weibo.core import Crawler
from weibo.utils import load_targets

for target in load_targets():
    Crawler(target).start()
