import feedparser
import re
import sys
import code
import os

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console, strip


L = "0,11Twitter" 
  
def usage():
  print "%s Usage: !twitter username [n]" % L
  exit(-1)

if len(sys.argv) < 2:
  usage()

user = sys.argv[1]
try:
  n = int(sys.argv[2])
except IndexError:
  n = 0
except ValueError:
  n = 0

url = "https://api.twitter.com/1/statuses/user_timeline.rss?screen_name=%s"
profile_url = url % user

f = feedparser.parse(profile_url)

if f.bozo == 1:
  print_console("%s omg :( %s" % (f.bozo, f.bozo_exception))
  exit(-1)

if 'error' in f.feed.keys() or f.feed.keys() == []:
  print_console("%s Twitter feed for %s is private or doesn't exist" % (L, user))
  exit(-1)
  
try:
  entry = f.entries[n]
except IndexError:
  print_console("%s Tweet not available" % L)
  exit(-1)
  
summary = entry.summary
print_console("%s %s (%s)" % (L, summary, entry.published.rsplit(' ', 1)[0]))

