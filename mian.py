from flask import Flask, render_template, session, request
from databaseconfig import config
import pymysql
from function import checklogin

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def hello_world():
    checklogin()
    if 'username' in session:
        print session['username']
        return render_template('teacher.html')
    return render_template('login.html')


@app.route('/login', methods=['post', 'get'])
def fun_login():
    username = request.form.get('username')
    password = request.form.get('password')
    print username, password
    session['username'] = username
    coon = pymysql.connect(**config)
    cur = coon.cursor()
    sql = "SELECT * from account WHERE  username= %s"
    cur.execute(sql, (username))
    coon.commit()
    result = cur.fetchone()
    cur.close()
    coon.close()

    if result[2] == password:
        session['username'] = username
        session['idenfity'] = result[4]
        return render_template('teacher.html')
    else:
        return render_template('login.html')


@app.route('/logout', methods=['get'])
def logout():
    session.pop('username', None)
    return "log out success"


@app.route('/changepassword', methods=['post'])
def changepassword():
    checklogin()
    print  "change"
    username = session['username']
    newpassword = request.form.get('newpassword')
    oldpassword = request.form.get('oldpassword')

    print  newpassword
    print oldpassword
    coon = pymysql.connect(**config)
    cur = coon.cursor()
    sql = "SELECT * from account WHERE  username= %s"

    cur.execute(sql, (username))
    coon.commit()
    result = cur.fetchone()
    cur.close()
    coon.close()

    if result[2] == oldpassword:
        coon = pymysql.connect(**config)
        cur = coon.cursor()
        sql = "UPDATE  account SET password =%s WHERE  username= %s"
        cur.execute(sql, (newpassword, username))
        coon.commit()
        cur.close()
        coon.close()
        return app.send_static_file('hello.html')
    else:
        return "please input the right old password <a> /static/changepassword</a>"


@app.route('/adduser', methods=['get'])
def adduse_html():
    return render_template('root_adduser.html')


@app.route('/add', methods=['post'])
def adduser():
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    print username, name, password
    return "success"


@app.route('/test', methods=['get'])
def test():
    return


if __name__ == '__main__':
    app.run()
