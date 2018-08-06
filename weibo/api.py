# coding=utf-8
import json
import re
from time import time

import requests

import settings


class Url(object):
    ALBUM_LIST = 'http://photo.weibo.com/albums/get_all'
    PHOTO_IDS = 'http://photo.weibo.com/photos/get_photo_ids'
    LARGE_LIST = 'http://photo.weibo.com/photos/get_multiple'


class Pattern(object):
    CONFIG = re.compile(r"\$CONFIG\['(?P<key>.*)'\]='(?P<value>.*)';")


class Formatter(object):
    INDEX_URL = 'http://weibo.com/u/{uid}'.format
    LARGE_URL = '{host}/large/{name}'.format


def _load_headers(url):
    """
    从设置中解析cookies
    :return: dict
    """
    assert settings.COOKIES, '请在`settings.py`中粘贴cookies'
    spltAr = url.split("://");
    i = (0,1)[len(spltAr)>1];
    dm = spltAr[i].split("?")[0].split('/')[0].split(':')[0].lower();
    headers = {"Host": dm,
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Cookie": settings.COOKIES}
    return headers

class WeiboApi(object):
    """
    微博API
    访问流程: url -> id -> albums -> photo_ids(all) -> large_pics(batch)
    """

    @staticmethod
    def get(*args, **kwargs):
        """
        添加了cookies的request.get的快捷方式
        :param args: see request.get
        :param kwargs: see request.get
        :return: request.Response
        """
        for i in args:
            if(i[0:4]=='http'):
                url = i
        kwargs.setdefault('headers', _load_headers(url))
        return requests.get(*args, **kwargs)

    @staticmethod
    def get_json(*args, **kwargs):
        """
        获取response中的json数据的data域
        :param args: see get
        :param kwargs: see get
        :return: dict
        """
        return json.loads(WeiboApi.get(*args, **kwargs).text)['data']

    @staticmethod
    def fetch_user_info(url):
        """
        从任意用户的主页获取其相关数据
        :param url: 主页url
        :return: dict
        """
        content = WeiboApi.get(url).text
        return dict(Pattern.CONFIG.findall(content))

    @staticmethod
    def fetch_album_list(uid, page=1, count=20):
        """
        获取用户的相册列表数据
        :param uid: 用户id
        :param page: 相册列表-页号
        :param count: 相册列表-页长
        :return: int 相册总数, list 相册列表
        """
        params = {
            'uid': uid,
            'page': page,
            'count': count,
            '__rnd': WeiboApi.make_rnd()
        }
        data = WeiboApi.get_json(Url.ALBUM_LIST, params=params)
        return data['total'], data['album_list']

    @staticmethod
    def fetch_photo_ids(uid, album_id, type):
        """
        获取相册的图片列表
        :param uid: 用户id
        :param album_id: 相册id
        :param type: 相册类型
        :return: list
        """
        params = {
            'uid': uid,
            'album_id': album_id,
            'type': type,
            '__rnd': WeiboApi.make_rnd()
        }
        return WeiboApi.get_json(Url.PHOTO_IDS, params=params)

    @staticmethod
    def fetch_large_list(uid, ids, type):
        """
        获取大图列表
        :param uid: 用户id
        :param ids: 图片id列表
        :param type: 相册类型
        :return: list
        """
        params = {
            'uid': uid,
            'ids': ','.join(map(str, ids)),
            'type': type
        }
        data = WeiboApi.get_json(Url.LARGE_LIST, params=params)
        return filter(None.__ne__, data.values())

    @staticmethod
    def make_rnd():
        """
        生成__rnd参数
        :return: int
        """
        return int(time() * 1000)

    @staticmethod
    def make_large_url(large_pic):
        """
        生成大图下载url
        :param large_pic: 大图数据
        :return: str
        """
        host, name = large_pic['pic_host'], large_pic['pic_name']
        return Formatter.LARGE_URL(host=host, name=name)
