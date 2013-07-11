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
except IndexError:
  n = 0
except ValueError:
  n = 0

try:
  t = pytwitter.Api(consumer_key = 'laKcPz3kAAH3TVz8wIRAA', consumer_secret = 'P7CD74v1ea5dO9JvJvv0blAmZaGmhQebAJIH2XLCI', access_token_key = '1523563723-gcn8yyeFiGK1PlxfnoPve9j0QWO3OVP2qyfhTCs', access_token_secret = 'QihKi7KCPFD7n9Yq3AFXDgWVc2vO3dmlzhClgsDxrU0')
  tweets = t.GetUserTimeline(None, user)
  tweet = tweets[n].GetText().encode('utf8').replace('\n', ' ')
  print_console("%s %s: %s" % (L, user, tweet))
except pytwitter.TwitterError as e:
  err_msg = e.message[0].get('message').encode('utf8')
  err_code = str(e.message[0].get('code'))
  print_console("%s Code: %s - %s" % (L, err_code, err_msg))
  exit(-1)


