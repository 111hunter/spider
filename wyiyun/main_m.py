import play_m 
import search_m 
import recommends_m 
import comments_m 
import words_m 
import os

id = '1328146041'

def search():
	global id
	search_m.init_search()
	tid = search_m.req_search()
	if(tid != None):
		y = input("播放? 'y' or 'n':")
		if(y == 'y'):	
			id = tid
			url = play_m.init_url(id)
			id = play_m.get_song(url)
			input()

def rec_dfs(tid):
	global id
	tid = recommends_m.rec(tid)
	if(tid != None):
		url = play_m.init_url(tid)
		y = input("播放? 'y' or 'n':")
		if(y == 'y'):
			id = play_m.get_song(url)
		rec_dfs(tid)


def choice(w):
	global id
	if(w == '1'):
		try:
			search()
		except:
			print("请您检查网络并输入正确歌曲名☕")
			input()
	elif(w == '2'):
		try:
			tid = id
			rec_dfs(tid)
		except:
			print("网络异常")
			input()
	elif(w == '3'):
		try:
			comments_m.init_url(id)
			comments_m.get_comments()
		except:
			print("网络异常")
			input()
	elif(w == '4'):
		try:
			words_m.get_words(id)
		except:
			print("网络异常")
			input()
	elif(w == '5'):
		try:
			play_m.play_pause()
		except:
			print("请先加载音乐")
			input()
	elif(w == '0'):
		exit()

if __name__ == '__main__':
	while True:
		os.system('cls')
		print("""
 *****--welcome--*****
 *                   *
 *     one-song      *
 *    1.搜索歌曲     *
 *    2.相似推荐     *
 *    3.热门评论     *
 *    4.查看歌词     *
 *    5.播放暂停     *
 *    0.退出         *
 *                   *
 *********************
		""")
		w=input("  请选择：")
		os.system('cls')
		choice(w)	