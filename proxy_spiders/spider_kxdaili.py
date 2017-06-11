import requests
from bs4 import BeautifulSoup
import logging
import time
import threading

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_current_time():
    timenow = time.strftime('%Y-%m-%d %X', time.localtime())
    return timenow


def crawl():
    urls = ['http://www.kxdaili.com/dailiip/1/%s.html', 'http://www.kxdaili.com/dailiip/3/%s.html']
    result = []
    for url in urls:
        page = 1
        while page <= 10:
            try:
                html = requests.get(url % (page), headers=headers, timeout=30).text.encode('ISO-8859-1').decode('utf-8',
                                                                                                                'ignore')
                page += 1
                table = BeautifulSoup(html, 'lxml').find('table').find_all('tr')
            except Exception as e:
                print('[%s][Spider][kxdaili]ERROR!' % get_current_time(), logging.exception(e))
                continue
            for tr in table[1:]:
                try:
                    tds = tr.find_all('td')
                    ip = tds[0].get_text() + ':' + tds[1].get_text()
                except:
                    pass
                result.append(ip)
        time.sleep(3)
    print('[%s][Spider][kxdaili]OK!' % get_current_time(), 'Crawled IP Count:', len(result))
    return result


class SpiderKxdaili(threading.Thread):
    def __init__(self):
        super(SpiderKxdaili, self).__init__()

    def run(self):
        self.result = crawl()
