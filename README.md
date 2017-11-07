# Weibo Album Crawler 
![python](https://img.shields.io/badge/python-3.5-ff69b4.svg)

新浪微博相册多线程爬虫。

## Usage
1. 安装

    ```shell
    git clone git@github.com:Lodour/Weibo-Album-Crawler.git
    cd Weibo-Album-Crawler
    virtualenv env --python=python3.5
    source ./env/bin/activate
    pip install -r requirements.txt
    mv settings.sample.py settings.py
    ```

2. 设置`settings.py`

    * `STORE_PATH` 下载目录
    * `COOKIES` 任意用户微博的cookies
    * `TARGETS` 目标用户的微博主页url

3. 运行

    `python main.py`

## License
[MIT License](https://github.com/Lodour/Weibo-Album-Crawler/blob/master/LICENSE)
