import mysql.connector
from flask_sqlalchemy import SQLAlchemy

db = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    passwd="pm2021pm",
    db='week6',
    charset='utf8')

cursor = db.cursor()

inputName = "Otor"
inputUserName = "Octopus"
inputPassword = "genius"

# 查看 表單username全部值
cursor.execute("""
    SELECT name, username, password FROM userpassword; 
""")
myresult = cursor.fetchall()
# sql = "INSERT INTO userpassword(name, username, password) VALUES (%s, %s, %s)"
# val = (inputName, inputUserName, inputPassword)

# 帳號
# select = 'SELECT * FROM userpassword WHERE username= %(val)s'
# cursor.execute(select, {'val': inputUserName})
# friendName = cursor.fetchall()


# if len(friendName) > 0:
#     print("重複了")
# else:
#     print("沒重複")




# 變更密碼
select = 'UPDATE `week6`.`userpassword` SET `password`=%(PWval)s WHERE (`username`=%(nameval)s);'
cursor.execute(select, {'PWval': inputPassword,'nameval': inputUserName})
db.commit()


