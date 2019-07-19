import requests
from pyquery import PyQuery as pq
import re

base = 'https://music.163.com/song?id='

headers={
	"referer":"https://music.163.com/",
	"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
}

def rec(id):	
	html = requests.get(url = base + id,headers = headers).content.decode()
	doc = pq(html)
	a = doc('ul.m-sglist.f-cb a')
	result = re.findall(r'song\?id=(.*?)".*?">(.*?)</a>.*?id=.*?">(.*?)</a>',str(a),re.S)
	n = 1
	li = []
	print("\n相似推荐:\n")
	for i in result:
		print(n,i[1],i[2])
		li.append(i[0])
		n += 1
	ch = input("\n请选择:")
	try:
		chi = int(ch)
		if chi > 0 and chi <= 5:
			id = str(li[chi-1])
			return id
	except:
		return