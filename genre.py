#!/usr/bin/env python3
#-*-coding:utf-8-*-

import os, time, requests, concurrent.futures
from lxml import etree

def main():
    print('开始解析...')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:
        [e.submit(get_info, i) for i in range(1,2)]
    print('解析完成')

    print('开始下载...')
    all_list = list(zip(codes, dates, titles, links, srcs))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:
        [e.submit(download, code, date, title, link, src) for code, date, title, link, src in all_list]



def get_info(i):
    global codes, dates, srcs, titles, links
    # 我只喜欢巨乳，所以这里爬的是巨乳的网页，你可以自己修改
    if i == 1:
        url = 'https://www.javbus.com/genre/e'
    else:
        url = f'https://www.javbus.com/genre/e/{i}'

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return '连接出错'
    html = response.content.decode()
    tree = etree.HTML(html)
    # 番号
    code = tree.xpath('//*[@id="waterfall"]/div/a/div[2]/span/date[1]/text()')
    codes.extend(code)
    # 日期
    date = tree.xpath('//*[@id="waterfall"]/div/a/div[2]/span/date[2]/text()')
    dates.extend(date)
    # 图片
    src = tree.xpath('//*[@id="waterfall"]/div/a/div[1]/img/@src')
    srcs.extend(src)
    # 标题
    title = tree.xpath('//*[@id="waterfall"]/div/a/div[1]/img/@title')
    titles.extend(title)
    # 链接
    link = tree.xpath('//*[@id="waterfall"]/div/a/@href')
    links.extend(link)



def download(code, date, title, link, src):
    txt_filename = b + code + '.txt'
    with open(txt_filename, 'w', encoding='utf-8') as e:
        e.write(f'标题：{title}\n番号：{code}\n日期：{date}\n链接：{link}')

    img_filename = b + code + '.jpg'
    response = requests.get(src, headers=headers)
    with open(img_filename, 'wb') as f:
        f.write(response.content())
    print(f'下载完成：{code}')

if __name__ == "__main__":
    start = time.time()
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    codes = []
    dates = []
    srcs = []
    titles = []
    links = []

    t = time.strftime('%Y%m%d',time.localtime(time.time()))
    b = os.path.abspath('.') + f'\\{t}\\'
    if not os.path.exists(b):
        os.makedirs(b)

    main()
    print(f'用时{round(time.time()-start, 2)}秒')