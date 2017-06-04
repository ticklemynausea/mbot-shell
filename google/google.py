# -*- coding: utf-8 -*-
import urllib
import sys
import os
import code
import json as m_json

from apikeys import CSE_API_KEY, ENGINE_ID

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console, unescape, strip

# https://developers.google.com/custom-search/json-api/v1/overview
# Free API limited to 100 searches per day (lol)


logo = "2G4o8o2g3l4e"

if len(sys.argv) < 2:
  print_console("%s search syntax: !google <terms>" % logo);
  exit(-1)

arg = [i.decode(sys.getfilesystemencoding()) for i in sys.argv[1:]]
query = u" ".join(arg)

string = "%s %s: " % (logo, query)
query = urllib.urlencode ({ 'q' : query.encode(sys.getfilesystemencoding()) })
baseURL = "https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&alt=json&" % (CSE_API_KEY, ENGINE_ID)
response = urllib.urlopen(baseURL + query).read()
json = m_json.loads(response)
results = json.get('items', None)

if results:
  for result in results[:3]:
    title = result['title']
    url = result['link']
    string = string + "%s ( %s ); " % (title, url)

  print_console("%s: %s" % (string, url))

else:
  print_console("No results!")
