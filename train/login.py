'''
登录
'''
from conf.urls_conf import loginUrls
from net.NetUtils import eHttp
from utils.Log import Log
from utils.Utils import check

from collections import OrderedDict
from PIL import Image
from io import BytesIO
import time, copy, json, os

def loginLogic(func):
    def wrapper(*args, **kw):
        reslut = False
        msg = ''
        for count in range(10):
            Log.v('第%s次尝试获取验证图片' % str(count + 1))
            reslut, msg = func(*args, **kw)
            if reslut:
                break
            Log.w(msg)
        return reslut, msg

    return wrapper
 
class Captcha(object):
    __CAPTCHA_CHECK = '4'

    def getCaptcha(self):
        urlInfo = loginUrls['normal']['captcha']
        Log.v('正在获取验证码..')
        return eHttp.send(urlInfo)
    
    def __indexTransCaptchaResults(self, indexes, sep=r','):
        coordinates = ['31, 35', '116, 46', '191, 24', '243, 50', '22, 114', '117, 94', '167, 120', '251, 105']
        results = []
        for index in indexes.split(sep=sep):
            results.append(coordinates[int(index)])
        return ','.join(results)

    #人眼识别12306验证码
    def verifyCaptchaByHand(self):
        img = None
        try:
            img = Image.open(BytesIO(self.getCaptcha()))
            img.show()
            Log.v(
                """ 
                -----------------
                | 0 | 1 | 2 | 3 |
                -----------------
                | 4 | 5 | 6 | 7 |
                ----------------- """)
            results = input("输入验证码索引(见上图，以','分割）: ")
        except BaseException as e:
            print("验证码载入失败")
            return None, False
        finally:
            if img is not None:
                img.close()
        results = self.__indexTransCaptchaResults(results)
        Log.v('验证码坐标: %s' % results)
        return results, self._captchaCheck(results)

    #校验识别验证码结果
    def _captchaCheck(self, results):
        data = {
            'answer': results,
            'login_site': 'E',
            'rand': 'sjrand',
            '_': int(time.time() * 1000)
        }
        jsonRet = eHttp.send(loginUrls['normal']['captchaCheck'], params=data)
        def verify(response):
            return Captcha.__CAPTCHA_CHECK == response['result_code'] if 'result_code' in response else False
        return verify(jsonRet)

class Login(object):

    def _login_init(self):
        url_info = copy.deepcopy(self._urlInfo['getDevicesId'])
        ua = url_info['headers']['User-Agent'].replace(' ','%20')
        url_info['url'] = self._urlInfo['getDevicesId']['url'].format(ua, str(round(time.time()*1000)))
        devices_id_rsp = eHttp.get_custom(url_info)
        if devices_id_rsp:
            callback = devices_id_rsp.text.replace("callbackFunction('", '').replace("')", '')
            text = json.loads(callback)
            devices_id = text.get('dfp')
            exp = text.get('exp')
            eHttp.setCookies(RAIL_DEVICEID=devices_id, RAIL_EXPIRATION=exp)
            return True, '获取设备指纹成功'
        else:
            return False,'获取设备指纹失败'

    def _uamtk(self):
        jsonRet = eHttp.send(self._urlInfo['uamtk'], data={'appid': 'otn'})

        def isSuccess(response):
            return response['result_code'] == 0 if response and 'result_code' in response else False

        return isSuccess(jsonRet), \
                jsonRet['result_message'] if jsonRet and 'result_message' in jsonRet else 'no result_message', \
                jsonRet['newapptk'] if jsonRet and 'newapptk' in jsonRet else 'no newapptk'

    def _uamauthclient(self, apptk):
        jsonRet = eHttp.send(self._urlInfo['uamauthclient'], data={'tk': apptk})

        def isSuccess(response):
            return response['result_code'] == 0 if response and 'result_code' in response else False

        return isSuccess(jsonRet), '%s:%s' % (jsonRet['username'], jsonRet['result_message']) if jsonRet \
            else 'uamauthclient failed'

    def login(self, userName, userPwd):
        result, msg = self._loginNormal(userName, userPwd)
        if check(result, msg):
            return result, msg
        return False, '登录失败'

    @loginLogic 
    def _loginNormal(self, userName, userPwd):
        self._urlInfo = loginUrls['normal']
        status,msg = self._login_init()                    #登录前获取浏览器指纹
        if not status:
            return status, msg
        results, verify = Captcha().verifyCaptchaByHand()  #登录第一步验证码识别
        if not verify:
            return False, '验证码识别错误!'
        Log.v('验证码识别成功')
        payload = OrderedDict()                            #登录第二步验证用户账号和密码
        payload['username'] = userName
        payload['password'] = userPwd
        payload['appid'] = 'otn'
        payload['answer'] = results        
        response = eHttp.post_custom(self._urlInfo['login'], data=payload)
        result, msg, apptk = self._uamtk()                 #登录第三步获取uamtk作为下一次请求参数
        if not check(result, msg):
            return False, 'uamtk failed'
        return self._uamauthclient(apptk)                  #登录最后一步验证客户端