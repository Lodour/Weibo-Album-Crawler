# coding=utf-8
import os

import settings


def load_cookies():
    """
    从设置中解析cookies
    :return: dict
    """
    assert settings.COOKIES, '请在`settings.py`中粘贴cookies'
    return dict([l.split('=') for l in settings.COOKIES.split('; ')])


def init_folder(uid, name):
    """
    准备文件夹
    需要检测是否存在相同uid、不同name的情况
    :param uid: 用户id
    :param name: 用户微博名
    :return: str 该用户的存储文件夹名
    """
    # 根目录
    root = settings.STORE_PATH
    if not os.path.exists(root):
        os.mkdir(root)

    # 用户目录
    uid = str(uid)
    home = '-'.join([uid, name])

    # 处理用户更改微博名的情况
    for dir in os.listdir(root):
        if dir.startswith(uid):
            if dir != home:
                src = os.path.join(root, dir)
                dst = os.path.join(root, home)
                os.rename(src, dst)
            return home

    # 新的用户
    os.mkdir(os.path.join(root, home))
    return home
