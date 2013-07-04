import feedparser
import re
import sys
import code
import os
from mylib import print_console, unescape, strip

teh4chanLogo = "8,34chan /%s/"
teh4chanId = "4chn"

feeds = [
  {"id":"pplw", "logo": "11,2PPLWARE", "url":"http://pplware.sapo.pt/feed/"},
  {"id":"apod", "logo": "1,15APOD", "url":"http://apod.nasa.gov/apod.rss"},
  {"id":"tlks", "logo": "14,01TUGALEAKS", "url":"http://feeds.feedburner.com/tugaleaks"},
  {"id":teh4chanId, "logo": teh4chanLogo, "url":"http://boards.4chan.org/%s/index.rss"},
  {"id":"guns", "logo": "0,1Gun Show", "url":"http://www.rsspect.com/rss/gunshowcomic.xml"},
  {"id":"qcon", "logo": "10,12QC", "url":"http://www.questionablecontent.net/QCRSS.xml"},
  {"id":"xkcd", "logo": "1,0xkcd", "url":"http://xkcd.com/rss.xml"}
]

  
# argv         0      1     2     3 
#usage: python rss.py 4chan board n
#       python rss.py feedn n

def usage():
  print "Usage: !feedname [n] | !4chan [board] [n] "
  exit(-1)

#if len(sys.argv) < 2:
#  usage()

l = len(sys.argv)
if l < 2:
  usage() #-

fid = sys.argv[1]
if fid == teh4chanId:
  if l == 2:
    b = "b"
    n = 0
  elif l == 3:
    b = sys.argv[2]
    n = 0
  elif l == 4:
    b = sys.argv[2]
    try:
      n = int(sys.argv[3])
    except ValueError:
      n = 0
else:
  if l == 2:
    n = 0
  elif l == 3:
    try:
      n = int(sys.argv[2])
    except ValueError:
      n = 0


f = None
for feed in feeds:
  if feed["id"] == fid:
    f = feed

if f is None:
  print_console("%s is not a valid feed id!" % fid)
  exit(-1);


url = f["url"]
logo = f["logo"]

if fid == teh4chanId:
  url = url % b
  logo = logo % b

f = feedparser.parse(url)

if f.status == '404':
  if fid == teh4chanId:
    print_console("Board %s: Not Found!" % b)
  else:
    print_console("Feed %s: Not Found" % logo)
if f.bozo == 1:
  print_console("%s omg :( %s" % (f.bozo, f.bozo_exception))
  exit(-1)

try:
  entry = f.entries[n]
except IndexError:
  print_console("Entry not available")
  exit(-1)

title = entry.title
link = entry.link
summary = unescape(strip(entry.summary))

if 'published' in entry.keys():
  published = entry.published.rsplit(' ', 1)[0]
else:
  published = None

if published is not None:
  print_console("%s %s - %s (%s)" % (logo, title, link, published)) 
else:
  print_console("%s %s - %s" % (logo, title, link)) 

for l in summary.split("\n"):
  if len(l) > 0:
    print_console("%s %s" % (logo, l))

