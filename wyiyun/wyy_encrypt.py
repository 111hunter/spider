import json
import random
import binascii
import base64
from Crypto.Cipher import AES
import requests

url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='

headers = {
    "Host":"music.163.com",
    "Connection":"keep-alive",
    "Origin":"https://music.163.com",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Content-Type":"application/x-www-form-urlencoded",
    "Accept":"*/*",
    "Referer":"https://music.163.com/search/",
}

def random_b():
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(16):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return bytes(salt, 'utf-8')

#第二参数，rsa公匙组成
pub_key = "010001"
#第三参数，rsa公匙组成
modulus = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
#第四参数，aes密匙
secret_key = b'0CoJUm6Qyw8W8jud'

def aes_encrypt(text, key):
    # 偏移量
    iv = b'0102030405060708'
    # 对长度不是16倍数的字符串进行补全，然后在转为bytes数据
    pad = 16 - len(text) % 16
    try:
        # 如果接到bytes数据（如第一次aes加密得到的密文）要解码再进行补全
        text = text.decode()
    except:
        pass
    text = text + pad * chr(pad)
    try:
        text = text.encode()
    except:
        pass
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')  # 得到的密文还要进行base64编码
    return ciphertext

def rsa_encrypt(random_char):
    text = random_char[::-1]#明文处理，反序并hex编码
    rsa = int(binascii.hexlify(text), 16) ** int(pub_key, 16) % int(modulus, 16)
    return format(rsa, 'x').zfill(256)

def aes_param(data):
    text = json.dumps(data)
    print(text)
    random_char = random_b()
    params = aes_encrypt(text, secret_key)#两次aes加密
    params = aes_encrypt(params, random_char)
    enc_sec_key = rsa_encrypt(random_char)
    data = {
        'params': params,
        'encSecKey': enc_sec_key
    }
    return data

if __name__ == "__main__":
    str=input("请输入歌曲名字:")
    data = {
        "hlpretag": "<span class=\"s-fc7\">",
        "hlposttag": "</span>",
        "s": str,
        "type": "1",
        "offset": "0",
        "total": "true",
        "limit": "30",
        "csrf_token": ""
    }
    formdata = aes_param(data)
    print(formdata)