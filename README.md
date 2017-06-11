### ProxyPool

#### 1.配置
##### 1.数据库配置
在`conf.py`中修改数据库配置，并新建`proxypool`表。
```
sql>create table proxypool(ip char(20),port char(5),time char(30));
```

##### 2.安装Python库
```
pip3 install pymysql
pip3 install requests
pip3 install bs4
pip3 install lxml
```
#### 2.运行
抓取代理IP
```
python3 proxypool.py
```

定时验证IP
```
python3 verify.py
```





