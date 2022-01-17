import os.path
from urllib.parse import urlparse

import scrapy

from weibo import api, utils
from weibo import configs
from weibo.items import VideoItem


class VideoSpider(scrapy.Spider):
    name = 'video'
    allowed_domains = ['weibo.com']
    media_cache_key = 'mid'
    media_results_key = 'files'
    download_warnsize = 100 << 20  # 100 MB
    download_timeout = 10 * 60  # 10 min
    video_keys = ['mp4_720p_mp4', 'mp4_hd_url', 'mp4_sd_url']

    def start_requests(self):
        for target in configs.TARGETS:
            uid = os.path.basename(urlparse(target.rstrip('/')).path)
            yield scrapy.Request(api.info(uid), callback=self.parse_info)

    def parse_info(self, response):
        user = response.json()['user']
        uid, uname = user['id'], user['screen_name']
        meta = {'uid': uid, 'uname': uname}
        utils.migrate_folder_if_any(configs.VIDEOS_STORE, uid, uname)
        yield scrapy.Request(api.get_water_fall(uid), callback=self.parse_water_fall, meta=meta)

    def parse_water_fall(self, response):
        # prepare data
        data = response.json()
        uid, uname = response.meta['uid'], response.meta['uname']

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
                    video_url = next(filter(None, urls), '')  # take the first (best) one
                    yield VideoItem(uid=uid, uname=uname, mid=mid, file_urls=[video_url])

                case 'story':
                    for i, slide in enumerate(video['slide_cover']['slide_videos']):
                        video_url = slide['url']
                        yield VideoItem(uid=uid, uname=uname, mid=f'{mid}_{i}', file_urls=[video_url])

                case _:
                    raise NotImplementedError(f'Unsupported video type "{video_type}".')
