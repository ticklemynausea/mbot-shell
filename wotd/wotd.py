import feedparser
import re
import sys
import os

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console

def strip(html):
  return re.sub('<[^<]+?>', '', html)
  
url = "http://www.priberam.pt/dlpo/DoDiaRSS.aspx"

try:
  f = feedparser.parse(url)
  wotd_l = strip(f["items"][0]["summary"]).split("\n")
except Exception:
  print_console("Error parsing results.")
  exit(-1)
  

s = "\002%s\002" % wotd_l[0]
for l in wotd_l[1:]:
  if len(l) > 1:
   l = l.strip()
   s += "%s\002;\002 " % (l)

print_console(s)
