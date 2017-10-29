# coding=utf-8
import concurrent.futures
import itertools
import logging
import os

from colorama import Fore, Style

import settings
from weibo.api import WeiboApi


class Crawler(object):
    def __init__(self, target_url):
        """
        初始化
        :param target_url: 目标微博主页url
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        # 目标数据
        self.logger.info(Fore.BLUE + target_url)
        self.target = WeiboApi.fetch_user_info(target_url)
        self.uid, self.name = self.target['oid'], self.target['onick']

        # 本地预处理
        self.root = self.__init_folder()

    def start(self):
        """
        依次下载每一个相册
        :return: None
        """
        self.logger.info(Fore.BLUE + Style.BRIGHT + '开始下载 "%s" 的微博相册' % self.name)

        # 获取每一页的相册列表
        page_size, album_count = 20, 0
        for page in itertools.count(1):
            total, album_list = WeiboApi.fetch_album_list(self.uid, page, page_size)
            if not album_list:
                break

            for album in album_list:
                album_count += 1
                msg = '开始下载第 %d / %d 个微博相册《%s》' % (album_count, total, album['caption'])
                self.logger.info(Fore.BLUE + msg)
                self.__download_album(album)

    def __download_album(self, album):
        """
        下载单个相册
        :param album: 相册数据
        :return: None
        """
        # 相册所有图片的id
        all_photo_ids = WeiboApi.fetch_photo_ids(self.uid, album['album_id'], album['type'])
        self.logger.info(Fore.BLUE + '检测到 %d 张图片' % len(all_photo_ids))

        # 相册所有大图的数据
        all_large_pics = self.__fetch_large_pics(album, all_photo_ids)
        total = len(all_large_pics)

        # 下载所有大图
        with concurrent.futures.ThreadPoolExecutor() as executor:
            album_path = self.__make_album_path(album)

            future_to_large = {
                executor.submit(self.__download_pic, large, album_path): large
                for large in all_large_pics
            }

            for i, future in enumerate(concurrent.futures.as_completed(future_to_large)):
                large = future_to_large[future]
                count_msg = '%d/%d ' % (i + 1, total)
                try:
                    result, path = future.result()
                except Exception as exc:
                    err = '%s 抛出了异常: %s' % (WeiboApi.make_large_url(large), exc)
                    self.logger.error(''.join([Fore.RED, count_msg, err]))
                else:
                    style = result and Style.NORMAL or Style.DIM
                    self.logger.info(''.join([Fore.GREEN, style, count_msg, path]))
            else:
                self.logger.info(Fore.BLUE + '《%s》 已完成' % album['caption'])

    def __fetch_large_pics(self, album, ids):
        """
        获取某相册所有的大图数据
        :param album: 相册
        :param ids: 所有图片的id
        :return: list
        """
        chunk_size, all_large_pics = 50, []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_chunk = {
                executor.submit(
                    WeiboApi.fetch_large_list,
                    self.uid, ids[i: i + chunk_size], album['type']
                ): i
                for i in range(0, len(ids), chunk_size)
            }

            for future in concurrent.futures.as_completed(future_to_chunk):
                chunk = future_to_chunk[future]
                try:
                    large_list = future.result()
                except Exception as exc:
                    err = '在查询第 %d 块的 %d 个图片的大图时抛出了异常: %s'
                    self.logger.error(Fore.RED + err % (chunk, chunk_size, exc))
                else:
                    all_large_pics.extend(large_list)

        self.logger.info(Fore.BLUE + '检测到 %d 张大图' % len(all_large_pics))
        return all_large_pics

    def __download_pic(self, pic, path):
        """
        下载单个图片
        :param pic: 图片数据
        :param path: 存储路径目录
        :return: bool 下载结果, str 下载路径
        """
        path = os.path.join(path, self.__make_photo_name(pic))
        if not os.path.exists(path):
            url = WeiboApi.make_large_url(pic)
            response = WeiboApi.get(url, timeout=60)
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

    def __init_folder(self):
        """
        准备文件夹
        需要检测是否存在相同uid、不同name的情况
        :return: str 该用户的存储文件夹名
        """
        # 根目录
        root = settings.STORE_PATH
        if not os.path.exists(root):
            os.mkdir(root)

        # 用户目录名
        home = '-'.join([self.uid, self.name])
        home_path = os.path.join(root, home)

        # 处理用户更改微博名的情况
        for dir in os.listdir(root):
            if dir.startswith(self.uid):
                if dir != home:
                    src = os.path.join(root, dir)
                    dst = os.path.join(root, home)
                    os.rename(src, dst)
                break
        else:  # 没有已知uid的文件夹
            os.mkdir(home_path)

        return home_path
