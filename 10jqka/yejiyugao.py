import time
import json
import random
import requests
import pandas as pd
import pymysql
from bs4 import BeautifulSoup

def get_html(page_id):
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': '*******',
        'password': '*******',
        'db': 'mysql',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
    }
    #connection = pymysql.connect(**config)
    #http://data.10jqka.com.cn/financial/yjyg/
    headers = {
        'host':'q.10jqka.com.cn',
        'Referer':'http://q.10jqka.com.cn/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3554.0 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
    }
    url = 'http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/%s/ajax/1/' % page_id
    res = requests.get(url, headers=headers)
    res.encoding = 'GBK'
    soup = BeautifulSoup(res.text,'lxml')
    tr_list = soup.select('tbody tr')
    # print(tr_list)
    stocks = []
    for each_tr in tr_list:
        td_list = each_tr.select('td')
        data = {
        '股票代码':td_list[1].text,
        '股票简称':td_list[2].text,
        '股票链接':each_tr.a['href'],
        '现价':td_list[3].text,
        '涨幅':td_list[4].text,
        '涨跌':td_list[5].text,
        '涨速':td_list[6].text,
        '换手':td_list[7].text,
        '量比':td_list[8].text,
        '振幅':td_list[9].text,
        '成交额':td_list[10].text,
        '流通股':td_list[11].text,
        '流通市值':td_list[12].text,
        '市盈率':td_list[13].text,
        }
    stocks.append(data)
    return stocks


def get_pages(page_n):
  stocks_n = []
  for page_id in range(1, page_n+1):
    page = get_html(page_id)
    stocks_n.extend(page)
    time.sleep(random.randint(1, 10))
  return stocks_n
