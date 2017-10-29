# coding=utf-8
import logging

from colorama import Style
from colorama import init

# 设置log
logging.basicConfig(
    level=logging.INFO,
    format=''.join([Style.DIM, '[%(asctime)s] ',
                    Style.NORMAL, '%(message)s',
                    Style.RESET_ALL]),
    datefmt='%T',
)
logging.getLogger("requests").setLevel(logging.WARNING)

# 命令行
init(autoreset=True)

# 存储目录
STORE_PATH = './downloads'

# 在这里粘贴你的cookies
COOKIES = 'SINAGLOBAL=...; UM_distinctid=...; __guid=...; ...'

# 在这里添加目标用户的微博主页url
TARGETS = [
    # 'http://weibo.com/u/...',
]
