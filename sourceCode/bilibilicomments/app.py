from flask import Flask, render_template, request, session, redirect, url_for
import utils
import pymysql

app = Flask(__name__)

'''
@app.before_request
def before():
    url = request.path  # 当前请求的URL
    passUrl = ["/login", "/regist"]
    if url in passUrl:
        pass
    else:
        return render_template("login.html")'''


@app.route("/")
def main():
    return render_template("login.html")


@app.route("/login")
def login():
    if request.method == 'GET':  # 注册发送的请求为POST请求
        username = request.args.get('username')
        password = request.args.get('password')
        con = pymysql.connect(
            host='192.168.71.112',
            port=3306,
            user='root',
            passwd='',
            db='rpv_list',
            charset='utf8'
        )
        cur = con.cursor()
        if username == '' or password == '':
            login_massage = "温馨提示：请填写账户和密码!"
            return render_template('login.html', message=login_massage)

        sql = "SELECT * FROM users WHERE usrname ='%s' and pwd ='%s'" % (username, password)
        cur.execute(sql)
        result = cur.fetchall()
        #print(result)
        if len(result) != 0:
            return redirect(url_for('index'))

        sql = "SELECT * FROM users WHERE usrname ='%s'" % (username)
        cur.execute(sql)
        result = cur.fetchall()
        if len(result) != 0:
            login_massage = "温馨提示：密码错误，请输入正确密码"
            return render_template('login.html', message=login_massage)
        else:
            login_massage = "温馨提示：不存在该用户"
            return render_template('login.html', message=login_massage)
    return render_template('login.html')

@app.route("/templates/wordcloud.html", methods=["GET", "POST"])
def wordcloud():
    return render_template("wordcloud.html")


@app.route("/index", methods=["GET", "POST"])
def index():
    emoanalyselist, daycountlist, userinfolist, commentlist = utils.get_data(0)
    return render_template("index.html", emoanalyselist=emoanalyselist, daycountlist=daycountlist, users=userinfolist, comments=commentlist)

if __name__ == '__main__':
    app.run()
