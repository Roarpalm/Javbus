### 在 genre.py 里修改采集的页面就可以爬取自己想要的页面（默认为我的个人喜好），包括：缩略封面、番号、日期、网页链接
### 推荐手动挑选 想了解的网页链接 复制进 javbus.txt 注意换行
### 用 info.py 爬取详情，包括：封面大图、时长、演员、演员链接、多张详情图

## 2020年2月22日更新(1.0):
- 吐槽：用异步库 aiohttp 可以正常访问 javbus.com, 但在请求图片服务器 pics.javbus.com 时总是报错：
aiohttp.client_exceptions.ClientConnectorError: Cannot connect to host pics.javbus.com:443 ssl:default [远程计算机拒绝网络连接。]
不知道怎么解决，无奈在下载图片部分用多线程配合 requests

## 2020年2月26日更新(1.1):
- 新增显示进度的代码

## 2020年3月10日更新(1.2):
- 重写 genre.py 完全requests 版
- 新增 async genre.py 异步版，但是偶尔正常运行，大部分时间会有 ssl 443 错误