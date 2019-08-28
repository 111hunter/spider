import requests
import json
from hashlib import md5
import execjs

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Content-Type': 'application/json',
}

def sig(s):
    md5_v = str(md5(s.encode()).hexdigest()).upper()
    return md5_v

def de_cry(d):
    with open('xiniu.js', 'r',encoding='utf-8') as f:
        decrypt_js = f.read()
    ctx = execjs.compile(decrypt_js)
    data = ctx.call('decrypt', d)
    return data

def en_cry(n):
    with open('xiniu.js', 'r',encoding='utf-8') as f:
        encrypt_js = f.read()
    ctx = execjs.compile(encrypt_js)
    data = ctx.call('encrypt', n)
    return data

def company_lib():
    url = 'https://www.xiniudata.com/api/search2/company/lib'
    data = {
        "payload":"LBcgWUQrZGATHHVgSiogJ1Z2DG9kfnZeIi0zOT8qXG1tbhkUEjonPWp7Ah8UZywsXjhZQxtoD29hbCsoOildOAhBJV8SdB0HZGM9LVUgJj1bNxQOGyYmRyhsfm8wMFwrPlsjZ1QvMj9qewIfFGc8J0IhQhYDcHYebyEgKTM3EHV1USFLU2xqeDsuKzYaf2J/AmQCGBsiNVUobGh9emdBJi1QZgICfjs=",
        "sig":"DD2BC59355FD050B5850814DC002C693",
        "v":1
    }
    resp = requests.post(url, headers = headers, data = json.dumps(data)).json()
    res_json1 = de_cry(resp['d'])
    res_dic = json.loads(res_json1)
    list = []
    for i in res_dic['data']:
        list.append(i['companyCode'])
    dict = {"payload": {"codes": list}}
    str1 = str(json.dumps(dict))
    payload = en_cry(str1)
    return payload

def list_by_codes(payload):
    url = 'https://www.xiniudata.com/api2/service/x_service/person_company4_list/list_companies4_list_by_codes'
    p = "W5D80NFZHAYB8EUI2T649RT2MNRMVE2O"
    data1 = {"payload":payload,"sig":sig(payload + p),"v":1}
    resp = requests.post(url, headers = headers, data = json.dumps(data1)).json()
    res_json2 = de_cry(resp['d'])
    print(res_json2)

if __name__ == "__main__":
    payload = company_lib()
    list_by_codes(payload)