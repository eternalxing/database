# -*- coding: utf-8 -*-
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
    session['id'] = 3
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
        session['identify'] = result[4]
        if session['idetify'] == 1:
            return render_template('student.html')
        if session['idetify'] == 2:
            return render_template('teacher.html')
        if session['idetify'] == 3:
            return render_template('root.html')
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

    print newpassword
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


@app.route('/doadduser', methods=['get', 'post'])
def doadduser():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    identify = request.form.get('identify')
    idcard = request.form.get('idcard')
    print name, username, password, identify, idcard

    coon = pymysql.connect(**config)
    cur = coon.cursor()
    sql = "INSERT INTO   account (username ,password, realname ,identify) VALUES (%s,%s,%s,%s)"

    print sql % (username, password, name, identify)

    cur.execute(sql, (username, password, name, identify))
    coon.commit()
    #  result = cur.fetchone()
    cur.close()
    coon.close()

    return "添加成功"


@app.route('/changescore', methods=['get'])
def test():
    coon = pymysql.connect(**config)
    cur = coon.cursor()
    sql = "SELECT *  FROM score_201602 "
    cur.execute(sql)
    coon.commit()
    result = cur.fetchall()
    cur.close()
    coon.close()
    print  result
    scores = []
    for i in result:
        tmp = {}
        tmp['id'] = i[0]
        tmp['name'] = i[1]
        tmp['Dbbase'] = i[2]
        tmp['Math'] = i[3]
        tmp['Java'] = i[4]
        tmp['Linux'] = i[5]
        scores.append(tmp)
    print scores
    return render_template('teacher_seescore.html', scores=scores)


@app.route('/test/<int:id>')
def test1(id):
    coon = pymysql.connect(**config)
    cur = coon.cursor()
    sql = "SELECT * from score_201602 WHERE  id= %s"
    cur.execute(sql, (id))
    coon.commit()
    result = cur.fetchone()
    cur.close()
    coon.close()
    stu = {}
    stu["id"] = result[0]
    stu["name"] = result[1]
    stu["Dbbase"] = result[2]
    stu["Math"] = result[3]
    stu["Java"] = result[4]
    stu["Linux"] = result[5]
    return render_template('teacher_changescore_each.html', student=stu)


@app.route('/changescore/<int:id>', methods=['post'])
def changescore(id):
    Math = request.form.get("Math")
    Dbbase = request.form.get("Dbbase")
    Linux = request.form.get("Linux")
    Java = request.form.get("Java")
    print Math, Dbbase, Linux, Java
    coon = pymysql.connect(**config)
    cur = coon.cursor()
    sql = "UPDATE  score_201602 SET  Math=%s , Java=%s  ,Linux=%s , Dbbase=%s WHERE  id=%s"
    print sql % (Math, Java, Linux, Dbbase, str(id))
    cur.execute(sql, (Math, Java, Linux, Dbbase, str(id)))
    coon.commit()
    cur.close()
    coon.close()
    return "changed success"


@app.route('/delete/<int:id>', methods=['get'])
def delete(id):
    coon = pymysql.connect(**config)
    cur = coon.cursor()
    sql = "DELETE FROM score_201602 WHERE id=%s"
    cur.execute(sql, (str(id)))
    coon.commit()
    cur.close()
    coon.close()
    return "delete successfully"


@app.route('/student_seescore', methods=['get'])
def test2():
    coon = pymysql.connect(**config)
    cur = coon.cursor()
    id = session['id']
    sql = "SELECT *  FROM score_201602 WHERE id=%s"
    cur.execute(sql, (str(id)))
    coon.commit()
    i = cur.fetchone()
    cur.close()
    coon.close()
    print  i
    tmp = {}

    tmp['id'] = i[0]
    tmp['name'] = i[1]
    tmp['Dbbase'] = i[2]
    tmp['Math'] = i[3]
    tmp['Java'] = i[4]
    tmp['Linux'] = i[5]

    return render_template('student_seescore.html', score=tmp)

@app.route('/usermanager',methods=['get'])
def usermanager():
    coon = pymysql.connect(**config)
    cur = coon.cursor()
    id = session['id']
    sql = "SELECT *  FROM account "
    cur.execute(sql)
    coon.commit()
    result = cur.fetchall()
    cur.close()
    coon.close()
    print  result
    scores = []
    for i in result:
        tmp = {}
        tmp['id'] = i[0]
        tmp['name'] = i[1]
        tmp['password'] = i[2]
        tmp['identify'] = i[4]

        scores.append(tmp)
        print scores
    return render_template('root_usermanger.html', scores=scores)

if __name__ == '__main__':
    app.run(debug=True)
