import requests
import re
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
    urls = ['http://www.89ip.cn/tiqu.php?sxb=&tqsl=1000&ports=&ktip=&xl=on&submit=%CC%E1++%C8%A1']
    result = []
    for pageurl in urls:
        try:
            html = requests.get(pageurl, headers=headers, timeout=30).text
        except Exception as e:
            print('[%s][Spider][89ip]Error:' % get_current_time(), logging.exception(e))
            continue
        ips = re.findall('\d+\.\d+\.\d+\.\d+:\d+', html)
        result += ips
        time.sleep(2)
    print('[%s][Spider][89ip]OK!' % get_current_time(), 'Crawled IP Count:', len(result))
    return result


class SpiderIP89(threading.Thread):
    def __init__(self):
        super(SpiderIP89, self).__init__()

    def run(self):
        self.result = crawl()
