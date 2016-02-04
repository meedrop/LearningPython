#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from html.parser import HTMLParser
from html.entities import name2codepoint

class MyHTMLParser(HTMLParser):

    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self._flag = ''

    def handle_starttag(self, tag, attrs):
        if ('class', 'event-title') in attrs:
            self._flag = 'Title:'
        elif ('class', 'event-location') in attrs:
            self._flag = 'Location:'
        elif tag == "time":
            self._flag = 0

    def handle_data(self, data):
        if self._flag in ('Title:', 'Location:'):
            if self._flag == 'Title:':
                print('-'*30)
            print(self._flag, data.strip())
            self._flag = ''
        if isinstance(self._flag, int):
            l = ['-', ',', '\n']
            if self._flag < 3:
                print(data.strip(), end=l[self._flag])
                self._flag += 1

parser = MyHTMLParser()
with open('index.html') as html:
    parser.feed(html.read())