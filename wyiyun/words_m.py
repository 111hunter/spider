import requests

headers = {
    "Referer":"https://music.163.com/",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
}

def get_words(id):
    url = 'http://music.163.com/api/song/lyric?id={}&lv=1&kv=1&tv=-1'.format(id)
    resp = requests.get(url = url,headers = headers).json()
    try:
        res = resp['lrc']['lyric']
        print(res)
    except:
        print("纯音乐,请欣赏")
    input()