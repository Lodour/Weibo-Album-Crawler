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
