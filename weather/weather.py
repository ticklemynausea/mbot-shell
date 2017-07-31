#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
reload(sys)  
sys.setdefaultencoding('utf8')
import urllib2
city = ""

for x in range(1, len(sys.argv)):
	if x == 1:
		city = sys.argv[x]
	else:
		city = city + "%20" + sys.argv[x]

url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text=%22{}%22)%20and%20u=%22c%22&format=json&env=store://datatables.org/alltableswithkeys'.format(city)


response = urllib2.urlopen(url)
values = json.loads(response.read())
if values['query']['results'] is None:
	print("No results found")
else:
	channel = values['query']['results']['channel']
	conditions = channel['item']['condition']
	atemosphere = channel['atmosphere']
	astronomy = channel['astronomy']
	wind = channel['wind']
	print("%s Temperature: %s Cยบ  Condition: %s  Humidity: %s%%  Wind: %s km/h  Sunrise/Sunset: %s/%s" % (channel['item']['title'], conditions['temp'], conditions['text'], atemosphere['humidity'], wind['speed'], astronomy['sunrise'], astronomy['sunset'] ) )
