# coding=utf-8

import settings


def load_cookies():
    """
    从设置中解析cookies
    :return: dict
    """
    assert settings.COOKIES, '请在`settings.py`中粘贴cookies'
    return dict([l.split('=') for l in settings.COOKIES.split('; ')])
