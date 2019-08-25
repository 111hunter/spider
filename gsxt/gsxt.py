import requests
import re
import execjs

url = "http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html"

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}

session = requests.session()
response = session.get(url, headers=headers)

# 生成cookie中的字段，设置cookie
res = re.findall('<script>(.*?)</script', response.text)[0]
js = res.replace('{eval(', '{var params_1 = (')
node = execjs.get()
ctx = node.compile(js)
js1 = ctx.eval('params_1')
js2 = re.findall("document.(cookie=.+)\+';Expires", js1)[0]
ctx1 = node.compile(js2)
js_get_cookie = ctx1.eval('cookie')
cookies = js_get_cookie.split('=')
session.cookies.set(cookies[0], cookies[1])

session.get(url, headers=headers)
cookies = requests.utils.dict_from_cookiejar(session.cookies)
print(cookies)

querystring = {
    "noticeType": "11", 
    "areaid": "100000", 
    "noticeTitle": "", 
    "regOrg": ""
}

payload = "draw=1&start=0&length=10"
res = session.post(url, headers=headers,data=payload, params=querystring,cookies=cookies)
if res.status_code == 200:
    res.encoding = res.apparent_encoding
    print(res.text)