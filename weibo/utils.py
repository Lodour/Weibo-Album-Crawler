# coding=utf-8
import logging
import os
import re

from colorama import Fore

import settings
from weibo.api import Formatter


def load_targets_from_folder():
    """
    从指定的文件夹中加载已下载的目标
    :return: list
    """
    if not os.path.exists(settings.STORE_PATH):
        logging.info(Fore.YELLOW + '`settings.STORE_PATH`指定路径不存在，解析目标失败')
        return []
    matches = map(lambda x: re.search(r'(?P<id>\d+)-.+', x), os.listdir(settings.STORE_PATH))
    targets = map(lambda x: Formatter.INDEX_URL(uid=x.group('id')), filter(None.__ne__, matches))
    return targets


def load_targets():
    if not settings.TARGETS:
        logging.info(Fore.YELLOW + '`settings.TARGETS`为空，尝试从`settings.STORE_PATH`中解析目标')
        return load_targets_from_folder()
    return settings.TARGETS
