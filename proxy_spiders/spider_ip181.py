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
    urls = ['http://www.ip181.com/daili/2.html', 'http://www.ip181.com/daili/1.html']
    result = []
    for pageurl in urls:
        try:
            html = requests.get(pageurl, headers=headers, timeout=30).text
            table = BeautifulSoup(html, 'lxml').find('table', {'class': 'ctable'}).find_all('tr')
        except Exception as e:
            print('[%s][Spider][ip181]Error:' % get_current_time(), logging.exception(e))
            continue
        for item in table[1:]:
            try:
                tds = item.find_all('td')
                ip = tds[0].get_text()
                port = tds[1].get_text()
            except:
                continue
            line = ip + ':' + port
            result.append(line.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', ''))
    print('[%s][Spider][ip181]OK!' % get_current_time(), 'Crawled IP Count:', len(result))
    return result


class SpiderIP181(threading.Thread):
    def __init__(self):
        super(SpiderIP181, self).__init__()

    def run(self):
        self.result = crawl()
