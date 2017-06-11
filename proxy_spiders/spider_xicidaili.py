import requests
from bs4 import BeautifulSoup
import logging
import time
import threading


def get_current_time():
    timenow = time.strftime('%Y-%m-%d %X', time.localtime())
    return timenow


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def crawl():
    urls = ['http://www.xicidaili.com/nn/', 'http://www.xicidaili.com/nn/2', 'http://www.xicidaili.com/wn/']
    result = []
    for url in urls:
        try:
            html = requests.get(url, headers=headers, timeout=30).text
            table = BeautifulSoup(html, 'lxml').find('table', id='ip_list').find_all('tr')
        except Exception as e:
            print('[%s][Spider][xicidaili]ERROR!' % get_current_time(), logging.exception(e))
            continue
        for tr in table[1:]:
            try:
                tds = tr.find_all('td')
                ip = tds[1].get_text() + ':' + tds[2].get_text()
                result.append(ip)
            except:
                pass
    print('[%s][Spider][xicidaili]OK!' % get_current_time(), 'Crawled IP Count:', len(result))
    return result


class SpiderXicidaili(threading.Thread):
    def __init__(self):
        super(SpiderXicidaili, self).__init__()

    def run(self):
        self.result = crawl()
