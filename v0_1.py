# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 09:00:14 2018

@author: yuzy
"""

import pymysql

# 打开数据库连接
db = pymysql.connect("localhost","root","123456","medicine" )
 
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# SQL 查询语句
sql = "SELECT * FROM chufang WHERE id = '20150215140027_85805' "
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      department = row[1]
      diag=row[11]
       # 打印结果
      print(department,diag)
except:
   print ("Error: unable to fetch data")

# 关闭数据库连接
db.close()