"""
This module contains weibo's api links.
"""


def info(uid: str) -> str:
    return f'https://weibo.com/ajax/profile/info?uid={uid}'


def get_image_wall(uid: str, since: str = '0') -> str:
    url = f'https://weibo.com/ajax/profile/getImageWall?uid={uid}&sinceid={since}'
    return url


def large_image(pid: str, cdn: int = 1) -> str:
    return f'https://wx{cdn}.sinaimg.cn/large/{pid}.jpg'
