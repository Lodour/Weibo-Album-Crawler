# coding=utf-8
from time import time


def load_cookies():
    """从文件中解析cookies

    :return: dict
    """
    with open('cookies.txt', 'r') as f:
        cookies = f.read().strip()
        assert cookies, '请在`cookies.txt`中粘贴cookies'
    return dict([l.split('=') for l in cookies.split('; ')])


def get_ms():
    """返回毫秒时间戳

    :return: int
    """
    return int(time() * 1000)
