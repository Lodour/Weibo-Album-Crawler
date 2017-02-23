# coding=utf-8
import logging as log
from colorama import init
from colorama import Fore, Style

# 下载间歇(s)
wait_second = 0

# 设置log
log.basicConfig(
    level=log.INFO,
    format=''.join([Style.DIM, '[%(asctime)s] ',
                    Style.NORMAL, '%(message)s',
                    Style.RESET_ALL]),
    datefmt='%T', 
)
log.getLogger("requests").setLevel(log.WARNING)

# 设置cookies
with open('cookies.txt', 'r') as f:
    COOKIES = f.read().strip()
assert COOKIES, '请在`cookies.txt`中粘贴cookies'
COOKIES = dict((l.split('=') for l in COOKIES.split('; ')))

# 命令行
init(autoreset=True)
