import pymysql
import jieba
import re
from collections import Counter
from snownlp import SnowNLP
import time

# 保存评论
commentlist = []
# 创建连接对象
con = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='loski2000',
    db='bilicomments',
    charset='utf8'
)
# 获取游标对象
cur = con.cursor()
# sql语句
sql = "select message from bilicomment"
# 执行 SQL 语句 返回值就是 SQL 语句在执行过程中影响的行数
data = cur.execute(sql)
# 获得查询结果 () ()
result = cur.fetchall()
# 处理结果数据类型
for item in result:
    commentlist.append(item[0])
cur.close()
con.close()
# print(commentlist)

# 预测标签结果
tag_list = ['消极', '中性', '积极']
# 对应情感
num_list = [0, 0, 0]
# 情感判定
for comment in commentlist:
    sentiments_score = SnowNLP(comment).sentiments
    if sentiments_score < 0.5:
        num_list[0] += 1
    elif 0.5 <= sentiments_score < 0.6:
        num_list[2] += 1
    else:
        num_list[1] += 1
# print(num_list)

#插入hadoop2数据库rpv_list.emotion_list中
# 创建连接对象
con = pymysql.connect(
    host='192.168.71.112',
    port=3306,
    user='root',
    passwd='Loski@2000',
    db='rpv_list',
    charset='utf8'
)
# 获取游标对象
cur = con.cursor()
for i in range(3):
    # sql语句
    sql = "insert into emotion_list values('%s', %s)" % (tag_list[i], num_list[i])
    # 执行 SQL 语句 返回值就是 SQL 语句在执行过程中影响的行数
    print(sql)
    data = cur.execute(sql)
    print(data)
cur.close()
con.close()

# 数据清洗、打印输出、汇总
comment_all = ''  # 创建一个空字符串，用于汇总评论
for comment in commentlist:
    comment = comment.strip()
    comment = re.sub('<.*?>', '', comment)
    comment = re.sub('[\u200b]', '', comment)
    comment = re.sub(' ', '', comment)
    comment_all = comment_all + comment  # 通过字符串拼接汇总数据

# 用jieba库中的cut()函数进行分词
words = jieba.lcut(comment_all)

# 通过for循环语句提取长度大于等于两个字的词
report_words = []
for word in words:
    if len(word) >= 2:
        report_words.append(word)
# print(report_words)

# 获取词频最高的50个词
result = Counter(report_words).most_common(50)
# print(result)

# 按特定形状和特定颜色绘制词云图
# 获取词云图形状参数mask
from PIL import Image
import numpy as np
from wordcloud import WordCloud  # 导入相关库

background_pic = 'bilibili.jpg'  # 形状蒙版图片转换为数值数组
images = Image.open(background_pic)  # 打开形状蒙版图片
maskImages = np.array(images)  # 将形状蒙版图片转换为数值数组
# print(maskImages)

# 按照形状蒙版绘制词云图
content = ' '.join(report_words)  # 把列表转换为字符串
wc = WordCloud(font_path='simhei.ttf',  # 字体文件路径（这里为黑体）
               background_color='white',  # 背景颜色（这里为白色）
               width=700,  # 宽度
               height=700,  # 高度
               mask=maskImages  # 应用形状蒙版
               ).generate(content)  # 绘制词云图

# 修改词云图的底层颜色，这个blackgroud_pic就是之前的背景图片
from wordcloud import WordCloud, ImageColorGenerator
from imageio import imread

t = time.strftime('%y-%m-%d', time.localtime())
print(t)
path = t + '.png'
back_color = imread(background_pic)  # 读取图片
image_colors = ImageColorGenerator(back_color)  # 获取图片的颜色
wc.recolor(color_func=image_colors)  # 为词云图上色
wc.to_file('result.png')  # 导出成PNG格式图片


