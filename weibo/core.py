# coding=utf-8
import itertools

from weibo.api import WeiboApi


class JobManager(object):
    """
    任务管理
    接收用户id，提供生成任务的方法
    """

    def __init__(self, uid):
        """初始化

        :param uid: 目标用户id
        """
        self.uid = uid

    def albums(self):
        """
        迭代所有的相册
        :returns: dict
        """
        for page in itertools.count(1):
            album_list = WeiboApi.fetch_album_list(self.uid, page)
            if album_list:
                for album in album_list:
                    yield album
            else:
                break

    def photo_lists(self, album):
        """
        迭代相册中所有的图片list
        :param album: 相册数据
        :returns: list
        """
        static_args = self.uid, album['album_id'], album['type']
        for page in itertools.count(1):
            photo_list = WeiboApi.fetch_photo_list(*static_args, page)
            if photo_list:
                yield photo_list
            else:
                break

    def large_pics(self, album, photo_list):
        """
        迭代相册中所有大图
        :param album: 相册数据
        :param photo_list: 某一批图片
        :returns: dict
        """
        ids = [p['photo_id'] for p in photo_list]
        return WeiboApi.fetch_large_list(self.uid, ids, album['type'])
