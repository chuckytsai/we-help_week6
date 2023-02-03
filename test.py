# 載入模組
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from markupsafe import escape
import mysql.connector
from mysql.connector import Error
from flask_sqlalchemy import SQLAlchemy
import os
import json

# 帳號密碼的資料庫讀取
db = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    passwd="pm2021pm",
    db='week6',
    charset='utf8')

cursor = db.cursor()

# 查看 表單(name, username, password)3個值
cursor.execute("""
    SELECT name, username, password FROM userpassword; 
""")
myresult = cursor.fetchall()




# 建立Application物件
# 設定靜態檔案的路徑處理
app = Flask(
    __name__,
    static_folder="material",  # 靜態檔案的資料匣名稱
    static_url_path="/spider"
)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# 建立首頁
@app.route("/")
def index():
    successMessage = request.args.get("success")
    return render_template("index.html",success=successMessage)


# 建立登入頁面並且判斷帳號密碼登入通往其他頁面(POST)
@app.route("/signin", methods=["POST"])
def signin():
    #尋找帳號的字串是否在SQL中
    selectName = 'SELECT * FROM userpassword WHERE username= %(nameval)s'
    cursor.execute(selectName, {'nameval': request.values.get("whatName")})
    friendName = cursor.fetchall()
    # 登入成功頁面(session)
    if len(friendName) > 0 and request.values.get("whatPW")==friendName[0][3]:
       return render_template("member.html")
 
    # 輸入的帳號或是密碼錯誤的話
    else:
        return redirect("/error?message=ID or Password is error")


# 變更使用者密碼(POST)
@app.route("/changpw", methods=["POST"])
def changpw():
    #判斷使用者ID以及密碼正確
    selectName = 'SELECT * FROM userpassword WHERE username= %(nameval)s'
    cursor.execute(selectName, {'nameval': request.values.get("checkName")})
    friendName = cursor.fetchall()
    #判斷正確才可以改帳號密碼
    if len(friendName) > 0 and request.values.get("checkPW")==friendName[0][3]:
        select = 'UPDATE `week6`.`userpassword` SET `password`=%(PWval)s WHERE (`username`=%(nameval)s);'
        cursor.execute(select, {'PWval': request.values.get("checkAgain"),'nameval': request.values.get("checkName")})
        db.commit()
        return render_template("member.html")
    # 輸入的帳號或是密碼錯誤的話
    else:
        return redirect("/error?message=ID or Password is error")

# 建立註冊頁面並且判斷帳號密碼是否重複(POST)
@app.route("/signup", methods=["POST"])
def signup():
    #尋找帳號的字串是否在SQL中
    selectName = 'SELECT * FROM userpassword WHERE username= %(val)s'
    cursor.execute(selectName, {'val': request.values.get("wantID")})
    newName = cursor.fetchall()
    # 重複帳號去error頁面
    if len(newName) > 0:
        return redirect("/error?message=ID is duplicated !")
    # 沒重複帳號則在SQL創建
    else :
       inputName = request.values.get("wantName")
       inputUserName = request.values.get("wantID")
       inputPassword = request.values.get("wantPW")
       sql = "INSERT INTO userpassword(name, username, password) VALUES (%s, %s, %s)"
       val = (inputName, inputUserName, inputPassword)
       cursor.execute(sql, val)
       db.commit()
       return redirect(url_for('index'))


# 帳號或是密碼錯誤

@app.route("/error")
def error():
    errorMessage = request.args.get("message")
    return render_template("error.html", message=errorMessage)

# 登出帳號且瀏覽器忘記該帳號訊息


@app.route('/logout')
def logout():
    session.pop("whatName", None)
    return redirect(url_for('index'))


# 用port3000
app.run(port=3000)
