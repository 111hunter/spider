import requests
import execjs
import json

url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Referer":"https://music.163.com/search/",
}

parm_2='010001'
parm_3='00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
parm_4='0CoJUm6Qyw8W8jud'

formdata = {}

def init_search():
    str=input("\n请输入歌曲名字:")
    if(str == None):
        return
    parm_1={"hlpretag":"<span class=\"s-fc7\">","hlposttag":"</span>","s":str,"type":"1","offset":"0","total":"true","limit":"30","csrf_token":""}
    parm_1=json.dumps(parm_1)
    with open("core.js") as f:
        data=f.read()
    getParams=execjs.compile(data).call("asrsea",parm_1,parm_2,parm_3,parm_4)
    global formdata
    formdata = {
        "params":getParams["encText"],
        "encSecKey":getParams["encSecKey"]
    }

def req_search():
    print("为您找到以下歌曲:\n")
    resp=requests.post(url=url,headers=headers,data=formdata).json()
    li = resp['result']['songs']
    n = 1
    lis = []
    for i in li:
        print(n,i['name'],"  --"+i['ar'][0]['name']+"--  ") #,i['id'])
        lis.append(i['id'])
        n += 1
    print("\n")
    ch = input("请选择:")
    try:
        chi = int(ch)
        if chi > 0 and chi < 31:
            return lis[chi-1]
    except:
        return

