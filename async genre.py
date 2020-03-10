#!/usr/bin/env python3
#-*-coding:utf-8-*-

import aiohttp, asyncio, os, time
from lxml import etree
from tqdm import tqdm

async def main():
    async with aiohttp.connector.TCPConnector(limit=300, force_close=True, enable_cleanup_closed=True) as tc:
        async with aiohttp.ClientSession(connector=tc) as session:
            print('开始解析...')
            two = asyncio.Semaphore(2)
            # 采集的页数
            tasks = [get_url(session, i, two) for i in range(2,3)]
            await asyncio.gather(*tasks)

            print('-'*10 + '解析完成' + '-'*10)

            all_list = list(zip(codes, dates, titles, links, srcs))
            ten = asyncio.Semaphore(10)
            works = [get_info(code, date, title, link, src, session, ten) for code, date, title, link, src in all_list]
            await asyncio.gather(*works)



async def get_url(session, i, two):
    global codes, dates, srcs, titles, links
    async with two:
        # 我只喜欢巨乳，所以这里爬的是巨乳的网页，你可以自己修改
        if i == 1:
            url = 'https://www.javbus.com/genre/e'
        else:
            url = f'https://www.javbus.com/genre/e/{i}'

        async with session.get(url, headers=headers) as response:
            html = await response.read()
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



async def get_info(code, date, title, link, src, session, ten):
    txt_filename = b + code + '.txt'
    with open(txt_filename, 'w', encoding='utf-8') as e:
        e.write(f'标题：{title}\n番号：{code}\n日期：{date}\n链接：{link}')

    img_filename = b + code +'.jpg'
    async with session.get(src, headers=headers) as response:
        with open(img_filename, 'wb') as file:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                file.write(chunk)
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

    asyncio.run(main())
    print(f'用时{time.time()-start}秒')