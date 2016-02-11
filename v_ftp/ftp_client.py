#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import os
import re
import hashlib
import base64
import getpass
from time import sleep

#初始化服务器地址以及端口
HOST='192.168.226.13'
PORT=17000
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))
#print(2016-02-10)

def md5sum(file):
    with open(file,'rb') as f:
        d=f.read()
    md5=hashlib.md5()
    md5.update(d)
    return md5.hexdigest().encode('utf-8')

def base64_password(password):
    return base64.b64encode(password.encode('utf-8'))

print('--------------------------------------')
print('|    Weclome to Linqz Ftp Server     |')
print('|           Version 1.0              |')
print('--------------------------------------')
print('*****Please input Username/Passwor****')

#先验证用户名密码是否正确
USERNAME=input('Username:')
PASSWD=getpass.getpass() #输入密码不回显
#发送用户名到server
s.sendall(USERNAME.encode('utf-8'))
#发送密码到server
s.send(base64_password(PASSWD))

#接收server端验证，密码是否正确
get_verify=s.recv(1024)
if get_verify == b'pass':
    print('Login sucessfule!!^_^')
    while 1:
        COMMAND=input('ftp>')
        if COMMAND=='exit':break #break
        #帮助说明函数
        elif COMMAND=='help' or COMMAND=='?':
            print('put\t\tsend files(excluded path) to remote ftpserver')
            print('get\t\tget files from remote ftpserver')
            print('exit\t\tlogout')
            print('help|?\t\tget help informaton')
        elif 'put' in COMMAND or 'get' in COMMAND:
            cmd=re.split(r'\s+',COMMAND)[0]
            file_name=re.split(r'\s+',COMMAND)[1]

            #发送文件以及接收server的信息并打应出来
            if cmd=='put':
                #检测put的文件是否存在
                if os.path.exists(file_name):
                    #发送put命令
                    s.sendall(COMMAND.encode('utf-8'))
                    #发送文件的MD5checksum
                    md5_checksum=md5sum(file_name)
                    s.sendall(md5_checksum)
                    sleep(0.2) #这里不sleep一下，会把下面一部分的data的数据也发送过去
                    #发送文件
                    with open(file_name,'rb') as f:
                        put_data=f.read()
                    s.sendall(put_data)
                    sleep(0.5)
                    s.sendall(b'send ok')
                    #获取server信息
                    message_from_server=s.recv(8096)
                    print(message_from_server.decode('utf-8'))
                else:
                    print('Error: file not exist!!!')

            #获取文件以及接受server返回信息
            if cmd=='get':
                #发送get命令
                s.sendall(COMMAND.encode('utf-8'))
                #获取服务器返回的文件状态（是否存在）
                get_file_error_message=s.recv(8096).decode('utf-8')
                #get远端文件不存在的判断及错误输出
                if get_file_error_message == 'OK':
                    md5_checksum1=s.recv(1024) #获取服务器返回的文件的MD5checksum
                    buffer=[]
                    while 1:
                        d=s.recv(8096)
                        if d==b'get ok':
                            break
                        buffer.append(d)
                    get_data=b''.join(buffer)
                    with open(file_name,'wb') as f:
                        f.write(get_data)
                    #server返回get成功信息但根据checksum是否一致判断是否打印
                    get_message=s.recv(1024)
                    md5_checksum2=md5sum(file_name)
                    if md5_checksum1==md5_checksum2:
                        print(get_message.decode('utf-8'))
                    else:
                        print('Warnings: "%s" data not completed!' % file_name)
                else:
                    get_message=s.recv(1024)
                    print(get_message.decode('utf-8'))
        else:
            print('command not found')
        sleep(0.2)

    #跳出循环关闭这个socket
    s.close()

elif get_verify == b'null_user':
    print('Username not found!')
    s.close()
else:
    print('Password error!T T')
    s.close()


