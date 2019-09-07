import requests
import re, os, random, time
import numpy as np
import jieba
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 评论数据保存文件
COMMENTS_FILE_PATH = 'comments.txt'
# 词云形状图片
WC_MASK_IMG = 'butterfly.jpeg'
# 词云字体
WC_FONT_PATH = r'C:\\Windows\\Fonts\\msyhl.ttc'

def spider_comment(p=1):
    comment_url = 'https://book.douban.com/subject/1084336/comments/hot?p=' + str(p)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    try:
        print("开始爬取第" + str(p) + "页:" + comment_url)
        r = requests.get(comment_url, headers = headers)
        r.raise_for_status()
    except:
        print("爬取失败, p=" + str(p))
    comments = re.findall('<span class="short">(.*?)</span>', r.text)   
    with open(COMMENTS_FILE_PATH, 'a+', encoding = r.encoding) as f:
        f.write('\n'.join(comments))

def batch_spider(p=1):
    while spider_comment(p):
        time.sleep(random.random() * 3)

# 对数据分词
def cut_word():
    with open(COMMENTS_FILE_PATH, encoding = 'utf-8') as file:
        comment_txt = file.read()
        wordlist = jieba.cut(comment_txt, cut_all=True)
        wl = " ".join(wordlist)
        print(wl)
        return wl

# 生成词云
def create_word_cloud():
    # 设置词云形状图片
    wc_mask = np.array(Image.open(WC_MASK_IMG))
    # 设置词云的一些配置，如：字体，背景色，词云形状，大小
    wc = WordCloud(background_color="white", max_words=2000, mask=wc_mask, scale=4,
                   max_font_size=50, random_state=42, font_path=WC_FONT_PATH)
    wc.generate(cut_word())
    # 在只设置mask的情况下,你将会得到一个拥有图片形状的词云
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    plt.show()

if __name__ == '__main__':
    # if os.path.exists(COMMENTS_FILE_PATH):
    #     os.remove(COMMENTS_FILE_PATH)
    # p = 1
    # while p <= 50:
    #     batch_spider(p)
    #     p += 1
    # print("爬取完毕, 可生成词云")
    create_word_cloud()    
