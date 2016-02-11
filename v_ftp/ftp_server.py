#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#能够put以及get文件，并且检查文件是否存在(包括本地端以及远端)，同时检查本地客户端命令是否正确
#对传输文件的完整一致性进行MD5校验
#使用base64进行用户密码认证
import os
import re
import hashlib
from time import sleep
import socketserver

#服务端socket进程
class MyTCPHandler(socketserver.BaseRequestHandler):
    def sendfile(self):
        #判断本地文件是否存在
        if os.path.exists(self.file_name):
            self.request.sendall("OK".encode('utf-8'))
            #发送文件MD5checksum
            md5_checksum=self.md5sum(self.file_name)
            self.request.sendall(md5_checksum)
            sleep(0.2) #这里不sleep一下，会把下面一部分的data的数据也发送过去
            with open(self.file_name,'rb') as f:
                send_data=f.read()
            self.request.sendall(send_data)
            sleep(0.5)
            self.request.sendall(b'get ok')
            self.request.sendall(('Get "%s" Sucessful!!' % self.file_name).encode('utf-8'))
        else:
            self.request.sendall(b'error')
            self.request.sendall('Error: remote file not exist!!!'.encode('utf-8'))

    def recvfile(self):
        #接受MD5checksum
        md5_checksum1=self.request.recv(1024)
        buffer=[]
        while 1:
            #接收发送的数据
            d=self.request.recv(4096)
            if d == b'send ok':
                break
            else:
                buffer.append(d)
        data_from_client=b''.join(buffer)
        with open(self.file_name,'wb') as f:
            f.write(data_from_client)
        #比较MD5checksum的值
        md5_checksum2=self.md5sum(self.file_name)
        if md5_checksum1 == md5_checksum2:
            self.request.sendall(('Put "%s" Sucessful!!' % self.file_name).encode('utf-8'))
        else:
            self.request.sendall(('Warnings: "%s" data not completed!!' % self.file_name).encode('utf-8'))

    def md5sum(self,file):
        with open(file,'rb') as f:
            d=f.read()
        md5=hashlib.md5()
        md5.update(d)
        return md5.hexdigest().encode('utf-8')

    def handle(self):
        passwd_dict={'jack':'amFjaw==','marry':'bWFycnk='}
        #接收用户名
        USERNAME=self.request.recv(1024).decode('utf-8')
        #接收密码
        PASSWD=self.request.recv(1024).decode('utf-8')
        #检验用户名密码是否正确
        try: #用户名不存在的时候pass掉Keyerror，会返回
            if passwd_dict[USERNAME] == PASSWD:
                self.request.sendall(b'pass')
            else:
                #同时客户端会关闭这条连接
                self.request.sendall(b'wrong')
        except KeyError as e:
            self.request.sendall(b'null_user')
        while 1:
            HOST,PORT=self.client_address
            print('connect from %s:%s' % (HOST,PORT))
            #接受(put,get)命令
            self.data_from_client=self.request.recv(4096)
            if not self.data_from_client:
                break
            else:
                self.remote_cmd=re.split(r'\s+',self.data_from_client.decode('utf-8'))[0]
                self.file_name=re.split(r'\s+',self.data_from_client.decode('utf-8'))[1]
            if self.remote_cmd == 'put':
                self.recvfile()
            if self.remote_cmd == 'get':
                self.sendfile()
            #if othercommand
            #ls等相关命令检查put文件名是否存在，以及get的文件名是否存在，还有用户账号及密码校验,权限！
            #cd ls

if __name__=='__main__':
    HOST,PORT='',17000
    #有客户端连入的时候，启动一个线程来启动handle函数
    server=socketserver.ThreadingTCPServer((HOST,PORT),MyTCPHandler)
    server.serve_forever()