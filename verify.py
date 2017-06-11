import requests
import threading
import time
import pymysql
from conf import MYSQL_CONF

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_current_time():
    return time.strftime('%Y-%m-%d %X', time.localtime())


class VerifyIP(threading.Thread):
    def __init__(self, ip):
        super(VerifyIP, self).__init__()
        self.ip = ip
        self.proxies = {
            'http': 'http://%s' % (ip)
        }

    def run(self):
        try:
            html = requests.get('http://httpbin.org/ip', proxies=self.proxies, timeout=3).text
            result = eval(html)['origin']
            if len(result.split(',')) == 2:
                with lock:
                    self.delete()
                return
            elif result in self.ip:
                with lock:
                    self.update()
            else:
                with lock:
                    self.delete()
        except:
            with lock:
                self.delete()

    def update(self):
        global cursor
        global conn
        global update_ip_count
        try:
            date = get_current_time()
            cursor.execute("update proxypool set time='%s' where ip='%s'" % (date, self.ip.split(':')[0]))
            conn.commit()
            update_ip_count += 1
        except:
            pass

    def delete(self):
        global cursor
        global conn
        global delete_ip_count
        try:
            cursor.execute("delete from proxypool where ip='%s'" % (self.ip.split(':')[0]))
            conn.commit()
            delete_ip_count += 1
        except:
            pass


def verify():
    cursor.execute('select ip,port from proxypool')
    ip_list = []
    for row in cursor.fetchall():
        ip_list.append("%s:%s" % (row[0], row[1]))
    while len(ip_list):
        count = 0
        while count < 20:
            try:
                ip = ip_list.pop()
                count += 1
            except:
                break
            work = VerifyIP(ip)
            work.setDaemon(True)
            work.start()
        time.sleep(5)


if __name__ == '__main__':
    lock = threading.Lock()
    while True:
        delete_ip_count = 0
        update_ip_count = 0
        conn = pymysql.connect(host=MYSQL_CONF['host'],
                               user=MYSQL_CONF['user'],
                               passwd=MYSQL_CONF['passwd'],
                               db=MYSQL_CONF['db'],
                               port=MYSQL_CONF['port'],
                               charset='utf8')
        cursor = conn.cursor()
        verify()
        print('[%s][Verify]Delete IP Count:' % get_current_time(), delete_ip_count)
        print('[%s][Verify]Update IP Count:' % get_current_time(), update_ip_count)
        time.sleep(180)
        cursor.close()
        conn.commit()
        conn.close()
