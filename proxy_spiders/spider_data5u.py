import requests
import re
import logging
import time
import threading
from bs4 import BeautifulSoup

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_current_time():
    timenow = time.strftime('%Y-%m-%d %X', time.localtime())
    return timenow


def crawl():
    urls = ['http://www.data5u.com/']
    result = []
    for url in urls:
        try:
            html = requests.get(url, headers=headers, timeout=30).text
            table = BeautifulSoup(html, 'lxml').find('div', {'class': 'wlist'}).find_all('ul', {"class": 'l2'})
        except Exception as e:
            print('[%s][Spider][data5u]Error:' % get_current_time(), logging.exception(e))
            continue
        for item in table[1:]:
            try:
                spans = item.find_all('span')
                ip = spans[0].get_text()
                port = spans[1].get_text()
            except:
                continue
            line = ip + ':' + port
            result.append(line.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', ''))
    print('[%s][Spider][data5u]OK!' % get_current_time(), 'Crawled IP Count:', len(result))
    return result


class SpiderData5u(threading.Thread):
    def __init__(self):
        super(SpiderData5u, self).__init__()

    def run(self):
        self.result = crawl()
