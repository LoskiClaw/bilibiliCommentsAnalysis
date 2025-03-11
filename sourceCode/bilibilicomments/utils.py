import time, datetime
import pymysql


def get_time(n):
    # 获取今天（现在时间）
    now = datetime.datetime.today()
    # 获取前n天
    nex = now - datetime.timedelta(days=n)
    return nex.strftime("%Y%m%d")


def get_data(num):
    con = pymysql.connect(
        host='192.168.71.112',
        port=3306,
        user='root',
        passwd='Loski@2000',
        db='rpv_list',
        charset='utf8'
    )
    cur = con.cursor()

    if num == 0 or num == 1:
        emoanalyse_sql = "select * from emotion_list"; '''where dt={get_time(num)}'''
        daycount_sql = "select * from day_count_list"; '''where dt={get_time(num)}'''
        comment_sql = "select * from comment_list"; '''where dt={get_time(num)}'''
        userinfo_sql = "select * from usr_rank_list"; '''where dt={get_time(num)}'''
    else:
        emoanalyse_sql = "select emotiontype, sum(count_num) from emotion_list"; '''where dt between {get_time(num)} and {get_time(0)} group by emotiontype'''
        daycount_sql = "select daytime,sum(countnum),sum(likesnum) from day_count_list"; '''where dt between {get_time(num)} and {get_time(0)} group by weekday'''
        comment_sql = "select comtime, content from comment_list"; '''where dt between {get_time(num)} and {get_time(0)}'''
        userinfo_sql = "select usrname, usrlevel, usrsex, sum(usrlikes) from view_usr_rank_list"; '''where dt between {get_time(num)} and {get_time(0)} group by usrname order by usrlikes desc limit 10'''

    # get emoAnalyse
    emoanalyselist = []
    emoanalyselist.append(0)
    emoanalyselist.append(0)
    emoanalyselist.append(0)
    data = cur.execute(emoanalyse_sql)
    result = cur.fetchall()
    for item in result:
        if item[0] == '平和':
            emoanalyselist[0] += item[1]
        if item[0] == '积极':
            emoanalyselist[1] += item[1]
        if item[0] == '消极':
            emoanalyselist[2] += item[1]

    # get daycount
    daycountlist = [[], [], []]
    data = cur.execute(daycount_sql)
    result = cur.fetchall()
    for item in result:
        daycountlist[0].append(str(item[0]))
        daycountlist[1].append(item[1])
        daycountlist[2].append(0)
    #print(daycountlist)
    # get comments
    commentlist = []
    data = cur.execute(comment_sql)
    result = cur.fetchall()
    for item in result:
        commentlist.append(item)
    #print(commentlist)
    # get userinfo by userlikes desc
    userinfolist = []
    data = cur.execute(userinfo_sql)
    result = cur.fetchall()
    for item in result:
        usr = []
        usr.append(item[0])
        usr.append(item[1])
        usr.append(item[2])
        usr.append(item[3])
        usr.append(item[4])
        userinfolist.append(usr)
    #print(userinfolist)
    cur.close()
    con.close()
    return emoanalyselist, daycountlist, userinfolist, commentlist


if __name__ == "__main__":
    # res = []
    # for tup in get_pv_region(1):
    #     res.append({"name": tup[0], "value": int(tup[1])})
    # res.sort(key=lambda x:x["value"], reverse=True)
    # print(res)
    print(get_data(0))
    # print(get_time(0))
    pass
