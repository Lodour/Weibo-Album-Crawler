import logging
import os

from scrapy import logformatter


class LogFormatter(logformatter.LogFormatter):
    """
    Set DropItem to the debug level because we need to drop a lot of items.
    """

    def dropped(self, item, exception, response, spider):
        formatter = super().dropped(item, exception, response, spider)
        formatter['level'] = logging.DEBUG
        return formatter


def prepare_folder(uid: str, uname: str, store_dir: str):
    """
    Migrate a target's folder (with the ald uname, if any) to the new name.
    This is useful if some target changed their name.
    """
    new_folder = f'{uid}_{uname}'

    for old_folder in os.listdir(store_dir):
        if old_folder.startswith(f'{uid}_') and old_folder != new_folder:
            src = os.path.join(store_dir, old_folder)
            dst = os.path.join(store_dir, new_folder)
            os.rename(src, dst)
            break

    return new_folder
