# -*- encoding: utf-8 -*-
# @Time    :   2024/12/08 22:58:40
# @File    :   main.py
# @Author  :   ciaoyizhen
# @Contact :   yizhen.ciao@gmail.com
# @Function:   爬取笔趣阁斗破苍穹

import os
import re
import time
import requests
from lxml import etree
from tqdm import tqdm
from urllib.parse import urljoin

CHAPTER_SET = set()  # 存过的章节名

def getCurrentPage(url:str|None)->tuple[bool, str, str]:
    """
    爬取单页主程序

    Args:
        url (str | None): 如果是None，则结束，否则解析结果

    Returns:
        tuple[bool, str, str]
            flag (bool): 若是False，则结束爬取
            text (str): 主页面
            url (str): 下一页的url
    """
    if url is None:
        return False, "", ""
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    text = response.text
    html = etree.HTML(text)
    title = html.xpath("//div/span[@class='title']/text()")[0]
    title = re.sub(r"^.*?）", "", title)
    context = html.xpath("//*[@id='chaptercontent']/text()")
    context = list(map(lambda x: x.replace("\u3000", " ").replace("\r", "").replace("\n", "").replace("\t", ""), context))[:-2]  # 去掉换行和收藏
    context = "\n".join(context)
    if title in CHAPTER_SET:
        text = context + "\n"
    else:
        text = "\n" + title + "\n" + context + "\n"
        CHAPTER_SET.add(title)
    
    next_url = html.xpath("//*[@id='pb_next']/@href")[0]
    if next_url == "/look/9695/":
        next_url = None
    return True, text, next_url


def main(basic_url, url, save_file="斗破苍穹.txt"):
    process_bar = tqdm()
    flag = True
    is_start = True
    while flag:
        url = urljoin(basic_url, url)
        flag, text, url = getCurrentPage(url)
        if is_start:
            text = text[1:]  # 去掉第一个换行符
            is_start = False
        with open(save_file, "a", encoding="utf-8") as f:
            f.write(text)
        process_bar.update(1)
            


if __name__ == "__main__":
    basic_url = "https://m.bqgl.cc"
    start_uri = "look/9695/1.html"
    main(basic_url, start_uri)
    
    basic_url = "https://bbb974fbaae10d221e8e13.bi53.cc/"
    start_uri = "book/45813/1.html"
    main(basic_url, start_uri, "武动乾坤.txt")