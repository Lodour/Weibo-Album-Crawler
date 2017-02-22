# coding=utf-8
import os
from collections import namedtuple
import concurrent.futures

import requests

from settings import *

Album = namedtuple('Album', 'uid id name size type')
Photo = namedtuple('Photo', 'name feed url')


def delay(second):
    """
    装饰器，将某个函数执行后延迟second秒
    """
    from time import sleep

    def _delay(func):
        def delayed_func(*args, **kwargs):
            ret = func(*args, **kwargs)
            sleep(second)
            return ret
        return delayed_func

    return _delay


def get_rand():
    """
    返回一个特定的随机数
    经过测试，参数中的__rnd实际上是以毫秒为单位的时间戳
    """
    from time import time
    return int(round(time() * 1000))


def get_page(url, params=None, cookies=None, attr='text'):
    """
    返回GET某url返回的数据 即Response.attr
    attr为None时返回Response本身
    """
    cookies = cookies or COOKIES
    req = requests.get(url, params=params, cookies=cookies)
    return attr and req.__getattribute__(attr) or req


def get_json(url, params):
    """
    返回GET某url返回的json数据中的data部分
    """
    from json import loads

    json_content = get_page(url, params)
    try:
        data = loads(json_content)
        assert data.get('result')
        assert data.get('data'), '获取数据不含data项'
    except Exception as e:
        print('获取数据失败，请更新Cookies后重试')
        return None

    return data['data']


def get_album_list(uid, page=1, count=20):
    """
    返回某用户相册列表，具体内容参见Album命名元组
    这里假定相册数量不超过20，特殊情况需修改page/count参数
    """
    log.info(Fore.GREEN + Style.BRIGHT + '开始获取 {0} 的相册列表'.format(uid))

    # 获取数据
    url = 'http://photo.weibo.com/albums/get_all'
    params = {
        'uid': uid,
        'page': page,
        'count': count,
        '__rnd': get_rand()
    }
    data = get_json(url, params)

    # 相册个数
    total = data.get('total')
    log.info(Fore.BLUE + '获取到 {0} 个相册列表'.format(total))

    # 相册列表
    album_list = data.get('album_list')
    result = [Album(uid=album['uid'],
                    id=album['album_id'],
                    name=album['caption'],
                    size=album['count']['photos'],
                    type=album['type'])
              for album in album_list]

    return result


def get_photo_ids(album, count=None, page=1):
    """
    返回某相册所有图片的id
    默认请求所有图片，也可修改count/page参数
    """
    if count == None:
        count = album.size + 1
    url = 'http://photo.weibo.com/photos/get_all'
    params = {
        'uid': album.uid,
        'album_id': album.id,
        'count': count,
        'page': page,
        'type': album.type,
        '__rnd': get_rand(),
    }

    data = get_json(url, params)
    ids = [p['photo_id'] for p in data['photo_list']]
    log.info(Fore.BLUE + '获取到 {0} 个项目'.format(len(ids)))
    return ids


def get_large_photos(album, photo_ids):
    """
    根据相册及图片ids返回大图数据
    """
    if not photo_ids:
        return list()

    url = 'http://photo.weibo.com/photos/get_multiple'
    params = {
        'uid': album.uid,
        'ids': ','.join(photo_ids),
        'type': album.type,
    }

    data = get_json(url, params)
    large = list()
    for i in photo_ids:
        if data[i]:
            large.append(Photo(name=data[i]['pic_name'],
                               feed=data[i].get('feed_id'),
                               url=data[i]['large_pic_tmp']))
        else:
            err = '《%s》的图片 %s 不存在或已被删除' % (album.name, i)
            log.warning(Fore.YELLOW + err)
    log.info(Fore.BLUE + '获取到 {0} 个大图'.format(len(large)))
    return large


def get_album_path(album):
    """
    生成相册保存路径，不存在则创建
    """
    path = './downloads/{name}/{album}'.format(
        name=get_username(album.uid),
        album=album.name
    )
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_username(uid):
    """
    根据uid获取用户名
    """
    import re

    url = 'http://photo.weibo.com/{uid}/albums'
    content = get_page(url.format(uid=uid))
    name = re.search(r'title>(?P<name>.*?) -', content)
    return name.group('name')


def get_picname(photo):
    """
    生成保存的图片文件名
    """
    l = list()
    if photo.feed:
        l.append(photo.feed)
    l.append(photo.name)
    return '_'.join(l)


@delay(wait_second)
def down_pic(photo, path):
    """
    根据相册及图片，进行下载操作
    保存路径为'./相册名/图片名'
    """
    filename = get_picname(photo)
    path = os.path.join(path, filename)
    is_downloaded = False
    if not os.path.exists(path):
        is_downloaded = True
        content = get_page(photo.url, attr='content')
        with open(path, 'wb') as f:
            f.write(content)
    return is_downloaded, path


def pagenavi(total, count):
    """
    分页器，一共total个项目，每页count个，
    """
    max_page = int((total + count - 1) / count)
    for page in range(max_page):
        yield page + 1, max_page


def down_album(album, page_size=100):
    """
    执行下载album的操作
    每页请求的图片个数page_size默认为100（太大了会被服务器断开连接）
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_pic = dict()

        # 对相册进行分页
        for page, tot in pagenavi(album.size, page_size):
            log.info(Fore.CYAN + '《{0}》{1}/{2}'.format(album.name, page, tot))

            # 获取该页包含图片id及大图
            ids = get_photo_ids(album, page_size, page)
            large_photos = get_large_photos(album, ids)

            # 开始任务
            album_path = get_album_path(album)
            future = {executor.submit(down_pic, pic, album_path): pic
                      for pic in large_photos}
            future_to_pic.update(future)
        else:
            tot = vars().get('tot', 0)
            log.info(Fore.CYAN + '《{0}》共发现 {1} 页'.format(album.name, tot))

        # 等待任务完成
        for future in concurrent.futures.as_completed(future_to_pic):
            pic = future_to_pic[future]
            try:
                is_downloaded, path = future.result()
            except Exception as e:
                msg = '微博 %s 中的图片 %s 产生了异常: %s' % (pic.feed, pic.name, e)
                log.info(Fore.RED + msg)
            else:
                style = is_downloaded and Style.NORMAL or Style.DIM
                log.info(Fore.GREEN + style + path)
        else:
            color = Fore.GREEN + Style.BRIGHT
            log.info(color + '《{0}》 已完成'.format(album.name))


def run(uid):
    """
    执行对uid的操作
    """
    for album in get_album_list(uid):
        down_album(album)
    log.info(Fore.GREEN + Style.BRIGHT + '全部任务已完成')


if __name__ == '__main__':
    target = ['']
    for t in target:
        run(t)
