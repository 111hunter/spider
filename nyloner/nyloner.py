import requests
from hashlib import md5
import time
import execjs

url = 'https://nyloner.cn/proxy'

headers = {
    'Host':'nyloner.cn',
    'Connection':'keep-alive',
    'X-Requested-With':'XMLHttpRequest',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Referer':'https://nyloner.cn/proxy',
    'Cookie':'sessionid=kgi38x996rkysjhpyytnvmqkaafcyzjc',
}

page = '1'
num = '15'
t = str(int(time.time()))
s = page + num + t
data = {
    'page': page,
    'num': num,
    'token': str(md5(s.encode()).hexdigest()),
    't': t,
}

resp = requests.get(url, headers = headers, params = data).json()
en_str = resp['list']
with open('nyloner.js', 'r',encoding='utf-8') as f:
    nyloner_js = f.read()
ctx = execjs.compile(nyloner_js)
de_str = ctx.call('decode_str', en_str)
print(de_str)
