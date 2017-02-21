# Weibo-Album-Crawler
A crawler to download weibo albums based on python with requests, threading.

_API Version: 2017.2.21_

## Usage
1. `git clone git@github.com:Lodour/Weibo-Album-Crawler.git`

2. `virtualenv env --python=python3.5`

3. `source ./env/bin/activate`

4. `pip install -r requirements.txt`

5. 手动获取目标用户**相册专辑**页面URL里的数字即`uid`，并添加到`weibo.py`中的`target`内
如`http://photo.weibo.com/{uid}/albums`

6. 手动复制访问自己**相册专辑**页面时的`Cookies`并粘贴到`cookies.txt`内

7. `python weibo.py`

8. 相册保存在同目录下的`downloads`文件夹内

## Hint
1. API可能会失效，具体请查看本页面的 _API Version_

2. 有时速度会比较慢，`Ctrl + C`重新运行即可

3. 若经常出错请更换cookies

4. 默认线程数`25`，线程下载间歇`0.5s`，可以在`settings.py`中修改

## License
[MIT License](https://github.com/Lodour/Weibo-Album-Crawler/blob/master/LICENSE)

## Todo
- [ ] 相同`feed_id`的图片按索引顺序命名
- [ ] 保存的图片按点赞数排序
- [ ] 封装为类

## Update
### 2017-2-21
Initial commit

