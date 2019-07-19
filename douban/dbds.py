import requests
import execjs  
import re
from urllib.request import quote

name=input("搜索请输入图书名字☖:")
print("\n为您找到以下图书及评分信息☗:\nWaitting a few seconds...\n")
name_url=quote(name)
url='https://book.douban.com/subject_search?search_text={}&cat=1001'.format(name_url)
response = requests.get(url)
r = re.search('window.__DATA__ = "([^"]+)"', response.text).group(1)  # 加密的数据
with open('key_encrypt.js', 'r',encoding='utf-8') as f:
    decrypt_js = f.read()
ctx = execjs.compile(decrypt_js)
data = ctx.call('decrypt', r)
for item in data['payload']['items']:
    if 'title' and 'rating' in item:
        print(item['title'],item['rating']['value'])