import re
import execjs
import requests
import hashlib
from http import cookiejar  # 用于保存登陆的cookie

class wyy_login(object):
	def __init__(self):
		phone = input("请输入手机号:") 
		pwd = input("请输入密码:")
		pwd = hashlib.md5(bytes(pwd,encoding='utf-8')).hexdigest()
		self.parm_1 = '{"phone":"%s","password":"%s","rememberLogin":"true","checkToken":"","csrf_token":""}' % (phone,pwd)
		self.username = ''  #验证登录
		self.parm_2 = '010001'
		self.parm_3 = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
		self.parm_4 = '0CoJUm6Qyw8W8jud'
		self.headers = {
			"referer":"https://music.163.com/",
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
		}
		self.session = requests.session()
		self.session.cookies = cookiejar.LWPCookieJar('cookie.txt')  # 保存的cookie文件
		with open('core1.js', 'r', encoding='utf-8') as f:
			self.encry_js = f.read()

	def get_from_data(self):
		ctx=execjs.compile(self.encry_js)
		print(self.parm_1)
		encry=ctx.call("asrsea",self.parm_1,self.parm_2,self.parm_3,self.parm_4)
		return encry

	def login(self,encry):
		url='https://music.163.com/weapi/login/cellphone?csrf_token='		
		formdata={
			"params":encry["encText"],
			"encSecKey":encry["encSecKey"]
		}
		a=self.session.post(url,headers=self.headers,data=formdata)
		print(a.status_code)
		print(a.content.decode())

	def verify_login(self):
		r = self.session.get('https://music.163.com/#/friend', headers=self.headers)
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
		encry=self.get_from_data()
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
	wyy=wyy_login()
	wyy.read_cookie2login()