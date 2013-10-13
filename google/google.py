import urllib
import sys
import os
import code
import json as m_json

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console, unescape, strip


logo = "2G4o8o2g3l4e"

if len(sys.argv) < 2:
  print_console("%s search syntax: !google <terms>" % logo);
  exit(-1)

query = " ".join(sys.argv[1:])

string = "%s %s: " % (logo, query)
query = urllib.urlencode ({ 'q' : query })
response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query).read()
json = m_json.loads(response)
results = json['responseData']['results']

i = 0
for result in results[:3]:
 title = strip(unescape(result['title'].replace("<b>","").replace("</b>", "")))
 url = urllib.unquote(result['url'])   # was URL in the original and that threw a name error exception
 string = string + "%s (%s); " % (title, url)

print_console("%s: %s" % (string, url))
