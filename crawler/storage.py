# -*- coding: utf-8 -*-
# Store the data in mysql

import pymysql

with open('names', 'r') as file:
    names = eval(file.read())
config = {
    "host": "127.0.0.1",
    "user": "root",
    "port": 3306,
    "password": "123456",
    "db": 'zhihu_santi',
    "charset": 'utf8'
}
insert = "insert into name (`name`,`status`) VALUES( '%s' ,'0');"
SQL = ""
for name in names:
    SQL += insert % name
print(SQL)
with pymysql.connect(**config) as cursor:
    cursor.execute(SQL)
