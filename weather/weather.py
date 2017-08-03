#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import os
import urllib2

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console

city = ""
forecastnum = 0
if (len(sys.argv) == 1):
	print_console("Usage .w <location> [--forecast [1-9]]")
	sys.exit(0)
for x in range(1, len(sys.argv)):
	if x == 1:
		city = sys.argv[x]
	else:
		if sys.argv[x] != "--forecast":
			city = city + "%20" + sys.argv[x]
		else:
			if x == len(sys.argv) - 1:
				forecastnum = 3
			else:
				try:
					forecastnum = int(sys.argv[x + 1])
				except:
					forecastnum = 3
			break

url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text=%22{}%22)%20and%20u=%22c%22&format=json&env=store://datatables.org/alltableswithkeys'.format(city)

try:
	response = urllib2.urlopen(url, timeout=5)
except urllib2.URLError, e:
		print_console("There was an error: %r" % e)
		sys.exit(0)
values = json.loads(response.read())
if values['query']['results'] is None:
	print_console("No results found")
else:
	channel = values['query']['results']['channel']
	conditions = channel['item']['condition']
	atemosphere = channel['atmosphere']
	astronomy = channel['astronomy']
	wind = channel['wind']
	print_console("%s Temperature: %s Cº  Condition: %s  Humidity: %s%%  Wind: %s km/h  Sunrise/Sunset: %s/%s" % (channel['item']['title'], conditions['temp'], conditions['text'], atemosphere['humidity'], wind['speed'], astronomy['sunrise'], astronomy['sunset'] ) )
	if forecastnum > 0:
		if forecastnum > 9:
			forecastnum = 9
		forecast = channel['item']['forecast']
		forecastprint = ""
		for x in range(1, forecastnum + 1):
			forecastprint = forecastprint + "Forecast for %s: High: %s Low: %s Condition: %s " % (forecast[x]['date'], forecast[x]['high'], forecast[x]['low'], forecast[x]['text'])
		print (forecastprint)
