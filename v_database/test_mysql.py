#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
try:
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='123456')
    cur = conn.cursor()
    cur.execute('create database if not exists python')
    conn.select_db('python')
    cur.execute('create table host(id MEDIUMINT NOT NULL AUTO_INCREMENT,PRIMARY key(id),host varchar(20),username varchar(20),password varchar(30))')

    values=['1','192.168.226.12','jack','123456']
    cur.execute('insert into host values(%s,%s,%s,%s)',values)
    #cur.execute('update host set host="1.1.1.1" where username="jack"')
    values=cur.fetchall()
    conn.commit()

    cur.close()#关闭数据库连接
    conn.close()#关闭socket连接
except pymysql.err.OperationalError as e:
    print('Mysql error:',e)
