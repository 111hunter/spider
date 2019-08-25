import re
import execjs
import requests

headers={
    "referer":"https://music.163.com/",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}

url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_423228325?csrf_token='
def init_url(id):
	global url
	url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(id)

rid = re.findall('comments/(.*?)\?',url)[0]
offset=0
parm_1='{"rid":"%s","offset":"%d","total":"false","limit":"20","csrf_token":""}' % (rid,offset)
parm_2='010001'
parm_3='00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
parm_4='0CoJUm6Qyw8W8jud'

def get_comments():
	with open("core.js") as f:
	    data=f.read()
	getParams=execjs.compile(data).call("asrsea",parm_1,parm_2,parm_3,parm_4)
	formdata={
	    "params":getParams["encText"],
	    "encSecKey":getParams["encSecKey"]
	}
	resp=requests.post(url=url,headers=headers,data=formdata).json()
	print("\t----按'q'退出评论----\n")
	if len(resp["hotComments"]):
		for i in resp["hotComments"]:
		    print('"',i["content"],'"  --by',i["user"]["nickname"],"\n")
		    q = input()
		    if(q == 'q'):
		    	return
	else:
		for i in resp["comments"]:
		    print('"',i["content"],'"  --by',i["user"]["nickname"],"\n")
		    q = input()   
		    if(q == 'q'):
		    	return