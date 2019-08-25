import requests
import execjs
import base64

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}

url = 'https://vipapi.qimingpian.com/DataList/productListVip'

data = {
    'time_interval': '',
    'tag': '',
    'tag_type': '', 
    'province': '',
    'lunci': '',
    'page': '1',
    'num': '20',
    'unionid': '',
}

resp = requests.post(url, headers = headers, data = data).json()
t = resp['encrypt_data']
with open('qmp_decrypt.js', 'r',encoding='utf-8') as f:
    qmp_js = f.read()
ctx = execjs.compile(qmp_js)
data = ctx.call('decrypt', t)
a = base64.b64decode(data)
data = a.decode("unicode-escape")
print(data)

