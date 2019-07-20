import time
import hashlib
import random
import requests
import json

s=input("请输入你要翻译的汉语：")

def get_ts():
	ts=int(time.time()*1000)
	return ts

def get_bv():
	appVersion = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
	m=hashlib.md5()
	m.update(appVersion.encode('utf-8'))
	bv=m.hexdigest()
	return bv

def get_salt(ts):
	num=int(random.random()*10)
	salt=str(ts)+str(num)
	return salt

def get_sign(salt,s):
	a='fanyideskweb'
	b=str(s)
	c=salt
	d='97_3(jkMYg@T[KZQmqjTK'
	str_data=a+b+str(c)+d

	m=hashlib.md5()
	m.update(str_data.encode('utf-8'))
	sign=m.hexdigest()
	return sign

def get_form_data(s):
	ts=get_ts()
	salt=get_salt(ts)
	form_data={
		"i":str(s),
		"from":"AUTO",
		"to":"AUTO",
		"smartresult":"dict",
		"client":"fanyideskweb",
		"salt":str(salt),
		"sign":get_sign(salt,s),
		"ts":str(ts),
		"bv":get_bv(),
		"doctype":"json",
		"version":"2.1",
		"keyfrom":"fanyi.web",
		"action":"FY_BY_CLICKBUTTION",
	}
	return form_data

url='http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

headers={
	"Cookie":"_ntes_nnid=645d9bef1da9064d41f331b136f16d2d,1561639814911; OUTFOX_SEARCH_USER_ID_NCOO=946547902.8693012; OUTFOX_SEARCH_USER_ID=-1465406163@180.160.115.89; JSESSIONID=aaa3XcWEOSia-a86twrVw; ___rl__test__cookies=1562585479250",
	"Host":"fanyi.youdao.com",
	"Origin":"http://fanyi.youdao.com",
	"Pragma":"no-cache",
	"Referer":"http://fanyi.youdao.com/",
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
	"X-Requested-With":"XMLHttpRequest",
}

resp=requests.post(url,headers=headers,data=get_form_data(s)).json()
print("翻译结果：")
print(resp['translateResult'][0][0]['tgt'])
