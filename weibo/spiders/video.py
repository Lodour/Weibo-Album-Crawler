import os.path
from urllib.parse import urlparse

import scrapy

from weibo import api, utils
from weibo import configs
from weibo.items import WeiboItem


class VideoSpider(scrapy.Spider):
    name = 'video'
    allowed_domains = ['weibo.com']
    download_warnsize = 100 << 20  # 100 MB
    download_timeout = 10 * 60  # 10 min
    video_keys = ['mp4_720p_mp4', 'mp4_hd_url', 'mp4_sd_url']

    def start_requests(self):
        for target in configs.TARGETS:
            uid = os.path.basename(urlparse(target.rstrip('/')).path)
            yield scrapy.Request(api.info(uid), callback=self.parse_info)

    def parse_info(self, response):
        # prepare data
        user = response.json()['user']
        uid, uname = user['id'], user['screen_name']

        # prepare user folder
        folder = utils.prepare_folder(uid, uname, configs.STORE_PATH)

        # start from the first page
        meta = {'uid': uid, 'folder': folder}
        yield scrapy.Request(api.get_water_fall(uid), callback=self.parse_water_fall, meta=meta)

    def parse_water_fall(self, response):
        # prepare data
        data = response.json()
        uid, folder = response.meta['uid'], response.meta['folder']

        # continue to next page
        cursor = data['next_cursor']
        yield scrapy.Request(api.get_water_fall(uid, cursor), callback=self.parse_water_fall, meta=response.meta)

        # yield all videos
        for video in data['list']:
            video, mid = video['page_info'], video['mid']
            video_type = video['object_type']

            match video_type:
                case 'video':
                    urls = [video['media_info'][key] for key in self.video_keys]
                    url = urls[0] if urls else ''
                    self.logger.info(f'{folder} found 1 video (from {response.url})')
                    yield WeiboItem(uuid=mid, filename=f'{folder}/{mid}.mp4', file_urls=[url])

                case 'story':
                    for i, slide in enumerate(video['slide_cover']['slide_videos']):
                        url = slide['url']
                        yield WeiboItem(uuid=f'{mid}_{i}', filename=f'{folder}/{mid}_{i}.mp4', file_urls=[url])

                case _:
                    self.logger.warning('Unknown video type "%s".', video_type)
