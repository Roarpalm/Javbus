#!/usr/bin/env python3
#-*-coding:utf-8-*-

import os, time, requests, concurrent.futures
from lxml import etree

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:
        [e.submit(get_url, url) for url in list_url]

def get_url(url):
    code = url.split('/')[-1]
    # 新建文件夹
    b = os.path.abspath('.') + '//' + code + '//'
    if not os.path.exists(b):
        os.makedirs(b)

    print(f'开始解析...{url}')
    response = requests.get(url, headers=headers)
    html = response.content.decode()
    tree = etree.HTML(html)

    # 封面大图
    src = tree.xpath('/html/body/div[5]/div[1]/div[1]/a/img/@src')
    # 时长
    chong = tree.xpath('/html/body/div[5]/div[1]/div[2]/p[3]/text()')
    # 演员
    actress = tree.xpath('/html/body/div[5]/div[1]/div[2]/p[11]/span/a/text()')
    # 演员链接
    actress_link = tree.xpath('/html/body/div[5]/div[1]/div[2]/p[11]/span/a/@href')
    # 样品图
    imgs = tree.xpath('//*[@id="sample-waterfall"]/a/@href')

    # 保存信息
    txt_filename = b + code + '.txt'
    with open(txt_filename, 'w', encoding='utf-8') as e:
        e.write(f'番号：{code}\n时长：{chong}\n演员：{actress}\n演员链接：{actress_link}\n网页链接：{url}')

    print('下载完成：信息')
    
    # 下载封面
    for i in src:
        response = requests.get(i, headers=headers, stream=True)
        with open(f'{b}{code}.jpg', 'wb') as file:
            content_size = int(response.headers['content-length']) # 内容体总大小
            progress = ProgressBar(f'{code}.jpg', total=content_size, unit="KB", chunk_size=1024, run_status="正在下载", fin_status="下载完成")
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
                progress.refresh(count=len(chunk))

    # 下载详情图
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
        [e.submit(get_img, img, b) for img in imgs]

def get_img(img, b):
    name = img.split('/')[-1]
    img_filename = b + name
    response = requests.get(img, headers=headers, stream=True)
    with open(img_filename, 'wb') as file:
        content_size = int(response.headers['content-length']) # 内容体总大小
        progress = ProgressBar(name, total=content_size, unit="KB", chunk_size=1024, run_status="正在下载", fin_status="下载完成")
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
            progress.refresh(count=len(chunk))

class ProgressBar(object):

    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s]%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # [名称] 状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)

if __name__ == "__main__":
    start = time.time()
    with open('javbus.txt', 'r') as f:
        list_url = f.read().splitlines()
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    
    main()
    print(f'用时：{time.time()-start}秒')