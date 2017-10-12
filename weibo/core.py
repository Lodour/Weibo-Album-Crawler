# coding=utf-8
import concurrent.futures
import itertools
import logging
import os
from math import ceil

from colorama import Fore, Style

import settings
from weibo.api import WeiboApi
from weibo.utils import init_folder


class Crawler(object):
    def __init__(self, target_url):
        """
        初始化
        :param target_url: 目标微博主页url
        """
        self.uid = WeiboApi.fetch_uid(target_url)
        self.name = WeiboApi.fetch_name(self.uid)
        folder_name = init_folder(self.uid, self.name)
        self.root = os.path.join(settings.STORE_PATH, folder_name)
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self):
        """
        依次下载每一个相册
        :return: None
        """
        self.logger.info(Fore.BLUE + Style.BRIGHT + '开始下载 "%s" 的微博相册' % self.name)

        page_size = 20
        for page in itertools.count(1):
            total, album_list = WeiboApi.fetch_album_list(self.uid, page, page_size)
            if not album_list:
                break
            for i, album in enumerate(album_list):
                self.logger.info(
                    Fore.BLUE + '开始下载第 %d / %d 个微博相册《%s》' % (
                        (page - 1) * page_size + i + 1, total, album['caption']
                    )
                )
                self.download_album(album)

    def download_album(self, album):
        """
        下载相册
        :param album: 相册数据
        :return: None
        """
        page_size, photo_count = 50, album['count']['photos']
        page_count = int(ceil(photo_count / page_size))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 相册每一页的图片
            future_photo_to_page = {
                executor.submit(
                    WeiboApi.fetch_photo_list,
                    self.uid, album['album_id'], album['type'], page, page_size
                ): page
                for page in range(1, page_count + 1)
            }

            # 相册每一页的大图
            future_large_to_page = {}

            # 加载 future_photo_to_page
            for future in concurrent.futures.as_completed(future_photo_to_page):
                page = future_photo_to_page[future]
                try:
                    photo_list = future.result()
                except Exception as exc:
                    err = '在获取第 %r 页图片列表时抛出了异常: %s'
                    self.logger.error(Fore.RED + err % (page, exc))
                else:
                    photo_ids = [p['photo_id'] for p in photo_list]
                    future_large_to_page.update({
                        executor.submit(
                            WeiboApi.fetch_large_list,
                            self.uid, photo_ids, album['type']
                        ): page
                    })

            # 下载大图
            future_to_large = {}
            album_path = self.__make_album_path(album)

            # 加载 future_large_to_page
            for future in concurrent.futures.as_completed(future_large_to_page):
                page = future_large_to_page[future]
                try:
                    large_list = future.result()
                except Exception as exc:
                    err = '在获取第 %r 页大图列表时抛出了异常: %s'
                    self.logger.error(Fore.RED + err % (page, exc))
                else:
                    future_to_large.update({
                        executor.submit(self.download_pic, large, album_path): large
                        for large in large_list
                    })

            # 加载 future_to_large
            total = len(future_to_large)
            for i, future in enumerate(concurrent.futures.as_completed(future_to_large)):
                large = future_to_large[future]
                count_msg = '%d/%d ' % (i + 1, total)
                try:
                    result, path = future.result()
                except Exception as exc:
                    err = '在下载图片 %r 时抛出了异常: %s'
                    self.logger.error(''.join([Fore.RED, count_msg, err % (large['photo_id'], exc)]))
                else:
                    style = result and Style.NORMAL or Style.DIM
                    self.logger.info(''.join([Fore.GREEN, style, count_msg, path]))
            else:
                self.logger.info(Fore.BLUE + '《%s》 已完成' % album['caption'])

    def download_pic(self, pic, path):
        """
        下载单个图片
        :param pic: 图片数据
        :param path: 存储路径
        :return: bool 下载结果, str 下载路径
        """
        path = os.path.join(path, self.__make_photo_name(pic))
        if not os.path.exists(path):
            url = WeiboApi.make_large_url(pic)
            response = WeiboApi.get(url)
            with open(path, 'wb') as fp:
                fp.write(response.content)
            return True, path
        return False, path

    def __make_album_path(self, album):
        """
        生成并创建相册下载路径
        :param album: 相册数据
        :return: str 下载路径
        """
        album_path = os.path.join(self.root, album['caption'])
        if not os.path.exists(album_path):
            os.mkdir(album_path)
        return album_path

    def __make_photo_name(self, large):
        """
        生成图片文件名
        :param large: 图片数据
        :return: str 文件名
        """
        f, p = large.get('feed_id'), large['pic_name']
        return '_'.join(f and [f, p] or [p])
