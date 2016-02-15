#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#运维审计服务器，实现跳板机功能

import os

def input_choice():
    p=input('\n请选择需要登陆的服务器序号:')
    if p:
        d=int(p)
        return d
    else:
        input_choice()
f=open('ip_name.txt','r')
ip_dict={}
n=0

#将序号以及ip地址写入字典中
for line in f.readlines():
    n=n+1
    ip_dict[n]=line #{1:'192.168.226.13 数据库主机}
f.close()
while 1:
    print('-----------------------------------')
    print('|      欢迎登陆运维审计服务器      |')
    print('-----------------------------------')
    #将服务器选择打印到屏幕出来
    for k,v in ip_dict.items():
        print('\033[36m%s.%s\033[0m' % (k,v),end='')
    #判断用户输入
    p=input('\n请选择需要登陆的服务器序号:')
    try:
        option=int(p)
    except ValueError:
        option=None
        pass
    if option in ip_dict.keys():
        print('正在登录: %s' % ip_dict[option])
        USERNAME=input('Username:')
        print(ip_dict[option].split(' ')[0])
        cmd='ssh %s@%s' % (USERNAME,ip_dict[option].split(' ')[0])
        os.system(cmd)
    else:
        print('输入序号不正确')
