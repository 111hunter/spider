import requests 
import execjs
import json
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
}

cookies = dict()


def getanaly(synct, params):
    with open('qimai.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
        ctx = execjs.compile(js_content)
        new_pwd = ctx.call("get0analysis", synct, params)
        return new_pwd

def qimai():
    resp = requests.get('https://www.qimai.cn/rank', headers=headers)
    cookies.update(resp.cookies.get_dict())
    synct = cookies.get('synct')

    for i in range(3):
        params = {
            'brand': 'all',
            'country': 'cn',
            'device': 'iphone',
            'genre': '5000',
            'date': '2019-07-21',
        }
        url = "https://api.qimai.cn/rank/indexPlus/brand_id/" + str(i)
        analy_list = getanaly(synct, params)
        params['analysis'] = analy_list[i]
        resp = requests.get(url=url, params=params, headers=headers, cookies=cookies)
        resjson = json.loads(resp.text)
        contents = resjson['list']
        for content in contents:
            appInfo = content['appInfo']
            print(appInfo)
        time.sleep(5)

if __name__ == '__main__':
    qimai()
