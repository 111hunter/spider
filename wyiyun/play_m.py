import pygame
import requests
import os
import re

dirpath = 'D:\\temp\\'
file = 'one.mp3'

headers = {
    "Referer":"https://music.163.com/",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
}

def load_music(filepath):  #加载音乐
    pygame.mixer.music.load(filepath)

def play_music():
    pygame.mixer.music.play(-1)

def pause_music():
    pygame.mixer.music.pause()

def unpause_music():
    pygame.mixer.music.unpause() 

def play_pause():
	global pau
	p = input("""

	暂停按 'p' 
	继续按 'u'
	重新播放按 'r'

请选择:""")
	if(p == 'r'):
		play_music()
	elif(p == 'p'):
		pause_music()
	elif(p == 'u'):
		unpause_music()

def init_url(t):
	url = 'http://music.163.com/song/media/outer/url?id={}'.format(t)
	return url

def get_song(url):
	print("\nWait a few seconds...")
	pygame.mixer.init()
	filepath = dirpath + file
	print("下载链接: "+url)
	res=requests.get(url=url,headers=headers)
	if not os.path.exists(dirpath):
		os.mkdir(dirpath)
	load_music('C:\\Windows\\media\\Alarm01.wav') #此处需要加载别的文件取消程序占用才能写入
	with open(filepath,'wb') as f:
		f.write(res.content)
	print("加载成功!")
	load_music(filepath)
	play_music()
	id = re.findall(r'id=(\d+)',url)[0]
	return str(id)