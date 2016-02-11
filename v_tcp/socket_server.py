#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import os

#服务端启动socket监听
HOST=''
PORT=18000
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(2)

while 1:
    conn,addr=s.accept()
#连接建立后服务端程序
    print('Conncted from %s:%s' % addr)
#服务器状态为一直监听
    while 1:
        data=conn.recv(1024)
        #print(data.decode('utf-8'))
        if not data:
            break
        #执行客户端发送的命令并返回标准输出
        cmd = os.popen(data.decode('utf-8'))
        result = cmd.read()
        cmd.close()
        feedback=("\033[31m testt \033[0m\n" + result).encode('utf-8')
        conn.sendall(feedback)
#conn.close()