#!/usr/bin/env python3
#-*-coding:utf-8-*-

import aiohttp, asyncio, aiofiles, os, time, requests, concurrent.futures
from lxml import etree

async def main():
    async with aiohttp.ClientSession() as session:
        print('开始解析...')
        two = asyncio.Semaphore(2)
        tasks = []
        # 采集的页数，自己更改
        for i in range(1,11):
            task = get_url(session, i, two)
            tasks.append(task)
        await asyncio.gather(*tasks)

        print('-'*10 + '解析完成' + '-'*10)

        all_list = list(zip(codes, dates, titles, links))
        works = []
        for code, date, title, link in all_list:
            work = get_info(code, date, title, link)
            works.append(work)
        await asyncio.gather(*works)

        new_list = list(zip(srcs, codes))
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as e:
            [e.submit(get_img, src, code) for src, code in new_list]



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



async def get_info(code, date, title, link):
    txt_filename = b + code + '.txt'
    async with aiofiles.open(txt_filename, 'w', encoding='utf-8') as e:
        await e.write(f'标题：{title}\n番号：{code}\n日期：{date}\n链接：{link}')



def get_img(src, code):
    img_filename = b + code +'.jpg'
    response = requests.get(src, headers=headers)
    with open(img_filename, 'wb') as f:
        f.write(response.content)
    print(f'下载完成：{code}')

if __name__ == "__main__":
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    codes = []
    dates = []
    srcs = []
    titles = []
    links = []

    b = os.path.abspath('.') +'\\javbus\\'
    if not os.path.exists(b):
        os.makedirs(b)

    start = time.time()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(main())
    loop.run_until_complete(future)
    print(f'用时{time.time()-start}秒')