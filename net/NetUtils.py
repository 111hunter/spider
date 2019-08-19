from utils.Log import Log
import random
import time
from http import cookiejar
import requests

def sendLogic(func):
    def wrapper(*args, **kw):
        for count in range(5):
            response = func(*args, **kw)
            if response is not None:
                return response
            else:
                time.sleep(0.1)
        return None

    return wrapper

class eHttp(object):
    session = requests.Session()

    #静态方法是在类的作用域里的函数
    @staticmethod
    def get_session():
        return eHttp.session

    @staticmethod
    def check(target, log):
        if not target:
            Log.e(log)
            return False
        return True
        
    @staticmethod
    def setCookies(**kwargs):
        for k, v in kwargs.items():
            eHttp.session.cookies.set(k, v)    

    @staticmethod
    def load_cookies(cookie_path):
        #实例化一个LWPCookieJar对象
        load_cookiejar = cookiejar.LWPCookieJar()
        #从文件中加载cookies(LWP格式)
        load_cookiejar.load(cookie_path, ignore_discard=True, ignore_expires=True)
        #工具方法转换成字典
        load_cookies = requests.utils.dict_from_cookiejar(load_cookiejar)
        #工具方法将字典转换成RequestsCookieJar，赋值给session的cookies.
        eHttp.session.cookies = requests.utils.cookiejar_from_dict(load_cookies)

    @staticmethod
    def save_cookies(cookie_path):
        #实例化一个LWPcookiejar对象
        new_cookie_jar = cookiejar.LWPCookieJar(cookie_path)
        #将转换成字典格式的RequestsCookieJar（这里我用字典推导手动转的）保存到LWPcookiejar中
        requests.utils.cookiejar_from_dict({c.name: c.value for c in eHttp.session.cookies}, new_cookie_jar)        
        #保存到本地文件
        new_cookie_jar.save(cookie_path, ignore_discard=True, ignore_expires=True)

    @staticmethod
    def removeCookies(key=None):
        eHttp.session.cookies.set(key, None) if key else eHttp.session.cookies.clear()
 
    @staticmethod
    def resetHeaders():
        eHttp.session.headers.clear()
        eHttp.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        })

    @staticmethod
    def updateHeaders(headers):
        eHttp.session.headers.update(headers)
    
    @staticmethod
    @sendLogic
    def get_custom(urlInfo):
        try:
            response = eHttp.session.request(method=urlInfo['method'],
                                             url=urlInfo['url'],
                                             timeout=10,
                                             allow_redirects=False)
        except Exception as e:
            return None
        return response

    @staticmethod
    @sendLogic
    def post_custom(urlInfo,data=None):
        eHttp.resetHeaders()
        if 'headers' in urlInfo and urlInfo['headers']:
            eHttp.updateHeaders(urlInfo['headers'])
        try:
            response = eHttp.session.request(method=urlInfo['method'],
                                            url=urlInfo['url'],
                                            data=data,
                                            timeout=10,
                                            allow_redirects=False)
    
        except Exception as e:
            return None
        return response

    @staticmethod
    @sendLogic
    def send(urlInfo, params=None, data=None, **kwargs):
        eHttp.resetHeaders()
        if 'headers' in urlInfo and urlInfo['headers']:
            eHttp.updateHeaders(urlInfo['headers'])
        try:
            response = eHttp.session.request(method=urlInfo['method'],
                                            url=urlInfo['url'],
                                            params=params,
                                            data=data,
                                            timeout=10,
                                            allow_redirects=False,
                                            **kwargs)
            if response.status_code == requests.codes.ok:
                if 'response' in urlInfo:
                    if urlInfo['response'] == 'binary':
                        return response.content
                    if urlInfo['response'] == 'html':
                        response.encoding = response.apparent_encoding
                        return response.text
                return response.json()
        except:
            pass
        return None