import requests
import threading
import time
import pymysql

from proxy_spiders.spider_ipcn import SpiderIpcn
from proxy_spiders.spider_66ip import SpiderIP66
from proxy_spiders.spider_kxdaili import SpiderKxdaili
from proxy_spiders.spider_89ip import SpiderIP89
from proxy_spiders.spider_data5u import SpiderData5u
from proxy_spiders.spider_ip181 import SpiderIP181

from conf import MYSQL_CONF


class VerifyIP(threading.Thread):
    def __init__(self, ip):
        super(VerifyIP, self).__init__()
        self.ip = ip
        self.proxies = {
            'http': 'http://%s' % ip
        }

    def run(self):
        try:
            html = requests.get('http://httpbin.org/ip', proxies=self.proxies, timeout=5).text
            result = eval(html)['origin']
            if len(result.split(',')) == 2:
                return
            if result in self.ip:
                with lock:
                    self.insert_into_sql()
        except:
            return

    def insert_into_sql(self):
        global cursor
        global conn
        global crawl_ip_count
        try:
            date = time.strftime('%Y-%m-%d %X', time.localtime())
            cursor.execute("insert into proxypool(ip,port,time) values"
                           + str((self.ip.split(':')[0], self.ip.split(':')[1], date)))
            conn.commit()
            crawl_ip_count += 1
        except:
            pass


def get_current_time():
    return time.strftime('%Y-%m-%d %X', time.localtime())


if __name__ == '__main__':
    lock = threading.Lock()
    crawlers = [SpiderIP66, SpiderIpcn, SpiderIP181, SpiderData5u]
    while True:
        crawl_ip_count = 0
        conn = pymysql.connect(host=MYSQL_CONF['host'],
                               user=MYSQL_CONF['user'],
                               passwd=MYSQL_CONF['passwd'],
                               db=MYSQL_CONF['db'],
                               port=MYSQL_CONF['port'],
                               charset='utf8')
        cursor = conn.cursor()
        result = []
        tasks = []
        for crawler in crawlers:
            task = crawler()
            task.setDaemon(True)
            tasks.append(task)
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
        for task in tasks:
            try:
                result += task.result
            except:
                continue
        while (len(result)):
            num = 0
            while (num < 50):
                try:
                    ip = result.pop()
                except:
                    break
                work = VerifyIP(ip)
                work.setDaemon(True)
                work.start()
                num += 1
            time.sleep(5)
        try:
            conn.commit()
        except:
            pass
        cursor.close()
        conn.close()
        print('[%s][ProxyPool]Crawl IP Count:' % get_current_time(), crawl_ip_count)
        print('[%s][ProxyPool][Sleeping]' % get_current_time())
        time.sleep(300)
