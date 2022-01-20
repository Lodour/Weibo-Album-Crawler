# Weibo Album Crawler

![python](https://img.shields.io/badge/python-3.10-blue)
![scrapy](https://img.shields.io/badge/scrapy-v2.5-blue)

基于 Scrapy 的新浪微博爬虫，支持相册、视频等。

## 设置环境

```shell
conda create -n weibo python=3.10
conda activate weibo
pip install scrapy
```

## 配置爬虫

* `weibo/settings.py`
  * 并发请求数 `CONCURRENT_REQUESTS`
  * 视频下载目录 `FILES_STORE`

* `weibo/configs.py`
  * 生成配置文件 `cp weibo/configs.example.py weibo/configs.py`
  * 手动复制粘贴登录后的 cookies 至 `COOKIES`
  * 目标主页 `TARGETS`
  * 下载目录 `STORE_PATH`

## 运行

```shell
scrapy crawl image
scrapy crawl video
```
