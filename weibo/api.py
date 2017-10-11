# coding=utf-8
import json
import re
from time import time

import requests

from weibo.utils import load_cookies


class Url(object):
    ALBUM_LIST = 'http://photo.weibo.com/albums/get_all'
    PHOTO_LIST = 'http://photo.weibo.com/photos/get_all'
    LARGE_LIST = 'http://photo.weibo.com/photos/get_multiple'


class Pattern(object):
    OID = re.compile(r"\$CONFIG\['oid'\]='(?P<oid>\d+)';")
    NAME = re.compile(r"\$CONFIG\['onick'\]='(?P<name>.*)';")


class Formatter(object):
    INDEX_URL = 'http://weibo.com/u/{uid}'.format
    LARGE_URL = '{host}/large/{name}'.format


class WeiboApi(object):
    """
    微博API
    访问流程: url -> id -> albums -> photo_ids(batch) -> large_pics(batch)
    """

    COOKIES = load_cookies()

    @staticmethod
    def get(*args, **kwargs):
        """
        添加了cookies的request.get的快捷方式
        :param args: see request.get
        :param kwargs: see request.get
        :return: request.Response
        """
        kwargs.setdefault('cookies', WeiboApi.COOKIES)
        return requests.get(*args, **kwargs)

    @staticmethod
    def get_json(*args, **kwargs):
        """
        获取response中的json数据
        :param args: see get
        :param kwargs: see get
        :return: dict
        """
        return json.loads(WeiboApi.get(*args, **kwargs).text)

    @staticmethod
    def fetch_uid(url):
        """
        从任意用户的主页获取其uid，即html中的oid
        :param url: 主页url
        :return: 用户uid
        """
        content = WeiboApi.get(url).text
        return Pattern.OID.search(content).group('oid')

    @staticmethod
    def fetch_name(uid):
        """
        获取指定用户的微博名
        :param uid: 用户id
        :return: str
        """
        content = WeiboApi.get(Formatter.INDEX_URL(uid=uid)).text
        return Pattern.NAME.search(content).group('name')

    @staticmethod
    def fetch_album_list(uid, page=1, count=20):
        """
        获取用户的相册列表数据
        :param uid: 用户id
        :param page: 相册列表-页号
        :param count: 相册列表-页长
        :return: list
        """
        params = {
            'uid': uid,
            'page': page,
            'count': count,
            '__rnd': WeiboApi.make_rnd()
        }
        data = WeiboApi.get_json(Url.ALBUM_LIST, params=params)
        return data['data']['album_list']

    @staticmethod
    def fetch_photo_list(uid, album_id, type, page=1, count=30):
        """
        获取相册的图片列表
        :param uid: 用户id
        :param album_id: 相册id
        :param type: 相册类型
        :param page: 图片列表-页号
        :param count: 图片列表-页长
        :return: list
        """
        params = {
            'uid': uid,
            'album_id': album_id,
            'type': type,
            'page': page,
            'count': count,
            '__rnd': WeiboApi.make_rnd()
        }
        data = WeiboApi.get_json(Url.PHOTO_LIST, params=params)
        return data['data']['photo_list']

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
        return list(data['data'].values())

    @staticmethod
    def make_rnd():
        """
        生成__rnd参数
        :return: int
        """
        return int(time() * 1000)

    @staticmethod
    def make_large_url(pic_host, pic_name):
        """
        生成大图下载url
        :param pic_host: 图片host
        :param pic_name: 图片name
        :return: str
        """
        return Formatter.LARGE_URL(host=pic_host, name=pic_name)
