# coding=utf-8
import json
import re

import requests

from utils import load_cookies, get_ms


class Url(object):
    ALBUM_LIST = 'http://photo.weibo.com/albums/get_all'
    PHOTO_LIST = 'http://photo.weibo.com/photos/get_all'
    LARGE_LIST = 'http://photo.weibo.com/photos/get_multiple'


class Pattern(object):
    OID = re.compile(r"\$CONFIG\['oid'\]='(?P<oid>\d+)';")


class Formatter(object):
    LARGE_URL = '{host}/large/{name}'


class Weibo(object):
    """ 微博API """

    COOKIES = load_cookies()

    @staticmethod
    def get(*args, **kwargs):
        """添加了cookies的request.get的快捷方式

        :param args: see request.get
        :param kwargs: see request.get
        :return: request.Response
        """
        kwargs.setdefault('cookies', Weibo.COOKIES)
        return requests.get(*args, **kwargs)

    @staticmethod
    def fetch_uid(url):
        """从任意用户的主页获取其uid，即html中的oid

        :param url: 主页url
        :return: 用户uid
        """
        html = Weibo.get(url).content.decode('utf-8')
        return Pattern.OID.search(html).group('oid')

    @staticmethod
    def fetch_album_list(uid, page=1, count=20, __rnd=None):
        """获取用户的相册列表数据

        :param uid: 用户id
        :param page: 相册列表-页号
        :param count: 相册列表-页长
        :param __rnd: 毫秒时间戳
        :return: list
        """
        params = {
            'uid': uid,
            'page': page,
            'count': count,
            '__rnd': __rnd or get_ms()
        }
        response = Weibo.get(Url.ALBUM_LIST, params=params)
        data = json.loads(response.content.decode('utf-8'))
        return data['data']['album_list']

    @staticmethod
    def fetch_photo_list(uid, album_id, type, page=1, count=30, __rnd=None):
        """获取相册的图片列表
        
        :param uid: 用户id
        :param album_id: 相册id
        :param type: 相册类型
        :param page: 图片列表-页号
        :param count: 图片列表-页长
        :param __rnd: 毫秒时间戳
        :return: list
        """
        params = {
            'uid': uid,
            'album_id': album_id,
            'type': type,
            'page': page,
            'count': count,
            '__rnd': __rnd or get_ms()
        }
        response = Weibo.get(Url.PHOTO_LIST, params=params)
        data = json.loads(response.content.decode('utf-8'))
        return data['data']['photo_list']

    @staticmethod
    def fetch_large_list(uid, ids, type):
        """获取大图列表

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
        response = Weibo.get(Url.LARGE_LIST, params=params)
        data = json.loads(response.content.decode('utf-8'))
        return list(data['data'].values())

    @staticmethod
    def make_large_url(pic_host, pic_name):
        """生成大图下载url

        :param pic_host: 图片host
        :param pic_name: 图片name
        :return: str
        """
        return Formatter.LARGE_URL.format(host=pic_host, name=pic_name)
