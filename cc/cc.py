#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import os
import urllib2

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console

if (len(sys.argv) == 1):
	print_console("Usage .cc <coin> [ammount]")
	sys.exit(0)
coin = sys.argv[1].upper()
ammount = 1
if (len(sys.argv) > 2):
	try:
		ammount = float(sys.argv[2])
	except:
		ammount = 1
	if not isinstance(ammount, (int, long, float, complex)):
		print_console("Invalid input, usage .cc <coin> [ammount]")
		sys.exit(0)

url = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=EUR,USD'.format(coin)

try:
	response = urllib2.urlopen(url)
except urllib2.URLError, e:
		print_console("There was an error: %r" % e)
		sys.exit(0)
values = json.loads(response.read())
try:
	tmp = values['RAW'][coin]
except:
	print_console("No results found")
	sys.exit(0)
eur = float(values['RAW'][coin]['EUR']['PRICE'])
usd = float(values['RAW'][coin]['USD']['PRICE'])
print_console("%0.2f %s = %0.2f USD = %0.2f EUR" % (ammount, coin, usd * ammount, eur * ammount))
