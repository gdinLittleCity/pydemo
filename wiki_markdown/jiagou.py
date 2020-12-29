#coding=utf-8
import html2text as html2text
import requests
import codecs
import os

def markdown():
    ht = html2text.HTML2Text()
    ht.bypass_tables = False
    cookie = '''seraph.confluence=62554282%3A080ef4c3125bb185f9492de918cbea2e130e8c75; JSESSIONID=87E045B60D19A7F229B20F4314B12F73'''

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 53.0.2785.143Safari / 537.36',
        'Connection': 'keep-alive',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cookie': cookie
    }
    htmlfile = requests.get('http://wiki.ym/pages/viewpage.action?pageId=15302789', headers=header)#npurl 为网址
    htmlfile.encoding = 'utf-8'
    htmlpage = htmlfile.text
    text = ht.handle(htmlpage)
    with codecs.open("1.md", 'a', encoding='utf-8') as f:
        f.write(text)
markdown()