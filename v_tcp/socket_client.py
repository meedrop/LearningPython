#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
from time import sleep
HOST='192.168.226.13'
PORT=18000
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))
while 1:
    COMMAND=input('Plaease input a command for server to run:')
    if COMMAND=='exit':break
    s.sendall(COMMAND.encode('utf-8'))
    data=s.recv(8096)
    #print('Receved',data.decode('utf-8'))
    print(data.decode('utf-8'))
    sleep(1)
    s.sendall('haha'.encode('utf-8'))
    data1=s.recv(8096)
    print(data1.decode('utf-8'))
s.close()