# coding=utf8
#!/usr/bin/env python

import sys, os, urllib, urllib2
import code

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console

URL = 'http://xxxxxxxxxxxxxxxxxxxxxxxxx.xxx/'
if len(sys.argv) < 2:
  print_console("Usage: !xlongener <url>");
  sys.exit(0);

values = {'url':sys.argv[1]}
data = urllib.urlencode(values)
req = urllib2.Request(URL + 'create', data)

try: 
  response = urllib2.urlopen(req)
except urllib2.HTTPError:
  sys.exit(0)

#info = response.info()
text = response.read()

if text != 'not found':
  print_console(URL + text)
