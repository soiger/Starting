 # -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 09:00:14 2018

@author: yuzy
"""

import pymysql
def readsql(sqlword):
    # 打开数据库连接
    db = pymysql.connect("localhost","root","123456","recommander" )
 
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 查询语句
    try:
        # 执行SQL语句
        cursor.execute(sqlword)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results
    except:
        print ("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()

"""know user 288's rating matrixs"""
sqlword = "SELECT * FROM ratings WHERE id = 288 "
results = readsql(sqlword)
for row in results:
    mid=row[1]
    score=row[2]
    print(mid,score)

"""select every user"""
sqlword_1 = "SELECT DISTINCT id FROM ratings" 
users=readsql(sqlword_1)
for row in users:
    id=row[0]
    sqlword_x = "SELECT * FROM ratings WHERE id =" + id
    movies = readsql(sqlword)
