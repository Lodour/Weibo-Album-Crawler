# Weibo Album Crawler ![python](https://img.shields.io/badge/python-3.5-ff69b4.svg)
新浪微博相册大图多线程爬虫。

## Usage
1. `git clone git@github.com:Lodour/Weibo-Album-Crawler.git`

2. `cd Weibo-Album-Crawler`

3. `virtualenv env --python=python3.5`

4. `source ./env/bin/activate`

5. `pip install -r requirements.txt`

6. 手动获取目标用户**相册专辑**页面URL里的数字即`uid`，并添加到`weibo.py`中的`target`内
如`http://photo.weibo.com/{uid}/albums`

7. 手动复制访问自己**相册专辑**页面时的`Cookies`并粘贴到`cookies.txt`内

8. `python weibo.py`

9. 相册保存在同目录下的`downloads`文件夹内

## Hint
* API可能会失效，一般而言最近一次Commit的时候是有效的

* 有时速度会比较慢，排除图片较大的情况时，`Ctrl + Z`重新运行即可

* 根据[官方文档](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor)，默认线程数为**处理器数量的5倍**，如有需要请自行添加参数`max_workers`

* 下载操作默认不延时，如经常卡住或Cookies失效，请在`settings.py`中修改`wait_second`

* 已经下载过的图片会自动跳过

* 如果发现的图片数量和相册图片数量不符，是因为存在重复的图片

## License
[MIT License](https://github.com/Lodour/Weibo-Album-Crawler/blob/master/LICENSE)

## Todo
- [ ] 相同`feed_id`的图片按索引顺序命名
- [ ] 保存的图片按点赞数排序
- [ ] 封装为类
- [ ] 优化对异常的处理

## Update
### 2017-2-23
1. 添加下载计数的显示

### 2017-2-22
1. 多线程更改为使用`concurrent.futures.ThreadPoolExecutor`

2. 改进了部分逻辑

3. 修复当图片不存在或删除时的异常处理

### 2017-2-21
Initial commit

