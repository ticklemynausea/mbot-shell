import re
import sys
import os
import pytwitter

# ../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console, strip


L = "0,10Twitter" 
  
def usage():
  print "%s Usage: !twitter username [n]" % L
  exit(-1)

if len(sys.argv) < 2:
  usage()

user = sys.argv[1]
try:
  n = int(sys.argv[2])
except (IndexError, ValueError):
  n = 0

try:
  t = pytwitter.Api(consumer_key = 'laKcPz3kAAH3TVz8wIRAA', consumer_secret = 'P7CD74v1ea5dO9JvJvv0blAmZaGmhQebAJIH2XLCI', access_token_key = '1523563723-gcn8yyeFiGK1PlxfnoPve9j0QWO3OVP2qyfhTCs', access_token_secret = 'QihKi7KCPFD7n9Yq3AFXDgWVc2vO3dmlzhClgsDxrU0')
  username = t.GetUser(None, user)._screen_name
  tweets = t.GetUserTimeline(None, screen_name = username, count = 100)
  if not tweets:
    print_console("%s User: %s has no tweets" % (L, username))
    exit(-1)
  else:
    tweet = tweets[n].GetText().replace('\n', ' ')
    print_console("%s @%s: %s" % (L, username, tweet))
except pytwitter.TwitterError as e:
  print_console("%s Error: %s" % (L, e))
  exit(-1)
except IndexError:
  print_console("%s Error: YOU'VE GONE TOO FAR (keep below 100)" % (L))
  exit(-1)
