#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from xml.parsers.expat import ParserCreate

# 这个类负责解析地点、当日以及明日天气
class WeatherSaxHandler(object):
    b={}
    def start_element(self,name,attrs):
        if name == r'yweather:location':
            self.b['city']=attrs['city']
            self.b['country']=attrs['country']
        if name == r'yweather:forecast':
            if 'today' not in self.b:
                self.b['today']={}
                self.b['today']['text']=attrs['text']
                self.b['today']['low']=int(attrs['low'])
                self.b['today']['high']=int(attrs['high'])
            if 'tomorrow' not in self.b:
                self.b['tomorrow']={}
                self.b['tomorrow']['text']=attrs['text']
                self.b['tomorrow']['low']=int(attrs['low'])
                self.b['tomorrow']['high']=int(attrs['high'])
    def end_element(self,name):
        pass

    def char_data(self,text):
        pass

data = r'''<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<rss version="2.0" xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">
    <channel>
        <title>Yahoo! Weather - Beijing, CN</title>
        <lastBuildDate>Wed, 27 May 2015 11:00 am CST</lastBuildDate>
        <yweather:location city="Beijing" region="" country="China"/>
        <yweather:units temperature="C" distance="km" pressure="mb" speed="km/h"/>
        <yweather:wind chill="28" direction="180" speed="14.48" />
        <yweather:atmosphere humidity="53" visibility="2.61" pressure="1006.1" rising="0" />
        <yweather:astronomy sunrise="4:51 am" sunset="7:32 pm"/>
        <item>
            <geo:lat>39.91</geo:lat>
            <geo:long>116.39</geo:long>
            <pubDate>Wed, 27 May 2015 11:00 am CST</pubDate>
            <yweather:condition text="Haze" code="21" temp="28" date="Wed, 27 May 2015 11:00 am CST" />
            <yweather:forecast day="Wed" date="27 May 2015" low="20" high="33" text="Partly Cloudy" code="30" />
            <yweather:forecast day="Thu" date="28 May 2015" low="21" high="34" text="Sunny" code="32" />
            <yweather:forecast day="Fri" date="29 May 2015" low="18" high="25" text="AM Showers" code="39" />
            <yweather:forecast day="Sat" date="30 May 2015" low="18" high="32" text="Sunny" code="32" />
            <yweather:forecast day="Sun" date="31 May 2015" low="20" high="37" text="Sunny" code="32" />
        </item>
    </channel>
</rss>
'''

def parse_weather(xml):
    handler=WeatherSaxHandler()
    parser=ParserCreate()
    parser.StartElementHandler=handler.start_element
    parser.Parse(xml)
    return handler.b


weather=parse_weather(data)

print(weather['country'])
print(weather['today']['text'])
print(weather['tomorrow']['low'])


'''
weather = parse_weather(data)
assert weather['city'] == 'Beijing', weather['city']
assert weather['country'] == 'China', weather['country']
assert weather['today']['text'] == 'Partly Cloudy', weather['today']['text']
assert weather['today']['low'] == 20, weather['today']['low']
assert weather['today']['high'] == 33, weather['today']['high']
assert weather['tomorrow']['text'] == 'Sunny', weather['tomorrow']['text']
assert weather['tomorrow']['low'] == 21, weather['tomorrow']['low']
assert weather['tomorrow']['high'] == 34, weather['tomorrow']['high']
print('Weather:', str(weather))
'''
#b={'city':'beijing','country':'china','today':{'text':'cloudy','low':20}}





