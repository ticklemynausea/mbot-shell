#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
reload(sys)  
sys.setdefaultencoding('utf8')
import urllib2

if (len(sys.argv) == 1):
	print("Usage .cc <coin> [ammount]")
	sys.exit(0)
coin = sys.argv[1].upper()
ammount = 1
if (len(sys.argv) > 2):
	try:
		ammount = float(sys.argv[2])
	except:
		ammount = 1
	if not isinstance(ammount, (int, long, float, complex)):
		print("Invalid input, usage .cc <coin> [ammount]")
		sys.exit(0)

url = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=EUR,USD'.format(coin)

try:
	response = urllib2.urlopen(url)
except urllib2.URLError, e:
		print("There was an error: %r" % e)
		sys.exit(0)
values = json.loads(response.read())
try:
	tmp = values['RAW'][coin]
except:
	print("No results found")
	sys.exit(0)
eur = values['RAW'][coin]['EUR']['PRICE']
usd = values['RAW'][coin]['USD']['PRICE']
print("%0.2f %s = %0.2f USD = %0.2f EUR" % (ammount, coin, usd * ammount, eur * ammount))
