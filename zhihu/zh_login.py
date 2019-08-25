"""
知乎登录
如使用抓包工具如fiddler,在请求参数中添加"verify=False"
"""

# -*- coding:UTF-8 -*-
import requests
import execjs
import time
import hashlib
import hmac
from PIL import Image
import base64
from http import cookiejar  # 用于保存登陆的cookie


class ZhiHu(object):

    def __init__(self):
        self.timestamp = int(time.time() * 1000)
        self.phone = input("请输入手机号:")  # 账号
        self.password = input("请输入密码:")  # 密码
        self.username = '我的邀请'  # 用于验证登陆
        self.headers = {
            "content-type":"application/x-www-form-urlencoded",
            "origin":"https://www.zhihu.com",
            "pragma":"no-cache",
            "referer":"https://www.zhihu.com/signin?next=%2F",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "x-requested-with":"fetch",
            "x-xsrftoken":"PKIIKSi56hAGtkE2wvNuBaLHInUzvPb6",
            "x-zse-83":"3_2.0",
        }
        self.session = requests.session()
        self.session.cookies = cookiejar.LWPCookieJar('cookie.txt')  # 保存的cookie文件
        with open('zh_login.js', 'r', encoding='utf-8') as f:
            self.encry_js = f.read()

    def get_signature(self):
        h = hmac.new(b'd1b964811afb40118a12068ff74a12f4', None, hashlib.sha1)
        h.update('password'.encode('utf-8'))
        h.update('c3cef7c66a1843f8b3a9e6a1e3160e20'.encode('utf-8'))
        h.update('com.zhihu.web'.encode('utf-8'))
        h.update(str(self.timestamp).encode('utf-8'))
        return h.hexdigest()

    def get_captcha(self):
        url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
        r = self.session.get(url, headers=self.headers)
        if r.status_code == 200 and 'true' in r.text:
            print('需要输入验证码')
            r = self.session.put(url, headers=self.headers)
            with open('captcha.png', 'wb') as f:
                content = base64.b64decode(r.json()['img_base64'])  # 需要先将base64加密的解密为字符串
                f.write(content)
            img = Image.open('captcha.png')
            img.show()
            captcha = input('请输入验证码\n>')
            return captcha

    def verify_captcha(self, captcha):
        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        data = {
            'input_text': captcha
        }
        url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
        r = self.session.post(url, headers=headers, data=data)
        return 'true' in r.text

    def get_form_data(self, signature, captcha):
        text = "client_id=c3cef7c66a1843f8b3a9e6a1e3160e20&grant_type=password&timestamp={0}&" \
               "source=com.zhihu.web&signature={1}&username=%2B86{2}&password={3}&" \
               "captcha={4}&lang=en&ref_source=homepage&utm_source=&ref_source=other_https%3A%2F%2Fwww.zhihu.com%2Fsignin%3Fnext%3D%252F".format(self.timestamp, signature, self.phone, self.password, captcha)
        ctx = execjs.compile(self.encry_js)
        encry = ctx.call('b',text)
        return encry

    def login(self,encry):
        url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        a=self.session.post(url, headers=self.headers, data=encry)
        print(a.status_code)
        print(a.text)

    def verify_login(self):
        r = self.session.get('https://www.zhihu.com/notifications', headers=self.headers)
        with open('a.txt','wb') as f:
            f.write(r.content)
        if self.username in r.text:
            print('登陆成功')
            self.session.cookies.save()
            return True
        else:
            print('登陆失败')
            return False

    def run(self):
        sign = self.get_signature()
        captcha = self.get_captcha()
        if captcha:
            while not self.verify_captcha(captcha):
                captcha = self.get_captcha()
        encry = self.get_form_data(sign, captcha)
        encry=encry[:-4]
        self.login(encry)

    def read_cookie2login(self):
        # 读取cookie来登陆
        try:
            self.session.cookies.load()  # 加载cookie到session
            print('加载cookie成功')
        except:
            print('cookie未能加载，需要登陆')
            self.run()
        # 验证登陆
        print(self.verify_login())


if __name__ == '__main__':
    zhihu = ZhiHu()
    zhihu.read_cookie2login()