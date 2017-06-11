import requests
from bs4 import BeautifulSoup
from PIL import Image
import re
from .recognize import CaptchaRecognize, convert_image
import logging
import time

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def get_current_time():
    timenow = time.strftime('%Y-%m-%d %X', time.localtime())
    return timenow


def mimvp_proxy():
    urls = ['http://proxy.mimvp.com/free.php?proxy=in_hp', 'http://proxy.mimvp.com/free.php?proxy=out_hp',
            'http://proxy.mimvp.com/free.php?proxy=in_tp', 'http://proxy.mimvp.com/free.php?proxy=out_tp']
    result = []
    imageRecognize = CaptchaRecognize()
    for url in urls:
        try:
            html = requests.get(url, headers=headers, timeout=30).text
            table = BeautifulSoup(html, 'lxml').find('div', id='list').find('tbody')  # .find_all('tr')
        except Exception as e:
            print('[%s][Spider][mimvp]Error!' % get_current_time(), logging.exception(e))
            continue
        table = re.findall('(\d+\.\d+\.\d+\.\d+).*?img src="(.*?)"', str(table))
        for item in table:
            try:
                ip = item[0]
                imgurl = 'http://proxy.mimvp.com/' + item[1].replace('amp;', '')
                image = getimage(imgurl)
                port_str_list = imageRecognize.recognise(image)
                port = [item[1] for item in port_str_list]
                port = ''.join(port)
                result.append(ip + ':' + port)
            except:
                continue
    print('[%s][Spider][mimvp]OK!' % get_current_time(), 'Crawled IP Count:', len(result))
    return result


def getimage(imgurl):
    with open('./temp.png', 'wb') as img:
        content = requests.get(imgurl, headers=headers, timeout=20).content
        img.write(content)
    image = Image.open('./temp.png')
    image = convert_image(image)
    return image
